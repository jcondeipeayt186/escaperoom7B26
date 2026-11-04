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
            "SELECT id, nombre, descripcion, orden, activo "
            "FROM estacion WHERE id = %s",
            (estacion_id,),
        )
        return cursor.fetchone()


def contar_estaciones_activas():
    """Cantidad de estaciones que forman el recorrido."""

    with get_db().cursor() as cursor:
        cursor.execute("SELECT COUNT(*) AS total FROM estacion WHERE activo = 1")
        return cursor.fetchone()["total"]


def obtener_preguntas_seleccionadas(intento_id, estacion_id):
    """Preguntas congeladas y sus opciones, sin la marca de correcta.

    No se filtra por ``activo``: si el contenido se desactiva después de
    congelar la selección, el intento sigue mostrando lo que se guardó.
    """

    with get_db().cursor() as cursor:
        cursor.execute(
            "SELECT ip.orden, p.id AS pregunta_id, p.titulo, p.descripcion, "
            "       r.id AS respuesta_id, r.contenido "
            "FROM intento_pregunta ip "
            "JOIN pregunta p ON p.id = ip.pregunta_id "
            "LEFT JOIN respuesta r ON r.pregunta_id = p.id "
            "WHERE ip.intento_id = %s AND ip.estacion_id = %s "
            "ORDER BY ip.orden, r.id",
            (intento_id, estacion_id),
        )
        filas = cursor.fetchall()

    preguntas = []
    indices = {}
    for fila in filas:
        pregunta_id = fila["pregunta_id"]
        if pregunta_id not in indices:
            indices[pregunta_id] = len(preguntas)
            preguntas.append(
                {
                    "id": pregunta_id,
                    "orden": fila["orden"],
                    "titulo": fila["titulo"],
                    "descripcion": fila["descripcion"],
                    "opciones": [],
                }
            )

        if fila["respuesta_id"] is not None:
            preguntas[indices[pregunta_id]]["opciones"].append(
                {"id": fila["respuesta_id"], "contenido": fila["contenido"]}
            )

    return preguntas


def obtener_resumen_estacion(intento_id, estacion_id):
    """Ayudas, incorrectas y envíos acumulados en la estación."""

    with get_db().cursor() as cursor:
        cursor.execute(
            "SELECT ie.ayudas, "
            "  (SELECT COUNT(*) FROM intento_envio e "
            "   WHERE e.intento_id = %s AND e.estacion_id = %s) AS envios, "
            "  (SELECT COUNT(*) FROM incorrecta i "
            "   JOIN intento_envio e2 ON e2.id = i.intento_envio_id "
            "   WHERE i.intento_id = %s AND e2.estacion_id = %s) AS incorrectas "
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
        fila = cursor.fetchone()

    if fila is None:
        return {"ayudas": 0, "incorrectas": 0, "envios": 0}

    return {
        "ayudas": int(fila["ayudas"]),
        "incorrectas": int(fila["incorrectas"]),
        "envios": int(fila["envios"]),
    }
