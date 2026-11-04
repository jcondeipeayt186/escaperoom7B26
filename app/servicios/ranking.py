"""Ranking competitivo de los intentos completados.

El orden es el definido en ``AGENTS.md``: menor tiempo total, luego menos
respuestas incorrectas, luego menos ayudas, después el intento que comenzó
antes y, por último, el ``id`` ascendente como desempate estable.
"""

from ..db import get_db

_RANKING_BASE = """
WITH base AS (
    SELECT i.id AS intento_id,
           i.equipo_id,
           e.nombre AS equipo_nombre,
           i.fecha_inicio,
           i.fecha_fin,
           i.cantidad_ayudas,
           i.finalizado,
           TIMESTAMPDIFF(SECOND, i.fecha_inicio, i.fecha_fin) AS segundos,
           (SELECT COUNT(*) FROM incorrecta inc
            WHERE inc.intento_id = i.id) AS incorrectas,
           ROW_NUMBER() OVER (
               PARTITION BY i.equipo_id ORDER BY i.id ASC
           ) AS numero_intento
    FROM intento i
    JOIN equipo e ON e.id = i.equipo_id
), ranking AS (
    SELECT base.*,
           ROW_NUMBER() OVER (
               ORDER BY segundos ASC, incorrectas ASC, cantidad_ayudas ASC,
                        fecha_inicio ASC, intento_id ASC
           ) AS posicion
    FROM base
    WHERE finalizado = 'completo'
)
"""


def obtener_ranking(limite=None, equipo=None, numero_intento=None, fecha=None):
    """Devuelve el ranking completo con filtros opcionales.

    Los filtros no cambian la posición: cada fila conserva el lugar que ocupa
    en el ranking general. ``fecha`` es un ``datetime.date`` y filtra por el
    día calendario de ``fecha_fin``.
    """

    condiciones = []
    parametros = []

    if equipo:
        condiciones.append("equipo_nombre LIKE %s")
        parametros.append(f"%{equipo}%")

    if numero_intento is not None:
        condiciones.append("numero_intento = %s")
        parametros.append(numero_intento)

    if fecha is not None:
        condiciones.append("DATE(fecha_fin) = %s")
        parametros.append(fecha)

    consulta = _RANKING_BASE + " SELECT * FROM ranking"
    if condiciones:
        consulta += " WHERE " + " AND ".join(condiciones)
    consulta += " ORDER BY posicion ASC"

    if limite is not None:
        consulta += " LIMIT %s"
        parametros.append(limite)

    with get_db().cursor() as cursor:
        cursor.execute(consulta, tuple(parametros))
        return [_normalizar(fila) for fila in cursor.fetchall()]


def obtener_fila_ranking(intento_id):
    """Fila del ranking para un intento, o ``None`` si no está completo."""

    consulta = _RANKING_BASE + " SELECT * FROM ranking WHERE intento_id = %s"
    with get_db().cursor() as cursor:
        cursor.execute(consulta, (intento_id,))
        fila = cursor.fetchone()

    return _normalizar(fila) if fila is not None else None


def _normalizar(fila):
    return {
        "posicion": int(fila["posicion"]),
        "intento_id": int(fila["intento_id"]),
        "equipo_id": int(fila["equipo_id"]),
        "equipo_nombre": fila["equipo_nombre"],
        "numero_intento": int(fila["numero_intento"]),
        "fecha_inicio": fila["fecha_inicio"],
        "fecha_fin": fila["fecha_fin"],
        "segundos": int(fila["segundos"]),
        "incorrectas": int(fila["incorrectas"]),
        "cantidad_ayudas": int(fila["cantidad_ayudas"]),
    }
