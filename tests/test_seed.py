"""Los seeds son idempotentes y respetan los cambios del administrador."""

from helpers import aplicar_seed, conteo, ejecutar, fila, filas


def test_reejecutar_los_seeds_no_duplica_contenido(db, base_de_datos):
    base = base_de_datos["MYSQL_DB"]
    antes = {
        tabla: conteo(db, tabla)
        for tabla in ("estacion", "tema", "pregunta", "respuesta")
    }

    aplicar_seed(db, base)
    aplicar_seed(db, base)

    despues = {
        tabla: conteo(db, tabla)
        for tabla in ("estacion", "tema", "pregunta", "respuesta")
    }
    assert despues == antes
    assert antes["estacion"] == 5
    assert antes["tema"] == 14
    assert antes["pregunta"] == 80
    assert antes["respuesta"] == 240


def test_distribucion_de_preguntas_por_nivel_y_estacion(db):
    distribucion = filas(
        db,
        "SELECT p.dificultad, t.estacion_id, COUNT(*) AS total "
        "FROM pregunta p "
        "JOIN tema t ON t.id = p.tema_id "
        "WHERE p.activo = 1 "
        "GROUP BY p.dificultad, t.estacion_id "
        "ORDER BY p.dificultad, t.estacion_id",
    )

    assert len(distribucion) == 15
    for registro in distribucion:
        esperado = 4 if registro["dificultad"] == "inicial" else 6
        assert registro["total"] == esperado
    for dificultad in ("inicial", "intermedio", "avanzado"):
        esperado = 20 if dificultad == "inicial" else 30
        assert (
            conteo(
                db,
                "pregunta",
                "WHERE dificultad = %s AND activo = 1",
                (dificultad,),
            )
            == esperado
        )


def test_cada_pregunta_tiene_tres_opciones_y_una_correcta(db):
    incompletas = filas(
        db,
        "SELECT p.id, COUNT(r.id) AS opciones, "
        "       SUM(r.correcta) AS correctas "
        "FROM pregunta p "
        "LEFT JOIN respuesta r ON r.pregunta_id = p.id AND r.activo = 1 "
        "GROUP BY p.id "
        "HAVING opciones <> 3 OR correctas <> 1",
    )

    assert not incompletas


def test_el_seed_restaura_los_textos(db, base_de_datos):
    ejecutar(
        db,
        "UPDATE estacion SET nombre = 'Estación cambiada' WHERE id = 1",
    )
    ejecutar(
        db,
        "UPDATE pregunta SET titulo = 'Pregunta cambiada' WHERE id = 1",
    )
    ejecutar(
        db,
        "UPDATE respuesta SET contenido = 'Opción cambiada' WHERE id = 2",
    )
    ejecutar(
        db,
        "UPDATE pregunta SET titulo = 'Intermedia cambiada' WHERE id = 1001",
    )
    ejecutar(
        db,
        "UPDATE respuesta SET contenido = 'Avanzada cambiada' WHERE id = 4001",
    )

    aplicar_seed(db, base_de_datos["MYSQL_DB"])

    assert fila(db, "SELECT nombre FROM estacion WHERE id = 1")["nombre"] == "Redes"
    assert (
        fila(db, "SELECT titulo FROM pregunta WHERE id = 1")["titulo"]
        == "¿Qué significa IP?"
    )
    assert (
        fila(db, "SELECT contenido FROM respuesta WHERE id = 2")["contenido"]
        == "Internet Protocol"
    )
    assert fila(db, "SELECT titulo FROM pregunta WHERE id = 1001")[
        "titulo"
    ] == "¿Qué dirección IPv4 es una dirección de loopback?"
    assert fila(db, "SELECT contenido FROM respuesta WHERE id = 4001")[
        "contenido"
    ] == "DNS"


def test_los_seeds_no_reactivan_contenido_desactivado(db, base_de_datos):
    ejecutar(db, "UPDATE estacion SET activo = 0 WHERE id = 5")
    ejecutar(db, "UPDATE tema SET activo = 0 WHERE id = 1")
    for pregunta_id in (1, 1001, 3001):
        ejecutar(
            db,
            "UPDATE pregunta SET activo = 0 WHERE id = %s",
            (pregunta_id,),
        )
    for respuesta_id in (1, 2001, 4001):
        ejecutar(
            db,
            "UPDATE respuesta SET activo = 0 WHERE id = %s",
            (respuesta_id,),
        )

    aplicar_seed(db, base_de_datos["MYSQL_DB"])

    assert fila(db, "SELECT activo FROM estacion WHERE id = 5")["activo"] == 0
    assert fila(db, "SELECT activo FROM tema WHERE id = 1")["activo"] == 0
    for pregunta_id in (1, 1001, 3001):
        assert (
            fila(
                db,
                "SELECT activo FROM pregunta WHERE id = %s",
                (pregunta_id,),
            )["activo"]
            == 0
        )
    for respuesta_id in (1, 2001, 4001):
        assert (
            fila(
                db,
                "SELECT activo FROM respuesta WHERE id = %s",
                (respuesta_id,),
            )["activo"]
            == 0
        )


def test_los_seeds_no_pisan_la_configuracion(db, base_de_datos):
    ejecutar(
        db,
        "UPDATE configuracion SET valor = '180' "
        "WHERE clave = 'duracion_estacion_segundos'",
    )
    ejecutar(
        db,
        "UPDATE configuracion SET valor = '3' "
        "WHERE clave = 'max_ayudas_estacion'",
    )

    aplicar_seed(db, base_de_datos["MYSQL_DB"])

    assert fila(
        db,
        "SELECT valor FROM configuracion "
        "WHERE clave = 'duracion_estacion_segundos'",
    )["valor"] == "180"
    assert fila(
        db,
        "SELECT valor FROM configuracion "
        "WHERE clave = 'max_ayudas_estacion'",
    )["valor"] == "3"
