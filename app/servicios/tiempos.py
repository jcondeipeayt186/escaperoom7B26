"""Cálculo de los contadores a partir de las fechas guardadas en MySQL."""

from ..db import get_db

AVISO_SEGUNDOS = 30


def ahora_texto():
    """Devuelve la fecha y hora del servidor MySQL para las vistas públicas."""

    with get_db().cursor() as cursor:
        cursor.execute(
            "SELECT DATE_FORMAT(NOW(), %s) AS ahora",
            ("%d/%m/%Y %H:%i:%s",),
        )
        return cursor.fetchone()["ahora"]


def calcular_tiempos(intento_id, estacion_id, duracion_segundos):
    """Devuelve el estado de los contadores del intento y la estación.

    La fuente de verdad son ``intento.fecha_inicio`` e
    ``intento_estacion.fecha_inicio``. Si la estación ya terminó, su contador
    queda congelado en la fecha de fin. La respuesta incluye la hora del
    servidor para que el navegador solo dibuje la cuenta entre
    sincronizaciones.
    """

    with get_db().cursor() as cursor:
        cursor.execute(
            "SELECT ROUND(UNIX_TIMESTAMP(NOW(3)) * 1000) AS servidor_ms, "
            "       ROUND(UNIX_TIMESTAMP(i.fecha_inicio) * 1000) "
            "         AS intento_inicio_ms, "
            "       ROUND(UNIX_TIMESTAMP("
            "         COALESCE("
            "           ie.fecha_fin,"
            "           DATE_ADD(ie.fecha_inicio, INTERVAL %s SECOND)"
            "         )"
            "       ) * 1000) AS estacion_fin_ms, "
            "       TIMESTAMPDIFF("
            "         SECOND, i.fecha_inicio, COALESCE(i.fecha_fin, NOW(3))"
            "       ) AS general_segundos, "
            "       i.fecha_fin IS NOT NULL AS intento_finalizado, "
            "       TIMESTAMPDIFF("
            "         SECOND, ie.fecha_inicio, COALESCE(ie.fecha_fin, NOW(3))"
            "       ) AS estacion_transcurridos, "
            "       ie.completada "
            "FROM intento i "
            "JOIN intento_estacion ie "
            "  ON ie.intento_id = i.id AND ie.estacion_id = %s "
            "WHERE i.id = %s",
            (duracion_segundos, estacion_id, intento_id),
        )
        fila = cursor.fetchone()

    if fila is None:
        return {
            "general_segundos": 0,
            "general_congelado": False,
            "estacion_segundos": max(duracion_segundos, 0),
            "duracion_estacion_segundos": duracion_segundos,
            "aviso_segundos": AVISO_SEGUNDOS,
            "aviso_activo": False,
            "completada": False,
            "servidor_ms": 0,
            "intento_inicio_ms": 0,
            "estacion_fin_ms": 0,
        }

    general = max(int(fila["general_segundos"]), 0)
    transcurridos = max(int(fila["estacion_transcurridos"]), 0)
    restantes = max(duracion_segundos - transcurridos, 0)
    completada = bool(fila["completada"])

    return {
        "general_segundos": general,
        "general_congelado": bool(fila["intento_finalizado"]),
        "estacion_segundos": restantes,
        "duracion_estacion_segundos": duracion_segundos,
        "aviso_segundos": AVISO_SEGUNDOS,
        "aviso_activo": (not completada) and 0 < restantes <= AVISO_SEGUNDOS,
        "completada": completada,
        "servidor_ms": int(fila["servidor_ms"] or 0),
        "intento_inicio_ms": int(fila["intento_inicio_ms"] or 0),
        "estacion_fin_ms": int(fila["estacion_fin_ms"] or 0),
    }
