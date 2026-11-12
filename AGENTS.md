# AGENTS.md

Guía para agentes de IA que trabajen en el proyecto **Escape Room 7°B 2026** del IPEATyM 186 Castagnari.

## Fuente de verdad

1. `docs/escape-room.md` — requisitos funcionales y modelo de datos. **Tiene prioridad ante cualquier otro documento o prototipo.**
2. `docs/ESCAPE ROOM.pdf` — preguntas para cargar como contenido y pistas para leer en papel. Su transcripción revisada está en `docs/pistas-del-juego.md`.
3. `docs/banco-preguntas-intermedio-avanzado.md` — 60 preguntas nuevas de `intermedio` y `avanzado`, con opciones y pistas, aprobadas antes de generar los seeds.
4. `docs/src/index.html` — boceto visual y de flujo de las estaciones.
5. `docs/src/ranking-puntajes/ranking-puntajes.html` — boceto visual de la pantalla final y del ranking.
6. `docs/ideas-escape-room.md` — ideas para el stand (redes sociales, banner, ping pong). **No son requisitos de la aplicación.**

Si este archivo contradice a `docs/escape-room.md`, ver el apartado de este archivo de decisiones registradas, y preguntame para darte el ok y hay que actualizar este archivo resolviendo las dudas dejandolas en esa misma sección de decisiones registradas.

> Nota: `AGENTS.md` mencionaba antes un archivo `docs/REGLAS ESCAPE ROOM.pdf` que **no existe** en el repositorio. Si aparece más adelante, incorporarlo como fuente complementaria, nunca por encima de `docs/escape-room.md`.

## Memoria

Recuerda actualizar siempre el archivo MEMORY.md con el estado actual del proyecto.

## Objetivo del producto

Aplicación web para una feria escolar. Equipos de hasta 4 integrantes recorren 5 estaciones en orden, responden 4 preguntas por estación y compiten por completar el recorrido en el menor tiempo posible.

Temáticas de las estaciones:

1. Redes
2. Hardware
3. Internet
4. Ciberseguridad
5. Sistemas Operativos

Reglas principales:

- Una página de bienvenida pide **nombre del equipo**, **cantidad de integrantes (1–4)** y **dificultad** (`inicial`, `intermedio`, `avanzado`).
- Cada estación muestra **4 preguntas** del nivel elegido; deben estar todas correctas para avanzar.
- La selección de esas 4 preguntas sigue la regla de "Selección de preguntas por estación".
- Cada estación dura **4 minutos**. Al agotarse el tiempo, el equipo queda eliminado.
- **Dos respuestas incorrectas** en una estación eliminan al equipo. Ver "Decisiones registradas".
- Si por cada estación tuvo 1 respuesta incorrecta, al finalizar tendría 5 respuestas incorrectas, esto es válido.
- Abandonar el juego también elimina al equipo.
- Se muestra siempre un **tiempo general ascendente** y un **tiempo de estación descendente**.
- En cada página de estación se muestra: **cantidad de ayudas**, **cantidad de respuestas incorrectas** y **cantidad de envíos del formulario**. Al llegar a 2 envíos solo queda disponible el botón de finalizar juego por respuestas incorrectas.
- Las ayudas se piden con los botones **Ayuda 1** y **Ayuda 2** (con confirmación). Al usar las 2 se deshabilitan. La app **no muestra el texto de la pista**: los estudiantes de 7.º la leen en papel.
- A los **30 segundos restantes** de la estación: reproducir un audio de aviso y hacer titilar un texto debajo del contador.
- Al completar las 5 estaciones se calcula el puntaje y se muestra el ranking.
- Un equipo puede realizar varios intentos; el puntaje está asociado a cada intento.
- En el aula habrá una notebook conectada a un televisor mostrando el ranking de forma permanente.

### Selección de preguntas por estación

Siempre se muestran **4 preguntas**, todas del nivel del intento. El algoritmo es:

1. Tomar los temas activos de la estación.
2. Si hay **más de 4 temas**, elegir 4 temas al azar y una pregunta de cada uno.
3. Si hay **4 temas o menos**, elegir al menos una pregunta de cada tema y completar los lugares restantes al azar con preguntas de la estación y nivel.
4. Persistir la selección y el orden en `intento_pregunta`.

Reglas de contenido:

- **Máximo 4 temas por estación**, validado en `/admin`.
- Cada tema activo debe tener **al menos 1 pregunta del nivel**.
- Cada estación debe tener **al menos 4 preguntas del nivel** en total.
- `inicial` siempre está habilitada y debe tener cobertura completa.
- `intermedio` y `avanzado` solo se habilitan si **todas** las estaciones tienen cobertura de ese nivel.
- El contenido cargado tiene 80 preguntas: 20 `inicial` (4 por estación), 30 `intermedio` y 30 `avanzado` (6 por estación en esos niveles). Con esa cobertura los tres niveles pueden habilitarse desde `/admin/dificultades`.
- La selección se congela por intento: recargar la página no cambia las preguntas.

## Stack y arquitectura

- **Backend:** Python + Flask.
- **Base de datos:** MySQL.
- **Frontend:** HTML server-rendered con Jinja, Bootstrap.
- **Estilos:** Bootstrap mínimo, solo lo necesario.
- **Sin SPA ni frameworks frontend** (React, Vue, etc.). No agregar dependencias pesadas sin consultar.

El servidor es la autoridad del juego:

- Validar respuestas y orden de estaciones en el backend.
- No enviar respuestas correctas al navegador ni confiar en validaciones JavaScript.
- Calcular tiempos y ranking a partir de fechas guardadas en MySQL, no solo del reloj del cliente.
- Persistir la selección aleatoria de preguntas de cada intento: recargar la página no debe cambiar las preguntas.
- Persistir el inicio de cada estación y la última estación visitada para sobrevivir recargas.

Estructura sugerida una vez creado el scaffold:

```text
app/
  __init__.py          # app factory, configuración y login de admin
  db.py                # conexión MySQL y helpers
  servicios/           # lógica de dominio, fuera de las rutas web
    configuracion.py   # lectura de configuracion y dificultades habilitadas
    equipos.py         # identidad, alta y reanudación de intentos
    estaciones.py      # orden del recorrido y consultas de estaciones
    seleccion.py       # selección y congelamiento de preguntas por intento
    envios.py          # envíos, ayudas, abandono y cierre de estación
    ranking.py         # ranking completo, posición y número de intento
    tiempos.py         # contadores calculados desde fechas de MySQL
  routes/
    juego.py           # bienvenida, estaciones, transición, final, abandono
    ranking.py         # ranking público / vista de TV
    estadisticas.py    # página pública de estadísticas
    admin.py           # login y CRUD del panel de administración
  templates/
    bienvenida.html
    identificar.html
    juego.html
    _hud.html
    estacion.html
    transicion.html
    final.html
    ranking.html
    estadisticas.html
    eliminado.html
    admin/
  static/
    css/
      temporizadores.css
    js/
      juego.js
      temporizadores.js
    audio/
      aviso-30s.wav
    vendor/            # librerías locales, sin CDN
tests/
bd/
  schema.sql           # estructura de la base (MySQL 8)
  seeds/
    001_contenido_inicial.sql   # inicial: 20 preguntas y configuración
    002_contenido_intermedio.sql # intermedio: 30 preguntas
    003_contenido_avanzado.sql  # avanzado: 30 preguntas
requirements.txt
.env.example
README.md
```

Ajustar la estructura si el proyecto real adopta otra, pero mantener la separación entre rutas, plantillas, estáticos y acceso a datos.

## Modelo de datos requerido

Basado en `docs/escape-room.md`:


| Entidad             | Campos mínimos                                                                                                                                                                                                                                                            |
| --------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `equipo`            | `id`, `nombre`, `cantidad_personas` (1–4, obligatorio)                                                                                                                                                                                                                    |
| `intento`           | `id`, `equipo_id`, `dificultad` (`inicial`, `intermedio`, `avanzado`), `fecha_inicio`, `fecha_fin`, `se_completo_ok`, `cantidad_ayudas`, `puntaje_obtenido`, `finalizado` (`completo`, `abandono`, `por_respuestas_incorrectas`, `por_tiempo`), `ultima_estacion_visitada` |
| `estacion`          | `id`, `nombre`, `descripcion`, `orden`, `activo`                                                                                                                                                                                                                           |
| `tema`              | `id`, `nombre`, `estacion_id`, `activo`                                                                                                                                                                                                                                    |
| `pregunta`          | `id`, `titulo`, `descripcion`, `tema_id`, `dificultad` (`inicial`, `intermedio`, `avanzado`), `activo`                                                                                                                                                                     |
| `respuesta`         | `id`, `contenido`, `correcta` (booleano), `pregunta_id`, `activo`                                                                                                                                                                                                          |
| `respuesta_elegida` | `id`, `fecha_respondida`, `intento_id`, `intento_envio_id`, `respuesta_id`                                                                                                                                                                                                 |
| `incorrecta`        | `id`, `pregunta_id`, `respuesta_id`, `fecha`, `intento_id`, `intento_envio_id`                                                                                                                                                                                             |

Criterios:

- Usar `snake_case` para tablas y columnas, y claves foráneas `<entidad>_id`.
- Guardar **todas** las respuestas elegidas en `respuesta_elegida`, correctas e incorrectas.
- Guardar además en `incorrecta` cada respuesta incorrecta, tal como pide `docs/escape-room.md`. La duplicación es intencional: `respuesta_elegida` es el registro completo y `incorrecta` el subconjunto que alimenta el HUD y las estadísticas.
- No guardar ni mostrar la respuesta correcta en el HTML/JS del participante.
- `intento.fecha_fin` queda `NULL` mientras el intento está en curso.
- `intento.se_completo_ok` es derivado: verdadero solo si `finalizado = 'completo'`. No usar dos fuentes de verdad distintas.
- **Solo los intentos con `finalizado = 'completo'` participan del ranking competitivo.** `fecha_fin` no nula **no alcanza**: abandonos y eliminaciones también tienen fecha de fin.
- `puntaje_obtenido` se completa solo para intentos completados (ver "Reglas de puntaje y ranking").
- `equipo.cantidad_personas` es obligatorio, entre 1 y 4, y se carga en la bienvenida.
- `equipo.nombre` es único (la colación `utf8mb4_unicode_ci` compara sin distinguir mayúsculas ni acentos). Si el nombre ya existe, la bienvenida pide el `equipo_id` para continuar con ese equipo; no se crea un equipo duplicado.
- `intento.finalizado` queda `NULL` mientras el intento está en curso y se completa con uno de los cuatro valores al terminar.
- `intento.se_completo_ok` se implementa como columna generada a partir de `finalizado` (no se inserta ni se edita a mano).
- `intento.dificultad` guarda el nivel elegido y no cambia durante el intento.
- `estacion.orden` define el recorrido 1 a 5 de forma explícita; no depender del `id`.
- `estacion`, `tema`, `pregunta` y `respuesta` usan **borrado lógico** con `activo`. El juego y los selectores filtran `activo = 1`; los intentos históricos siguen leyendo las filas desactivadas.
- `respuesta_elegida.intento_envio_id` e `incorrecta.intento_envio_id` son una extensión al modelo base para agrupar las respuestas de un mismo envío del formulario.
- `equipo`, `intento`, `respuesta_elegida` e `incorrecta` son históricos: no se borran, ni física ni lógicamente.
- Respetar el **máximo de 4 temas por estación**.
- La clave primaria `id` debe ser auto incremental.

### Tablas de detalle necesarias

El modelo de `docs/escape-room.md` no alcanza para cronometrar cada estación, contar envíos, persistir la selección aleatoria, habilitar dificultades ni registrar ayudas. Agregar estas tablas **sin reemplazar** el modelo base:

```text
intento_estacion(id, intento_id, estacion_id, fecha_inicio, fecha_fin, ayudas, completada)
intento_envio(id, intento_id, estacion_id, fecha, respuestas_correctas, respuestas_incorrectas)
intento_pregunta(id, intento_id, estacion_id, pregunta_id, orden)   # selección aleatoria estable
configuracion(clave, valor)                                          # dificultades habilitadas y otros parámetros
```

- `intento_envio` es imprescindible para mostrar "cantidad de intentos de envío del formulario"; no intentar derivarlo solo de `respuesta_elegida`.
- `intento_pregunta` garantiza que al recargar se muestren las mismas 4 preguntas y que el resultado sea reproducible.
- `configuracion` guarda, por ejemplo, `dificultad_intermedia_habilitada` y `dificultad_avanzada_habilitada`, además de los parámetros del juego (`duracion_estacion_segundos`, `max_ayudas_estacion`, `max_envios_estacion`, `max_respuestas_incorrectas`, `max_integrantes_equipo`, `max_temas_por_estacion`, `preguntas_por_estacion`). La dificultad `inicial` queda siempre habilitada.
- Un nivel solo puede habilitarse si todas las estaciones tienen al menos 1 pregunta activa de ese nivel por tema y 4 en total.
- **No existe tabla `pista`.** Las pistas están en `docs/ESCAPE ROOM.pdf` y en su transcripción `docs/pistas-del-juego.md`, las leen los estudiantes, y la app solo registra 1 o 2 ayudas por estación en `intento_estacion.ayudas` y en `intento.cantidad_ayudas`.
- Cualquier tabla extra debe documentarse en `README.md` y en este archivo.

## Flujo de pantallas

1. **Bienvenida:** formulario con nombre de equipo, cantidad de integrantes (1–4) y dificultad. Validar nombre no vacío y cantidad entre 1 y 4. Solo se ofrecen las dificultades habilitadas en `configuracion`. Si el nombre ya existe, pedir el **ID del equipo** (el que se muestra siempre en el HUD) y continuar con ese equipo; si no existe, crear `equipo` e `intento`. Al reingresar con un equipo que tiene un intento activo (`fecha_fin IS NULL`), reanudar ese intento; si no, crear uno nuevo. Mostrar el ID del equipo en todas las pantallas del intento.
2. **Estación 1 a 5:** una página/ruta por estación, con sus 4 preguntas, el temporizador y el HUD (ayudas, incorrectas, envíos). No permitir saltar estaciones por URL.
3. **Transición:** confirmar estación superada y permitir continuar. La estación siguiente se prepara y su cronómetro arranca recién al presionar **Continuar**. Desde la transición de las estaciones 1 a 4 también se puede abandonar con confirmación.
4. **Final:** mostrar el resultado del intento, la posición general y la posición dentro de su nivel, el top 10 del nivel del intento y el ranking completo filtrable por equipo, número de intento, fecha de fin y nivel. Incluye la fecha y hora de fin de cada intento.
5. **Ranking público:** vista de solo lectura, pensada para el televisor. `GET /ranking` renderiza una tabla por nivel en el servidor y `GET /ranking/datos` entrega el JSON agrupado por nivel para el polling cada 8 segundos. Se actualiza sola, conserva las últimas tablas si falla la conexión y es legible a distancia.
6. **Eliminación:** pantalla clara cuando el equipo queda fuera por tiempo, respuestas incorrectas o abandono.
7. **Estadísticas públicas:** solo agregados (participantes, integrantes, intentos iniciados y completados, tiempo promedio de los completados, respuestas realizadas y porcentaje de aciertos), con barras por estado generadas en el servidor. Sin nombres de equipos, sin detalle por pregunta y sin respuestas correctas. Accesible sin login.
8. **Login de administración:** `/admin`, con usuario y clave.
9. **Panel de administración:** cards, gráficos y CRUD de las tablas.

## Administración

La administración es un **requisito**, no un extra opcional.

- Ruta `/admin`, **no enlazada** desde ninguna página pública.
- Login con usuario y clave; sin login no se accede a ninguna ruta `/admin/*`.
- Credenciales por variables de entorno: `ADMIN_USER` y `ADMIN_PASSWORD_HASH` (usar `werkzeug.security.generate_password_hash`). Nunca hardcodear claves ni commitearlas.
- Sesión de Flask para mantener el login; incluir cierre de sesión.
- Panel de control con cards de Bootstrap, una por tabla, y acceso a los listados.
- `GET /admin/cobertura`: reporte estación × nivel con temas activos, preguntas por tema, total y estado verde/rojo.
- `GET/POST /admin/dificultades`: toggles de `intermedio` y `avanzado`, con cobertura resumida y bloqueo por intentos activos.
- `GET /admin/intentos-activos`: equipos jugando, estación actual, tiempo transcurrido y última actividad.
- `GET /admin/estadisticas`: gráficos de equipos, intentos finalizados, tiempo promedio por estación, tiempo promedio de completados, utilización de cada pregunta y porcentaje de aciertos.
- Gráficos estadísticos: equipos participantes, intentos finalizados, tiempo promedio por estación, tiempo promedio de los intentos finalizados, porcentaje de utilización de cada pregunta sobre el total de intentos (completados o no) y porcentaje de aciertos.
- CRUD de todas las tablas del modelo base.
- En los listados, permitir filtros y ordenamiento por `id` y por otros campos relevantes (nombre, dificultad, estación, tema, fechas).
- Habilitar/deshabilitar las dificultades `intermedio` y `avanzado` desde el panel, persistiendo en `configuracion`.
- **Solo se puede deshabilitar una dificultad si no hay equipos jugando** (`intento.fecha_fin IS NULL`). El panel muestra los intentos activos y bloquea el toggle hasta que terminen.
- Un nivel solo se puede habilitar si **todas** las estaciones tienen cobertura completa de ese nivel: al menos 1 pregunta por tema activo y al menos 4 en total.
- Mostrar un reporte de cobertura estación × nivel con los conteos y marcar en rojo lo que falta.
- Validar el **máximo de 4 temas por estación**.
- Borrado **lógico** (`activo = 0`) en `estacion`, `tema`, `pregunta` y `respuesta`; los listados permiten filtrar activos e inactivos.
- Bloquear el borrado de `equipo`, `intento`, `respuesta_elegida` e `incorrecta`: son históricos.
- Cambiar la respuesta correcta de una pregunta no debe alterar intentos ya finalizados.

## Reglas de puntaje y ranking

Según `docs/escape-room.md`, el ranking se ordena por:

1. **Menor tiempo total** para completar las 5 estaciones.
2. A igual tiempo, **menor cantidad de respuestas incorrectas**.
3. A igual tiempo e incorrectas, **menor cantidad de ayudas**.
4. A igualdad de todo lo anterior, el intento que **comenzó antes** (`fecha_inicio`).
5. Desempate final estable por `id` ascendente.

Query de referencia (solo intentos completados):

```sql
SELECT i.id, e.nombre,
       TIMESTAMPDIFF(SECOND, i.fecha_inicio, i.fecha_fin) AS segundos,
       (SELECT COUNT(*) FROM incorrecta inc WHERE inc.intento_id = i.id)
         AS incorrectas,
       i.cantidad_ayudas,
       i.fecha_inicio
FROM intento i
JOIN equipo e ON e.id = i.equipo_id
WHERE i.finalizado = 'completo'
ORDER BY segundos ASC,
         incorrectas ASC,
         i.cantidad_ayudas ASC,
         i.fecha_inicio ASC,
         i.id ASC
```

- `puntaje_obtenido` guarda los **segundos totales** del intento completado (`TIMESTAMPDIFF(SECOND, fecha_inicio, fecha_fin)`). Para intentos no completados queda `NULL`.
- El ranking se ordena por tiempo, incorrectas y ayudas, **no** por `puntaje_obtenido`.
- **La competencia es por nivel.** `posicion` es la posición general entre todos los niveles y `posicion_nivel` la posición dentro de `intento.dificultad`. Ambas usan el mismo orden y se calculan con `ROW_NUMBER() OVER (PARTITION BY dificultad ...)` para la de nivel. No se comparan tiempos de `inicial`, `intermedio` y `avanzado` para definir el ganador de un nivel.
- Al mostrar un equipo que repitió intentos, indicar al lado el número de intento. Se cuenta sobre todos los intentos del equipo, incluidos los no completados.
- Los filtros del ranking completo se resuelven en el servidor con parámetros GET; no cambian la posición general ni la de nivel de cada fila.
- No usar el orden del prototipo `ranking-puntajes.html` (puntos descendente y luego tiempo). Ese prototipo era una demostración con carga manual de puntos.

## Temporizadores

- El contador general se calcula como `ahora - intento.fecha_inicio` y solo aumenta.
- El contador de estación parte de 4:00 y baja hasta 0:00. La duración global vive en `configuracion.duracion_estacion_segundos`; no debe cambiarse mientras haya equipos jugando.
- Los dos contadores se calculan en `app/servicios/tiempos.py` con `TIMESTAMPDIFF(SECOND, ...)` desde las fechas de MySQL. El navegador solo dibuja la cuenta entre sincronizaciones.
- `GET /juego/estado` devuelve los contadores en JSON y el JS lo consulta cada 10 segundos y al volver a la pestaña. Normalmente es de solo lectura; si el tiempo ya se agotó, cierra el intento y devuelve una redirección.
- El tiempo agotado se valida en **cada** request de juego, incluidos los POST, con el reloj del servidor. El reloj del navegador no es fuente de verdad.
- Al llegar a 30 segundos restantes: audio + texto titilante visible. El aviso visual funciona aunque el audio esté bloqueado.
- Al llegar a 0: el intento pasa a `finalizado = 'por_tiempo'`, `fecha_fin` se escribe con la hora del servidor, `puntaje_obtenido` queda `NULL` y no puede continuar.
- El tiempo debe sobrevivir a recargas de página. Persistir `intento_estacion.fecha_inicio` y recalcular desde el servidor.
- Al reanudar, retomar desde `intento.ultima_estacion_visitada`.
- La transición muestra los contadores con el tiempo de estación congelado al completarla; el contador general sigue subiendo hasta completar la quinta. Al completar la quinta estación, el tiempo total queda congelado en `intento.fecha_fin` y la transición y la pantalla final no suman tiempo.
- El audio puede estar bloqueado por el navegador hasta que haya una interacción del usuario. Se desbloquea con la primera interacción dentro de la estación y se mantiene siempre la advertencia visual.
- Usar archivos locales de Bootstrap y audio: la feria puede no tener Internet confiable.

## Decisiones registradas

Estas decisiones interpretan puntos que el documento no cierra del todo. Si el equipo las redefine, actualizar esta sección y el código.

1. **Eliminación por respuestas incorrectas:** se acumulan las respuestas incorrectas del intento dentro de la estación; al llegar a **2** el intento pasa a `finalizado = 'por_respuestas_incorrectas'`. Además hay un máximo de **2 envíos** del formulario por estación: si el segundo envío no tiene todo correcto, solo queda el botón de finalizar. Un mismo envío con 2 o más incorrectas elimina de inmediato. 
2. **Ranking:** participa únicamente `finalizado = 'completo'`.
3. **Puntaje:** `puntaje_obtenido` = segundos totales del intento completado; `NULL` en el resto.
4. **Selección de preguntas:** siempre 4, del nivel del intento. Se elige al menos 1 por tema y se completa al azar; con más de 4 temas se sortean 4 temas y 1 pregunta de cada uno. Se persiste en `intento_pregunta`.
5. **Dificultades:** `inicial` siempre habilitada. `intermedio` y `avanzado` solo se habilitan si todas las estaciones tienen cobertura de ese nivel y solo se deshabilitan si no hay equipos jugando.
6. **Admin:** un único usuario configurado por variables de entorno.
7. **Gráficos:** barras CSS generadas en el servidor, sin Chart.js ni CDN. Bootstrap y el audio quedan locales en `static/`.
8. **`se_completo_ok`:** derivado de `finalizado`; no se edita a mano.
9. **Cantidad de integrantes:** se pide en la bienvenida, es obligatoria y va de 1 a 4.
10. **Borrado:** lógico (`activo`) en el contenido; bloqueado en los históricos.
11. **Estadísticas públicas:** agregados sin nombres de equipos, sin detalle por pregunta y sin respuestas correctas.
12. **Dificultad del intento:** queda guardada en `intento.dificultad` y no cambia durante el intento.
13. **Máximo de temas:** 4 por estación.
14. **Regla de contenido:** se usa "al menos 1 pregunta por tema activo y 4 por estación", no la lectura literal de "mínimo 4 preguntas por tema" de `docs/escape-room.md`. El contenido actual cumple esta regla con 14 temas y 80 preguntas: 20 `inicial` (4 por estación) y 30 `intermedio` y 30 `avanzado` (6 por estación en esos niveles).
15. **Ayudas:** la app **no muestra pistas**. Por estación y por intento se pueden registrar hasta 2 ayudas con los botones **Ayuda 1** y **Ayuda 2**; cada una suma en `intento_estacion.ayudas` y en `intento.cantidad_ayudas`. Al llegar a 2 se deshabilitan. Las pistas las leen los estudiantes desde `docs/ESCAPE ROOM.pdf` o desde `docs/pistas-del-juego.md`.
16. **Identidad del equipo:** `equipo.nombre` es único. Si el nombre ya existe, la bienvenida pide el ID del equipo y no crea uno nuevo. El ID se muestra siempre. Cada reingreso crea un intento nuevo, salvo que el equipo tenga un intento activo (`fecha_fin IS NULL`), en cuyo caso se reanuda. Si dos equipos distintos quieren el mismo nombre, deben usar un sufijo.
17. **Datos al reingresar:** cuando un equipo existente vuelve a ingresar, `equipo.cantidad_personas` **no se actualiza**: se conserva el valor original. La cantidad del formulario solo se usa al crear el equipo. Los datos pendientes de identificación (nombre normalizado, cantidad y dificultad) se guardan temporalmente en la sesión hasta confirmar el ID; la sesión de juego guarda solo `equipo_id` e `intento_id` y el servidor vuelve a leer la base en cada request. Un ID incorrecto se rechaza sin revelar el nombre ni otros datos del equipo.
18. **Intento activo y dificultad:** si el equipo tiene un intento activo, se reanuda con la dificultad de ese intento y se ignora la elegida en el formulario. Si no lo tiene, el nuevo intento usa la dificultad pendiente y se revalida que siga habilitada antes de crearlo. `GET /` con un intento activo en la sesión muestra el formulario y un aviso con **Continuar**, sin redirección automática. Los POST inválidos vuelven a mostrar el formulario con estado `400` y errores inline, sin crear ni modificar datos.
19. **Entrada a estación:** `intento_estacion` y `intento_pregunta` se crean en una sola transacción, bloqueando la fila del intento con `FOR UPDATE`. Si la estación ya tiene su fila, se reutiliza y nunca se reinicia `fecha_inicio`; si la selección ya tiene 4 filas, se usa tal cual.
20. **Orden de preguntas:** el orden de las 4 preguntas se sortea una vez y se persiste en `intento_pregunta.orden`; no se recalcula al recargar.
21. **Cobertura insuficiente:** si falta al menos una pregunta por tema activo o no hay 4 del nivel, la estación responde `503` con `estacion_no_disponible.html` y no crea filas parciales. Una selección parcial ya guardada se trata como error y tampoco se completa automáticamente.
22. **Navegación de estaciones:** `GET /juego` redirige a la estación actual; `GET /juego/estacion/<orden>` valida la estación activa y el rango 1–5. Cualquier orden distinta de la actual redirige a la estación actual; un orden fuera de rango devuelve `404`. La selección congelada se muestra aunque el contenido se desactive después.
23. **Envío de respuestas:** se exige exactamente una opción por cada una de las 4 preguntas congeladas y que cada respuesta pertenezca a su pregunta. En una transacción con bloqueo de intento y estación se crea `intento_envio`, se guardan las 4 filas de `respuesta_elegida` y solo las falladas en `incorrecta`. Un envío inválido no crea ninguna fila.
24. **Orden de evaluación del envío:** primero todo correcto (estación completada), después incorrectas acumuladas en la estación (eliminación), después fin de envíos (modo “solo finalizar”) y si no, se vuelve a mostrar el formulario.
25. **Modo “solo finalizar”:** con `envios >= max_envios_estacion` y la estación sin completar, se ocultan el formulario, las ayudas y el abandono. Solo queda el botón **Finalizar juego**, que cierra el intento como `por_respuestas_incorrectas`.
26. **Ayudas:** se permiten mientras queden ayudas, la estación no esté completada y no se haya llegado al máximo de envíos. Cada ayuda suma en `intento_estacion.ayudas` e `intento.cantidad_ayudas` en una transacción. La app no muestra el texto de la pista.
27. **Abandono y eliminación:** ambos cierran `intento.fecha_fin`, `intento.finalizado` y también `intento_estacion.fecha_fin` si estaba abierta. `puntaje_obtenido` queda `NULL`. En el `paso04` el abandono se toma solamente desde la estación; la transición completa llega en el `paso06`.
28. **Doble envío:** se usa POST + redirección (PRG) y se deshabilita el botón al enviar. No hay token de idempotencia: dos POST simultáneos pueden registrarse como dos envíos.
29. **Respuestas desactivadas:** al enviar se acepta cualquier respuesta que pertenezca a una de las preguntas congeladas, aunque `respuesta.activo = 0` después de la selección. Así la partida no queda trabada por cambios de contenido.
30. **Transición y eliminación mínimas:** en el `paso04` existen `GET /juego/transicion/<orden>` y `GET /juego/eliminado` en versión mínima. La transición no tiene botón **Continuar**; el recorrido completo y las pantallas definitivas llegan en el `paso06`.
31. **Ruta `/juego/estado`:** es una ruta nueva respecto de `docs/navegacion-por-app.md`, documentada en `MEMORY.md`. Devuelve JSON de solo lectura con los contadores y la hora del servidor. Si el tiempo de la estación ya se agotó, puede cerrar el intento como `por_tiempo` y devolver `redirigir` a `/juego/eliminado`; en el resto de los casos no modifica datos.
32. **Contadores en la transición:** se muestran también en `GET /juego/transicion/<orden>`. El contador general sigue subiendo; el de la estación queda congelado en `intento_estacion.fecha_fin` para que se vea el tiempo que tardó la estación completada.
33. **Desbloqueo del audio:** se intenta con la primera interacción dentro de la estación (`pointerdown` o `keydown`). Si el navegador lo bloquea, el texto titilante de los 30 segundos se muestra igual.
34. **Precisión de segundos:** los contadores usan segundos enteros con `TIMESTAMPDIFF(SECOND, ...)`. El cierre por tiempo puede ocurrir hasta un segundo después del límite teórico. La duración es global y no debe modificarse mientras haya intentos activos.
35. **Actualización de `ultima_estacion_visitada`:** se actualiza al entrar a la estación siguiente después de presionar **Continuar**, no al completar la estación anterior. Completar una estación deja el valor en esa estación para que la transición siga siendo accesible.
36. **Continuar idempotente:** `POST /juego/transicion/<orden>/continuar` valida que la estación esté completada y prepara la siguiente en una transacción. La creación de `intento_estacion`, la selección de preguntas y la actualización de `ultima_estacion_visitada` no se duplican si se repite el POST.
37. **Abandono desde la transición:** las estaciones 1 a 4 ofrecen **Abandonar** con confirmación. La quinta ya finalizó el intento como `completo`, así que solo muestra **Ver resultado**.
38. **Final y eliminación:** `/juego/final` solo acepta intentos con `finalizado = 'completo'`; con un intento activo redirige a la estación actual y con uno no completado redirige a `/juego/eliminado`. `/juego/eliminado` redirige al final si el intento está completo.
39. **Pantalla final:** muestra el resultado del intento, el top 10 del nivel del intento y, en una card aparte, el ranking completo con posiciones general y de nivel, columna **Nivel** y filtros por nombre de equipo, número de intento, fecha de fin y nivel. La fecha se muestra como `dd/mm/aaaa HH:MM`. Los filtros se aplican solo al ranking completo y no alteran ninguna posición. El KPI principal usa `posicion_nivel` y muestra la posición general como dato secundario.
40. **Cierre de la quinta estación:** al registrar las 4 respuestas correctas de la última estación activa, el intento pasa a `finalizado = 'completo'`, `fecha_fin` es la misma que la de `intento_estacion` y `puntaje_obtenido` se calcula con esa fecha. Así el puntaje no incluye la transición ni la pantalla final.
41. **Ranking público:** `GET /ranking` renderiza en el servidor una tabla por nivel como respaldo y `GET /ranking/datos` devuelve `{actualizado, niveles: [{valor, etiqueta, filas}]}` para el polling. Solo incluye `finalizado = 'completo'`, usa el mismo orden y el mismo número de intento que `app/servicios/ranking.py`, y no expone `equipo_id` ni `intento_id`. Dentro de cada nivel, `posicion` es la posición de nivel. El JSON se sirve con `Cache-Control: no-store`.
42. **Polling del televisor:** `static/js/ranking.js` consulta `/ranking/datos` cada 8 segundos y al volver a la pestaña. Recorre las secciones `data-nivel`, reemplaza las filas con `textContent` (nunca `innerHTML` con el nombre del equipo), actualiza la hora del servidor y, si falla la consulta, conserva todas las tablas y muestra **Reconectando…**. Sin WebSockets y sin borrar datos ante un error.
43. **Estadísticas públicas:** `GET /estadisticas` calcula todo en `app/servicios/estadisticas.py` con agregados de `equipo`, `intento`, `respuesta_elegida` e `intento_envio`. Los aciertos salen de `intento_envio.respuestas_correctas`, que guarda el resultado del envío en ese momento, para que cambiar después una respuesta correcta no altere el historial. Las barras por estado incluyen **En curso** (`finalizado IS NULL`) y se generan con CSS en el servidor. No se muestran nombres, detalle por pregunta ni la palabra “correcta”: la etiqueta es **Aciertos**.
44. **Rutas públicas exactas:** los blueprints `ranking` y `estadisticas` se registran sin `url_prefix` y declaran `/ranking`, `/ranking/datos` y `/estadisticas` sin barra final. La bienvenida enlaza a ranking y estadísticas, el final a estadísticas y la eliminación a ranking.
45. **Fecha de actualización:** las vistas públicas muestran la hora del servidor MySQL con `DATE_FORMAT(NOW(), ...)`, no el reloj del navegador.
46. **Sesión del admin:** el panel usa solo `session["admin_autenticado"]` y no toca `equipo_id` ni `intento_id` de la partida. El login valida `ADMIN_USER` y `ADMIN_PASSWORD_HASH` con `check_password_hash`; un error devuelve `401` con un mensaje genérico. El logout es `POST /admin/logout` y elimina únicamente `admin_autenticado`. Las cookies de sesión se configuran `HttpOnly`, `SameSite=Lax` y sin `Secure` para el aula sin HTTPS. El rate limiting sigue pendiente; el CSRF se resolvió en el `paso11` (decisión 57).
47. **Rutas del admin:** el blueprint `admin` se registra sin `url_prefix` y declara `/admin`, `/admin/login`, `/admin/logout`, `/admin/`, `/admin/<tabla>`, `/admin/<tabla>/nuevo`, `/admin/<tabla>/<fila_id>`, `/admin/<tabla>/<fila_id>/editar`, `/admin/<tabla>/<fila_id>/desactivar`, `/admin/cobertura`, `/admin/dificultades` (GET y POST), `/admin/intentos-activos` y `/admin/estadisticas`. Todas salvo el login exigen sesión. Las rutas estáticas se resuelven antes que `/admin/<tabla>`. El panel muestra cards de las 12 tablas, el estado del juego y accesos a cobertura, dificultades, intentos activos y estadísticas.
48. **Edición del contenido:** las tablas históricas (`equipo`, `intento`, `intento_estacion`, `intento_envio`, `intento_pregunta`, `respuesta_elegida`, `incorrecta`) son de solo lectura: sus rutas de alta, edición y baja devuelven `404`. En el contenido, la baja es lógica. Una pregunta nueva se guarda inactiva y solo se activa con al menos 2 respuestas activas y exactamente 1 correcta. Marcar una respuesta como correcta desmarca las demás de esa pregunta.
49. **Bloqueos por intentos activos:** con un intento `fecha_fin IS NULL` no se crean estaciones, no se cambia su `orden` ni su `activo`, no se editan los parámetros del juego y no se agregan respuestas ni se cambia `correcta`/`activo` de respuestas de preguntas seleccionadas en ese intento. Tampoco se mueve contenido ya usado entre `pregunta.tema_id`, `tema.estacion_id` o `respuesta.pregunta_id`.
50. **Orden de estaciones:** los órdenes son únicos entre 1 y 5. Al editar una estación hacia un orden ocupado se intercambian ambas en la misma transacción. Siempre debe quedar al menos una estación activa con `orden = 1`. Con los 5 órdenes ocupados no se puede crear otra estación hasta liberar uno.
51. **Configuración desde el admin:** `dificultad_intermedia_habilitada`, `dificultad_avanzada_habilitada`, `preguntas_por_estacion` y `max_temas_por_estacion` no se editan desde el CRUD de configuración; las dificultades se administran en `/admin/dificultades`. Los parámetros del juego se validan por rango y se bloquean con intentos activos. La `clave` de una fila es inmutable.
52. **Filtros del admin:** los filtros, el orden y la paginación se resuelven en el servidor. Los valores inválidos caen a los predeterminados; el `ORDER BY` sale siempre de una lista blanca de `app/servicios/admin_tablas.py`. El buscador escapa `%`, `_` y `\` para `LIKE`.
53. **Cobertura de niveles:** se calcula en `app/servicios/cobertura.py` con una única función reutilizada por el reporte y por los toggles. Solo cuenta estaciones, temas y preguntas activas. Cada tema activo necesita al menos 1 pregunta activa del nivel y cada estación al menos `preguntas_por_estacion` (4, leído de `configuracion` con respaldo 4). Sin estaciones activas el nivel no está completo. `inicial` se reporta pero nunca se habilita ni deshabilita desde la app.
54. **Toggles de dificultad:** `POST /admin/dificultades` valida en el servidor aunque el cliente mande el formulario directamente. Los cambios se aplican en una transacción con `FOR UPDATE` y solo sobre transiciones reales. Con un intento activo (`fecha_fin IS NULL`) se bloquean todos los cambios, tanto habilitar como deshabilitar. Habilitar exige cobertura completa del nivel; deshabilitar no exige cobertura. `inicial` y claves desconocidas se rechazan; se persiste `'1'` o `'0'` en `configuracion`. Ante un error, el formulario se vuelve a mostrar con el estado persistido y los errores inline, con `400`.
55. **Estadísticas del admin:** `GET /admin/estadisticas` calcula todo en `app/servicios/admin_estadisticas.py`, con filtros `desde`, `hasta` y `dificultad` sobre `intento.fecha_inicio` e `intento.dificultad`. Si `desde > hasta` se avisa y se muestra un rango vacío, sin intercambiar fechas. El tiempo promedio por estación usa solo `intento_estacion.completada = 1` con `fecha_fin` no nula. La utilización de preguntas incluye las activas con 0 usos y las inactivas que ya se usaron, marcadas como inactivas; se calcula sobre los intentos filtrados. El gráfico de intentos incluye **En curso** y los finalizados se muestran en un KPI aparte. Las barras son CSS generadas en el servidor, sin Chart.js ni CDN.
56. **Intentos activos y navegación:** `GET /admin/intentos-activos` lista equipo, intento, dificultad, estación actual, tiempo transcurrido y última actividad, y muestra el motivo del bloqueo de los toggles. El panel y `admin/_nav.html` enlazan a cobertura, dificultades, intentos activos y estadísticas. Las cuatro rutas nuevas exigen login y no se enlazan desde páginas públicas.
57. **CSRF propio, sin dependencias:** `app/csrf.py` genera un token estable por sesión con `secrets.token_urlsafe(32)` y lo valida con `hmac.compare_digest`. Un `before_request` rechaza con `400` y la plantilla `400.html` cualquier POST sin token o con uno inválido. La validación corre antes de `login_requerido`, así un POST al login sin token también devuelve `400`. Todos los formularios POST incluyen `_csrf_campo.html`; el token se rota al iniciar y al cerrar la sesión de administración. `GET /juego/estado` queda excluido porque el polling no envía formularios, aunque pueda cerrar el intento por tiempo.
58. **Suite de pruebas:** `pytest.ini` fija `testpaths = tests` y `pythonpath = .`. `tests/conftest.py` elimina y recrea la base de test al inicio de la sesión, exige que el nombre termine en `_test` y sea distinto de `MYSQL_DB`, carga `bd/schema.sql` y los tres seeds, y antes y después de cada test limpia las tablas en orden inverso a las claves foráneas y vuelve a sembrar. La base real nunca se toca. Las credenciales de admin y `SECRET_KEY` de test se generan en runtime. `tests/helpers.py` centraliza el token CSRF, los POST, los datos de juego y el reenvío de los seeds.
59. **Ranking por nivel:** `posicion` es la posición general y `posicion_nivel` la del nivel del intento, calculada con `PARTITION BY dificultad`. Ambas usan el mismo orden (tiempo, incorrectas, ayudas, `fecha_inicio`, `id`). La pantalla final muestra la posición de nivel como principal, el top 10 del nivel y el ranking completo con columna **Nivel** y filtro por nivel. La vista pública muestra una tabla por nivel: `inicial` siempre, y los demás si están habilitados en `configuracion` o si ya tienen intentos completados. Los niveles sin filas muestran su mensaje de vacío. Esta decisión amplía las 39, 41 y 42 sin reemplazarlas.
60. **Docker post-feria:** queda como taller educativo opcional en el `paso13`, después del 16/11. No reemplaza waitress/systemd del `paso12`, no se agrega a `requirements.txt` ni se usa en la feria. La base del taller es independiente de la base real y los seeds se cargan solo al crear el volumen. Cualquier cambio de alcance requiere consultar.
61. **Descripciones de preguntas:** `pregunta.descripcion` es una mini ayuda de contexto que se muestra debajo del enunciado en `app/templates/estacion.html`. Se completa en los niveles `intermedio` y `avanzado`; las 20 preguntas de `inicial` quedan en `NULL` para que ese nivel se juegue sin ayuda extra. No es una pista y no debe nombrar ni parafrasear la respuesta correcta. Los textos viven en los seeds `002` y `003`, no llevan punto y coma porque el cargador de seeds de las pruebas separa las sentencias con ese signo, y reejecutar los seeds pisa lo editado desde `/admin`, igual que el título.

## Convenciones de código

- UI y textos en **español rioplatense**, consistentes con el prototipo ("Ingresá", "Respondé", "Superá").
- Nombres de dominio en español (`equipo`, `intento`, `estacion`, `pregunta`, `respuesta`); nombres técnicos pueden ir en inglés.
- Rutas Flask con blueprints y app factory.
- SQL siempre parametrizado. Nunca interpolar datos del usuario.
- Transacciones para registrar un intento, envíos, respuestas y ayudas.
- Configuración por variables de entorno; incluir `.env.example` y nunca commitear credenciales.
- Bootstrap y JS local en `static/`; no depender de CDN para el funcionamiento en el aula.
- Preguntas, opciones y respuestas correctas deben vivir en la base de datos y cargarse con seeds idempotentes (`bd/seeds/001_contenido_inicial.sql`, `002_contenido_intermedio.sql` y `003_contenido_avanzado.sql`). No duplicarlas en plantillas ni en varios archivos JS. Las pistas no se guardan en la base: están en `docs/pistas-del-juego.md` y en el PDF, y las leen los estudiantes.
- Las preguntas del prototipo, de `docs/ESCAPE ROOM.pdf` y de `docs/banco-preguntas-intermedio-avanzado.md` son la fuente de contenido; unificar diferencias antes de cargarlas.
- No agregar autenticación de participantes ni registro público. El único login es el de administración.
- La regla de **máximo 3 equipos simultáneos** y el ingreso de un nuevo equipo cuando otro llega a la estación 3 es operativa. No imponerla en el software sin confirmación.
- La página de estadísticas pública es de solo lectura; no expone respuestas correctas ni datos personales.
- Código simple, nombres descriptivos y comentarios solo donde aporten.
- Diseño limpio y responsive; cualquier pantalla nueva debe verse bien en el móvil.

## Comandos

```bash
mysql -u <usuario> -p < bd/schema.sql
mysql -u <usuario> -p < bd/seeds/001_contenido_inicial.sql
mysql -u <usuario> -p < bd/seeds/002_contenido_intermedio.sql
mysql -u <usuario> -p < bd/seeds/003_contenido_avanzado.sql

# Alternativa: estructura y contenido de una sola vez.
# Elimina y vuelve a crear las 12 tablas: hacer backup si la base ya se usó.
mysql -u <usuario> -p < bd/escape_room_7b2026_completa.sql

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
flask --app app run --debug
pytest -q
pytest -q
```

`pytest` usa la base `escape_room_7b2026_test` (o `TEST_MYSQL_DB`) y la recrea al iniciar la sesión. El usuario de MySQL necesita permisos `CREATE` y `DROP`. Ver `README.md` para el detalle.

No inventar comandos de arranque ni dependencias que no estén implementadas.

## Pruebas y verificación

Priorizar pruebas automatizadas para:

- Avance solo con las 4 respuestas correctas.
- Eliminación por 2 respuestas incorrectas.
- Eliminación por tiempo agotado.
- Eliminación por abandono.
- Orden del ranking: tiempo ascendente; en empate, menos incorrectas; luego menos ayudas; luego el intento que empezó antes; luego `id`.
- Exclusión de intentos no completados (`abandono`, `por_respuestas_incorrectas`, `por_tiempo`).
- Cierre de la quinta estación con `finalizado = 'completo'`, `puntaje_obtenido` igual a los segundos totales y tiempo congelado.
- Filtros del ranking completo por equipo, número de intento, fecha de fin y nivel sin alterar la posición general ni la de nivel.
- Posición general y posición por nivel: un intento de `intermedio` puede ser `#1` de su nivel aunque su tiempo sea mayor que el de un intento de `inicial`.
- Top 10 del final limitado al nivel del intento.
- Niveles visibles en `/ranking`: `inicial` siempre; los demás si están habilitados o tienen intentos completados; un nivel sin filas muestra su mensaje.
- Filtrado de preguntas por dificultad y por tema.
- Descripciones: 30 de `intermedio` y 30 de `avanzado` visibles en la estación; las 20 de `inicial` sin descripción.
- Bienvenida con cantidad de integrantes entre 1 y 4.
- Reingreso con un nombre de equipo existente: pide el ID y no duplica el equipo.
- Ayudas: máximo 2 por estación e intento, con contador visible y botones deshabilitados al llegar a 2.
- La app no muestra ni envía el texto de las pistas.
- Selección de 4 preguntas con al menos una por tema y 4 en total.
- Con más de 4 temas, se usan 4 temas al azar y una pregunta de cada uno.
- Nivel no habilitable si falta cobertura en alguna estación o tema.
- Cobertura estación × nivel: tema sin preguntas del nivel y estación con menos de 4 se marcan en rojo; `inicial` aparece siempre habilitada.
- Toggle de dificultad bloqueado mientras hay intentos activos, tanto para habilitar como para deshabilitar.
- POST directo para habilitar un nivel sin cobertura rechazado con `400` y sin cambios en `configuracion`.
- Estadísticas del admin con filtros por fecha y dificultad, rango invertido sin datos y barras generadas en el servidor.
- Panel `/admin` sin Chart.js ni referencias a CDN.
- Borrado lógico de contenido sin romper intentos históricos.
- Estadísticas públicas sin nombres de equipos ni respuestas correctas.
- `/ranking/datos` devuelve solo intentos completados, agrupados por nivel, en el orden del ranking y sin `equipo_id`.
- `/estadisticas` no expone nombres de equipos, `respuesta_id`, `equipo_id` ni la palabra “correcta”.
- La tabla de `/ranking` se conserva y muestra **Reconectando…** cuando falla el polling.
- Selección aleatoria estable tras recargar (mismas 4 preguntas del intento).
- Registro de todas las respuestas elegidas y de las incorrectas en `incorrecta`.
- Conteo de envíos del formulario y bloqueo al segundo envío.
- Recarga de página sin reiniciar tiempos.
- Reanudación desde `ultima_estacion_visitada`.
- Ausencia de respuestas correctas en el HTML/JS enviado al cliente.
- `/admin` inaccesible sin login y no enlazado desde páginas públicas.
- Habilitar/deshabilitar dificultades, su efecto en la bienvenida y el bloqueo con intentos activos.
- Cálculo de estadísticas y gráficos.
- Seed idempotente: ejecutarlo dos veces no duplica datos.

Verificación manual antes de entregar:

- Bienvenida con nombre, cantidad de integrantes (1–4) y dificultad, mostrando solo dificultades habilitadas.
- Las 5 estaciones se recorren en orden.
- HUD con ayudas, incorrectas y envíos.
- Contador general sube y contador de estación baja.
- Aviso visual y sonoro a los 30 segundos.
- Pantalla de eliminación y pantalla final.
- Final con top 10 del nivel, posición general y de nivel, tiempo total y ranking completo filtrable por equipo, número de intento, fecha de fin y nivel.
- Ranking visible y actualizado en la vista de TV.
- Página pública de estadísticas.
- Panel `/admin` con login, CRUD, filtros, orden y gráficos.
- Funcionamiento sin conexión a Internet.

## Qué no hacer

- No modificar ni eliminar `docs/`, sus PDF ni los prototipos.
- No presentar `docs/src/index.html` como la aplicación final ni copiar su lógica de respuestas en el cliente.
- No reutilizar `basededatos.py`, `basededatos_contador.db` ni `contador.php`; el stack es Flask + MySQL.
- No ordenar el ranking por puntos como en el prototipo de ranking.
- No ordenar el ranking público por `puntaje_obtenido`: se ordena por tiempo, incorrectas, ayudas, `fecha_inicio` e `id`.
- No comparar tiempos de niveles distintos para la posición competitiva: la competencia se resuelve con `posicion_nivel`.
- No borrar la tabla del ranking ni reemplazarla por un estado vacío cuando falla el polling.
- No enlazar `/admin` desde la interfaz pública ni dejar sus rutas sin autenticación.
- No aleatorizar preguntas sin persistir la selección por intento.
- No borrar físicamente contenido ni filas históricas desde el CRUD; usar borrado lógico o bloquear.
- No habilitar un nivel sin cobertura completa en todas las estaciones.
- No deshabilitar una dificultad mientras haya equipos jugando.
- No mostrar nombres de equipos, detalle por pregunta ni respuestas correctas en la página pública de estadísticas.
- No introducir React/Vue, ORM pesado ni otra infraestructura sin necesidad y sin consultar. Docker queda fuera del camino de la feria: el taller post-feria está documentado en el `paso13` y requiere consultar antes de implementarlo.
- No usar CDN para Bootstrap, gráficos ni audio.
- No hardcodear preguntas, respuestas, credenciales ni tiempos en múltiples lugares.
- No commitear `.env`, volcados de base de datos ni archivos generados.
- No mostrar ni cargar pistas en la aplicación: solo se registran las ayudas.
- No permitir dos equipos con el mismo nombre ni crear un equipo nuevo cuando la bienvenida pide el ID.

## Forma de trabajar

- Haz solo lo que se pide: no añadas funcionalidades por tu cuenta.
- Cambios pequeños y enfocados; no reescribas lo que ya funciona.
- Al terminar, resume qué has cambiado y cualquier decisión que deba revisar.

## Límites

- Siempre: respetar las reglas y mantener los textos en español.
- Pregunta antes: crear archivos nuevos, cambiar el formato de los datos guardados.
- Nunca: añadir dependencias, frameworks  o un paso de build que no haya establecido.
