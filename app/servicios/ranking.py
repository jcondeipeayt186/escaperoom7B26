"""Ranking competitivo de los intentos completados.

El orden es el definido en ``AGENTS.md``: menor tiempo total, luego menos
respuestas incorrectas, luego menos ayudas, después el intento que comenzó
antes y, por último, el ``id`` ascendente como desempate estable.

``posicion`` es la posición general entre todos los niveles y
``posicion_nivel`` la posición dentro del nivel del intento. La competencia
se resuelve por nivel: no se comparan tiempos de ``inicial`` con
``intermedio`` o ``avanzado``.
"""

from ..db import get_db
from .configuracion import (
    DIFICULTADES,
    ETIQUETAS_DIFICULTAD,
    dificultades_habilitadas,
    leer_configuracion,
)

_RANKING_BASE = """
WITH base AS (
    SELECT i.id AS intento_id,
           i.equipo_id,
           e.nombre AS equipo_nombre,
           i.dificultad,
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
           ) AS posicion,
           ROW_NUMBER() OVER (
               PARTITION BY dificultad
               ORDER BY segundos ASC, incorrectas ASC, cantidad_ayudas ASC,
                        fecha_inicio ASC, intento_id ASC
           ) AS posicion_nivel
    FROM base
    WHERE finalizado = 'completo'
)
"""


def obtener_ranking(
    limite=None, equipo=None, numero_intento=None, fecha=None, dificultad=None
):
    """Devuelve el ranking completo con filtros opcionales.

    Los filtros no cambian la posición: cada fila conserva el lugar que ocupa
    en el ranking general y en su nivel. ``fecha`` es un ``datetime.date`` y
    filtra por el día calendario de ``fecha_fin``. ``dificultad`` se ignora si
    no es un nivel válido.
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

    if dificultad in DIFICULTADES:
        condiciones.append("dificultad = %s")
        parametros.append(dificultad)

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


def obtener_ranking_por_nivel(configuracion=None, **filtros):
    """Agrupa el ranking en una tabla por nivel.

    Devuelve los niveles habilitados y también los que ya tienen intentos
    completados, para no ocultar historial si después se deshabilita un nivel.
    Dentro de cada nivel, las filas conservan el orden del ranking general.
    """

    if configuracion is None:
        configuracion = leer_configuracion()

    habilitadas = {
        nivel["valor"] for nivel in dificultades_habilitadas(configuracion)
    }

    por_nivel = {dificultad: [] for dificultad in DIFICULTADES}
    for fila in obtener_ranking(**filtros):
        por_nivel[fila["dificultad"]].append(fila)

    niveles = []
    for dificultad in DIFICULTADES:
        filas = por_nivel[dificultad]
        if dificultad not in habilitadas and not filas:
            continue
        niveles.append(
            {
                "valor": dificultad,
                "etiqueta": ETIQUETAS_DIFICULTAD[dificultad],
                "filas": filas,
            }
        )

    return niveles


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
        "posicion_nivel": int(fila["posicion_nivel"]),
        "intento_id": int(fila["intento_id"]),
        "equipo_id": int(fila["equipo_id"]),
        "equipo_nombre": fila["equipo_nombre"],
        "dificultad": fila["dificultad"],
        "numero_intento": int(fila["numero_intento"]),
        "fecha_inicio": fila["fecha_inicio"],
        "fecha_fin": fila["fecha_fin"],
        "segundos": int(fila["segundos"]),
        "incorrectas": int(fila["incorrectas"]),
        "cantidad_ayudas": int(fila["cantidad_ayudas"]),
    }
