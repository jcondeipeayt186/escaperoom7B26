"""Estadísticas públicas, solo con datos agregados."""

from flask import Blueprint, render_template

from ..servicios import estadisticas
from ..servicios.tiempos import ahora_texto

bp = Blueprint("estadisticas", __name__)


@bp.get("/estadisticas")
def publico():
    """Muestra agregados de la feria sin nombres ni respuestas correctas."""

    return render_template(
        "estadisticas.html",
        resumen=estadisticas.obtener_resumen(),
        actualizado=ahora_texto(),
    )
