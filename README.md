# Escape Room 7.º B 2026

Aplicación web para la Feria de Producciones del IPEATyM 186 Castagnari (13/11/2026).

## Documentación

- `docs/proyectoEscapeRoom-7B.md` — título y reseña breve del proyecto.
- `docs/escape-room.md` — requisitos funcionales y contenido inicial.
- `docs/primeros-pasos.md` — hoja de ruta y guion de pedidos, paso a paso.
- `docs/argumentos-pasos/` — un archivo por paso (`paso00` a `paso12`), listo para usar con `/feature`. Incluye el índice y los criterios de aceptación.
- `docs/navegacion-por-app.md` — pantallas, rutas, elementos y objetivos.
- `docs/tecnologias.md` — stack explicado: frontend, backend, base de datos y herramientas.
- `docs/instalacion-y-puesta-en-funcionamiento.md` — instalación en Ubuntu y uso desde las notebooks.
- `sql/descripcion-de-la-base-de-datos.md` — modelo de datos, tablas y consultas.
- `AGENTS.md` — decisiones registradas, modelo de datos y convenciones.

## Base de datos

El esquema y el contenido inicial ya están disponibles:

```bash
mysql -u <usuario> -p < bd/schema.sql
mysql -u <usuario> -p < bd/seeds/001_contenido_inicial.sql
```

El seed es idempotente: se puede volver a ejecutar sin duplicar filas.

## Puesta en marcha (desarrollo)

Requiere Python 3 y MySQL 8.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
chmod 600 .env
```

Completar en `.env` las variables de MySQL (`MYSQL_USER` y `MYSQL_PASSWORD`)
y generar los valores reales de `FLASK_SECRET_KEY` y `ADMIN_PASSWORD_HASH`:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
python -c "from werkzeug.security import generate_password_hash; print(generate_password_hash('CAMBIA-ESTA-CLAVE'))"
```

El archivo `.env` no se versiona.

Levantar el servidor de desarrollo:

```bash
source .venv/bin/activate
flask --app app run --debug
```

La aplicación queda en <http://127.0.0.1:5000>. Para comprobar que responde
y que MySQL está accesible:

```bash
curl -i http://127.0.0.1:5000/salud
```

Respuesta esperada: `200` con `{"estado": "ok", "base": "ok"}`. Si la base no
responde, devuelve `503` sin exponer credenciales.

## Flujo implementado hasta el paso 02

- `GET /` muestra la bienvenida con nombre, cantidad de integrantes (1–4) y
  solo las dificultades habilitadas en `configuracion`.
- `POST /` valida el formulario, crea `equipo` e `intento` en una transacción
  o deriva a identificación si el nombre ya existe.
- `GET/POST /equipo/identificar` pide el ID del equipo y lo compara con el
  nombre. Si el equipo tiene un intento activo lo reanuda; si no, crea uno
  nuevo con la dificultad elegida.
- `GET /juego` es un tablero provisorio con el HUD mínimo
  (`Equipo N.º X · nombre`) y la estación que corresponde al intento. En el
  `paso03` pasa a mostrar las preguntas de la estación.

La lógica de identidad y configuración vive en `app/servicios/`. La sesión de
Flask guarda solo `equipo_id` e `intento_id`; el servidor vuelve a leer y
validar la base en cada request.

Pruebas automatizadas (todavía no hay tests; `pytest` termina con código 5):

```bash
pytest
```

> Para la feria se usa waitress, no el servidor de desarrollo. El
> procedimiento de producción está en
> `docs/instalacion-y-puesta-en-funcionamiento.md` y se cierra en el paso 12.
