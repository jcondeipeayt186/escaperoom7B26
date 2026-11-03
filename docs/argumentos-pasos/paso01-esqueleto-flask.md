# Paso 01 — Esqueleto Flask y conexión a MySQL

> **Origen:** Pedido 1 de `docs/primeros-pasos.md` (Pasos 0 y 2).
> **Tipo:** código.
> **Requiere:** `paso00` verificado.
> **Commit:** `feat: esqueleto flask y configuración`.
>
> **Antes de empezar:** leé `AGENTS.md`, `docs/escape-room.md`,
> `docs/navegacion-por-app.md`, `sql/descripcion-de-la-base-de-datos.md` y
> `MEMORY.md`. No copies esas reglas acá: este archivo solo agrega las del
> paso.

## Contexto

La base `escape_room_7b2026` existe, con el esquema y el contenido inicial
cargados. No hay aplicación Flask, ni `requirements.txt`, ni `.env`.

## Objetivo

Dejar la app levantando con la estructura base, la conexión a MySQL y una
ruta `/salud` que confirme que la base responde.

## Alcance

- `requirements.txt` con Flask, PyMySQL, python-dotenv, pytest y waitress,
  con versiones fijas.
- `.env.example` con `FLASK_SECRET_KEY`, `MYSQL_HOST`, `MYSQL_PORT`,
  `MYSQL_USER`, `MYSQL_PASSWORD`, `MYSQL_DB`, `ADMIN_USER` y
  `ADMIN_PASSWORD_HASH`.
- `.gitignore` para `.venv/`, `.env`, `__pycache__/`, `*.pyc` y volcados de
  base.
- `app/__init__.py` con `create_app()`, carga de `.env`, `SECRET_KEY`,
  registro de blueprints y manejadores de error 404 y 500.
- `app/db.py` con conexión por request, cursor de diccionarios, cierre en
  `teardown` y un helper de transacción.
- Blueprints vacíos: `juego`, `ranking`, `estadisticas`, `admin`.
- `templates/base.html`, `templates/404.html`, `templates/500.html`.
- Bootstrap local en `static/vendor/bootstrap/`.
- Ruta `GET /salud`.
- Comandos reales en `README.md`.

No crear todavía pantallas de juego, modelos ni migraciones.

## Reglas

- Configuración solo por variables de entorno. Nada de credenciales en el
  código ni en archivos versionados.
- Sin CDN: Bootstrap se guarda en `static/vendor/`.
- La app no crea la base ni ejecuta el esquema; eso lo hace `mysql`.
- La app debe poder arrancar con `flask --app app run --debug`.
- `/salud` no expone credenciales ni detalles internos: solo confirma app y
  base.
- Los errores 404 y 500 muestran páginas amigables con enlace a `/`.
- En producción no se usa `debug=True`.

## Criterio de aceptación

- [ ] `python3 -m venv .venv && pip install -r requirements.txt` funciona.
- [ ] `flask --app app run --debug` levanta sin errores.
- [ ] `GET /salud` responde 200 y confirma la conexión a MySQL.
- [ ] Una URL inexistente muestra la página 404, no la traza de Flask.
- [ ] Un error forzado muestra la página 500.
- [ ] `.env` no aparece en `git status` (está ignorado).
- [ ] Los conteos del seed siguen siendo 5/14/20/60.

## Verificación

```bash
curl -i http://127.0.0.1:5000/salud
curl -i http://127.0.0.1:5000/no-existe
git status --short
```

Para el 500, agregar una ruta temporal que haga `1/0`, comprobarla y
quitarla antes del commit.

Para el 404 y el 500, verificar que las plantillas extienden `base.html` y
que no muestran variables de entorno.

## Trampas conocidas

- Si MySQL usa `caching_sha2_password` y PyMySQL falla al conectar, puede
  hacer falta el paquete `cryptography`. Agregarlo a `requirements.txt` es
  una dependencia nueva: consultar antes.
- `dotenv` tiene que cargarse antes de leer las variables, también cuando se
  ejecutan los tests.
- El cursor de diccionarios simplifica las plantillas, pero no cambia el
  hecho de que todo SQL debe ir parametrizado.
- No usar `sqlite3` ni un ORM para "simplificar": el stack es Flask +
  PyMySQL.

## No hagas todavía

Bienvenida, estaciones, temporizadores, ranking y admin. En este paso solo
se levanta el esqueleto.

## Al terminar

- Resumir archivos creados, comandos para probar y resultado de `/salud`.
- Actualizar `MEMORY.md` con el estado del scaffold.
- Commit: `feat: esqueleto flask y configuración`.
