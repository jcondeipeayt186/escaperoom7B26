"""Ranking público, pensado para la pantalla del televisor."""

from flask import Blueprint, jsonify, make_response, render_template

from ..servicios import ranking
from ..servicios.tiempos import ahora_texto

bp = Blueprint("ranking", __name__)

# El televisor consulta /ranking/datos dentro de este intervalo.
INTERVALO_POLLING_MS = 8000


@bp.get("/ranking")
def publico():
    """Vista de solo lectura con el ranking completo de intentos completados."""

    return render_template(
        "ranking.html",
        filas=ranking.obtener_ranking(),
        actualizado=ahora_texto(),
        intervalo_ms=INTERVALO_POLLING_MS,
    )


@bp.get("/ranking/datos")
def datos():
    """JSON para el polling de la vista pública."""

    filas = [
        {
            "posicion": fila["posicion"],
            "equipo": fila["equipo_nombre"],
            "numero_intento": fila["numero_intento"],
            "segundos": fila["segundos"],
            "incorrectas": fila["incorrectas"],
            "ayudas": fila["cantidad_ayudas"],
            "fecha_fin": fila["fecha_fin"].strftime("%d/%m/%Y %H:%M"),
        }
        for fila in ranking.obtener_ranking()
    ]

    respuesta = make_response(
        jsonify({"actualizado": ahora_texto(), "filas": filas})
    )
    respuesta.headers["Cache-Control"] = "no-store"
    return respuesta
