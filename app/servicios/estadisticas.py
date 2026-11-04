"""Estadísticas públicas, solo con datos agregados.

Las respuestas y los aciertos salen de ``intento_envio``, que guarda el
resultado de cada envío en el momento en que se registró. Cambiar después la
respuesta correcta de una pregunta no altera las estadísticas históricas.
"""

from ..db import get_db

# Orden fijo de las barras. ``None`` representa los intentos en curso.
_ESTADOS = (
    (None, "en_curso", "En curso"),
    ("completo", "completo", "Completos"),
    ("abandono", "abandono", "Abandonos"),
    ("por_tiempo", "por_tiempo", "Por tiempo"),
    ("por_respuestas_incorrectas", "por_fallas", "Por respuestas fallidas"),
)


def obtener_resumen():
    """Devuelve los agregados de la feria listos para la plantilla."""

    with get_db().cursor() as cursor:
        cursor.execute(
            "SELECT "
            "  (SELECT COUNT(*) FROM equipo) AS equipos, "
            "  (SELECT COALESCE(SUM(cantidad_personas), 0) FROM equipo) "
            "    AS integrantes, "
            "  (SELECT COUNT(*) FROM intento) AS intentos_iniciados, "
            "  (SELECT COUNT(*) FROM intento "
            "   WHERE finalizado = 'completo') AS intentos_completados, "
            "  (SELECT COALESCE(ROUND(AVG("
            "     TIMESTAMPDIFF(SECOND, fecha_inicio, fecha_fin)"
            "   )), 0) FROM intento "
            "   WHERE finalizado = 'completo') AS promedio_segundos, "
            "  (SELECT COUNT(*) FROM respuesta_elegida) "
            "    AS respuestas_realizadas, "
            "  (SELECT COALESCE(SUM(respuestas_correctas), 0) FROM intento_envio) "
            "    AS aciertos"
        )
        fila = cursor.fetchone()

        cursor.execute(
            "SELECT finalizado, COUNT(*) AS total "
            "FROM intento GROUP BY finalizado"
        )
        por_estado = {
            fila_estado["finalizado"]: int(fila_estado["total"])
            for fila_estado in cursor.fetchall()
        }

    intentos_iniciados = int(fila["intentos_iniciados"])
    respuestas_realizadas = int(fila["respuestas_realizadas"])
    aciertos = int(fila["aciertos"])
    porcentaje_aciertos = (
        round(aciertos * 100 / respuestas_realizadas, 1)
        if respuestas_realizadas
        else 0.0
    )

    estados = [
        {
            "clave": clave,
            "etiqueta": etiqueta,
            "total": por_estado.get(finalizado, 0),
        }
        for finalizado, clave, etiqueta in _ESTADOS
    ]

    maximo = max((estado["total"] for estado in estados), default=0)
    for estado in estados:
        estado["porcentaje_total"] = (
            round(estado["total"] * 100 / intentos_iniciados, 1)
            if intentos_iniciados
            else 0.0
        )
        estado["ancho"] = (
            round(estado["total"] * 100 / maximo) if maximo else 0
        )

    return {
        "equipos": int(fila["equipos"]),
        "integrantes": int(fila["integrantes"]),
        "intentos_iniciados": intentos_iniciados,
        "intentos_completados": int(fila["intentos_completados"]),
        "promedio_segundos": int(fila["promedio_segundos"]),
        "respuestas_realizadas": respuestas_realizadas,
        "aciertos": aciertos,
        "porcentaje_aciertos": porcentaje_aciertos,
        "estados": estados,
    }
