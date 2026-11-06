"""Selección de 4 preguntas por estación, estable y por dificultad."""

import pytest

from app.servicios import seleccion
from helpers import (
    crear_equipo,
    ejecutar,
    fila,
    filas,
    iniciar_sesion,
    post,
)


def _preparar(app, intento_id, estacion_id, dificultad="inicial"):
    with app.app_context():
        return seleccion.preparar_estacion(
            intento_id, estacion_id, dificultad
        )


def _temas_de_preguntas(db, pregunta_ids):
    if not pregunta_ids:
        return set()
    marcadores = ", ".join(["%s"] * len(pregunta_ids))
    return {
        fila["tema_id"]
        for fila in filas(
            db,
            f"SELECT DISTINCT tema_id FROM pregunta WHERE id IN ({marcadores})",
            tuple(pregunta_ids),
        )
    }


def test_cada_estacion_recibe_cuatro_preguntas_y_una_por_tema(app, db):
    _, intento_id = crear_equipo(db, "Equipo Selección")

    for estacion in filas(db, "SELECT id FROM estacion ORDER BY orden"):
        estacion_id = estacion["id"]
        elegidas = _preparar(app, intento_id, estacion_id)
        ids = [registro["pregunta_id"] for registro in elegidas]

        assert len(ids) == 4
        assert len(set(ids)) == 4
        assert [registro["orden"] for registro in elegidas] == [1, 2, 3, 4]

        temas_activos = {
            tema["id"]
            for tema in filas(
                db,
                "SELECT id FROM tema WHERE estacion_id = %s AND activo = 1",
                (estacion_id,),
            )
        }
        temas_elegidos = _temas_de_preguntas(db, ids)
        assert temas_activos <= temas_elegidos

        dificultades = {
            registro["dificultad"]
            for registro in filas(
                db,
                f"SELECT dificultad FROM pregunta WHERE id IN "
                f"({', '.join(['%s'] * len(ids))})",
                tuple(ids),
            )
        }
        assert dificultades == {"inicial"}


def test_el_html_de_la_estacion_no_revela_la_correcta(cliente, db):
    equipo_id, intento_id = crear_equipo(db, "Equipo Sin Fugas")
    iniciar_sesion(cliente, equipo_id, intento_id)

    html = cliente.get("/juego/estacion/1").get_data(as_text=True)

    assert "data-correcta" not in html.lower()
    assert "checked" not in html.lower()
    assert "respuesta_id" not in html
    assert "respuesta correcta" not in html.lower()


def test_seleccion_es_estable_al_repetir_y_recargar(app, db, cliente):
    equipo_id, intento_id = crear_equipo(db, "Equipo Estable")
    estacion_id = fila(db, "SELECT id FROM estacion WHERE orden = 1")["id"]

    primera = _preparar(app, intento_id, estacion_id)
    segunda = _preparar(app, intento_id, estacion_id)
    assert primera == segunda

    iniciar_sesion(cliente, equipo_id, intento_id)
    cliente.get("/juego/estacion/1")
    tercera = filas(
        db,
        "SELECT pregunta_id, orden FROM intento_pregunta "
        "WHERE intento_id = %s AND estacion_id = %s ORDER BY orden",
        (intento_id, estacion_id),
    )
    assert [
        {"pregunta_id": registro["pregunta_id"], "orden": registro["orden"]}
        for registro in primera
    ] == [
        {"pregunta_id": registro["pregunta_id"], "orden": registro["orden"]}
        for registro in tercera
    ]

    cliente.get("/juego/estacion/1")
    cuarta = filas(
        db,
        "SELECT pregunta_id, orden FROM intento_pregunta "
        "WHERE intento_id = %s AND estacion_id = %s ORDER BY orden",
        (intento_id, estacion_id),
    )
    assert tercera == cuarta


def test_sin_cobertura_del_nivel_no_guarda_seleccion_parcial(app, db, cliente):
    equipo_id, intento_id = crear_equipo(db, "Equipo Sin Nivel")
    estacion_id = fila(db, "SELECT id FROM estacion WHERE orden = 1")["id"]

    with pytest.raises(seleccion.ErrorSeleccion):
        _preparar(app, intento_id, estacion_id, "intermedio")

    assert (
        fila(
            db,
            "SELECT COUNT(*) AS total FROM intento_pregunta "
            "WHERE intento_id = %s",
            (intento_id,),
        )["total"]
        == 0
    )
    assert (
        fila(
            db,
            "SELECT COUNT(*) AS total FROM intento_estacion "
            "WHERE intento_id = %s",
            (intento_id,),
        )["total"]
        == 0
    )

    iniciar_sesion(cliente, equipo_id, intento_id)
    ejecutar(
        db,
        "UPDATE intento SET dificultad = 'intermedio' WHERE id = %s",
        (intento_id,),
    )
    respuesta = cliente.get("/juego/estacion/1")
    assert respuesta.status_code == 503


def test_seleccion_parcial_guardada_es_error(app, db):
    _, intento_id = crear_equipo(db, "Equipo Parcial")
    estacion_id = fila(db, "SELECT id FROM estacion WHERE orden = 1")["id"]
    ejecutar(
        db,
        "INSERT INTO intento_estacion (intento_id, estacion_id, fecha_inicio) "
        "VALUES (%s, %s, NOW(3))",
        (intento_id, estacion_id),
    )
    ejecutar(
        db,
        "INSERT INTO intento_pregunta "
        "(intento_id, estacion_id, pregunta_id, orden) VALUES (%s, %s, 1, 1)",
        (intento_id, estacion_id),
    )

    with pytest.raises(seleccion.SeleccionIncompleta):
        _preparar(app, intento_id, estacion_id)

    assert (
        fila(
            db,
            "SELECT COUNT(*) AS total FROM intento_pregunta "
            "WHERE intento_id = %s",
            (intento_id,),
        )["total"]
        == 1
    )


def test_mas_de_cuatro_temas_sortea_cuatro_temas(app, db):
    # La estación 2 tiene 3 temas; se agregan 2 para forzar el caso > 4.
    estacion_id = fila(db, "SELECT id FROM estacion WHERE orden = 2")["id"]
    for indice in range(2):
        tema_id = ejecutar(
            db,
            "INSERT INTO tema (nombre, estacion_id, activo) VALUES (%s, %s, 1)",
            (f"Tema extra {indice}", estacion_id),
        )
        ejecutar(
            db,
            "INSERT INTO pregunta "
            "(titulo, tema_id, dificultad, activo) "
            "VALUES (%s, %s, 'inicial', 1)",
            (f"Pregunta extra {indice}", tema_id),
        )

    for numero in range(5):
        _, intento_id = crear_equipo(db, f"Equipo Cinco Temas {numero}")
        elegidas = _preparar(app, intento_id, estacion_id)
        ids = [registro["pregunta_id"] for registro in elegidas]

        assert len(ids) == 4
        assert len(set(ids)) == 4
        assert len(_temas_de_preguntas(db, ids)) == 4
