"""Lectura y validación de los parámetros guardados en ``configuracion``."""

from ..db import get_db

DIFICULTADES = ("inicial", "intermedio", "avanzado")

ETIQUETAS_DIFICULTAD = {
    "inicial": "Inicial",
    "intermedio": "Intermedio",
    "avanzado": "Avanzado",
}

CLAVES_DIFICULTAD = {
    "intermedio": "dificultad_intermedia_habilitada",
    "avanzado": "dificultad_avanzada_habilitada",
}


def leer_configuracion():
    """Devuelve la tabla ``configuracion`` como un diccionario de textos."""

    with get_db().cursor() as cursor:
        cursor.execute("SELECT clave, valor FROM configuracion")
        return {fila["clave"]: fila["valor"] for fila in cursor.fetchall()}


def dificultad_habilitada(dificultad, configuracion):
    """``inicial`` siempre está habilitada; el resto depende de la base."""

    if dificultad == "inicial":
        return True

    clave = CLAVES_DIFICULTAD.get(dificultad)
    if clave is None:
        return False

    return str(configuracion.get(clave, "0")).strip() == "1"


def dificultades_habilitadas(configuracion):
    """Lista de dificultades que la bienvenida puede ofrecer."""

    return [
        {"valor": dificultad, "etiqueta": ETIQUETAS_DIFICULTAD[dificultad]}
        for dificultad in DIFICULTADES
        if dificultad_habilitada(dificultad, configuracion)
    ]


def maximo_integrantes(configuracion):
    """Máximo de integrantes configurado, acotado al rango real del juego."""

    try:
        maximo = int(configuracion.get("max_integrantes_equipo", "4"))
    except (TypeError, ValueError):
        maximo = 4

    return max(1, min(maximo, 4))


def es_dificultad_valida(dificultad, configuracion):
    """Indica si el valor existe y está habilitado."""

    return dificultad in DIFICULTADES and dificultad_habilitada(
        dificultad, configuracion
    )
