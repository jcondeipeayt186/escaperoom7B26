"""Contadores calculados desde MySQL, aviso de 30 segundos y tiempo agotado."""

import re

from app.servicios.tiempos import calcular_tiempos
from helpers import (
    conteo,
    crear_equipo,
    ejecutar,
    enviar,
    estado_intento,
    fila_tiempo,
    formulario,
    iniciar_sesion,
    post,
    preparar_por_url,
)


def _estado_json(cliente):
    respuesta = cliente.get("/juego/estado")
    assert respuesta.status_code == 200
    return respuesta.get_json()


def test_contadores_desde_las_fechas_de_mysql(cliente, db):
    equipo_id, intento_id = crear_equipo(db, "Equipo Tiempos")
    iniciar_sesion(cliente, equipo_id, intento_id)
    estacion_id, _ = preparar_por_url(cliente, db, intento_id, 1)

    ejecutar(
        db,
        "UPDATE intento SET fecha_inicio = DATE_SUB(NOW(3), "
        "INTERVAL 200 SECOND) WHERE id = %s",
        (intento_id,),
    )
    ejecutar(
        db,
        "UPDATE intento_estacion SET fecha_inicio = DATE_SUB(NOW(3), "
        "INTERVAL 100 SECOND) WHERE intento_id = %s AND estacion_id = %s",
        (intento_id, estacion_id),
    )

    datos = _estado_json(cliente)
    assert abs(datos["general_segundos"] - 200) <= 2
    assert abs(datos["estacion_segundos"] - 140) <= 2
    assert datos["duracion_estacion_segundos"] == 240
    assert datos["aviso_activo"] is False
    assert datos["servidor_ms"] > 0
    assert datos["intento_inicio_ms"] > 0
    assert datos["estacion_fin_ms"] > 0


def test_aviso_de_treinta_segundos(cliente, db):
    equipo_id, intento_id = crear_equipo(db, "Equipo Aviso")
    iniciar_sesion(cliente, equipo_id, intento_id)
    estacion_id, _ = preparar_por_url(cliente, db, intento_id, 1)

    ejecutar(
        db,
        "UPDATE intento_estacion SET fecha_inicio = DATE_SUB(NOW(3), "
        "INTERVAL 215 SECOND) WHERE intento_id = %s AND estacion_id = %s",
        (intento_id, estacion_id),
    )

    datos = _estado_json(cliente)
    assert 0 < datos["estacion_segundos"] <= 30
    assert datos["aviso_activo"] is True
    assert datos["aviso_segundos"] == 30


def test_hud_muestra_el_tiempo_general_en_mm_ss(cliente, db):
    equipo_id, intento_id = crear_equipo(db, "Equipo HUD")
    iniciar_sesion(cliente, equipo_id, intento_id)
    preparar_por_url(cliente, db, intento_id, 1)

    ejecutar(
        db,
        "UPDATE intento SET fecha_inicio = DATE_SUB(NOW(3), "
        "INTERVAL 125 SECOND) WHERE id = %s",
        (intento_id,),
    )

    html = cliente.get("/juego/estacion/1").get_data(as_text=True)
    bloque = html.split('id="tiempo-general"', 1)[1].split("</div>", 1)[0]

    assert re.search(r"\d{2}:\d{2}", bloque)
    assert not re.search(r"\d{2}:\d{2}:\d{2}", bloque)


def test_recarga_no_reinicia_las_fechas_ni_la_seleccion(cliente, db):
    equipo_id, intento_id = crear_equipo(db, "Equipo Recarga")
    iniciar_sesion(cliente, equipo_id, intento_id)
    estacion_id, _ = preparar_por_url(cliente, db, intento_id, 1)

    primera = fila_tiempo(db, intento_id, estacion_id)
    seleccion = conteo(
        db, "intento_pregunta", "WHERE intento_id = %s", (intento_id,)
    )

    for _ in range(3):
        assert cliente.get("/juego/estacion/1").status_code == 200

    segunda = fila_tiempo(db, intento_id, estacion_id)
    assert segunda["fecha_inicio"] == primera["fecha_inicio"]
    assert conteo(
        db, "intento_pregunta", "WHERE intento_id = %s", (intento_id,)
    ) == seleccion


def test_tiempo_agotado_en_estado_cierra_como_por_tiempo(cliente, db):
    equipo_id, intento_id = crear_equipo(db, "Equipo Tiempo Estado")
    iniciar_sesion(cliente, equipo_id, intento_id)
    estacion_id, _ = preparar_por_url(cliente, db, intento_id, 1)

    ejecutar(
        db,
        "UPDATE intento_estacion SET fecha_inicio = DATE_SUB(NOW(3), "
        "INTERVAL 241 SECOND) WHERE intento_id = %s AND estacion_id = %s",
        (intento_id, estacion_id),
    )

    datos = _estado_json(cliente)
    assert datos["estado"] == "por_tiempo"
    assert datos["redirigir"].endswith("/juego/eliminado")

    intento = estado_intento(db, intento_id)
    assert intento["finalizado"] == "por_tiempo"
    assert intento["fecha_fin"] is not None
    assert intento["puntaje_obtenido"] is None


def test_tiempo_agotado_tambien_se_valida_en_post(cliente, db):
    equipo_id, intento_id = crear_equipo(db, "Equipo Tiempo POST")
    iniciar_sesion(cliente, equipo_id, intento_id)
    estacion_id, preguntas = preparar_por_url(cliente, db, intento_id, 1)

    ejecutar(
        db,
        "UPDATE intento_estacion SET fecha_inicio = DATE_SUB(NOW(3), "
        "INTERVAL 241 SECOND) WHERE intento_id = %s AND estacion_id = %s",
        (intento_id, estacion_id),
    )

    respuesta = enviar(cliente, 1, formulario(preguntas))
    assert respuesta.status_code == 302
    assert respuesta.headers["Location"].endswith("/juego/eliminado")
    assert estado_intento(db, intento_id)["finalizado"] == "por_tiempo"
    assert conteo(db, "intento_envio", "WHERE intento_id = %s", (intento_id,)) == 0


def test_tiempo_de_estacion_congelado_en_la_transicion(app, cliente, db):
    equipo_id, intento_id = crear_equipo(db, "Equipo Transición")
    iniciar_sesion(cliente, equipo_id, intento_id)
    estacion_id, preguntas = preparar_por_url(cliente, db, intento_id, 1)
    ejecutar(
        db,
        "UPDATE intento_estacion SET fecha_inicio = DATE_SUB(NOW(3), "
        "INTERVAL 100 SECOND) WHERE intento_id = %s AND estacion_id = %s",
        (intento_id, estacion_id),
    )
    enviar(cliente, 1, formulario(preguntas))

    with app.app_context():
        antes = calcular_tiempos(intento_id, estacion_id, 240)
    assert antes["completada"] is True
    assert antes["estacion_segundos"] == 140

    ejecutar(
        db,
        "UPDATE intento_estacion SET fecha_fin = DATE_ADD(fecha_inicio, "
        "INTERVAL 123 SECOND) WHERE intento_id = %s AND estacion_id = %s",
        (intento_id, estacion_id),
    )
    with app.app_context():
        despues = calcular_tiempos(intento_id, estacion_id, 240)
        otra_vez = calcular_tiempos(intento_id, estacion_id, 240)
    assert despues["estacion_segundos"] == 117
    assert {
        clave: valor
        for clave, valor in despues.items()
        if clave != "servidor_ms"
    } == {
        clave: valor
        for clave, valor in otra_vez.items()
        if clave != "servidor_ms"
    }

    html = cliente.get("/juego/transicion/1").get_data(as_text=True)
    assert "02:03" in html
