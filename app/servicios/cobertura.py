"""Cobertura de preguntas por estación y nivel.

Una estación está cubierta para un nivel cuando cada tema activo tiene al
menos una pregunta activa de ese nivel y la estación suma al menos
``preguntas_por_estacion`` preguntas activas del nivel. Sin estaciones
activas no hay cobertura completa.
"""

from ..db import get_db
from .configuracion import DIFICULTADES, ETIQUETAS_DIFICULTAD

PREGUNTAS_POR_ESTACION_PREDETERMINADAS = 4


def _entero(valor, predeterminado):
    try:
        return int(valor)
    except (TypeError, ValueError):
        return predeterminado


def calcular_cobertura(cursor):
    """Calcula la cobertura con el cursor indicado.

    El cursor permite reutilizar la misma transacción y los mismos bloqueos
    desde el reporte y desde los toggles de dificultad.
    """

    cursor.execute(
        "SELECT valor FROM configuracion WHERE clave = 'preguntas_por_estacion'"
    )
    fila = cursor.fetchone()
    requeridas = max(
        1,
        _entero(
            fila["valor"] if fila is not None else None,
            PREGUNTAS_POR_ESTACION_PREDETERMINADAS,
        ),
    )

    cursor.execute(
        "SELECT id, nombre, orden FROM estacion WHERE activo = 1 "
        "ORDER BY orden, id"
    )
    estaciones = []
    for fila in cursor.fetchall():
        estaciones.append(
            {
                "id": fila["id"],
                "nombre": fila["nombre"],
                "orden": fila["orden"],
                "temas": {},
            }
        )

    if estaciones:
        cursor.execute(
            "SELECT e.id AS estacion_id, t.id AS tema_id, "
            "       t.nombre AS tema_nombre, p.dificultad, "
            "       COUNT(p.id) AS preguntas "
            "FROM estacion e "
            "JOIN tema t ON t.estacion_id = e.id AND t.activo = 1 "
            "LEFT JOIN pregunta p ON p.tema_id = t.id AND p.activo = 1 "
            "WHERE e.activo = 1 "
            "GROUP BY e.id, t.id, t.nombre, p.dificultad "
            "ORDER BY e.id, t.nombre, t.id"
        )
        por_estacion = {estacion["id"]: estacion for estacion in estaciones}
        for fila in cursor.fetchall():
            estacion = por_estacion[fila["estacion_id"]]
            tema = estacion["temas"].setdefault(
                fila["tema_id"],
                {
                    "id": fila["tema_id"],
                    "nombre": fila["tema_nombre"],
                    "conteos": {dificultad: 0 for dificultad in DIFICULTADES},
                },
            )
            if fila["dificultad"] in tema["conteos"]:
                tema["conteos"][fila["dificultad"]] = int(fila["preguntas"])

    niveles = []
    for dificultad in DIFICULTADES:
        estaciones_nivel = []
        temas_sin_preguntas = 0
        for estacion in estaciones:
            temas = []
            total = 0
            sin_preguntas = 0
            for tema in sorted(
                estacion["temas"].values(),
                key=lambda item: (item["nombre"], item["id"]),
            ):
                preguntas = tema["conteos"][dificultad]
                suficiente = preguntas >= 1
                if not suficiente:
                    sin_preguntas += 1
                total += preguntas
                temas.append(
                    {
                        "id": tema["id"],
                        "nombre": tema["nombre"],
                        "preguntas": preguntas,
                        "suficiente": suficiente,
                    }
                )

            completa = bool(temas) and sin_preguntas == 0 and total >= requeridas
            temas_sin_preguntas += sin_preguntas
            estaciones_nivel.append(
                {
                    "id": estacion["id"],
                    "nombre": estacion["nombre"],
                    "orden": estacion["orden"],
                    "temas": temas,
                    "temas_activos": len(temas),
                    "temas_sin_preguntas": sin_preguntas,
                    "total": total,
                    "requeridas": requeridas,
                    "faltantes": max(requeridas - total, 0),
                    "completa": completa,
                }
            )

        niveles.append(
            {
                "valor": dificultad,
                "etiqueta": ETIQUETAS_DIFICULTAD[dificultad],
                "completa": bool(estaciones_nivel)
                and all(estacion["completa"] for estacion in estaciones_nivel),
                "estaciones": estaciones_nivel,
                "total_estaciones": len(estaciones_nivel),
                "estaciones_completas": sum(
                    1 for estacion in estaciones_nivel if estacion["completa"]
                ),
                "temas_sin_preguntas": temas_sin_preguntas,
            }
        )

    return {
        "preguntas_por_estacion": requeridas,
        "estaciones_activas": len(estaciones),
        "niveles": niveles,
    }


def obtener_cobertura():
    """Devuelve la cobertura actual de todas las estaciones activas."""

    with get_db().cursor() as cursor:
        return calcular_cobertura(cursor)


def obtener_nivel(cobertura, dificultad):
    """Devuelve el resumen de un nivel o ``None``."""

    for nivel in cobertura["niveles"]:
        if nivel["valor"] == dificultad:
            return nivel
    return None


def nivel_completo(cobertura, dificultad):
    """Indica si el nivel tiene cobertura completa en todas las estaciones."""

    nivel = obtener_nivel(cobertura, dificultad)
    return bool(nivel and nivel["completa"])
