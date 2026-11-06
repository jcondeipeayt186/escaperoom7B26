"""Orden del ranking, exclusiones y puntaje de los intentos completados."""

from datetime import date, datetime, timedelta

from app.servicios import ranking
from helpers import ejecutar, fila


def crear_intento_controlado(
    db,
    nombre,
    segundos,
    incorrectas=0,
    ayudas=0,
    inicio="2026-01-01T10:00:00",
    finalizado="completo",
    con_fin=True,
):
    equipo_id = ejecutar(
        db,
        "INSERT INTO equipo (nombre, cantidad_personas) VALUES (%s, 2)",
        (nombre,),
    )
    fecha_inicio = datetime.fromisoformat(inicio)
    fecha_fin = (
        fecha_inicio + timedelta(seconds=segundos) if con_fin else None
    )
    puntaje = segundos if finalizado == "completo" else None
    intento_id = ejecutar(
        db,
        "INSERT INTO intento "
        "(equipo_id, dificultad, fecha_inicio, fecha_fin, cantidad_ayudas, "
        " puntaje_obtenido, finalizado, ultima_estacion_visitada) "
        "VALUES (%s, 'inicial', %s, %s, %s, %s, %s, 1)",
        (equipo_id, fecha_inicio, fecha_fin, ayudas, puntaje, finalizado),
    )

    if incorrectas:
        envio_id = ejecutar(
            db,
            "INSERT INTO intento_envio "
            "(intento_id, estacion_id, fecha, respuestas_correctas, "
            " respuestas_incorrectas) VALUES (%s, 1, %s, 0, %s)",
            (intento_id, fecha_inicio, incorrectas),
        )
        for _ in range(incorrectas):
            ejecutar(
                db,
                "INSERT INTO incorrecta "
                "(pregunta_id, respuesta_id, fecha, intento_id, "
                " intento_envio_id) VALUES (1, 1, %s, %s, %s)",
                (fecha_inicio, intento_id, envio_id),
            )

    return intento_id


def test_ranking_ordena_tiempo_incorrectas_ayudas_fecha_e_id(app, db):
    crear_intento_controlado(db, "Equipo A", 90, inicio="2026-01-01T10:00:00")
    crear_intento_controlado(db, "Equipo B", 90, inicio="2026-01-01T10:00:01")
    crear_intento_controlado(
        db, "Equipo C", 90, ayudas=1, inicio="2026-01-01T09:00:00"
    )
    crear_intento_controlado(
        db, "Equipo D", 90, incorrectas=1, inicio="2026-01-01T08:00:00"
    )
    crear_intento_controlado(db, "Equipo E", 120, inicio="2026-01-02T07:00:00")

    with app.app_context():
        tablas = ranking.obtener_ranking()

    assert [fila["equipo_nombre"] for fila in tablas] == [
        "Equipo A",
        "Equipo B",
        "Equipo C",
        "Equipo D",
        "Equipo E",
    ]
    assert [fila["posicion"] for fila in tablas] == [1, 2, 3, 4, 5]
    assert tablas[0]["segundos"] == 90
    assert tablas[2]["cantidad_ayudas"] == 1
    assert tablas[3]["incorrectas"] == 1


def test_ranking_excluye_intentos_no_completados(app, db):
    crear_intento_controlado(db, "Equipo Completo", 100)
    crear_intento_controlado(
        db, "Equipo Abandono", 5, finalizado="abandono"
    )
    crear_intento_controlado(
        db, "Equipo Tiempo", 4, finalizado="por_tiempo"
    )
    crear_intento_controlado(
        db, "Equipo Incorrectas", 3, finalizado="por_respuestas_incorrectas"
    )
    crear_intento_controlado(
        db, "Equipo En Curso", 0, finalizado=None, con_fin=False
    )

    with app.app_context():
        tablas = ranking.obtener_ranking()

    assert [fila["equipo_nombre"] for fila in tablas] == ["Equipo Completo"]
    assert (
        fila(
            db,
            "SELECT puntaje_obtenido FROM intento "
            "WHERE finalizado = 'completo'",
        )["puntaje_obtenido"]
        == 100
    )
    assert fila(
        db,
        "SELECT COUNT(*) AS total FROM intento "
        "WHERE (finalizado IS NULL OR finalizado <> 'completo') "
        "AND puntaje_obtenido IS NULL",
    )["total"] == 4


def test_numero_de_intento_y_fila_individual(app, db):
    # Se crean dos intentos del mismo equipo para verificar la numeración.
    equipo_id = ejecutar(
        db,
        "INSERT INTO equipo (nombre, cantidad_personas) "
        "VALUES ('Equipo Repite', 2)",
    )
    primero = ejecutar(
        db,
        "INSERT INTO intento "
        "(equipo_id, dificultad, fecha_inicio, fecha_fin, puntaje_obtenido, "
        " finalizado, ultima_estacion_visitada) "
        "VALUES (%s, 'inicial', '2026-01-03 10:00:00', "
        "        '2026-01-03 10:01:00', 60, 'completo', 1)",
        (equipo_id,),
    )
    segundo = ejecutar(
        db,
        "INSERT INTO intento "
        "(equipo_id, dificultad, fecha_inicio, fecha_fin, puntaje_obtenido, "
        " finalizado, ultima_estacion_visitada) "
        "VALUES (%s, 'inicial', '2026-01-04 10:00:00', "
        "        '2026-01-04 10:02:00', 120, 'completo', 1)",
        (equipo_id,),
    )

    with app.app_context():
        tablas = ranking.obtener_ranking(equipo="Equipo Repite")
        primera = ranking.obtener_fila_ranking(primero)
        segunda = ranking.obtener_fila_ranking(segundo)
        inexistente = ranking.obtener_fila_ranking(999999)

    assert [fila["numero_intento"] for fila in tablas] == [1, 2]
    assert primera["posicion"] == 1
    assert segunda["posicion"] == 2
    assert inexistente is None


def test_filtros_del_ranking_no_cambian_la_posicion(app, db):
    crear_intento_controlado(db, "Equipo Filtro Uno", 90, inicio="2026-01-01T10:00:00")
    crear_intento_controlado(db, "Equipo Filtro Dos", 100, inicio="2026-01-02T10:00:00")
    crear_intento_controlado(db, "Equipo Filtro Tres", 110, inicio="2026-01-01T11:00:00")

    with app.app_context():
        por_nombre = ranking.obtener_ranking(equipo="Filtro Dos")
        por_fecha = ranking.obtener_ranking(fecha=date(2026, 1, 1))
        completo = ranking.obtener_ranking()

    assert [fila["equipo_nombre"] for fila in por_nombre] == ["Equipo Filtro Dos"]
    assert por_nombre[0]["posicion"] == 2
    assert [fila["equipo_nombre"] for fila in por_fecha] == [
        "Equipo Filtro Uno",
        "Equipo Filtro Tres",
    ]
    assert [fila["posicion"] for fila in por_fecha] == [1, 3]
    assert [fila["posicion"] for fila in completo] == [1, 2, 3]
