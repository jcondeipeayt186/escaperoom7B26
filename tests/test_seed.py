"""El seed es idempotente y respeta los cambios del administrador."""

from helpers import aplicar_seed, conteo, ejecutar, fila


def test_reejecutar_el_seed_no_duplica_contenido(db, base_de_datos):
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
    assert antes["pregunta"] == 20
    assert antes["respuesta"] == 60


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


def test_el_seed_no_reactiva_contenido_desactivado(db, base_de_datos):
    ejecutar(db, "UPDATE estacion SET activo = 0 WHERE id = 5")
    ejecutar(db, "UPDATE tema SET activo = 0 WHERE id = 1")
    ejecutar(db, "UPDATE pregunta SET activo = 0 WHERE id = 1")
    ejecutar(db, "UPDATE respuesta SET activo = 0 WHERE id = 1")

    aplicar_seed(db, base_de_datos["MYSQL_DB"])

    assert fila(db, "SELECT activo FROM estacion WHERE id = 5")["activo"] == 0
    assert fila(db, "SELECT activo FROM tema WHERE id = 1")["activo"] == 0
    assert fila(db, "SELECT activo FROM pregunta WHERE id = 1")["activo"] == 0
    assert fila(db, "SELECT activo FROM respuesta WHERE id = 1")["activo"] == 0


def test_el_seed_no_pisa_la_configuracion(db, base_de_datos):
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
