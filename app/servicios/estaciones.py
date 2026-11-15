"""Consultas de estaciones compartidas por las pantallas del juego."""

from ..db import get_db
from . import configuracion as config


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


def obtener_estacion_por_orden(orden):
    """Estación activa que ocupa un orden del recorrido."""

    with get_db().cursor() as cursor:
        cursor.execute(
            "SELECT id, nombre, descripcion, orden, activo "
            "FROM estacion WHERE activo = 1 AND orden = %s LIMIT 1",
            (orden,),
        )
        return cursor.fetchone()


def siguiente_estacion(orden):
    """Primera estación activa con un orden mayor, o ``None``."""

    with get_db().cursor() as cursor:
        cursor.execute(
            "SELECT id, nombre, descripcion, orden, activo "
            "FROM estacion WHERE activo = 1 AND orden > %s "
            "ORDER BY orden LIMIT 1",
            (orden,),
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
            "SELECT ie.ayudas, ie.completada, "
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
        return {
            "ayudas": 0,
            "incorrectas": 0,
            "envios": 0,
            "completada": False,
        }

    return {
        "ayudas": int(fila["ayudas"]),
        "incorrectas": int(fila["incorrectas"]),
        "envios": int(fila["envios"]),
        "completada": bool(fila["completada"]),
    }


def obtener_aprendizaje_estacion(intento_id, estacion_id):
    """Introducciones de los temas y explicación de cada pregunta respondida.

    Solo se llama desde la transición, cuando la estación ya está completada.
    Devuelve ``{"temas": [...], "preguntas": [...]}``. Las preguntas salen del
    envío que completó la estación (``respuestas_correctas`` completo), así la
    respuesta mostrada es la que el equipo eligió y no la que esté marcada como
    correcta después.
    """

    parametros = config.leer_configuracion()
    requeridas = max(
        1,
        config.entero_configuracion(
            parametros, "preguntas_por_estacion", 4
        ),
    )

    with get_db().cursor() as cursor:
        cursor.execute(
            "SELECT id FROM intento_envio "
            "WHERE intento_id = %s AND estacion_id = %s "
            "AND respuestas_correctas = %s "
            "ORDER BY fecha DESC, id DESC LIMIT 1",
            (intento_id, estacion_id, requeridas),
        )
        envio = cursor.fetchone()
        if envio is None:
            return {"temas": [], "preguntas": []}

        cursor.execute(
            "SELECT ip.orden, p.id AS pregunta_id, p.titulo, p.explicacion, "
            "       t.id AS tema_id, t.nombre AS tema, t.introduccion, "
            "       r.contenido AS respuesta_elegida "
            "FROM intento_pregunta ip "
            "JOIN pregunta p ON p.id = ip.pregunta_id "
            "JOIN tema t ON t.id = p.tema_id "
            "LEFT JOIN respuesta_elegida re "
            "       ON re.intento_id = ip.intento_id "
            "      AND re.intento_envio_id = %s "
            "      AND re.respuesta_id IN ("
            "            SELECT r2.id FROM respuesta r2 "
            "            WHERE r2.pregunta_id = p.id"
            "          ) "
            "LEFT JOIN respuesta r ON r.id = re.respuesta_id "
            "WHERE ip.intento_id = %s AND ip.estacion_id = %s "
            "ORDER BY ip.orden",
            (envio["id"], intento_id, estacion_id),
        )
        filas = cursor.fetchall()

    temas = []
    vistos = set()
    preguntas = []
    for fila in filas:
        if fila["tema_id"] not in vistos:
            vistos.add(fila["tema_id"])
            temas.append(
                {
                    "id": fila["tema_id"],
                    "nombre": fila["tema"],
                    "introduccion": fila["introduccion"],
                }
            )
        preguntas.append(
            {
                "orden": fila["orden"],
                "titulo": fila["titulo"],
                "explicacion": fila["explicacion"],
                "tema": fila["tema"],
                "respuesta_elegida": fila["respuesta_elegida"],
            }
        )

    return {"temas": temas, "preguntas": preguntas}

