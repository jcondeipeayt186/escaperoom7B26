"""Bienvenida, cantidad de integrantes y reingreso con nombre existente."""

import pytest

from helpers import (
    cerrar_sesion,
    conteo,
    crear_equipo,
    estado_intento,
    ejecutar,
    fila,
    post,
)


def test_bienvenida_muestra_solo_dificultades_habilitadas(cliente, db):
    respuesta = cliente.get("/")

    html = respuesta.get_data(as_text=True)
    assert respuesta.status_code == 200
    assert "Inicial" in html
    assert "Intermedio" not in html
    assert "Avanzado" not in html

    ejecutar(
        db,
        "UPDATE configuracion SET valor = '1' "
        "WHERE clave = 'dificultad_intermedia_habilitada'",
    )
    html = cliente.get("/").get_data(as_text=True)
    assert "Intermedio" in html
    assert "Avanzado" not in html


@pytest.mark.parametrize("cantidad", [1, 2, 3, 4])
def test_cantidad_de_integrantes_valida(cliente, db, cantidad):
    respuesta = post(
        cliente,
        "/",
        {
            "nombre": f"Equipo Cantidad {cantidad}",
            "cantidad_personas": str(cantidad),
            "dificultad": "inicial",
        },
    )

    assert respuesta.status_code == 302
    equipo = fila(
        db,
        "SELECT id, cantidad_personas FROM equipo WHERE nombre = %s",
        (f"Equipo Cantidad {cantidad}",),
    )
    assert equipo["cantidad_personas"] == cantidad


@pytest.mark.parametrize("cantidad", ["0", "5", "", "dos"])
def test_cantidad_de_integrantes_invalida(cliente, db, cantidad):
    respuesta = post(
        cliente,
        "/",
        {
            "nombre": f"Equipo Inválido {cantidad}",
            "cantidad_personas": cantidad,
            "dificultad": "inicial",
        },
    )

    assert respuesta.status_code == 400
    assert (
        conteo(
            db,
            "equipo",
            "WHERE nombre = %s",
            (f"Equipo Inválido {cantidad}",),
        )
        == 0
    )


def test_dificultad_no_habilitada_es_rechazada(cliente, db):
    respuesta = post(
        cliente,
        "/",
        {
            "nombre": "Equipo Nivel Cerrado",
            "cantidad_personas": "2",
            "dificultad": "avanzado",
        },
    )

    assert respuesta.status_code == 400
    assert conteo(db, "equipo", "WHERE nombre = %s", ("Equipo Nivel Cerrado",)) == 0


def test_nombre_existente_pide_id_y_no_duplica(cliente, db):
    primer_envio = post(
        cliente,
        "/",
        {
            "nombre": "Equipo Repetido",
            "cantidad_personas": "2",
            "dificultad": "inicial",
        },
    )
    assert primer_envio.status_code == 302
    equipo = fila(
        db, "SELECT id FROM equipo WHERE nombre = %s", ("Equipo Repetido",)
    )
    assert conteo(db, "equipo") == 1

    cerrar_sesion(cliente)
    segundo_envio = post(
        cliente,
        "/",
        {
            "nombre": "equipo repetido",
            "cantidad_personas": "4",
            "dificultad": "inicial",
        },
    )
    assert segundo_envio.status_code == 302
    assert segundo_envio.headers["Location"].endswith("/equipo/identificar")
    assert conteo(db, "equipo") == 1

    respuesta = post(cliente, "/equipo/identificar", {"equipo_id": equipo["id"]})
    assert respuesta.status_code == 302
    assert conteo(db, "equipo") == 1
    # Reanuda el intento activo, no crea otro.
    assert conteo(db, "intento", "WHERE equipo_id = %s", (equipo["id"],)) == 1

    # La cantidad del formulario no pisa la original del equipo.
    conservado = fila(
        db,
        "SELECT cantidad_personas FROM equipo WHERE id = %s",
        (equipo["id"],),
    )
    assert conservado["cantidad_personas"] == 2


def test_id_incorrecto_no_revela_ni_crea_intento(cliente, db):
    equipo_id, intento_id = crear_equipo(db, "Equipo Identificar")
    otro_equipo_id, _ = crear_equipo(db, "Equipo Secreto")
    ejecutar(
        db,
        "UPDATE intento SET finalizado = 'abandono', fecha_fin = NOW(3) "
        "WHERE id = %s",
        (intento_id,),
    )

    cerrar_sesion(cliente)
    post(
        cliente,
        "/",
        {
            "nombre": "Equipo Identificar",
            "cantidad_personas": "2",
            "dificultad": "inicial",
        },
    )
    respuesta = post(
        cliente, "/equipo/identificar", {"equipo_id": str(otro_equipo_id)}
    )

    html = respuesta.get_data(as_text=True)
    assert respuesta.status_code == 400
    # El ID pertenece a otro equipo: no debe revelar su nombre ni sus datos.
    assert "Equipo Secreto" not in html
    assert "Equipo Identificar" in html
    assert conteo(db, "intento", "WHERE equipo_id = %s", (equipo_id,)) == 1


def test_reingreso_sin_intento_activo_crea_uno_nuevo(cliente, db):
    equipo_id, intento_id = crear_equipo(db, "Equipo Vuelve")
    ejecutar(
        db,
        "UPDATE intento SET finalizado = 'abandono', fecha_fin = NOW(3) "
        "WHERE id = %s",
        (intento_id,),
    )

    cerrar_sesion(cliente)
    post(
        cliente,
        "/",
        {
            "nombre": "Equipo Vuelve",
            "cantidad_personas": "2",
            "dificultad": "inicial",
        },
    )
    respuesta = post(cliente, "/equipo/identificar", {"equipo_id": equipo_id})

    assert respuesta.status_code == 302
    intentos = db.cursor()
    with intentos as cursor:
        cursor.execute(
            "SELECT id, fecha_fin FROM intento WHERE equipo_id = %s ORDER BY id",
            (equipo_id,),
        )
        filas_intento = cursor.fetchall()
    assert len(filas_intento) == 2
    assert filas_intento[0]["fecha_fin"] is not None
    assert filas_intento[1]["fecha_fin"] is None
    assert estado_intento(db, filas_intento[1]["id"])["finalizado"] is None
