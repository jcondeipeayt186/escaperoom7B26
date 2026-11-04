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

    maximo = entero_configuracion(configuracion, "max_integrantes_equipo", 4)
    return max(1, min(maximo, 4))


def duracion_estacion(configuracion):
    """Duración de cada estación en segundos, con respaldo seguro."""

    return max(
        1, entero_configuracion(configuracion, "duracion_estacion_segundos", 240)
    )


def maximos_estacion(configuracion):
    """Máximos visibles en el HUD de una estación."""

    return {
        "ayudas": max(
            1, entero_configuracion(configuracion, "max_ayudas_estacion", 2)
        ),
        "incorrectas": max(
            1, entero_configuracion(configuracion, "max_respuestas_incorrectas", 2)
        ),
        "envios": max(
            1, entero_configuracion(configuracion, "max_envios_estacion", 2)
        ),
    }


def entero_configuracion(configuracion, clave, predeterminado):
    """Lee una clave numérica de ``configuracion`` con respaldo seguro."""

    try:
        return int(configuracion.get(clave, predeterminado))
    except (TypeError, ValueError):
        return predeterminado


def es_dificultad_valida(dificultad, configuracion):
    """Indica si el valor existe y está habilitado."""

    return dificultad in DIFICULTADES and dificultad_habilitada(
        dificultad, configuracion
    )
