"""Configuración de pytest con una base MySQL independiente.

La base de prueba se crea al inicio de la sesión, se carga con el esquema y el
seed, y se limpia antes y después de cada test. Nunca se apunta a la base real
de la feria: el nombre debe terminar en ``_test`` y ser distinto de ``MYSQL_DB``.
"""

import secrets
from pathlib import Path

import pymysql
import pytest
from dotenv import dotenv_values
from pymysql.cursors import DictCursor
from werkzeug.security import generate_password_hash

from app import create_app

RAIZ = Path(__file__).resolve().parents[1]
ESQUEMA = RAIZ / "bd" / "schema.sql"
SEEDS = (
    RAIZ / "bd" / "seeds" / "001_contenido_inicial.sql",
    RAIZ / "bd" / "seeds" / "002_contenido_intermedio.sql",
    RAIZ / "bd" / "seeds" / "003_contenido_avanzado.sql",
)

TABLAS_LIMPIABLES = (
    "incorrecta",
    "respuesta_elegida",
    "intento_pregunta",
    "intento_envio",
    "intento_estacion",
    "intento",
    "respuesta",
    "pregunta",
    "tema",
    "estacion",
    "equipo",
    "configuracion",
)


def _leer_entorno():
    return dotenv_values(RAIZ / ".env")


def _conectar(entorno, base=None):
    return pymysql.connect(
        host=entorno["MYSQL_HOST"],
        port=int(entorno["MYSQL_PORT"]),
        user=entorno["MYSQL_USER"],
        password=entorno.get("MYSQL_PASSWORD", ""),
        database=base,
        charset="utf8mb4",
        cursorclass=DictCursor,
        autocommit=True,
    )


def _sentencias(texto):
    """Separa un script SQL simple por punto y coma, sin ejecutar comentarios."""

    for fragmento in texto.split(";"):
        if not fragmento.strip():
            continue
        sin_comentarios = "\n".join(
            linea
            for linea in fragmento.splitlines()
            if not linea.strip().startswith("--")
        )
        if not sin_comentarios.strip():
            continue
        yield fragmento


def _ejecutar_script(conexion, ruta, base):
    texto = ruta.read_text(encoding="utf-8").replace(
        "escape_room_7b2026", base
    )
    with conexion.cursor() as cursor:
        for sentencia in _sentencias(texto):
            cursor.execute(sentencia)


def _limpiar_y_sembrar(conexion, base):
    with conexion.cursor() as cursor:
        for tabla in TABLAS_LIMPIABLES:
            cursor.execute(f"DELETE FROM {tabla}")
    for seed in SEEDS:
        _ejecutar_script(conexion, seed, base)


@pytest.fixture(scope="session")
def credenciales_admin():
    """Credenciales de administración generadas en runtime, nunca fijas."""

    return {
        "usuario": f"admin_{secrets.token_hex(4)}",
        "clave": secrets.token_urlsafe(24),
    }


@pytest.fixture(scope="session")
def base_de_datos():
    """Crea la base de test, carga esquema y seed y devuelve la configuración."""

    entorno = _leer_entorno()
    base = (
        entorno.get("TEST_MYSQL_DB")
        or "escape_room_7b2026_test"
    )
    if not base.endswith("_test"):
        raise RuntimeError(
            "TEST_MYSQL_DB debe terminar en _test para no tocar datos reales."
        )
    if base == entorno.get("MYSQL_DB"):
        raise RuntimeError("TEST_MYSQL_DB no puede ser la base de desarrollo.")

    servidor = _conectar(entorno)
    with servidor.cursor() as cursor:
        cursor.execute(f"DROP DATABASE IF EXISTS {base}")
        cursor.execute(
            f"CREATE DATABASE {base} CHARACTER SET utf8mb4 "
            "COLLATE utf8mb4_unicode_ci"
        )
    servidor.close()

    conexion = _conectar(entorno, base)
    _ejecutar_script(conexion, ESQUEMA, base)
    for seed in SEEDS:
        _ejecutar_script(conexion, seed, base)
    conexion.close()

    configuracion = dict(entorno)
    configuracion["MYSQL_PORT"] = int(entorno["MYSQL_PORT"])
    configuracion["MYSQL_DB"] = base
    return configuracion


@pytest.fixture(scope="session")
def app(base_de_datos, credenciales_admin):
    """Aplicación apuntada exclusivamente a la base de test."""

    return create_app(
        config_override={
            **base_de_datos,
            "SECRET_KEY": secrets.token_hex(32),
            "ADMIN_USER": credenciales_admin["usuario"],
            "ADMIN_PASSWORD_HASH": generate_password_hash(
                credenciales_admin["clave"]
            ),
        }
    )


@pytest.fixture(autouse=True)
def base_limpia(base_de_datos):
    """Deja el contenido del seed antes y después de cada test."""

    conexion = _conectar(base_de_datos, base_de_datos["MYSQL_DB"])
    _limpiar_y_sembrar(conexion, base_de_datos["MYSQL_DB"])
    yield
    _limpiar_y_sembrar(conexion, base_de_datos["MYSQL_DB"])
    conexion.close()


@pytest.fixture
def db(base_de_datos):
    """Conexión de apoyo con autocommit para preparar y verificar datos."""

    conexion = _conectar(base_de_datos, base_de_datos["MYSQL_DB"])
    yield conexion
    conexion.close()


@pytest.fixture
def cliente(app):
    return app.test_client()
