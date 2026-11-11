"""Panel de administración: acceso, contenido, cobertura y estadísticas."""

import pytest

from app.servicios import admin_estadisticas
from helpers import (
    conteo,
    crear_equipo,
    ejecutar,
    fila,
    filas,
    login_admin,
    post,
)

RUTAS_PROTEGIDAS = (
    "/admin/",
    "/admin/estacion",
    "/admin/equipo",
    "/admin/cobertura",
    "/admin/dificultades",
    "/admin/intentos-activos",
    "/admin/estadisticas",
    "/admin/estacion/nuevo",
    "/admin/estacion/1/editar",
)

TABLAS_HISTORICAS = (
    "equipo",
    "intento",
    "intento_estacion",
    "intento_envio",
    "intento_pregunta",
    "respuesta_elegida",
    "incorrecta",
)


def _con_sesion(cliente, credenciales_admin):
    respuesta = login_admin(cliente, credenciales_admin)
    assert respuesta.status_code == 302
    assert respuesta.headers["Location"].endswith("/admin/")


def _crear_pregunta(cliente, db, tema_id, titulo):
    respuesta = post(
        cliente,
        "/admin/pregunta/nuevo",
        {
            "titulo": titulo,
            "descripcion": "",
            "tema_id": str(tema_id),
            "dificultad": "inicial",
        },
    )
    assert respuesta.status_code == 302, respuesta.get_data(as_text=True)
    return fila(db, "SELECT id FROM pregunta WHERE titulo = %s", (titulo,))["id"]


def _crear_respuesta(cliente, db, pregunta_id, contenido, correcta):
    respuesta = post(
        cliente,
        "/admin/respuesta/nuevo",
        {
            "contenido": contenido,
            "pregunta_id": str(pregunta_id),
            "correcta": "1" if correcta else "",
            "activo": "1",
        },
    )
    assert respuesta.status_code == 302, respuesta.get_data(as_text=True)
    return fila(
        db,
        "SELECT id FROM respuesta WHERE contenido = %s",
        (contenido,),
    )["id"]


def _activar_pregunta(cliente, db, pregunta, activo=True):
    return post(
        cliente,
        f"/admin/pregunta/{pregunta['id']}/editar",
        {
            "titulo": pregunta["titulo"],
            "descripcion": pregunta["descripcion"] or "",
            "tema_id": str(pregunta["tema_id"]),
            "dificultad": pregunta["dificultad"],
            "activo": "1" if activo else "",
        },
    )


def _datos_pregunta(db, pregunta_id):
    return fila(
        db,
        "SELECT id, titulo, descripcion, tema_id, dificultad, activo "
        "FROM pregunta WHERE id = %s",
        (pregunta_id,),
    )


def _crear_intento(db, nombre, dificultad, inicio, fin, finalizado):
    equipo_id = ejecutar(
        db,
        "INSERT INTO equipo (nombre, cantidad_personas) VALUES (%s, 2)",
        (nombre,),
    )
    segundos = int((fin - inicio).total_seconds()) if fin is not None else None
    return ejecutar(
        db,
        "INSERT INTO intento "
        "(equipo_id, dificultad, fecha_inicio, fecha_fin, puntaje_obtenido, "
        " finalizado, ultima_estacion_visitada) "
        "VALUES (%s, %s, %s, %s, %s, %s, 1)",
        (
            equipo_id,
            dificultad,
            inicio,
            fin,
            segundos if finalizado == "completo" else None,
            finalizado,
        ),
    )


# ---------------------------------------------------------------------------
# Acceso
# ---------------------------------------------------------------------------


def test_rutas_del_admin_exigen_login(cliente):
    for ruta in RUTAS_PROTEGIDAS:
        respuesta = cliente.get(ruta)
        assert respuesta.status_code == 302, ruta
        assert respuesta.headers["Location"].endswith("/admin"), ruta

    respuesta = post(cliente, "/admin/estacion/nuevo", {})
    assert respuesta.status_code == 302
    assert respuesta.headers["Location"].endswith("/admin")


def test_admin_no_esta_enlazado_desde_paginas_publicas(cliente):
    for ruta in ("/", "/ranking", "/estadisticas"):
        html = cliente.get(ruta).get_data(as_text=True)
        assert "/admin" not in html, ruta


def test_login_y_logout_del_admin(cliente, credenciales_admin):
    _con_sesion(cliente, credenciales_admin)

    panel = cliente.get("/admin/")
    assert panel.status_code == 200
    assert "Panel de control" in panel.get_data(as_text=True)

    salida = post(cliente, "/admin/logout")
    assert salida.status_code == 302
    assert salida.headers["Location"].endswith("/admin")
    assert cliente.get("/admin/").status_code == 302


def test_login_incorrecto_devuelve_401(cliente, credenciales_admin):
    cliente.get("/admin")
    respuesta = post(
        cliente,
        "/admin/login",
        {"usuario": credenciales_admin["usuario"], "clave": "clave-incorrecta"},
    )

    assert respuesta.status_code == 401
    assert "Usuario o clave incorrectos" in respuesta.get_data(as_text=True)
    assert cliente.get("/admin/").status_code == 302


# ---------------------------------------------------------------------------
# Tablas históricas y contenido
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("tabla", TABLAS_HISTORICAS)
def test_tablas_historicas_son_de_solo_lectura(
    cliente, credenciales_admin, tabla
):
    _con_sesion(cliente, credenciales_admin)

    assert cliente.get(f"/admin/{tabla}/nuevo").status_code == 404
    assert post(cliente, f"/admin/{tabla}/nuevo", {}).status_code == 404
    assert cliente.get(f"/admin/{tabla}/1/editar").status_code == 404
    assert (
        post(cliente, f"/admin/{tabla}/1/editar", {}).status_code == 404
    )
    assert (
        post(cliente, f"/admin/{tabla}/1/desactivar").status_code == 404
    )


def test_maximo_cuatro_temas_por_estacion(cliente, db, credenciales_admin):
    _con_sesion(cliente, credenciales_admin)
    estacion_id = fila(db, "SELECT id FROM estacion WHERE orden = 2")["id"]
    activos = conteo(
        db,
        "tema",
        "WHERE estacion_id = %s AND activo = 1",
        (estacion_id,),
    )
    assert activos == 3

    for numero in range(activos, 4):
        respuesta = post(
            cliente,
            "/admin/tema/nuevo",
            {
                "nombre": f"Tema permitido {numero}",
                "estacion_id": str(estacion_id),
                "activo": "1",
            },
        )
        assert respuesta.status_code == 302

    assert (
        conteo(
            db,
            "tema",
            "WHERE estacion_id = %s AND activo = 1",
            (estacion_id,),
        )
        == 4
    )

    respuesta = post(
        cliente,
        "/admin/tema/nuevo",
        {
            "nombre": "Tema de más",
            "estacion_id": str(estacion_id),
            "activo": "1",
        },
    )
    assert respuesta.status_code == 400
    assert "máximo es de 4 temas" in respuesta.get_data(as_text=True)
    assert (
        conteo(
            db,
            "tema",
            "WHERE estacion_id = %s AND activo = 1",
            (estacion_id,),
        )
        == 4
    )


def test_pregunta_con_dos_correctas_no_se_activa(
    cliente, db, credenciales_admin
):
    _con_sesion(cliente, credenciales_admin)
    pregunta_id = _crear_pregunta(cliente, db, 1, "Pregunta con dos correctas")
    _crear_respuesta(cliente, db, pregunta_id, "Opción A", correcta=True)
    _crear_respuesta(cliente, db, pregunta_id, "Opción B", correcta=True)

    pregunta = _datos_pregunta(db, pregunta_id)
    assert pregunta["activo"] == 0

    respuesta = _activar_pregunta(cliente, db, pregunta)
    assert respuesta.status_code == 400
    assert "exactamente una marcada como correcta" in respuesta.get_data(
        as_text=True
    )
    assert _datos_pregunta(db, pregunta_id)["activo"] == 0


def test_pregunta_sin_correctas_no_se_activa(cliente, db, credenciales_admin):
    _con_sesion(cliente, credenciales_admin)
    pregunta_id = _crear_pregunta(cliente, db, 1, "Pregunta sin correcta")
    _crear_respuesta(cliente, db, pregunta_id, "Opción A", correcta=False)
    _crear_respuesta(cliente, db, pregunta_id, "Opción B", correcta=False)

    pregunta = _datos_pregunta(db, pregunta_id)
    respuesta = _activar_pregunta(cliente, db, pregunta)
    assert respuesta.status_code == 400
    assert _datos_pregunta(db, pregunta_id)["activo"] == 0


def test_pregunta_con_una_correcta_se_activa(cliente, db, credenciales_admin):
    _con_sesion(cliente, credenciales_admin)
    pregunta_id = _crear_pregunta(cliente, db, 1, "Pregunta válida")
    _crear_respuesta(cliente, db, pregunta_id, "Opción A", correcta=True)
    _crear_respuesta(cliente, db, pregunta_id, "Opción B", correcta=False)

    pregunta = _datos_pregunta(db, pregunta_id)
    respuesta = _activar_pregunta(cliente, db, pregunta)

    assert respuesta.status_code == 302
    assert _datos_pregunta(db, pregunta_id)["activo"] == 1


def test_marcar_otra_correcta_desmarca_la_anterior(
    cliente, db, credenciales_admin
):
    _con_sesion(cliente, credenciales_admin)
    pregunta_id = _crear_pregunta(cliente, db, 1, "Pregunta cambia correcta")
    _crear_respuesta(cliente, db, pregunta_id, "Opción A", correcta=True)
    b_id = _crear_respuesta(cliente, db, pregunta_id, "Opción B", correcta=False)
    _crear_respuesta(cliente, db, pregunta_id, "Opción C", correcta=False)
    _activar_pregunta(cliente, db, _datos_pregunta(db, pregunta_id))

    respuesta = post(
        cliente,
        f"/admin/respuesta/{b_id}/editar",
        {
            "contenido": "Opción B",
            "pregunta_id": str(pregunta_id),
            "correcta": "1",
            "activo": "1",
        },
    )
    assert respuesta.status_code == 302

    correctas = filas(
        db,
        "SELECT id, correcta FROM respuesta "
        "WHERE pregunta_id = %s AND activo = 1 ORDER BY id",
        (pregunta_id,),
    )
    assert sum(1 for registro in correctas if registro["correcta"]) == 1
    assert [registro["id"] for registro in correctas if registro["correcta"]] == [
        b_id
    ]


def test_baja_logica_de_una_estacion(cliente, db, credenciales_admin):
    _con_sesion(cliente, credenciales_admin)

    respuesta = post(cliente, "/admin/estacion/5/desactivar")
    assert respuesta.status_code == 302

    estacion = fila(
        db, "SELECT id, activo FROM estacion WHERE id = 5"
    )
    assert estacion is not None
    assert estacion["activo"] == 0
    assert conteo(db, "estacion", "WHERE id = 5") == 1


# ---------------------------------------------------------------------------
# Cobertura, dificultades y estadísticas
# ---------------------------------------------------------------------------


def test_cobertura_muestra_todos_los_niveles_completos(
    cliente, credenciales_admin
):
    _con_sesion(cliente, credenciales_admin)

    html = cliente.get("/admin/cobertura").get_data(as_text=True)
    assert "Cobertura de niveles" in html
    assert "Inicial" in html
    assert "Intermedio" in html
    assert "Avanzado" in html
    assert "Siempre habilitada" in html
    assert "Cobertura completa" in html
    assert "Falta cobertura" not in html


def test_cobertura_marca_falta_si_un_tema_no_tiene_preguntas(
    cliente, db, credenciales_admin
):
    ejecutar(
        db,
        "UPDATE pregunta SET activo = 0 "
        "WHERE dificultad = 'intermedio' AND tema_id = 1",
    )
    _con_sesion(cliente, credenciales_admin)

    html = cliente.get("/admin/cobertura").get_data(as_text=True)
    assert "Falta cobertura" in html
    assert "Incompleta" in html


def test_toggle_sin_cobertura_es_rechazado(
    cliente, db, credenciales_admin
):
    ejecutar(
        db,
        "UPDATE pregunta SET activo = 0 "
        "WHERE dificultad = 'intermedio' AND tema_id = 1",
    )
    _con_sesion(cliente, credenciales_admin)

    respuesta = post(
        cliente, "/admin/dificultades", {"intermedio": "1"}
    )

    assert respuesta.status_code == 400
    assert "No hay cobertura completa" in respuesta.get_data(as_text=True)
    valor = fila(
        db,
        "SELECT valor FROM configuracion "
        "WHERE clave = 'dificultad_intermedia_habilitada'",
    )["valor"]
    assert valor == "0"


def test_toggle_bloqueado_con_intento_activo(
    cliente, db, credenciales_admin
):
    crear_equipo(db, "Equipo Jugando")
    _con_sesion(cliente, credenciales_admin)

    html = cliente.get("/admin/dificultades").get_data(as_text=True)
    assert "No se pueden cambiar las" in html
    assert "dificultades hasta que terminen" in html

    respuesta = post(
        cliente, "/admin/dificultades", {"intermedio": "1"}
    )
    assert respuesta.status_code == 400
    assert "mientras hay equipos jugando" in respuesta.get_data(as_text=True)
    valor = fila(
        db,
        "SELECT valor FROM configuracion "
        "WHERE clave = 'dificultad_intermedia_habilitada'",
    )["valor"]
    assert valor == "0"


def test_toggle_falla_si_falta_una_estacion(cliente, db, credenciales_admin):
    ejecutar(
        db,
        "UPDATE pregunta SET activo = 0 "
        "WHERE dificultad = 'intermedio' AND tema_id IN "
        "(SELECT id FROM tema WHERE estacion_id = 5)",
    )
    _con_sesion(cliente, credenciales_admin)

    respuesta = post(
        cliente, "/admin/dificultades", {"intermedio": "1"}
    )

    assert respuesta.status_code == 400
    assert "No hay cobertura completa" in respuesta.get_data(as_text=True)
    assert fila(
        db,
        "SELECT valor FROM configuracion "
        "WHERE clave = 'dificultad_intermedia_habilitada'",
    )["valor"] == "0"


def test_toggle_con_cobertura_completa(cliente, db, credenciales_admin):
    _con_sesion(cliente, credenciales_admin)

    habilitar = post(
        cliente, "/admin/dificultades", {"intermedio": "1"}
    )
    assert habilitar.status_code == 302
    assert fila(
        db,
        "SELECT valor FROM configuracion "
        "WHERE clave = 'dificultad_intermedia_habilitada'",
    )["valor"] == "1"
    assert "Intermedio" in cliente.get("/").get_data(as_text=True)

    deshabilitar = post(cliente, "/admin/dificultades", {})
    assert deshabilitar.status_code == 302
    assert fila(
        db,
        "SELECT valor FROM configuracion "
        "WHERE clave = 'dificultad_intermedia_habilitada'",
    )["valor"] == "0"


def test_intentos_activos_muestra_el_equipo(
    cliente, db, credenciales_admin
):
    crear_equipo(db, "Equipo Visible")
    _con_sesion(cliente, credenciales_admin)

    html = cliente.get("/admin/intentos-activos").get_data(as_text=True)
    assert "Equipo Visible" in html
    assert "No se pueden deshabilitar dificultades" in html


def test_estadisticas_del_admin_filtran_y_no_usan_cdn(
    app, cliente, db, credenciales_admin
):
    from datetime import datetime

    _crear_intento(
        db,
        "Equipo Histórico",
        "inicial",
        datetime(2026, 1, 1, 10, 0, 0),
        datetime(2026, 1, 1, 10, 1, 40),
        "completo",
    )
    _crear_intento(
        db,
        "Equipo En Curso",
        "avanzado",
        datetime(2026, 1, 2, 10, 0, 0),
        None,
        None,
    )

    with app.app_context():
        todas = admin_estadisticas.obtener_estadisticas({})
        avanzado = admin_estadisticas.obtener_estadisticas(
            {"dificultad": "avanzado"}
        )
        invertido = admin_estadisticas.obtener_estadisticas(
            {"desde": "2026-01-02", "hasta": "2026-01-01"}
        )

    assert todas["resumen"]["equipos"] == 2
    assert todas["resumen"]["intentos_iniciados"] == 2
    assert todas["resumen"]["intentos_finalizados"] == 1
    assert todas["resumen"]["intentos_completados"] == 1
    assert todas["resumen"]["promedio_completados"] == 100
    assert avanzado["resumen"]["intentos_iniciados"] == 1
    assert avanzado["resumen"]["intentos_completados"] == 0
    assert invertido["rango_invalido"] is True
    assert invertido["resumen"]["intentos_iniciados"] == 0

    _con_sesion(cliente, credenciales_admin)
    html = cliente.get(
        "/admin/estadisticas?desde=2026-01-02&hasta=2026-01-01"
    ).get_data(as_text=True)
    assert "es posterior a la fecha" in html
    assert "chart.js" not in html.lower()
    assert "cdn." not in html.lower()


def test_filtros_y_orden_del_admin_no_rompen_el_sql(
    cliente, db, credenciales_admin
):
    _con_sesion(cliente, credenciales_admin)

    valido = cliente.get(
        "/admin/pregunta?dificultad=inicial&orden=titulo&dir=desc"
    )
    assert valido.status_code == 200

    invalido = cliente.get(
        "/admin/pregunta?orden=inventado&dir=otro&pagina=-5"
    )
    assert invalido.status_code == 200

    # El buscador escapa LIKE: un % literal no debe coincidir con todo.
    escapado = cliente.get("/admin/pregunta?q=%25").get_data(as_text=True)
    assert "¿Qué significa IP?" not in escapado
