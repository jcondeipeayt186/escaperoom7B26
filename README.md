# Escape Room 7.º B 2026

Aplicación web para la Feria de Producciones del IPEATyM 186 Castagnari (16/11/2026).

## Documentación

- `docs/proyectoEscapeRoom-7B.md` — título y reseña breve del proyecto.
- `docs/escape-room.md` — requisitos funcionales y contenido inicial.
- `docs/primeros-pasos.md` — hoja de ruta y guion de pedidos, paso a paso.
- `docs/argumentos-pasos/` — un archivo por paso (`paso00` a `paso12`, más `paso11b`, `paso11c` y el `paso13` opcional de Docker post-feria), listo para usar con `/feature`. Incluye el índice y los criterios de aceptación.
- `docs/navegacion-por-app.md` — pantallas, rutas, elementos y objetivos.
- `docs/tecnologias.md` — stack explicado: frontend, backend, base de datos y herramientas.
- `docs/instalacion-y-puesta-en-funcionamiento.md` — instalación en Ubuntu y uso desde las notebooks.
- `docs/dejar-funcionando-proyecto-luego-clone.md` — pasos para dejar el proyecto funcionando después de clonarlo: MySQL, base de datos, entorno virtual, `.env` y pruebas.
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

## Flujo implementado hasta el paso 11

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
- `GET /juego/final` muestra el resultado, la posición dentro del nivel del
  intento, la posición general, el top 10 del nivel y el ranking completo con
  columnas **Pos. general**, **Pos. nivel** y **Nivel**. Se puede filtrar por
  nombre de equipo, número de intento, fecha de fin y nivel. Las filas incluyen
  la fecha y hora de fin (`dd/mm/aaaa HH:MM`).
- `GET /juego/eliminado` explica el motivo (`por_tiempo`,
  `por_respuestas_incorrectas` o `abandono`) y muestra un resumen del intento.
- El ranking usa solo intentos completos y ordena por tiempo, luego
  incorrectas, luego ayudas, luego el intento que comenzó antes y, por
  último, `id`. La competencia es por nivel: `posicion` es la general y
  `posicion_nivel` la del nivel del intento, con el mismo orden.
- El HUD muestra equipo, estación, los dos contadores, ayudas, respuestas
  incorrectas y envíos.
- `GET /ranking` es la vista pública para el televisor: una tabla grande por
  nivel con posición, equipo, número de intento, tiempo, incorrectas, ayudas y
  fecha de fin. Se renderiza en el servidor y se actualiza sola consultando
  `GET /ranking/datos` cada 8 segundos. Si el polling falla, conserva todas las
  tablas y muestra **Reconectando…**. El JSON agrupa las filas por nivel, solo
  incluye intentos completados y no expone `equipo_id` ni `intento_id`.
  `inicial` se muestra siempre; `intermedio` y `avanzado` si están habilitados
  o si ya tienen intentos completados.
- `GET /estadisticas` muestra agregados de la feria: equipos, integrantes,
  intentos iniciados y completados, tiempo promedio de los completados,
  respuestas realizadas, porcentaje de aciertos y barras de intentos por
  estado. No muestra nombres de equipos, detalle por pregunta ni respuestas
  correctas. Los aciertos se toman del resultado guardado en cada
  `intento_envio`, para que el historial no cambie si después se edita una
  pregunta.
- La bienvenida enlaza a `/ranking` y `/estadisticas`; el final enlaza a
  estadísticas y la eliminación a ranking.
- `GET /admin` muestra el login y `POST /admin/login` valida `ADMIN_USER` y
  `ADMIN_PASSWORD_HASH`. `POST /admin/logout` cierra la sesión administrativa.
  Todas las rutas `/admin/*` salvo el login exigen sesión; `/admin` no está
  enlazada desde ninguna página pública.
- `/admin/` muestra cards con el total y los activos/inactivos de las 12
  tablas, además del estado del juego (intentos activos, equipos jugando y
  última actividad).
- `/admin/<tabla>` lista cualquier tabla con búsqueda, filtros, orden y
  paginación resueltos en el servidor. El orden siempre sale de una lista
  blanca y los valores inválidos caen a los predeterminados.
- `/admin/<tabla>/nuevo`, `/admin/<tabla>/<id>/editar` y
  `POST /admin/<tabla>/<id>/desactivar` gestionan estaciones, temas,
  preguntas, respuestas y configuración. La baja es lógica (`activo = 0`).
  `/admin/<tabla>/<id>` muestra el detalle de cualquier fila.
- Las tablas históricas (`equipo`, `intento`, `intento_estacion`,
  `intento_envio`, `intento_pregunta`, `respuesta_elegida` e `incorrecta`) son
  de solo lectura: sus rutas de alta, edición y baja devuelven `404`.
- Una pregunta nueva queda inactiva hasta tener al menos 2 respuestas activas
  y exactamente 1 correcta. Marcar una respuesta como correcta desmarca las
  demás de esa pregunta. Con intentos activos no se cambian el orden ni el
  estado de las estaciones, los parámetros del juego, ni las respuestas
  correctas de las preguntas en curso. Tampoco se puede mover contenido ya
  usado en un intento.
- `/admin/cobertura` muestra la cobertura de cada nivel por estación y tema:
  preguntas activas por tema, total, lo que falta y estado verde/rojo.
  `inicial` siempre figura habilitada. Cada tema activo necesita al menos
  1 pregunta del nivel y cada estación 4 en total.
- `/admin/dificultades` permite habilitar o deshabilitar `intermedio` y
  `avanzado`. Habilitar exige cobertura completa en todas las estaciones y
  cualquier cambio se bloquea mientras haya intentos activos. El servidor
  valida los toggles aunque el formulario se envíe directamente.
- `/admin/intentos-activos` lista los equipos que están jugando, su estación
  actual, el tiempo transcurrido y la última actividad registrada.
- `/admin/estadisticas` muestra equipos, intentos iniciados, finalizados y
  completados, tiempo promedio de los completados, aciertos, intentos por
  estado (incluye **En curso**), tiempo promedio por estación completada y
  utilización de cada pregunta. Los filtros por fecha y dificultad se aplican
  sobre `intento.fecha_inicio` e `intento.dificultad`. Las barras son CSS
  generadas en el servidor, sin Chart.js ni CDN.
- El panel de administración y la barra de navegación del admin enlazan a
  cobertura, dificultades, intentos activos y estadísticas.
- Todos los formularios POST (bienvenida, identificación, estación, ayudas,
  abandono, transición, admin, login y logout) incluyen un token CSRF guardado
  en la sesión. El servidor lo valida antes de ejecutar cualquier vista: un
  POST sin token o con un token inválido devuelve `400` sin modificar datos.
  El token se rota al iniciar y al cerrar la sesión de administración.
  `GET /juego/estado` queda fuera porque el polling no envía formularios.

La lógica de identidad y configuración vive en `app/servicios/`. La sesión de
Flask guarda solo `equipo_id` e `intento_id`; el servidor vuelve a leer y
validar la base en cada request.

## Pruebas automatizadas

La suite usa una base MySQL independiente. Al iniciar la sesión de pytest se
elimina y se vuelve a crear `escape_room_7b2026_test` (o la que indique
`TEST_MYSQL_DB`), se carga `bd/schema.sql` y el seed, y antes y después de
cada test se limpian las tablas y se vuelve a ejecutar el seed. La base de
desarrollo nunca se toca: el nombre debe terminar en `_test` y ser distinto de
`MYSQL_DB`. El usuario de MySQL necesita permisos `CREATE` y `DROP` sobre esa
base.

```bash
source .venv/bin/activate
pytest -q
pytest -q
```

La configuración está en `pytest.ini` (`testpaths = tests` y
`pythonpath = .`). Al terminar, la base de test queda creada y con el seed.

> Para la feria se usa waitress, no el servidor de desarrollo. El
> procedimiento de producción está en
> `docs/instalacion-y-puesta-en-funcionamiento.md` y se cierra en el paso 12.
