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

## Flujo implementado hasta el paso 06

- `GET /` muestra la bienvenida con nombre, cantidad de integrantes (1–4) y
  solo las dificultades habilitadas en `configuracion`.
- `POST /` valida el formulario, crea `equipo` e `intento` en una transacción
  o deriva a identificación si el nombre ya existe.
- `GET/POST /equipo/identificar` pide el ID del equipo y lo compara con el
  nombre. Si el equipo tiene un intento activo lo reanuda; si no, crea uno
  nuevo con la dificultad elegida.
- `GET /juego` redirige a la estación actual del intento y retoma desde
  `intento.ultima_estacion_visitada` después de una recarga.
- `GET /juego/estacion/<orden>` muestra la estación con sus 4 preguntas y
  3 opciones cada una. La selección se sortea una vez y queda congelada en
  `intento_pregunta`; recargar no cambia las preguntas ni el orden.
  `intento_estacion.fecha_inicio` se crea una sola vez. No se permite saltar
  estaciones por URL y el HTML no incluye cuál opción es la correcta.
- Los contadores se calculan en `app/servicios/tiempos.py` desde las fechas de
  MySQL: el tiempo total sube en `HH:MM:SS` y el de la estación baja en
  `MM:SS` desde 4:00. Recargar no reinicia ninguno de los dos.
- `static/js/temporizadores.js` dibuja la cuenta entre sincronizaciones y
  consulta `GET /juego/estado` cada 10 segundos y al volver a la pestaña.
- A los 30 segundos restantes aparece el texto titilante y se intenta
  reproducir `app/static/audio/aviso-30s.wav`. El audio se desbloquea con la
  primera interacción; el aviso visual funciona igual si el navegador lo
  bloquea.
- Al agotarse el tiempo, el servidor cierra el intento como `por_tiempo` con
  `fecha_fin` del servidor y `puntaje_obtenido` en `NULL`, y redirige a
  `/juego/eliminado`. El control se repite en cada GET y POST, incluso si el
  reloj del navegador está manipulado.
- `POST /juego/estacion/<orden>/responder` registra el envío, guarda las 4
  respuestas en `respuesta_elegida` y solo las incorrectas en `incorrecta`.
  Si las 4 son correctas pasa a la transición; las incorrectas acumuladas
  eliminan; al agotar los envíos solo queda **Finalizar juego**.
- `POST /juego/estacion/<orden>/ayuda` suma una ayuda sin mostrar la pista.
- `POST /juego/estacion/<orden>/abandonar` y `/finalizar` cierran el intento
  y la estación.
- `GET /juego/transicion/<orden>` muestra el resumen de la estación y, en las
  estaciones 1 a 4, los botones **Continuar** y **Abandonar**. **Continuar**
  prepara la estación siguiente y actualiza `ultima_estacion_visitada`; su
  cronómetro arranca recién ahí. La quinta muestra **Ver resultado**.
- Al completar la quinta estación, el intento queda `finalizado = 'completo'`
  con la misma `fecha_fin` de la estación y `puntaje_obtenido` igual a los
  segundos totales. El contador general queda congelado.
- `GET /juego/final` muestra el resultado, la posición, el top 10 y el
  ranking completo con filtros por nombre de equipo, número de intento y
  fecha de fin. Las filas incluyen la fecha y hora de fin (`dd/mm/aaaa HH:MM`).
- `GET /juego/eliminado` explica el motivo (`por_tiempo`,
  `por_respuestas_incorrectas` o `abandono`) y muestra un resumen del intento.
- El ranking usa solo intentos completos y ordena por tiempo, luego
  incorrectas, luego ayudas, luego el intento que comenzó antes y, por
  último, `id`.
- El HUD muestra equipo, estación, los dos contadores, ayudas, respuestas
  incorrectas y envíos.

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
