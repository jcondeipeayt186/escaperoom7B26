"""Aplicación del Escape Room 7.º B 2026.

El servidor es la autoridad del juego: acá se validan respuestas, se calculan
tiempos y se persiste el estado. El navegador solo dibuja lo que el servidor
devuelve.
"""

import os

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template

from . import csrf
from . import db as db_module
from .routes import register_blueprints


def create_app(config_override=None):
    """Crea y configura la aplicación.

    ``config_override`` permite que los tests reemplacen la configuración
    leída de las variables de entorno.
    """

    load_dotenv()

    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("FLASK_SECRET_KEY"),
        MYSQL_HOST=os.environ.get("MYSQL_HOST"),
        MYSQL_PORT=os.environ.get("MYSQL_PORT"),
        MYSQL_USER=os.environ.get("MYSQL_USER"),
        MYSQL_PASSWORD=os.environ.get("MYSQL_PASSWORD", ""),
        MYSQL_DB=os.environ.get("MYSQL_DB"),
        ADMIN_USER=os.environ.get("ADMIN_USER"),
        ADMIN_PASSWORD_HASH=os.environ.get("ADMIN_PASSWORD_HASH"),
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
        SESSION_COOKIE_SECURE=False,
    )

    if config_override:
        app.config.update(config_override)

    _validar_configuracion(app)

    db_module.init_app(app)
    csrf.init_app(app)
    register_blueprints(app)

    @app.get("/salud")
    def salud():
        """Confirma que la app responde y que MySQL está accesible."""

        try:
            with db_module.get_db().cursor() as cursor:
                cursor.execute("SELECT 1")
                cursor.fetchone()
        except Exception:
            app.logger.exception("Fallo la verificación de la base de datos")
            return jsonify({"estado": "error", "base": "error"}), 503

        return jsonify({"estado": "ok", "base": "ok"})

    @app.errorhandler(400)
    def solicitud_invalida(error):
        return render_template("400.html"), 400

    @app.errorhandler(404)
    def no_encontrado(error):
        return render_template("404.html"), 404

    @app.errorhandler(500)
    def error_interno(error):
        return render_template("500.html"), 500

    @app.template_filter("hhmmss")
    def formato_hhmmss(segundos):
        """Formatea segundos como ``HH:MM:SS`` para resultados y ranking."""

        total = max(int(segundos or 0), 0)
        return (
            f"{total // 3600:02d}:"
            f"{(total % 3600) // 60:02d}:"
            f"{total % 60:02d}"
        )

    @app.template_filter("mmss")
    def formato_mmss(segundos):
        """Formatea segundos como ``MM:SS`` para los contadores del HUD."""

        total = max(int(segundos or 0), 0)
        return f"{total // 60:02d}:{total % 60:02d}"

    @app.template_filter("fecha_hora")
    def formato_fecha_hora(valor):
        """Formatea una fecha de MySQL como ``dd/mm/aaaa HH:MM``."""

        if valor is None:
            return "—"
        return valor.strftime("%d/%m/%Y %H:%M")

    return app


def _validar_configuracion(app):
    """Falla temprano si falta una variable obligatoria."""

    obligatorias = {
        "SECRET_KEY": "FLASK_SECRET_KEY",
        "MYSQL_HOST": "MYSQL_HOST",
        "MYSQL_PORT": "MYSQL_PORT",
        "MYSQL_USER": "MYSQL_USER",
        "MYSQL_DB": "MYSQL_DB",
    }

    for clave, variable in obligatorias.items():
        if not app.config.get(clave):
            raise RuntimeError(
                f"Falta la variable de entorno {variable}. "
                "Revisá el archivo .env (podés copiar .env.example)."
            )

    try:
        app.config["MYSQL_PORT"] = int(app.config["MYSQL_PORT"])
    except (TypeError, ValueError):
        raise RuntimeError(
            "MYSQL_PORT debe ser un número entero (por ejemplo, 3306)."
        )

    if app.config["SECRET_KEY"] == "cambiar-por-una-clave-larga-y-aleatoria":
        raise RuntimeError(
            "FLASK_SECRET_KEY tiene el valor de ejemplo. Generá una clave real "
            "con: python -c \"import secrets; print(secrets.token_hex(32))\""
        )
