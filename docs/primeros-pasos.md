# Primeros pasos

Hoja de ruta para construir la aplicación del **Escape Room 7.º B 2026** antes de la feria del **13 de noviembre de 2026**.

Este documento no reemplaza a las fuentes de verdad:

- `docs/escape-room.md` — requisitos funcionales y contenido.
- `AGENTS.md` — interpretación operativa, modelo de datos y decisiones registradas.
- `docs/navegacion-por-app.md` — pantallas, rutas y elementos de cada página.
- `sql/descripcion-de-la-base-de-datos.md` — modelo de datos y detalle de tablas.

Acá solo se ordena el trabajo: qué hacer primero, en qué orden y cómo saber que cada paso está terminado.

---

## 1. Punto de partida

Lo que ya existe:

- La documentación funcional y los prototipos visuales en `docs/`.
- El esquema de la base: `bd/schema.sql` (MySQL 8).
- El contenido inicial: `bd/seeds/001_contenido_inicial.sql` (5 estaciones, 14 temas, 20 preguntas, 60 respuestas y configuración).
- La decisión de usar la regla **1 pregunta por tema + 4 por estación** y de **no cargar pistas en la app**.

Lo que falta:

- La aplicación Flask (rutas, plantillas, estáticos, lógica del juego).
- La selección aleatoria persistida de preguntas.
- Los temporizadores, el HUD y las pantallas de eliminación.
- El ranking público y las estadísticas.
- El panel `/admin`.
- Los tests automatizados.
- Los archivos de arranque y el despliegue para el aula.

> Importante: el contenido actual es solo de nivel `inicial`. Las dificultades `intermedio` y `avanzado` quedan deshabilitadas hasta que el admin cargue cobertura completa.

---

## 2. Decisiones ya cerradas

No hace falta volver a discutirlas; están en `AGENTS.md` → "Decisiones registradas".

| Tema | Decisión |
| --- | --- |
| Regla de contenido | Al menos 1 pregunta por tema activo y 4 por estación. |
| Temas por estación | Máximo 4. El seed carga 14 temas en total. |
| Dificultades | `inicial` siempre; `intermedio` y `avanzado` solo con cobertura completa. |
| Ayudas | La app no muestra pistas; registra hasta 2 ayudas por estación e intento. |
| Identidad | `equipo.nombre` es único; si el nombre existe, la bienvenida pide el ID del equipo. |
| Intentos | Un equipo puede tener varios; si hay uno activo, se reanuda. |
| Ranking | Solo `finalizado = 'completo'`; orden por tiempo y luego por menos ayudas. |
| Borrado | Lógico en contenido; bloqueado en históricos. |

---

## 3. Orden de trabajo

### Paso 0 — Preparar el entorno

**Objetivo:** poder ejecutar el esquema y levantar Flask.

Tareas:

- Crear `.venv` y `requirements.txt` con: Flask, PyMySQL, python-dotenv, pytest y waitress.
- Crear `.env.example` con `FLASK_SECRET_KEY`, `MYSQL_HOST`, `MYSQL_PORT`, `MYSQL_USER`, `MYSQL_PASSWORD`, `MYSQL_DB`, `ADMIN_USER` y `ADMIN_PASSWORD_HASH`.
- Crear `.gitignore` para `.venv/`, `.env`, `__pycache__/`, `*.pyc` y volcados de base.
- Documentar en `README.md` los comandos reales.
- Ejecutar `bd/schema.sql` y `bd/seeds/001_contenido_inicial.sql` en una base limpia.

**Terminado cuando:** `python -c "import flask, pymysql"` funciona y el seed deja 5 estaciones, 14 temas, 20 preguntas y 60 respuestas.

---

### Paso 1 — Verificar la base y el contenido

**Objetivo:** confirmar que el contenido cumple las reglas antes de programar el juego.

Tareas:

- Correr el seed dos veces y comprobar que no duplica filas.
- Verificar que cada estación tenga 4 preguntas y cada tema al menos 1.
- Verificar que cada pregunta tenga exactamente 3 opciones y 1 correcta.
- Confirmar que `configuracion` tenga las dificultades en `0`.

**Terminado cuando:** las consultas de control dan los conteos esperados y no hay temas sin preguntas.

---

### Paso 2 — Esqueleto Flask

**Objetivo:** tener la estructura mínima para empezar a agregar pantallas.

Tareas:

- App factory en `app/__init__.py`.
- Configuración por variables de entorno y `SECRET_KEY`.
- `app/db.py` con conexión por request, cursor de diccionarios y helper de transacciones.
- Blueprints vacíos: `juego`, `ranking`, `estadisticas`, `admin`.
- `templates/base.html` con Bootstrap local desde `static/vendor/`.
- Manejo de errores 404 y 500.

**Terminado cuando:** `flask --app app run --debug` levanta y una ruta de salud confirma la conexión a MySQL.

---

### Paso 3 — Bienvenida e identidad del equipo

**Objetivo:** crear el equipo y el intento, y poder reingresar.

Tareas:

- Formulario con nombre, cantidad de integrantes (1–4) y dificultad.
- Mostrar solo las dificultades habilitadas en `configuracion`.
- Normalizar el nombre (trim y espacios repetidos).
- Si el nombre no existe: crear `equipo` e `intento`.
- Si el nombre existe: pedir el **ID del equipo** y validar que coincida.
- Si el equipo tiene un intento activo (`fecha_fin IS NULL`), reanudarlo; si no, crear uno nuevo.
- Guardar `intento_id` y `equipo_id` en la sesión de Flask.
- Mostrar **"Equipo N.º X"** en el HUD y en todas las pantallas.

**Terminado cuando:** el primer ingreso crea el equipo; el segundo con el mismo nombre pide el ID; un ID incorrecto se rechaza; recargar no pierde el intento.

---

### Paso 4 — Selección de preguntas y estación 1

**Objetivo:** jugar una estación completa de punta a punta.

Tareas:

- Implementar la selección: temas activos, 1 pregunta por tema, completar hasta 4 al azar, con el nivel del intento.
- Persistir la selección y el orden en `intento_pregunta`.
- Renderizar las 4 preguntas con los IDs de las opciones (nunca la respuesta correcta).
- Validar en el servidor que las respuestas pertenezcan a las preguntas del intento.
- Registrar `intento_envio`, `respuesta_elegida` e `incorrecta` en una transacción.
- Actualizar el HUD: ayudas, incorrectas y envíos.
- Aplicar las reglas: 2 incorrectas eliminan; 2 envíos dejan solo el botón de finalizar; todo correcto pasa a transición.

**Terminado cuando:** se puede jugar la estación 1, recargar y ver las mismas 4 preguntas, y las respuestas correctas no aparecen en el HTML.

---

### Paso 5 — Temporizadores y reanudación

**Objetivo:** que el tiempo sea del servidor y sobreviva recargas.

Tareas:

- Guardar `intento.fecha_inicio` e `intento_estacion.fecha_inicio`.
- Enviar al cliente los segundos restantes y la hora del servidor.
- Contador general ascendente y contador de estación descendente.
- Resincronizar cada pocos segundos.
- A los 30 segundos: audio local y texto titilante.
- Al llegar a 0: `finalizado = 'por_tiempo'` y pantalla de eliminación.
- Al reanudar: retomar desde `ultima_estacion_visitada`.

**Terminado cuando:** recargar no reinicia los tiempos, el aviso de 30 segundos funciona y el tiempo agotado elimina al equipo.

---

### Paso 6 — Recorrido completo y finales (MVP)

**Objetivo:** cerrar el juego completo.

Tareas:

- Estaciones 2 a 5 con la misma lógica.
- Transición entre estaciones.
- Botón de abandono con confirmación.
- Pantallas de eliminación por tiempo, por respuestas incorrectas y por abandono.
- Pantalla final con resultado del intento.
- Cálculo de `puntaje_obtenido` (segundos) solo para intentos completados.
- Ranking según tiempo y ayudas.

**Terminado cuando:** un equipo puede completar las 5 estaciones o quedar eliminado por las 4 causas, y el ranking ordena bien.

**Este es el MVP jugable.** Antes de seguir, probarlo con dos o tres personas.

---

### Paso 7 — Ranking público y estadísticas

**Objetivo:** la vista del televisor y la página pública de datos.

Tareas:

- `/ranking` de solo lectura, con polling cada 5–10 segundos y tipografía grande.
- Mostrar número de intento cuando un equipo repitió.
- `/estadisticas` con agregados: participantes, integrantes, intentos, tiempo promedio y respuestas realizadas / correctas.
- Sin nombres de equipos, sin detalle por pregunta y sin respuestas correctas.

**Terminado cuando:** la vista se actualiza sola y no expone datos sensibles.

---

### Paso 8 — Panel de administración

**Objetivo:** gestionar contenido y dificultades.

Tareas:

- `/admin` con login por variables de entorno y cierre de sesión.
- Proteger todas las rutas `/admin/*`.
- Cards por tabla y acceso a listados.
- CRUD con filtros y ordenamiento por id, nombre, dificultad, estación, tema y fechas.
- Borrado lógico en contenido y bloqueo en históricos.
- Reporte de cobertura estación × nivel, marcando en rojo lo que falta.
- Toggle de dificultades, bloqueado si hay intentos activos.
- Gráficos con Chart.js local o barras SVG/CSS.

**Terminado cuando:** sin login no se accede a nada de `/admin`, el toggle respeta la cobertura y el bloqueo por intentos activos, y el CRUD no rompe intentos históricos.

---

### Paso 9 — Pruebas y endurecimiento

**Objetivo:** asegurar las reglas críticas antes del ensayo.

Tareas:

- Configurar pytest con una base de prueba.
- Cubrir los casos listados en `AGENTS.md` → "Pruebas y verificación".
- Revisar que ninguna respuesta correcta viaje al cliente.
- Revisar SQL parametrizado y CSRF en formularios.
- Probar el seed dos veces.

**Terminado cuando:** `pytest` pasa y el checklist manual de `AGENTS.md` está completo.

---

### Paso 10 — Ensayo en el aula

**Objetivo:** llegar a la feria sin sorpresas.

Tareas:

- Levantar la app con waitress en `0.0.0.0` y probar desde 3 notebooks.
- Probar el televisor con `/ranking`.
- Cortar Internet y verificar que todo siga funcionando.
- Probar audio, recarga, reinicio de MySQL y restauración de un backup.
- Congelar el contenido y hacer un volcado de la base.

**Terminado cuando:** un simulacro completo con 3 equipos simultáneos termina sin errores.

---

## 4. Qué no hacer todavía

- No empezar por el panel `/admin`: primero el MVP jugable.
- No cargar niveles `intermedio` o `avanzado` sin contenido completo.
- No implementar el límite de 3 equipos simultáneos: es una regla operativa.
- No invertir tiempo en estilos hasta que el juego funcione.
- No copiar la lógica de `docs/src/index.html`: las respuestas se validan en el servidor.

---

## 5. Orden de commits sugerido

1. `chore: esquema y seed de contenido inicial`
2. `feat: esqueleto flask y configuración`
3. `feat: bienvenida e identidad de equipo`
4. `feat: estación con selección persistida y envío`
5. `feat: temporizadores y reanudación`
6. `feat: recorrido completo y pantallas de finalización`
7. `feat: ranking público y estadísticas`
8. `feat: panel de administración`
9. `test: reglas del juego`
10. `docs: comandos y puesta en marcha`

---

## 6. Definición de MVP jugable

El MVP está listo cuando:

- Un equipo se registra con nombre, cantidad de integrantes y dificultad.
- Juega las 5 estaciones en orden, con 4 preguntas por estación.
- Ve el tiempo general, el tiempo de estación, las ayudas, las incorrectas y los envíos.
- Puede pedir hasta 2 ayudas por estación.
- Es eliminado por tiempo, por 2 respuestas incorrectas o por abandono.
- Al completar las 5 estaciones ve su resultado y el ranking.
- Recargar la página no reinicia tiempos ni cambia preguntas.
- Nada de esto depende de Internet.

El admin y las estadísticas pueden quedar para después del MVP, pero antes del ensayo general.

---

## 7. Checklist para el día de la feria

- [ ] Base creada con `bd/schema.sql` y seed ejecutado.
- [ ] Contenido revisado y congelado.
- [ ] `ADMIN_PASSWORD_HASH` y `FLASK_SECRET_KEY` configurados.
- [ ] Backup de la base hecho y probado.
- [ ] 3 notebooks y el televisor probados en la red del aula.
- [ ] `/ranking` actualizándose solo en el televisor.
- [ ] Audio de aviso funcionando tras la primera interacción.
- [ ] Pistas impresas para los estudiantes.
- [ ] ID de equipo visible en todas las pantallas.
- [ ] Prueba completa sin conexión a Internet.
- [ ] Cargadores y baterías.

---

## 8. Riesgos y mitigaciones

| Riesgo | Mitigación |
| --- | --- |
| El admin lleva más tiempo que el juego | Priorizar el MVP y dejar el admin para la segunda semana. |
| Solo hay contenido `inicial` | Comunicarlo: las otras dificultades se habilitan cuando haya cobertura. |
| El navegador bloquea el audio | Desbloquearlo con el botón "Iniciar" y mantener siempre el aviso visual. |
| Se corta MySQL en plena feria | Backup previo y script de reinicio probado. |
| Relojes distintos entre servidor y notebooks | Calcular todo desde las fechas del servidor. |
| Dos equipos con el mismo nombre | El nombre es único; usar un sufijo si hace falta. |
| Internet inestable | Bootstrap, Chart.js y audio locales. |

---

## 9. Calendario sugerido

| Fecha | Qué hacer |
| --- | --- |
| 30/10 – 1/11 | Pasos 0 y 1: entorno, base y contenido. |
| 2/11 | Pedidos 1 y 2: esqueleto Flask y bienvenida. |
| 3/11 | Pedidos 3 y 4: selección de preguntas y estación 1 completa. |
| 4/11 | Pedido 5: temporizadores y reanudación. |
| 5/11 | Pedido 6: recorrido completo y finales. **MVP jugable**. |
| 6/11 | Pedido 7: prueba manual del MVP y correcciones. |
| 7/11 | Pedido 8: ranking público y estadísticas. |
| 8/11 | Pedido 9: login, panel y CRUD del admin. |
| 9/11 | Pedido 10: cobertura, dificultades y gráficos. |
| 10/11 | Pedido 11: pruebas automatizadas y endurecimiento. |
| 11/11 | Pedido 12: congelar contenido, backup y puesta en marcha. |
| 12/11 | Ensayo general en el aula. |
| 13/11 | Feria. |

---

## 10. Cómo pedir el desarrollo

El desarrollo se pide **por bloques verificables**, no de una sola vez. Un pedido grande esconde errores; un pedido chico se prueba y se corrige antes de seguir.

### 10.1 Reglas para cada pedido

1. **Un pedido, un objetivo.** Si el pedido tiene dos objetivos, se parte en dos.
2. **Dar contexto siempre.** El agente tiene que leer `AGENTS.md`, `docs/escape-room.md`, `docs/navegacion-por-app.md` y `sql/descripcion-de-la-base-de-datos.md` antes de escribir código.
3. **Fijar el alcance.** Decir qué archivos se esperan y qué **no** se quiere todavía.
4. **Pedir el criterio de aceptación.** No alcanza con "que funcione": hay que decir cómo se comprueba.
5. **Pedir pruebas.** Cada bloque termina con al menos una prueba manual y, desde el pedido 3, una prueba automatizada.
6. **Pedir un commit.** Un commit por pedido, con mensaje claro, para poder volver atrás.
7. **Revisar antes de seguir.** Si el pedido no cumple el criterio, se corrige antes de arrancar el siguiente.

### 10.2 Plantilla de pedido

```text
Contexto: Escape Room 7.º B 2026 (Flask + MySQL). Antes de tocar código leé
AGENTS.md, docs/escape-room.md, docs/navegacion-por-app.md y
sql/descripcion-de-la-base-de-datos.md.

Objetivo: <qué tiene que quedar funcionando>.

Alcance:
- <archivo o pantalla 1>
- <archivo o pantalla 2>

Reglas:
- <regla de negocio que aplica>
- <restricción técnica>

Criterio de aceptación:
- <prueba concreta 1>
- <prueba concreta 2>

No hagas todavía: <lo que queda para el próximo pedido>.

Al terminar: resumí los archivos tocados, los comandos para probarlo y dejá
un commit con el mensaje "<tipo>: <resumen>".
```

### 10.3 Qué pedir siempre al cerrar un pedido

- Lista de archivos creados y modificados.
- Comandos exactos para levantar la app y probar el bloque.
- Resultado de las pruebas (manuales y `pytest` si aplica).
- Riesgos o deudas técnicas que quedaron.
- Commit hecho.

### 10.4 Qué no delegar

- La revisión del contenido pedagógico.
- La decisión de habilitar `intermedio` o `avanzado`.
- La prueba con personas reales.
- El backup y la puesta en marcha en el aula.
- La aprobación final de cada pantalla.

---

## 11. Guion de pedidos, uno por uno

### Pedido 1 — Esqueleto Flask y conexión a MySQL

**Cuándo:** lunes 2/11, primera mitad de la mañana.
**Pasos de referencia:** 0 y 2.

**Pedido:**

```text
Contexto: Escape Room 7.º B 2026 (Flask + MySQL). Leé AGENTS.md,
docs/escape-room.md y sql/descripcion-de-la-base-de-datos.md.

Objetivo: dejar la app levantando con la estructura base y conexión a MySQL.

Alcance:
- requirements.txt con Flask, PyMySQL, python-dotenv, pytest y waitress.
- .env.example y .gitignore.
- app/__init__.py con app factory, SECRET_KEY y registro de blueprints.
- app/db.py con conexión por request, cursor de diccionarios y helper de
  transacción.
- Blueprints vacíos: juego, ranking, estadisticas, admin.
- templates/base.html con Bootstrap local desde static/vendor/.
- Ruta /salud que confirme la conexión a MySQL.
- Manejo de errores 404 y 500.

Reglas:
- Configuración solo por variables de entorno.
- No usar CDN.
- No crear todavía pantallas de juego.

Criterio de aceptación:
- flask --app app run --debug levanta.
- /salud responde 200 y confirma la base.
- Un 404 muestra una página amigable.
- Ejecutar bd/schema.sql y bd/seeds/001_contenido_inicial.sql deja
  5 estaciones, 14 temas, 20 preguntas y 60 respuestas.

No hagas todavía: bienvenida, estaciones, admin.

Al terminar: resumí archivos, comandos y dejá el commit
"feat: esqueleto flask y configuración".
```

**Verificación:** `curl localhost:5000/salud`, abrir una URL inexistente y confirmar el 404. Revisar que `.env` no esté versionado.

**Ojo con:** no hardcodear credenciales; no crear la base desde la app; no usar `debug=True` en producción.

---

### Pedido 2 — Bienvenida e identidad del equipo

**Cuándo:** lunes 2/11, segunda mitad de la mañana.
**Paso de referencia:** 3.

**Pedido:**

```text
Contexto: ya existe el esqueleto Flask y la base cargada.

Objetivo: registrar un equipo, crear su intento y permitir el reingreso.

Alcance:
- Ruta GET/POST / con formulario de nombre, cantidad de integrantes (1–4)
  y dificultad.
- Solo mostrar dificultades habilitadas en configuracion.
- Normalizar el nombre (trim y espacios repetidos).
- Si el nombre no existe: crear equipo e intento y guardar la sesión.
- Si el nombre existe: redirigir a /equipo/identificar y pedir el ID.
- Si el equipo tiene un intento activo (fecha_fin IS NULL), reanudarlo.
- Si no, crear un intento nuevo.
- Mostrar "Equipo N.º X" en el HUD.
- templates/bienvenida.html y templates/identificar.html.

Reglas:
- equipo.nombre es único.
- cantidad_personas entre 1 y 4.
- La dificultad del intento no cambia después de crearlo.
- No crear un equipo duplicado cuando el nombre ya existe.

Criterio de aceptación:
- Nombre nuevo crea equipo e intento y entra al juego.
- El mismo nombre pide el ID y no duplica el equipo.
- Un ID incorrecto se rechaza.
- Recargar no pierde el intento.
- Cantidad 0 o 5 se rechaza.

No hagas todavía: estaciones, temporizadores ni admin.

Al terminar: resumí archivos, comandos, pruebas y dejá el commit
"feat: bienvenida e identidad de equipo".
```

**Verificación:** crear "Los Tigres", salir, volver a entrar con el mismo nombre, probar ID correcto e incorrecto. Mirar en MySQL que haya un solo `equipo`.

**Ojo con:** el nombre único no distingue mayúsculas ni acentos; el ID tiene que verse siempre; no guardar el nombre en la sesión como fuente de verdad.

---

### Pedido 3 — Selección de preguntas y estación 1

**Cuándo:** martes 3/11, primera mitad de la mañana.
**Paso de referencia:** 4 (primera parte).

**Pedido:**

```text
Contexto: ya existe bienvenida e intento activo.

Objetivo: jugar la estación 1 con 4 preguntas seleccionadas y persistidas.

Alcance:
- Función de selección: temas activos de la estación, 1 pregunta por tema,
  completar hasta 4 al azar con preguntas de la estación y del nivel del
  intento.
- Persistir la selección y el orden en intento_pregunta.
- Crear intento_estacion con fecha_inicio al entrar.
- Ruta GET /juego/estacion/<orden> y template estacion.html.
- Renderizar las 4 preguntas con sus 3 opciones; nunca la correcta.
- HUD con equipo, estación, ayudas, incorrectas y envíos.
- Validar en el servidor que el orden de la URL sea el que corresponde.

Reglas:
- Siempre 4 preguntas del nivel del intento.
- Al menos 1 por tema activo.
- Con más de 4 temas, elegir 4 temas al azar y 1 pregunta de cada uno.
- La selección no cambia al recargar.
- No permitir saltar estaciones por URL.

Criterio de aceptación:
- La estación 1 muestra 4 preguntas.
- Recargar muestra las mismas 4 y en el mismo orden.
- En el HTML no aparece cuál es la correcta.
- Entrar a /juego/estacion/3 sin haber pasado la 2 redirige.
- Hay 4 filas en intento_pregunta para el intento.

No hagas todavía: envío del formulario, temporizadores ni estaciones 2–5.

Al terminar: resumí archivos, comandos, pruebas y dejá el commit
"feat: selección persistida de preguntas".
```

**Verificación:** consultar `intento_pregunta`, recargar 5 veces, buscar en el HTML el texto de la respuesta correcta (`grep`).

**Ojo con:** no usar `ORDER BY RAND()` sin persistir; no mezclar niveles; no confiar en el `orden` que manda el cliente.

---

### Pedido 4 — Envío, HUD y reglas de eliminación

**Cuándo:** martes 3/11, segunda mitad de la mañana.
**Paso de referencia:** 4 (segunda parte).

**Pedido:**

```text
Contexto: la estación 1 ya muestra las preguntas persistidas.

Objetivo: procesar el envío del formulario y aplicar las reglas del juego.

Alcance:
- POST /juego/estacion/<orden>/responder.
- Crear intento_envio con fecha y conteos.
- Insertar todas las respuestas en respuesta_elegida y las incorrectas
  también en incorrecta, dentro de una transacción.
- Actualizar el HUD: ayudas, incorrectas y envíos.
- Si todo está correcto: marcar intento_estacion.completada y redirigir a
  transición.
- Si hay 2 incorrectas en la estación: finalizar como
  por_respuestas_incorrectas y redirigir a eliminación.
- Si es el segundo envío y no está todo correcto: dejar solo el botón de
  finalizar juego.
- POST /juego/estacion/<orden>/ayuda: registrar ayuda con confirmación,
  máximo 2, deshabilitar botones al llegar a 2.
- POST /juego/estacion/<orden>/abandonar: finalizar como abandono.

Reglas:
- Máximo 2 envíos por estación.
- Máximo 2 ayudas por estación e intento.
- La app no muestra el texto de las pistas.
- No confiar en validaciones JavaScript.

Criterio de aceptación:
- Un envío con todo correcto pasa a transición.
- Un envío con 2 incorrectas elimina.
- Dos envíos con 1 incorrecta cada uno eliminan.
- Al segundo envío incorrecto solo queda finalizar.
- Las ayudas llegan como máximo a 2 y quedan deshabilitadas.
- Abandonar pide confirmación y cierra el intento.
- Todas las respuestas quedan en respuesta_elegida.

No hagas todavía: temporizadores ni estaciones 2–5.

Al terminar: resumí archivos, comandos, pruebas y dejá el commit
"feat: envío de respuestas y reglas de la estación".
```

**Verificación:** jugar la estación con respuestas correctas, con 1 incorrecta y con 2 incorrectas. Contar filas en `respuesta_elegida`, `incorrecta` e `intento_envio`. Probar doble clic en enviar.

**Ojo con:** el doble envío (usar POST + redirección y validar en el servidor); no permitir más de 2 envíos; no borrar la selección de preguntas al recargar.

---

### Pedido 5 — Temporizadores y reanudación

**Cuándo:** miércoles 4/11.
**Paso de referencia:** 5.

**Pedido:**

```text
Contexto: la estación 1 ya se juega y se registran envíos y ayudas.

Objetivo: que el tiempo sea del servidor y sobreviva recargas.

Alcance:
- Enviar al cliente los segundos restantes y la hora del servidor.
- Contador general ascendente desde intento.fecha_inicio.
- Contador de estación descendente desde intento_estacion.fecha_inicio.
- Resincronizar cada pocos segundos.
- A los 30 segundos: audio local y texto titilante.
- Al llegar a 0: finalizar como por_tiempo y redirigir a eliminación.
- Al reanudar: retomar desde intento.ultima_estacion_visitada.
- Desbloquear el audio con la primera interacción.

Reglas:
- No confiar en el reloj del navegador.
- El tiempo no se reinicia al recargar.
- El aviso de 30 segundos es visual y sonoro.

Criterio de aceptación:
- Recargar no reinicia ningún contador.
- A los 30 segundos aparece el texto titilante y suena el audio.
- Al llegar a 0 el intento queda por_tiempo y no se puede seguir.
- Reabrir la app retoma la estación correcta.

No hagas todavía: estaciones 2–5 ni ranking.

Al terminar: resumí archivos, comandos, pruebas y dejá el commit
"feat: temporizadores y reanudación".
```

**Verificación:** bajar `duracion_estacion_segundos` a 20 en `configuracion` para probar rápido; recargar; cerrar el navegador y volver.

**Ojo con:** no calcular el tiempo con `Date.now()` como fuente de verdad; no reiniciar `fecha_inicio` al recargar; el audio puede estar bloqueado hasta el primer clic.

---

### Pedido 6 — Recorrido completo y finales (MVP)

**Cuándo:** jueves 5/11.
**Paso de referencia:** 6.

**Pedido:**

```text
Contexto: la estación 1 funciona con temporizadores.

Objetivo: cerrar el recorrido de 5 estaciones y las pantallas finales.

Alcance:
- Estaciones 2 a 5 con la misma lógica de la 1.
- Transición entre estaciones con confirmación.
- Pantalla de eliminación por tiempo, por incorrectas y por abandono.
- Pantalla final con tiempo total, ayudas y posición.
- Calcular puntaje_obtenido (segundos) solo para intentos completados.
- Ranking básico por tiempo y luego ayudas.
- Actualizar ultima_estacion_visitada al avanzar.
- Bloquear el avance fuera de orden.

Reglas:
- Solo finalizado = 'completo' participa del ranking.
- puntaje_obtenido queda NULL en el resto.
- No se puede reanudar un intento finalizado.
- El abandono pide confirmación.

Criterio de aceptación:
- Un equipo completa las 5 estaciones y ve su resultado.
- Un equipo es eliminado por tiempo, por incorrectas y por abandono.
- El ranking ordena por tiempo y desempata por ayudas.
- Un intento no completado no aparece en el ranking.
- No se puede saltar de la estación 2 a la 5 por URL.

No hagas todavía: ranking público con polling, estadísticas ni admin.

Al terminar: resumí archivos, comandos, pruebas y dejá el commit
"feat: recorrido completo y pantallas de finalización".
```

**Verificación:** jugar las 5 estaciones; probar las 3 eliminaciones; revisar `intento.finalizado`, `fecha_fin` y `puntaje_obtenido` en MySQL.

**Ojo con:** el MVP es el corte más importante; no seguir al ranking sin probarlo con dos o tres personas.

---

### Pedido 7 — Prueba manual del MVP y correcciones

**Cuándo:** viernes 6/11.
**Paso de referencia:** 6 (cierre).

**Pedido:**

```text
Contexto: el MVP jugable está completo.

Objetivo: probarlo de punta a punta y corregir solo lo que rompe el juego.

Alcance:
- Probar con 2 o 3 personas: bienvenida, 5 estaciones, ayudas, envíos,
  recargas, eliminaciones y final.
- Corregir errores de flujo, mensajes confusos y problemas de tiempo.
- Revisar el HUD en pantalla chica y en el televisor.
- Ajustar textos en español rioplatense.

Reglas:
- No agregar funcionalidad nueva en este pedido.
- No tocar el esquema ni el seed salvo un error bloqueante.
- Cada corrección lleva su prueba.

Criterio de aceptación:
- Dos personas completan el recorrido sin ayuda técnica.
- Ninguna recarga rompe el intento.
- No hay respuestas correctas visibles en el HTML.
- Los mensajes se entienden sin explicación previa.

Al terminar: listá los errores encontrados, los corregidos y los que quedan,
y dejá el commit "fix: correcciones del MVP".
```

**Verificación:** hacer de "equipo" y jugar sin mirar el código. Anotar cada tropiezo.

**Ojo con:** resistir la tentación de empezar el admin antes de cerrar el MVP.

---

### Pedido 8 — Ranking público y estadísticas

**Cuándo:** sábado 7/11.
**Paso de referencia:** 7.

**Pedido:**

```text
Contexto: el MVP funciona y el ranking básico existe.

Objetivo: dejar la vista del televisor y la página pública de estadísticas.

Alcance:
- GET /ranking de solo lectura, tipografía grande y polling cada 5–10 s.
- GET /ranking/datos con JSON para el polling.
- Mostrar número de intento cuando un equipo repitió.
- GET /estadisticas con agregados: equipos, integrantes, intentos,
  tiempo promedio y respuestas realizadas/correctas.
- Gráfico simple de intentos por estado.

Reglas:
- Solo intentos completos en el ranking.
- Sin nombres de equipos ni detalle por pregunta en /estadisticas.
- Sin respuestas correctas.
- Si falla el polling, mantener la última tabla y avisar "reconectando".
- Nada depende de Internet.

Criterio de aceptación:
- El ranking se actualiza solo al terminar un intento.
- La vista se lee a varios metros.
- /estadisticas no expone datos sensibles.
- Cortar la red no rompe la vista.

No hagas todavía: admin.

Al terminar: resumí archivos, comandos, pruebas y dejá el commit
"feat: ranking público y estadísticas".
```

**Verificación:** abrir `/ranking` en el televisor o en una ventana grande; completar un intento desde otra notebook y ver el cambio; revisar el HTML de `/estadisticas` buscando nombres.

**Ojo con:** no usar WebSockets si alcanza el polling; no exponer `equipo_id` innecesario; el ranking no se ordena por puntos.

---

### Pedido 9 — Login, panel y CRUD del admin

**Cuándo:** domingo 8/11.
**Paso de referencia:** 8 (primera parte).

**Pedido:**

```text
Contexto: el juego y el ranking funcionan.

Objetivo: proteger /admin y permitir gestionar el contenido.

Alcance:
- GET /admin con formulario de login y POST /admin/login con validación por
  ADMIN_USER y ADMIN_PASSWORD_HASH.
- Sesión de Flask y cierre de sesión por POST.
- Proteger todas las rutas /admin/*.
- Panel con cards por tabla y accesos a listados.
- Listados con filtros y orden por id, nombre, dificultad, estación, tema
  y fechas.
- Alta y edición de estacion, tema, pregunta, respuesta y configuracion.
- Baja lógica (activo = 0) en contenido.
- Bloquear borrado de equipo, intento, respuesta_elegida e incorrecta.

Reglas:
- /admin no se enlaza desde páginas públicas.
- Nunca hardcodear credenciales.
- SQL siempre parametrizado.
- Cambiar la respuesta correcta no altera intentos finalizados.
- Validar máximo 4 temas activos por estación.
- Validar exactamente una respuesta correcta por pregunta.

Criterio de aceptación:
- Sin sesión, cualquier /admin/* redirige al login.
- Con sesión, se listan y editan las tablas.
- Un tema 5 en una estación se rechaza.
- Una pregunta con 0 o 2 correctas se rechaza.
- Los históricos no se pueden borrar.

No hagas todavía: cobertura, toggles de dificultad ni gráficos.

Al terminar: resumí archivos, comandos, pruebas y dejá el commit
"feat: panel de administración y CRUD".
```

**Verificación:** probar `/admin` en incógnito; intentar borrar un equipo; cargar un tema extra; revisar que el login no filtre qué campo falló.

**Ojo con:** no usar GET para logout; no mostrar el hash; no permitir editar históricos.

---

### Pedido 10 — Cobertura, dificultades y gráficos

**Cuándo:** lunes 9/11.
**Paso de referencia:** 8 (segunda parte).

**Pedido:**

```text
Contexto: el admin ya tiene login y CRUD.

Objetivo: controlar qué niveles se pueden habilitar y ver métricas.

Alcance:
- /admin/cobertura con tabla estación × nivel, conteos y faltantes en rojo.
- /admin/dificultades con toggles para intermedio y avanzado.
- Bloquear la habilitación si falta cobertura en alguna estación o tema.
- Bloquear la deshabilitación si hay intentos activos (fecha_fin IS NULL).
- /admin/intentos-activos con los equipos jugando.
- /admin/estadisticas con los gráficos pedidos en AGENTS.md.
- Gráficos con Chart.js local o barras SVG/CSS.

Reglas:
- inicial siempre habilitada.
- Los cambios se guardan en configuracion.
- No deshabilitar una dificultad con equipos jugando.
- Un nivel necesita al menos 1 pregunta por tema activo y 4 en total.

Criterio de aceptación:
- Con el contenido actual, intermedio y avanzado no se pueden habilitar.
- El reporte marca en rojo los temas sin preguntas.
- Con un intento activo, los toggles quedan bloqueados.
- Al terminar todos los intentos, se pueden cambiar.
- Los gráficos cargan sin Internet.

No hagas todavía: pruebas automatizadas completas.

Al terminar: resumí archivos, comandos, pruebas y dejá el commit
"feat: cobertura y control de dificultades".
```

**Verificación:** intentar habilitar `avanzado` y confirmar el bloqueo; crear un intento activo y probar el toggle; revisar que el gráfico no dependa de CDN.

**Ojo con:** la cobertura se calcula por tema y por estación, no solo por estación; el bloqueo es por `fecha_fin IS NULL`, no por `finalizado`.

---

### Pedido 11 — Pruebas automatizadas y endurecimiento

**Cuándo:** martes 10/11.
**Paso de referencia:** 9.

**Pedido:**

```text
Contexto: la app está completa y probada a mano.

Objetivo: cubrir las reglas críticas con pytest y cerrar agujeros.

Alcance:
- Configurar pytest con una base de prueba independiente.
- Cubrir los casos de AGENTS.md → "Pruebas y verificación".
- Verificar que ninguna respuesta correcta viaje al cliente.
- Revisar SQL parametrizado, CSRF en formularios y sesión de admin.
- Probar el seed dos veces.
- Documentar los comandos reales en README.md.

Reglas:
- Los tests no dependen de la base de producción.
- Cada test deja la base limpia.
- No bajar cobertura de reglas críticas para "que pase".

Criterio de aceptación:
- pytest pasa completo.
- Hay tests de ranking, eliminaciones, ayudas, envíos, selección,
  reingreso, cobertura y borrado lógico.
- El seed es idempotente.
- README.md tiene los comandos reales.

Al terminar: resumí archivos, comandos, resultado de pytest y dejá el commit
"test: reglas del juego y endurecimiento".
```

**Verificación:** correr `pytest` dos veces seguidas; revisar que no queden datos de prueba.

**Ojo con:** no testear contra la base de la feria; no dejar `SECRET_KEY` de desarrollo.

---

### Pedido 12 — Congelar, respaldar y poner en marcha

**Cuándo:** miércoles 11/11.
**Paso de referencia:** 10 (preparación).

**Pedido:**

```text
Contexto: la app y los tests están listos.

Objetivo: dejarla lista para el aula, sin cambios de último momento.

Alcance:
- Revisar y congelar el contenido.
- Generar un volcado de la base y probar la restauración.
- Documentar el arranque con waitress en 0.0.0.0.
- Configurar ADMIN_PASSWORD_HASH y FLASK_SECRET_KEY reales.
- Probar desde 3 notebooks y el televisor.
- Verificar el funcionamiento sin Internet.
- Dejar un script de reinicio y backup.

Reglas:
- No cargar contenido nuevo después de este pedido.
- No cambiar el esquema.
- El backup se prueba, no solo se genera.

Criterio de aceptación:
- La app levanta desde cero con los comandos del README.
- El backup se restaura en una base limpia.
- 3 notebooks juegan a la vez sin errores.
- El televisor muestra /ranking actualizándose.
- Sin Internet, todo sigue funcionando.

Al terminar: resumí el procedimiento, los comandos y dejá el commit
"docs: puesta en marcha y respaldo".
```

**Verificación:** simular un aula: 3 equipos, un televisor, sin Internet. Cronometrar el arranque.

**Ojo con:** no hacer cambios de código el día de la feria; tener el backup en un pendrive y en la nube.

---

### Día de la feria (13/11)

No se pide desarrollo. Solo se ejecuta el checklist de la sección 7 y se usa el procedimiento del pedido 12.

---

## 12. Checklist de aceptación por pedido

| Pedido | Se considera terminado cuando… |
| --- | --- |
| 1 | `/salud` responde y la base tiene el contenido del seed. |
| 2 | El reingreso pide ID y no duplica equipos. |
| 3 | Las 4 preguntas se mantienen al recargar y no se filtra la correcta. |
| 4 | Se aplican envíos, ayudas y las 3 formas de eliminación. |
| 5 | Los tiempos sobreviven recargas y el aviso de 30 s funciona. |
| 6 | Se completa el recorrido y el ranking ordena por tiempo y ayudas. |
| 7 | Dos personas juegan sin asistencia técnica. |
| 8 | El ranking se actualiza solo y las estadísticas no exponen datos. |
| 9 | `/admin` está protegido y el CRUD respeta las validaciones. |
| 10 | Cobertura, toggles y bloqueo por intentos activos funcionan. |
| 11 | `pytest` pasa y el seed es idempotente. |
| 12 | Un simulacro con 3 equipos y sin Internet termina bien. |

---

## 13. Qué revisar en cada entrega

Antes de dar por bueno un pedido, revisar:

- **Alcance:** ¿hizo solo lo pedido o agregó cosas de más?
- **Reglas:** ¿respetó las decisiones de `AGENTS.md`?
- **Servidor:** ¿la validación está en el backend y no solo en JavaScript?
- **SQL:** ¿usa parámetros? ¿hay transacciones donde corresponde?
- **Respuestas:** ¿la correcta queda fuera del HTML y del JSON público?
- **Tiempo:** ¿se calcula desde las fechas del servidor?
- **Persistencia:** ¿recargar no cambia preguntas ni reinicia relojes?
- **Admin:** ¿está protegido y sin enlaces públicos?
- **Históricos:** ¿se pueden borrar? No deberían.
- **Pruebas:** ¿el criterio de aceptación se probó de verdad?
- **Commit:** ¿está hecho y con un mensaje claro?

---

## 14. Frases útiles para corregir el rumbo

Cuando algo no cierra, conviene pedir el ajuste con precisión:

- "No cambies el alcance: solo corregí X, sin tocar Y."
- "Mostrame el diff y explicá por qué cambiaste ese archivo."
- "Agregá una prueba que demuestre que esto no vuelve a pasar."
- "Revisá que la respuesta correcta no esté en el HTML ni en el JSON."
- "El tiempo tiene que salir de la base, no del reloj del navegador."
- "Esto tiene que funcionar sin Internet: bajá la librería a `static/vendor/`."
- "Antes de seguir, hacé un commit de lo que funciona."
- "Si el pedido es ambiguo, preguntá antes de inventar."
