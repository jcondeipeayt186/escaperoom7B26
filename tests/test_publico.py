"""Vistas públicas: ranking del televisor y estadísticas agregadas."""

from datetime import datetime, timedelta

from helpers import ejecutar


def _crear_intento(
    db,
    nombre,
    inicio,
    segundos,
    finalizado="completo",
    incorrectas=0,
    ayudas=0,
    con_fin=True,
    dificultad="inicial",
):
    equipo_id = ejecutar(
        db,
        "INSERT INTO equipo (nombre, cantidad_personas) VALUES (%s, 2)",
        (nombre,),
    )
    fecha_fin = (
        inicio + timedelta(seconds=segundos) if con_fin else None
    )
    intento_id = ejecutar(
        db,
        "INSERT INTO intento "
        "(equipo_id, dificultad, fecha_inicio, fecha_fin, cantidad_ayudas, "
        " puntaje_obtenido, finalizado, ultima_estacion_visitada) "
        "VALUES (%s, %s, %s, %s, %s, %s, %s, 1)",
        (
            equipo_id,
            dificultad,
            inicio,
            fecha_fin,
            ayudas,
            segundos if finalizado == "completo" else None,
            finalizado,
        ),
    )

    if incorrectas:
        envio_id = ejecutar(
            db,
            "INSERT INTO intento_envio "
            "(intento_id, estacion_id, fecha, respuestas_correctas, "
            " respuestas_incorrectas) VALUES (%s, 1, %s, 0, %s)",
            (intento_id, inicio, incorrectas),
        )
        for _ in range(incorrectas):
            ejecutar(
                db,
                "INSERT INTO incorrecta "
                "(pregunta_id, respuesta_id, fecha, intento_id, "
                " intento_envio_id) VALUES (1, 1, %s, %s, %s)",
                (inicio, intento_id, envio_id),
            )
    return intento_id


def test_ranking_renderiza_solo_intentos_completados(cliente, db):
    _crear_intento(db, "Equipo Segundo", datetime(2026, 1, 2, 10, 0, 0), 120)
    _crear_intento(db, "Equipo Primero", datetime(2026, 1, 1, 10, 0, 0), 90)
    _crear_intento(
        db,
        "Equipo Abandona",
        datetime(2026, 1, 3, 10, 0, 0),
        10,
        finalizado="abandono",
    )

    html = cliente.get("/ranking").get_data(as_text=True)

    assert "Ranking Escape Room" in html
    assert "Reconectando…" in html
    assert "Equipo Primero" in html
    assert "Equipo Segundo" in html
    assert "Equipo Abandona" not in html
    assert html.index("Equipo Primero") < html.index("Equipo Segundo")
    assert "01:30" in html
    assert "02:00" in html


def test_ranking_vacio_muestra_el_mensaje(cliente):
    html = cliente.get("/ranking").get_data(as_text=True)

    assert "Todavía no hay equipos" in html
    assert "Reconectando…" in html


def test_ranking_datos_es_json_sin_ids_y_sin_cache(cliente, db):
    _crear_intento(db, "Equipo Dos", datetime(2026, 1, 2, 10, 0, 0), 120)
    _crear_intento(db, "Equipo Uno", datetime(2026, 1, 1, 10, 0, 0), 90)
    _crear_intento(
        db,
        "Equipo Intermedio",
        datetime(2026, 1, 3, 10, 0, 0),
        300,
        dificultad="intermedio",
    )
    _crear_intento(
        db,
        "Equipo Tiempo",
        datetime(2026, 1, 4, 10, 0, 0),
        5,
        finalizado="por_tiempo",
    )

    respuesta = cliente.get("/ranking/datos")
    datos = respuesta.get_json()

    assert respuesta.status_code == 200
    assert respuesta.headers["Cache-Control"] == "no-store"
    assert datos["actualizado"]
    assert [nivel["valor"] for nivel in datos["niveles"]] == [
        "inicial",
        "intermedio",
    ]

    inicial = datos["niveles"][0]
    assert inicial["etiqueta"] == "Inicial"
    assert [fila["equipo"] for fila in inicial["filas"]] == [
        "Equipo Uno",
        "Equipo Dos",
    ]
    assert [fila["posicion"] for fila in inicial["filas"]] == [1, 2]

    intermedio = datos["niveles"][1]
    assert [fila["equipo"] for fila in intermedio["filas"]] == [
        "Equipo Intermedio"
    ]
    # Dentro de su nivel vuelve a empezar en 1.
    assert intermedio["filas"][0]["posicion"] == 1

    assert set(inicial["filas"][0]) == {
        "posicion",
        "equipo",
        "numero_intento",
        "segundos",
        "incorrectas",
        "ayudas",
        "fecha_fin",
    }
    texto = respuesta.get_data(as_text=True)
    assert "equipo_id" not in texto
    assert "intento_id" not in texto
    assert "respuesta" not in texto


def test_ranking_muestra_una_tabla_por_nivel(cliente, db):
    _crear_intento(db, "Equipo Inicial", datetime(2026, 1, 1, 10, 0, 0), 90)
    _crear_intento(
        db,
        "Equipo Intermedio",
        datetime(2026, 1, 2, 10, 0, 0),
        300,
        dificultad="intermedio",
    )

    html = cliente.get("/ranking").get_data(as_text=True)

    assert 'data-nivel="inicial"' in html
    assert 'data-nivel="intermedio"' in html
    assert 'id="ranking-filas-inicial"' in html
    assert 'id="ranking-filas-intermedio"' in html
    assert html.index("Equipo Inicial") < html.index("Equipo Intermedio")


def test_estadisticas_publicas_solo_agregados(cliente, db):
    _crear_intento(
        db,
        "Equipo Público",
        datetime(2026, 1, 1, 10, 0, 0),
        100,
    )
    _crear_intento(
        db,
        "Equipo Público Abandona",
        datetime(2026, 1, 2, 10, 0, 0),
        10,
        finalizado="abandono",
    )
    _crear_intento(
        db,
        "Equipo Público En Curso",
        datetime(2026, 1, 3, 10, 0, 0),
        0,
        finalizado=None,
        con_fin=False,
    )

    html = cliente.get("/estadisticas").get_data(as_text=True)

    assert "Estadísticas de la feria" in html
    assert "Equipos participantes" in html
    assert "Intentos completados" in html
    assert "Aciertos" in html
    assert "En curso" in html
    assert "Completos" in html
    assert "Abandonos" in html
    assert "Equipo Público" not in html
    assert "equipo_id" not in html
    assert "respuesta_id" not in html
    assert "correcta" not in html.lower()
