"""Protección CSRF propia, sin dependencias externas.

El token vive en la sesión de Flask. Se genera en el primer formulario que lo
necesita, se incluye en un campo oculto y se compara con ``hmac.compare_digest``
en cada request que modifica datos. Login y logout también lo exigen.
"""

import hmac
import secrets

from flask import abort, request, session

CLAVE_SESION = "csrf_token"
NOMBRE_CAMPO = "csrf_token"
METODOS_PROTEGIDOS = {"POST", "PUT", "PATCH", "DELETE"}


def obtener_token():
    """Devuelve el token de la sesión, generándolo si todavía no existe."""

    token = session.get(CLAVE_SESION)
    if not isinstance(token, str) or not token:
        token = secrets.token_urlsafe(32)
        session[CLAVE_SESION] = token
    return token


def rotar_token():
    """Genera un token nuevo para la sesión actual."""

    token = secrets.token_urlsafe(32)
    session[CLAVE_SESION] = token
    return token


def token_valido(token):
    """Compara el token recibido con el guardado, sin filtrar tiempos."""

    esperado = session.get(CLAVE_SESION)
    if not isinstance(esperado, str) or not esperado:
        return False
    if not isinstance(token, str) or not token:
        return False
    return hmac.compare_digest(esperado, token)


def init_app(app):
    """Registra la validación previa a las vistas y el helper de plantillas."""

    @app.before_request
    def proteger_csrf():
        if request.method not in METODOS_PROTEGIDOS:
            return None
        if not token_valido(request.form.get(NOMBRE_CAMPO, "")):
            abort(400)
        return None

    app.jinja_env.globals["csrf_token"] = obtener_token
