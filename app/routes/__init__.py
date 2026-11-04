"""Registro de los blueprints de la aplicación."""

from .admin import bp as admin_bp
from .estadisticas import bp as estadisticas_bp
from .juego import bp as juego_bp
from .ranking import bp as ranking_bp


def register_blueprints(app):
    app.register_blueprint(juego_bp)
    app.register_blueprint(ranking_bp)
    app.register_blueprint(estadisticas_bp)
    app.register_blueprint(admin_bp, url_prefix="/admin")
