"""Reglas del juego: avance, eliminaciones, envíos, ayudas y cierre."""

import pytest

from helpers import (
    completar_estacion,
    conteo,
    crear_equipo,
    ejecutar,
    enviar,
    estado_intento,
    fila,
    fila_tiempo,
    formulario,
    iniciar_sesion,
    post,
    preguntas_del_intento,
    preparar_por_url,
)


def _resumen(db, intento_id, estacion_id):
    return fila(
        db,
        "SELECT ie.ayudas, ie.completada, "
        " (SELECT COUNT(*) FROM intento_envio e WHERE e.intento_id = %s "
        "  AND e.estacion_id = %s) AS envios, "
        " (SELECT COUNT(*) FROM incorrecta i "
        "  JOIN intento_envio e ON e.id = i.intento_envio_id "
        "  WHERE i.intento_id = %s AND e.estacion_id = %s) AS incorrectas "
        "FROM intento_estacion ie "
        "WHERE ie.intento_id = %s AND ie.estacion_id = %s",
        (
            intento_id,
            estacion_id,
            intento_id,
            estacion_id,
            intento_id,
            estacion_id,
        ),
    )


def test_avance_solo_con_las_cuatro_correctas(cliente, db):
    equipo_id, intento_id = crear_equipo(db, "Equipo Avance")
    iniciar_sesion(cliente, equipo_id, intento_id)
    estacion_id, preguntas = preparar_por_url(cliente, db, intento_id, 1)

    con_una_incorrecta = enviar(
        cliente, 1, formulario(preguntas, incorrectas=1)
    )
    assert con_una_incorrecta.status_code == 302
    assert con_una_incorrecta.headers["Location"].endswith("/juego/estacion/1")
    assert fila_tiempo(db, intento_id, estacion_id)["completada"] == 0
    assert _resumen(db, intento_id, estacion_id)["envios"] == 1

    assert conteo(db, "respuesta_elegida", "WHERE intento_id = %s", (intento_id,)) == 4
    assert conteo(db, "incorrecta", "WHERE intento_id = %s", (intento_id,)) == 1
    envio = fila(
        db,
        "SELECT respuestas_correctas, respuestas_incorrectas "
        "FROM intento_envio WHERE intento_id = %s",
        (intento_id,),
    )
    assert envio == {"respuestas_correctas": 3, "respuestas_incorrectas": 1}

    todas_correctas = enviar(cliente, 1, formulario(preguntas))
    assert todas_correctas.status_code == 302
    assert todas_correctas.headers["Location"].endswith("/juego/transicion/1")
    assert fila_tiempo(db, intento_id, estacion_id)["completada"] == 1
    assert estado_intento(db, intento_id)["finalizado"] is None

    assert conteo(db, "respuesta_elegida", "WHERE intento_id = %s", (intento_id,)) == 8
    assert conteo(db, "incorrecta", "WHERE intento_id = %s", (intento_id,)) == 1


def test_dos_incorrectas_en_un_envio_eliminan(cliente, db):
    equipo_id, intento_id = crear_equipo(db, "Equipo Dos Errores")
    iniciar_sesion(cliente, equipo_id, intento_id)
    estacion_id, preguntas = preparar_por_url(cliente, db, intento_id, 1)

    respuesta = enviar(cliente, 1, formulario(preguntas, incorrectas=2))

    assert respuesta.status_code == 302
    assert respuesta.headers["Location"].endswith("/juego/eliminado")
    intento = estado_intento(db, intento_id)
    assert intento["finalizado"] == "por_respuestas_incorrectas"
    assert intento["fecha_fin"] is not None
    assert intento["puntaje_obtenido"] is None
    estacion = fila_tiempo(db, intento_id, estacion_id)
    assert estacion["completada"] == 0
    assert estacion["fecha_fin"] is not None
    assert conteo(db, "incorrecta", "WHERE intento_id = %s", (intento_id,)) == 2


def test_incorrectas_acumuladas_en_dos_envios_eliminan(cliente, db):
    equipo_id, intento_id = crear_equipo(db, "Equipo Acumula")
    iniciar_sesion(cliente, equipo_id, intento_id)
    estacion_id, preguntas = preparar_por_url(cliente, db, intento_id, 1)

    primero = enviar(cliente, 1, formulario(preguntas, incorrectas=1))
    assert primero.headers["Location"].endswith("/juego/estacion/1")
    assert estado_intento(db, intento_id)["finalizado"] is None
    assert _resumen(db, intento_id, estacion_id)["incorrectas"] == 1

    segundo = enviar(cliente, 1, formulario(preguntas, incorrectas=1))
    assert segundo.headers["Location"].endswith("/juego/eliminado")
    assert estado_intento(db, intento_id)["finalizado"] == (
        "por_respuestas_incorrectas"
    )
    assert _resumen(db, intento_id, estacion_id)["envios"] == 2


def test_maximo_dos_envios_y_solo_finalizar(cliente, db):
    equipo_id, intento_id = crear_equipo(db, "Equipo Dos Envíos")
    iniciar_sesion(cliente, equipo_id, intento_id)
    estacion_id, preguntas = preparar_por_url(cliente, db, intento_id, 1)
    # Se sube el máximo de incorrectas para llegar al segundo envío sin eliminar.
    ejecutar(
        db,
        "UPDATE configuracion SET valor = '10' "
        "WHERE clave = 'max_respuestas_incorrectas'",
    )

    primero = enviar(cliente, 1, formulario(preguntas, incorrectas=4))
    assert primero.headers["Location"].endswith("/juego/estacion/1")
    assert _resumen(db, intento_id, estacion_id)["envios"] == 1

    segundo = enviar(cliente, 1, formulario(preguntas, incorrectas=4))
    assert segundo.headers["Location"].endswith("/juego/estacion/1")
    assert _resumen(db, intento_id, estacion_id)["envios"] == 2
    assert estado_intento(db, intento_id)["finalizado"] is None

    html = cliente.get("/juego/estacion/1").get_data(as_text=True)
    assert "Ya no quedan envíos" in html
    assert "Finalizar juego" in html
    assert "Comprobar respuestas" not in html
    assert "Ayuda 1" not in html

    tercero = enviar(cliente, 1, formulario(preguntas))
    assert tercero.headers["Location"].endswith("/juego/estacion/1")
    assert _resumen(db, intento_id, estacion_id)["envios"] == 2

    ayuda = post(cliente, "/juego/estacion/1/ayuda")
    assert ayuda.headers["Location"].endswith("/juego/estacion/1")
    assert _resumen(db, intento_id, estacion_id)["ayudas"] == 0

    finalizar = post(cliente, "/juego/estacion/1/finalizar")
    assert finalizar.headers["Location"].endswith("/juego/eliminado")
    assert estado_intento(db, intento_id)["finalizado"] == (
        "por_respuestas_incorrectas"
    )


def test_maximo_dos_ayudas_y_contadores(cliente, db):
    equipo_id, intento_id = crear_equipo(db, "Equipo Ayudas")
    iniciar_sesion(cliente, equipo_id, intento_id)
    estacion_id, _ = preparar_por_url(cliente, db, intento_id, 1)

    for numero in (1, 2):
        respuesta = post(cliente, "/juego/estacion/1/ayuda")
        assert respuesta.status_code == 302
        assert _resumen(db, intento_id, estacion_id)["ayudas"] == numero

    post(cliente, "/juego/estacion/1/ayuda")
    assert _resumen(db, intento_id, estacion_id)["ayudas"] == 2
    assert estado_intento(db, intento_id)["cantidad_ayudas"] == 2

    html = cliente.get("/juego/estacion/1").get_data(as_text=True)
    assert "Ayuda 1" in html
    assert "disabled" in html
    assert "La pista se lee en papel" in html


def test_envio_incompleto_o_con_respuesta_ajena_no_registra(cliente, db):
    equipo_id, intento_id = crear_equipo(db, "Equipo Envío Inválido")
    iniciar_sesion(cliente, equipo_id, intento_id)
    estacion_id, preguntas = preparar_por_url(cliente, db, intento_id, 1)

    incompleto = formulario(preguntas)
    incompleto.pop(f"pregunta_{preguntas[0]['id']}")
    respuesta = enviar(cliente, 1, incompleto)
    assert respuesta.status_code == 302
    assert conteo(db, "intento_envio", "WHERE intento_id = %s", (intento_id,)) == 0

    ajena = formulario(preguntas)
    ajena[f"pregunta_{preguntas[0]['id']}"] = preguntas[1]["correcta"]
    respuesta = enviar(cliente, 1, ajena)
    assert respuesta.status_code == 302
    assert conteo(db, "intento_envio", "WHERE intento_id = %s", (intento_id,)) == 0

    con_extra = formulario(preguntas)
    con_extra["pregunta_9999"] = preguntas[0]["correcta"]
    respuesta = enviar(cliente, 1, con_extra)
    assert respuesta.status_code == 302
    assert conteo(db, "intento_envio", "WHERE intento_id = %s", (intento_id,)) == 0


def test_abandono_cierra_intento_y_estacion(cliente, db):
    equipo_id, intento_id = crear_equipo(db, "Equipo Abandona")
    iniciar_sesion(cliente, equipo_id, intento_id)
    estacion_id, _ = preparar_por_url(cliente, db, intento_id, 1)

    respuesta = post(cliente, "/juego/estacion/1/abandonar")
    assert respuesta.status_code == 302
    assert respuesta.headers["Location"].endswith("/juego/eliminado")

    intento = estado_intento(db, intento_id)
    assert intento["finalizado"] == "abandono"
    assert intento["fecha_fin"] is not None
    assert intento["puntaje_obtenido"] is None
    assert fila_tiempo(db, intento_id, estacion_id)["fecha_fin"] is not None

    html = cliente.get("/juego/eliminado").get_data(as_text=True)
    assert "abandonó" in html


def test_recorrido_completo_cierra_la_quinta_estacion(cliente, db):
    equipo_id, intento_id = crear_equipo(db, "Equipo Completo")
    iniciar_sesion(cliente, equipo_id, intento_id)

    for orden in range(1, 6):
        estacion_id, primera = completar_estacion(
            cliente, db, intento_id, orden
        )
        assert primera.status_code == 302
        if orden < 5:
            assert primera.headers["Location"].endswith(
                f"/juego/transicion/{orden}"
            )
            continuar = post(
                cliente, f"/juego/transicion/{orden}/continuar"
            )
            assert continuar.status_code == 302
            assert continuar.headers["Location"].endswith(
                f"/juego/estacion/{orden + 1}"
            )
        else:
            assert primera.headers["Location"].endswith("/juego/transicion/5")

    intento = fila(
        db,
        "SELECT finalizado, fecha_inicio, fecha_fin, puntaje_obtenido, "
        "       se_completo_ok "
        "FROM intento WHERE id = %s",
        (intento_id,),
    )
    ultima = fila_tiempo(db, intento_id, estacion_id)
    assert intento["finalizado"] == "completo"
    assert intento["se_completo_ok"] == 1
    assert intento["fecha_fin"] == ultima["fecha_fin"]
    assert intento["puntaje_obtenido"] == int(
        (intento["fecha_fin"] - intento["fecha_inicio"]).total_seconds()
    )
    assert conteo(
        db,
        "intento_estacion",
        "WHERE intento_id = %s AND completada = 1",
        (intento_id,),
    ) == 5

    html = cliente.get("/juego/final").get_data(as_text=True)
    assert "Equipo Completo" in html
    assert "Ranking" in html
    assert "Top 10 · Inicial" in html
    assert "Posición · Inicial" in html


def test_final_de_intermedio_usa_el_ranking_de_su_nivel(cliente, db):
    equipo_id = ejecutar(
        db,
        "INSERT INTO equipo (nombre, cantidad_personas) "
        "VALUES ('Equipo Intermedio', 2)",
    )
    intento_id = ejecutar(
        db,
        "INSERT INTO intento "
        "(equipo_id, dificultad, fecha_inicio, fecha_fin, cantidad_ayudas, "
        " puntaje_obtenido, finalizado, ultima_estacion_visitada) "
        "VALUES (%s, 'intermedio', '2026-01-01 10:00:00', "
        "        '2026-01-01 10:05:00', 0, 300, 'completo', 1)",
        (equipo_id,),
    )

    equipo_rival = ejecutar(
        db,
        "INSERT INTO equipo (nombre, cantidad_personas) "
        "VALUES ('Rival Intermedio', 2)",
    )
    ejecutar(
        db,
        "INSERT INTO intento "
        "(equipo_id, dificultad, fecha_inicio, fecha_fin, cantidad_ayudas, "
        " puntaje_obtenido, finalizado, ultima_estacion_visitada) "
        "VALUES (%s, 'intermedio', '2026-01-01 09:00:00', "
        "        '2026-01-01 09:04:00', 0, 240, 'completo', 1)",
        (equipo_rival,),
    )

    equipo_inicial = ejecutar(
        db,
        "INSERT INTO equipo (nombre, cantidad_personas) "
        "VALUES ('Inicial Rápido', 2)",
    )
    ejecutar(
        db,
        "INSERT INTO intento "
        "(equipo_id, dificultad, fecha_inicio, fecha_fin, cantidad_ayudas, "
        " puntaje_obtenido, finalizado, ultima_estacion_visitada) "
        "VALUES (%s, 'inicial', '2026-01-01 08:00:00', "
        "        '2026-01-01 08:01:00', 0, 60, 'completo', 1)",
        (equipo_inicial,),
    )

    iniciar_sesion(cliente, equipo_id, intento_id)
    html = cliente.get("/juego/final").get_data(as_text=True)

    assert "Posición · Intermedio" in html
    assert "Top 10 · Intermedio" in html
    assert "Pos. general" in html
    assert "Pos. nivel" in html
    assert "Rival Intermedio" in html

    # El top 10 se limita al nivel del intento.
    top = html.split("Ranking completo", 1)[0]
    assert "Rival Intermedio" in top
    assert "Inicial Rápido" not in top
