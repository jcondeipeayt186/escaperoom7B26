"""Conexión a MySQL y helpers de acceso a datos."""

from contextlib import contextmanager

import pymysql
from flask import current_app, g
from pymysql.cursors import DictCursor


def get_db():
    """Devuelve la conexión del request actual, creándola si hace falta."""

    if "db" not in g:
        g.db = pymysql.connect(
            host=current_app.config["MYSQL_HOST"],
            port=current_app.config["MYSQL_PORT"],
            user=current_app.config["MYSQL_USER"],
            password=current_app.config["MYSQL_PASSWORD"],
            database=current_app.config["MYSQL_DB"],
            charset="utf8mb4",
            cursorclass=DictCursor,
            autocommit=False,
        )
    return g.db


def close_db(exc=None):
    """Cierra la conexión al terminar el request."""

    conexion = g.pop("db", None)
    if conexion is not None:
        conexion.close()


@contextmanager
def transaction():
    """Agrupa varias consultas en una transacción.

    Uso::

        with transaction() as cursor:
            cursor.execute(...)
            cursor.execute(...)

    Si algo falla, hace rollback y vuelve a lanzar la excepción.
    """

    conexion = get_db()
    try:
        with conexion.cursor() as cursor:
            yield cursor
        conexion.commit()
    except Exception:
        conexion.rollback()
        raise


def init_app(app):
    """Registra el cierre de conexión en el ciclo de vida de la app."""

    app.teardown_appcontext(close_db)
