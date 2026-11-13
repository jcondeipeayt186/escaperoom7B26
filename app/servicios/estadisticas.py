"""Estadísticas públicas, solo con datos agregados.

Las respuestas y los aciertos salen de ``intento_envio``, que guarda el
resultado de cada envío en el momento en que se registró. Cambiar después la
respuesta correcta de una pregunta no altera las estadísticas históricas.
"""

from ..db import get_db
from .configuracion import (
    DIFICULTADES,
    ETIQUETAS_DIFICULTAD,
    duracion_estacion,
    leer_configuracion,
)

# Orden fijo de las barras. ``None`` representa los intentos en curso.
_ESTADOS = (
    (None, "en_curso", "En curso"),
    ("completo", "completo", "Completos"),
    ("abandono", "abandono", "Abandonos"),
    ("por_tiempo", "por_tiempo", "Por tiempo"),
    ("por_respuestas_incorrectas", "por_fallas", "Por respuestas fallidas"),
)


def _promedios_por_estacion(cursor, dificultad, duracion):
    """Promedio de segundos por estación, opcionalmente filtrado por nivel.

    Solo cuentan las estaciones completadas con fecha de fin. El filtro se
    aplica sobre el intento al que pertenece cada estación, no sobre el total
    de la página. El ancho de la barra se escala contra la duración máxima de
    una estación: el 100 % equivale a ``duracion`` segundos.
    """

    condicion = " AND i.dificultad = %s" if dificultad else ""
    parametros = (dificultad,) if dificultad else ()
    filtro_intento = "SELECT i.id FROM intento i WHERE 1 = 1" + condicion

    cursor.execute(
        "SELECT e.id, e.nombre, e.orden, COUNT(ie.id) AS muestras, "
        "       COALESCE(ROUND(AVG(TIMESTAMPDIFF("
        "         SECOND, ie.fecha_inicio, ie.fecha_fin"
        "       ))), 0) AS promedio "
        "FROM estacion e "
        "LEFT JOIN intento_estacion ie "
        "  ON ie.estacion_id = e.id "
        " AND ie.completada = 1 "
        " AND ie.fecha_fin IS NOT NULL "
        " AND ie.intento_id IN (" + filtro_intento + ") "
        "GROUP BY e.id, e.nombre, e.orden "
        "ORDER BY e.orden, e.id",
        parametros,
    )
    estaciones = [
        {
            "id": fila["id"],
            "nombre": fila["nombre"],
            "orden": fila["orden"],
            "muestras": int(fila["muestras"] or 0),
            "promedio": int(fila["promedio"] or 0),
        }
        for fila in cursor.fetchall()
    ]

    for estacion in estaciones:
        estacion["ancho"] = (
            min(100, round(estacion["promedio"] * 100 / duracion))
            if estacion["promedio"]
            else 0
        )

    return estaciones


def obtener_resumen(dificultad=""):
    """Devuelve los agregados de la feria listos para la plantilla.

    ``dificultad`` filtra únicamente el tiempo promedio por estación. Un valor
    fuera de ``DIFICULTADES`` se trata como "general".
    """

    dificultad = (dificultad or "").strip()
    if dificultad not in DIFICULTADES:
        dificultad = ""

    duracion = duracion_estacion(leer_configuracion())

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

        promedios_estacion = _promedios_por_estacion(
            cursor, dificultad, duracion
        )

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

    for estado in estados:
        estado["porcentaje_total"] = (
            round(estado["total"] * 100 / intentos_iniciados, 1)
            if intentos_iniciados
            else 0.0
        )
        # El ancho de la barra es el porcentaje real sobre el total, no una
        # escala relativa al estado más grande: así un 42,9 % no llena la barra.
        estado["ancho"] = min(100, estado["porcentaje_total"])

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
        "dificultad": dificultad,
        "opciones_dificultad": [
            {"valor": valor, "etiqueta": ETIQUETAS_DIFICULTAD[valor]}
            for valor in DIFICULTADES
        ],
        "promedios_estacion": promedios_estacion,
        "duracion_estacion": duracion,
    }
