"""Ranking público, pensado para la pantalla del televisor."""

from flask import Blueprint, jsonify, make_response, render_template

from ..servicios import ranking
from ..servicios.tiempos import ahora_texto

bp = Blueprint("ranking", __name__)

# El televisor consulta /ranking/datos dentro de este intervalo.
INTERVALO_POLLING_MS = 8000


@bp.get("/ranking")
def publico():
    """Vista de solo lectura con una tabla por nivel."""

    niveles = ranking.obtener_ranking_por_nivel()

    return render_template(
        "ranking.html",
        niveles=niveles,
        hay_filas=any(nivel["filas"] for nivel in niveles),
        actualizado=ahora_texto(),
        intervalo_ms=INTERVALO_POLLING_MS,
    )


@bp.get("/ranking/datos")
def datos():
    """JSON para el polling de la vista pública, agrupado por nivel."""

    niveles = [
        {
            "valor": nivel["valor"],
            "etiqueta": nivel["etiqueta"],
            "filas": [
                {
                    "posicion": fila["posicion_nivel"],
                    "equipo": fila["equipo_nombre"],
                    "numero_intento": fila["numero_intento"],
                    "segundos": fila["segundos"],
                    "incorrectas": fila["incorrectas"],
                    "ayudas": fila["cantidad_ayudas"],
                    "fecha_fin": fila["fecha_fin"].strftime("%d/%m/%Y %H:%M"),
                }
                for fila in nivel["filas"]
            ],
        }
        for nivel in ranking.obtener_ranking_por_nivel()
    ]

    respuesta = make_response(
        jsonify({"actualizado": ahora_texto(), "niveles": niveles})
    )
    respuesta.headers["Cache-Control"] = "no-store"
    return respuesta
