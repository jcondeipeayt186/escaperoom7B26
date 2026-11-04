"""Identidad del equipo, alta y reanudación de intentos."""

import re
import unicodedata

from flask import session
from pymysql.err import IntegrityError

from ..db import get_db, transaction
from .estaciones import estacion_inicial

CLAVE_EQUIPO = "equipo_id"
CLAVE_INTENTO = "intento_id"
CLAVE_IDENTIFICACION = "identificacion"

LARGO_MAXIMO_NOMBRE = 120


class NombreDuplicado(Exception):
    """Otro request creó el mismo equipo mientras se intentaba el alta."""


def normalizar_nombre(nombre):
    """Recorta, colapsa espacios y unifica la forma Unicode del nombre."""

    if not isinstance(nombre, str):
        return ""

    texto = unicodedata.normalize("NFC", nombre)
    return re.sub(r"\s+", " ", texto).strip()


def buscar_equipo_por_nombre(nombre, cursor=None):
    """Busca un equipo por nombre usando la colación de MySQL.

    La comparación ignora mayúsculas y acentos; no se replica en Python.
    """

    if cursor is None:
        with get_db().cursor() as cursor_propio:
            return buscar_equipo_por_nombre(nombre, cursor_propio)

    cursor.execute(
        "SELECT id, nombre, cantidad_personas FROM equipo WHERE nombre = %s LIMIT 1",
        (nombre,),
    )
    return cursor.fetchone()


def equipo_por_id_y_nombre(equipo_id, nombre, cursor=None):
    """Confirma que el ID existe y pertenece al nombre ingresado."""

    if cursor is None:
        with get_db().cursor() as cursor_propio:
            return equipo_por_id_y_nombre(equipo_id, nombre, cursor_propio)

    cursor.execute(
        "SELECT id, nombre, cantidad_personas FROM equipo "
        "WHERE id = %s AND nombre = %s LIMIT 1",
        (equipo_id, nombre),
    )
    return cursor.fetchone()


def crear_equipo_y_intento(nombre, cantidad_personas, dificultad):
    """Crea equipo e intento en una sola transacción.

    Devuelve ``(equipo_id, intento_id)``. Si el nombre ya existe, lanza
    :class:`NombreDuplicado` para que la ruta derive a identificación.
    """

    try:
        with transaction() as cursor:
            estacion_id = estacion_inicial(cursor)
            cursor.execute(
                "INSERT INTO equipo (nombre, cantidad_personas) VALUES (%s, %s)",
                (nombre, cantidad_personas),
            )
            equipo_id = cursor.lastrowid
            intento_id = _insertar_intento(cursor, equipo_id, dificultad, estacion_id)
    except IntegrityError as error:
        if error.args and error.args[0] == 1062:
            raise NombreDuplicado from error
        raise

    return equipo_id, intento_id


def obtener_o_crear_intento(equipo_id, dificultad):
    """Reanuda el intento activo o crea uno nuevo.

    Bloquea la fila del equipo para que dos pestañas no abran dos intentos
    activos a la vez. Devuelve ``(intento_id, reanudado)`` o ``None`` si el
    equipo no existe.
    """

    with transaction() as cursor:
        cursor.execute("SELECT id FROM equipo WHERE id = %s FOR UPDATE", (equipo_id,))
        if cursor.fetchone() is None:
            return None

        cursor.execute(
            "SELECT id FROM intento "
            "WHERE equipo_id = %s AND fecha_fin IS NULL "
            "ORDER BY id DESC LIMIT 1 FOR UPDATE",
            (equipo_id,),
        )
        activo = cursor.fetchone()
        if activo is not None:
            return activo["id"], True

        estacion_id = estacion_inicial(cursor)
        intento_id = _insertar_intento(cursor, equipo_id, dificultad, estacion_id)
        return intento_id, False


def contexto_de_sesion():
    """Valida la sesión contra la base y devuelve equipo e intento.

    La sesión solo guarda IDs. En cada request se comprueba que el intento
    exista, pertenezca al equipo y siga activo.
    """

    equipo_id = session.get(CLAVE_EQUIPO)
    intento_id = session.get(CLAVE_INTENTO)
    if not isinstance(equipo_id, int) or not isinstance(intento_id, int):
        return None

    with get_db().cursor() as cursor:
        cursor.execute(
            "SELECT i.id AS intento_id, i.equipo_id, i.dificultad, i.fecha_inicio, "
            "       i.ultima_estacion_visitada, e.nombre AS equipo_nombre, "
            "       e.cantidad_personas "
            "FROM intento i "
            "JOIN equipo e ON e.id = i.equipo_id "
            "WHERE i.id = %s AND i.equipo_id = %s AND i.fecha_fin IS NULL "
            "LIMIT 1",
            (intento_id, equipo_id),
        )
        fila = cursor.fetchone()

    if fila is None:
        return None

    return {
        "equipo": {
            "id": fila["equipo_id"],
            "nombre": fila["equipo_nombre"],
            "cantidad_personas": fila["cantidad_personas"],
        },
        "intento": {
            "id": fila["intento_id"],
            "dificultad": fila["dificultad"],
            "fecha_inicio": fila["fecha_inicio"],
            "ultima_estacion_visitada": fila["ultima_estacion_visitada"],
        },
    }


def contexto_finalizado_de_sesion():
    """Devuelve el intento de la sesión si ya terminó, para eliminación."""

    equipo_id = session.get(CLAVE_EQUIPO)
    intento_id = session.get(CLAVE_INTENTO)
    if not isinstance(equipo_id, int) or not isinstance(intento_id, int):
        return None

    with get_db().cursor() as cursor:
        cursor.execute(
            "SELECT i.id AS intento_id, i.equipo_id, i.dificultad, i.fecha_inicio, "
            "       i.fecha_fin, i.finalizado, i.cantidad_ayudas, "
            "       i.puntaje_obtenido, i.ultima_estacion_visitada, "
            "       e.nombre AS equipo_nombre, e.cantidad_personas "
            "FROM intento i "
            "JOIN equipo e ON e.id = i.equipo_id "
            "WHERE i.id = %s AND i.equipo_id = %s AND i.fecha_fin IS NOT NULL "
            "LIMIT 1",
            (intento_id, equipo_id),
        )
        fila = cursor.fetchone()

    if fila is None:
        return None

    return {
        "equipo": {
            "id": fila["equipo_id"],
            "nombre": fila["equipo_nombre"],
            "cantidad_personas": fila["cantidad_personas"],
        },
        "intento": {
            "id": fila["intento_id"],
            "dificultad": fila["dificultad"],
            "fecha_inicio": fila["fecha_inicio"],
            "fecha_fin": fila["fecha_fin"],
            "finalizado": fila["finalizado"],
            "cantidad_ayudas": int(fila["cantidad_ayudas"]),
            "puntaje_obtenido": fila["puntaje_obtenido"],
            "ultima_estacion_visitada": fila["ultima_estacion_visitada"],
        },
    }


def guardar_sesion(equipo_id, intento_id):
    """Deja la sesión apuntando al equipo y su intento."""

    session[CLAVE_EQUIPO] = equipo_id
    session[CLAVE_INTENTO] = intento_id
    session.pop(CLAVE_IDENTIFICACION, None)


def guardar_identificacion(nombre, cantidad_personas, dificultad):
    """Guarda temporalmente los datos del formulario para el paso siguiente."""

    session[CLAVE_IDENTIFICACION] = {
        "nombre": nombre,
        "cantidad_personas": cantidad_personas,
        "dificultad": dificultad,
    }


def identificacion_pendiente():
    """Devuelve los datos pendientes de identificar, si siguen en sesión."""

    datos = session.get(CLAVE_IDENTIFICACION)
    if not isinstance(datos, dict):
        return None

    if not all(clave in datos for clave in ("nombre", "cantidad_personas", "dificultad")):
        return None

    return datos


def limpiar_identificacion():
    session.pop(CLAVE_IDENTIFICACION, None)


def limpiar_sesion_juego():
    session.pop(CLAVE_EQUIPO, None)
    session.pop(CLAVE_INTENTO, None)


def _insertar_intento(cursor, equipo_id, dificultad, estacion_id):
    cursor.execute(
        "INSERT INTO intento "
        "(equipo_id, dificultad, fecha_inicio, ultima_estacion_visitada) "
        "VALUES (%s, %s, NOW(3), %s)",
        (equipo_id, dificultad, estacion_id),
    )
    return cursor.lastrowid
