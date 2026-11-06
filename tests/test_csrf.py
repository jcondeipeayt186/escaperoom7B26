"""Protección CSRF: campo oculto, rechazo y rotación del token."""

import re
from pathlib import Path

from helpers import conteo, post

RAIZ = Path(__file__).resolve().parents[1]


def _token_de_sesion(cliente):
    with cliente.session_transaction() as sesion:
        return sesion.get("csrf_token")


def test_formularios_post_incluyen_el_campo_oculto():
    plantillas = RAIZ / "app" / "templates"
    for ruta in plantillas.rglob("*.html"):
        texto = ruta.read_text(encoding="utf-8")
        formularios = re.findall(
            r"<form\b[^>]*>", texto, re.IGNORECASE | re.DOTALL
        )
        posteos = [
            etiqueta
            for etiqueta in formularios
            if re.search(r"method\s*=\s*['\"]post['\"]", etiqueta, re.I)
        ]
        if not posteos:
            continue
        incluidos = texto.count('include "_csrf_campo.html"')
        assert incluidos >= len(posteos), ruta


def test_bienvenida_renderiza_el_token_de_la_sesion(cliente):
    html = cliente.get("/").get_data(as_text=True)

    assert re.search(
        r'<input type="hidden" name="csrf_token" value="[^"]+">', html
    )
    token = _token_de_sesion(cliente)
    assert token
    assert token in html


def test_post_sin_token_devuelve_400_y_no_crea_equipo(cliente, db):
    respuesta = cliente.post(
        "/",
        data={
            "nombre": "Equipo Sin Token",
            "cantidad_personas": "2",
            "dificultad": "inicial",
        },
    )

    assert respuesta.status_code == 400
    html = respuesta.get_data(as_text=True)
    assert "Solicitud no válida" in html
    assert conteo(db, "equipo", "WHERE nombre = %s", ("Equipo Sin Token",)) == 0


def test_post_con_token_invalido_devuelve_400(cliente):
    cliente.get("/")

    respuesta = cliente.post(
        "/",
        data={
            "nombre": "Equipo Token Falso",
            "cantidad_personas": "2",
            "dificultad": "inicial",
            "csrf_token": "token-que-no-corresponde",
        },
    )

    assert respuesta.status_code == 400


def test_post_con_token_valido_continua(cliente):
    respuesta = post(
        cliente,
        "/",
        {
            "nombre": "Equipo Con Token",
            "cantidad_personas": "2",
            "dificultad": "inicial",
        },
    )

    assert respuesta.status_code == 302


def test_csrf_se_valida_antes_del_login_del_admin(
    cliente, credenciales_admin
):
    respuesta = cliente.post(
        "/admin/login",
        data={
            "usuario": credenciales_admin["usuario"],
            "clave": credenciales_admin["clave"],
        },
    )

    assert respuesta.status_code == 400
    assert _token_de_sesion(cliente) is None


def test_login_y_logout_rotan_el_token(cliente, credenciales_admin):
    cliente.get("/admin")
    antes = _token_de_sesion(cliente)
    assert antes

    ingreso = post(
        cliente,
        "/admin/login",
        {
            "usuario": credenciales_admin["usuario"],
            "clave": credenciales_admin["clave"],
        },
    )
    assert ingreso.status_code == 302
    despues = _token_de_sesion(cliente)
    assert despues
    assert despues != antes

    salida = post(cliente, "/admin/logout")
    assert salida.status_code == 302
    final = _token_de_sesion(cliente)
    assert final
    assert final != despues


def test_get_estado_no_exige_token(cliente):
    respuesta = cliente.get("/juego/estado")

    assert respuesta.status_code == 200
    assert "redirigir" in respuesta.get_json()
