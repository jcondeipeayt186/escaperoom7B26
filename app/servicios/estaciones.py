"""Consultas de estaciones compartidas por las pantallas del juego."""

from ..db import get_db


class SinEstacionInicial(RuntimeError):
    """La base no tiene una estación activa con ``orden = 1``."""


def estacion_inicial(cursor):
    """Devuelve el id de la estación activa con ``orden = 1``.

    No se usa el ``id`` ni el ``DEFAULT 1`` del esquema: el orden es el que
    define el recorrido.
    """

    cursor.execute(
        "SELECT id FROM estacion WHERE activo = 1 AND orden = 1 LIMIT 1"
    )
    fila = cursor.fetchone()
    if fila is None:
        raise SinEstacionInicial(
            "No hay una estación activa con orden 1 en la base de datos."
        )
    return fila["id"]


def obtener_estacion(estacion_id):
    """Datos mínimos de una estación para mostrarla en el HUD."""

    with get_db().cursor() as cursor:
        cursor.execute(
            "SELECT id, nombre, descripcion, orden FROM estacion WHERE id = %s",
            (estacion_id,),
        )
        return cursor.fetchone()


def contar_estaciones_activas():
    """Cantidad de estaciones que forman el recorrido."""

    with get_db().cursor() as cursor:
        cursor.execute("SELECT COUNT(*) AS total FROM estacion WHERE activo = 1")
        return cursor.fetchone()["total"]
