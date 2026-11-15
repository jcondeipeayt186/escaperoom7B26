# Cómo se hizo el proyecto

Este documento cuenta el proceso de trabajo del **Escape Room 7.º B 2026** del
IPEATyM 186 Castagnari: de dónde salió la idea, cómo se convirtieron las reglas
en requisitos, qué reglas permanentes se usaron y cómo se construyó la
aplicación paso a paso con ayuda de un agente de IA.

No es un manual de uso. Para jugar o instalar la app ver `README.md` y
`docs/guia-de-estudio-para-estudiantes.md`. Para el contenido de estudio, ver
`docs/material-de-estudio-y-control.md`.

## 1. Punto de partida

El proyecto arrancó con material disperso:

- Un documento con la idea del juego, algunas reglas y los formularios del
  nivel inicial.
- Una página que mostraba el ranking de los equipos.
- Un prototipo visual de una sola página en `docs/src/index.html`, con un
  formulario por estación.

Ese material alcanzaba para explicar la idea, pero no para programarla: había
reglas ambiguas, no existía un modelo de datos y el prototipo resolvía las
respuestas en el navegador, algo que no sirve para una competencia real.

Las piezas originales quedaron como **referencia** en `docs/src/` y en
`docs/ESCAPE ROOM.pdf`. No se copiaron a la aplicación: el prototipo no tiene
una página por estación, no maneja tiempos, no persiste nada y no distingue
dificultades.

## 2. De la idea a los requisitos

El primer trabajo fue **sacar las ambigüedades**. Se escribió
`docs/escape-room.md`, que reúne en un solo lugar:

- Las reglas del juego: equipos de hasta 4 integrantes, 5 estaciones en orden,
  4 preguntas por estación, 4 minutos por estación, 2 respuestas incorrectas
  eliminan, abandono y tiempo agotado.
- El orden exacto del ranking: tiempo, incorrectas, ayudas, `fecha_inicio` e
  `id`.
- El stack: Python + Flask, MySQL, HTML con Jinja y Bootstrap, sin SPA.
- El modelo de datos y las tablas de detalle que el modelo base no cubría
  (`intento_estacion`, `intento_envio`, `intento_pregunta`, `configuracion`).
- El recorrido de pantallas y las rutas de la aplicación.
- El alcance de la administración, las estadísticas públicas y el ranking para
  el televisor.

Ese documento es la **fuente de verdad**: si otro archivo o el prototipo lo
contradicen, manda `docs/escape-room.md`. Alrededor se sumaron documentos de
apoyo: `docs/navegacion-por-app.md` (pantallas y rutas),
`sql/descripcion-de-la-base-de-datos.md` (tablas y columnas),
`docs/tecnologias.md` (stack explicado) y los documentos de instalación.

## 3. Las reglas permanentes: `AGENTS.md` y `MEMORY.md`

Con los requisitos claros faltaba algo que evitara que cada pedido se resolviera
de una manera distinta. Para eso se crearon dos archivos que se usan juntos:

| Archivo | Qué guarda | Cuándo se lee |
| --- | --- | --- |
| `AGENTS.md` | Las reglas estables: fuente de verdad, stack, modelo de datos, flujo, decisiones registradas, pruebas y “qué no hacer”. | Antes de cada pedido, siempre. |
| `MEMORY.md` | El estado real del proyecto: qué está hecho, cómo se verificó, qué quedó pendiente y cuál es el próximo paso. | Al empezar una sesión nueva y al terminarla. |

La interacción es simple:

1. `AGENTS.md` dice **cómo** se trabaja. No cambia con cada paso; solo cuando
   se toma una decisión nueva que hay que registrar.
2. `MEMORY.md` dice **dónde estamos parados**. Se actualiza al terminar cada
   paso con lo que realmente se hizo y verificó.
3. Si un pedido choca con `AGENTS.md`, no se avanza: se consulta y, si se
   redefine, se actualiza la decisión en el mismo archivo.

Las **decisiones registradas** de `AGENTS.md` son la parte más importante.
Cada una interpreta un punto que el documento de requisitos no cerraba del
todo, por ejemplo:

- Qué pasa cuando el segundo envío del formulario no está todo correcto.
- Cómo se eligen las 4 preguntas cuando la estación tiene más de 4 temas.
- Qué intentos participan del ranking (`finalizado = 'completo'`).
- Cómo se calcula la posición general y la posición por nivel.
- Qué se puede borrar y qué es histórico.
- Cómo se comporta el juego con intentos activos mientras se edita contenido.

Así, una decisión se toma una vez, queda escrita y no se vuelve a discutir en
cada paso.

## 4. El comando `/feature`

Para que los pedidos no empiecen directamente por el código se creó el comando
`/feature`, definido en `.opencode/commands/feature.md`. El comando corre con
el agente **plan** y obliga a responder, antes de tocar nada:

1. Cómo se va a implementar, respetando `AGENTS.md`.
2. Qué archivos se van a modificar y qué cambia en cada uno.
3. Los casos límite y las dudas que tiene que decidir la persona.
4. Qué habría que actualizar en `AGENTS.md` y en `MEMORY.md`.

La última línea es explícita: **no modificar ningún archivo hasta que el plan
esté aprobado**. Eso evita que el agente invente alcance o cambie cosas que
nadie pidió.

## 5. El guion de pasos

Con los requisitos y las reglas listos se pidió al agente que escribiera los
documentos necesarios para llevar el proyecto **desde cero hasta la app
funcionando**. Así nació `docs/argumentos-pasos/`, con un archivo por bloque
verificable:

- `paso00`: verificar la base y el contenido.
- `paso01` a `paso06`: esqueleto Flask, bienvenida, selección de preguntas,
  envío y reglas, temporizadores y recorrido completo.
- `paso07`: prueba manual del MVP con personas.
- `paso08` a `paso10`: ranking público, estadísticas, admin y cobertura.
- `paso11` y variantes (`11b` a `11g`): pruebas, ranking por nivel, contenido
  intermedio y avanzado, descripciones, imágenes, capturas y explicaciones en
  la transición.
- `paso12`: congelamiento y feria con Flask.
- `paso13` y `paso14`: waitress/systemd y Docker, posteriores a la feria.

Cada archivo incluye objetivo, contexto, tareas, criterio de aceptación y el
commit sugerido. La carpeta tiene su propio `README.md` con el índice, los
tipos de paso y el estado de cada uno; se mantiene actualizado a medida que se
avanza.

La lógica es **un paso, un objetivo, un commit**. Si el alcance crece, se para
y se consulta. Un paso no termina porque “compila”: termina cuando el criterio
de aceptación se verificó de verdad, a mano y con SQL.

## 6. El ciclo de trabajo

Cada paso se trabajó en una sesión nueva y siempre con el mismo ciclo:

```text
/feature @docs/argumentos-pasos/pasoNN-....md
        ↓
plan del agente (sin escribir código)
        ↓
revisión del plan y decisión de las dudas
        ↓
aprobación y cambio a modo build
        ↓
implementación + verificación del criterio de aceptación
        ↓
actualización de MEMORY.md (y AGENTS.md si hubo decisión nueva)
        ↓
commit indicado
        ↓
paso siguiente
```

Detalle de cada momento:

1. **Plan.** El comando corre con el agente plan. El agente propone, no
   escribe. Se lee el plan completo.
2. **Revisión.** Se corrigen desvíos, se eligen opciones y se responden las
   dudas que el plan deja abiertas. Muchas de esas respuestas terminaron como
   decisiones registradas en `AGENTS.md`.
3. **Build.** Recién con el plan aprobado se pasa al agente de
   implementación.
4. **Verificación.** No alcanza con que la app arranque: se prueba el flujo
   real, se consulta MySQL y se corre `pytest`. Cuando el paso toca reglas del
   juego, se agregan o ajustan pruebas automatizadas.
5. **Memoria.** `MEMORY.md` se actualiza con lo que se hizo, cómo se verificó
   y qué quedó pendiente. Si cambió una regla, también se actualiza
   `AGENTS.md`.
6. **Commit.** Cada paso deja un commit con el mensaje indicado en su archivo.

Este ciclo se repitió paso a paso, sin saltear el `paso07` (la prueba manual
del MVP) y sin arrancar el admin antes de tener el juego jugable.

## 7. Ajustes menores en build

No todo pasó por `/feature`. Después de probar la aplicación aparecieron
detalles chicos: textos, estilos, un enlace, un formato de hora, una barra que
se veía mal en el televisor. Esos ajustes se hicieron directamente en modo
build, con cambios acotados, y se registraron en `MEMORY.md` cuando cambiaban
el comportamiento visible o una decisión.

La regla que se mantuvo fue siempre la misma: si el cambio es menor y está
claro, se hace y se prueba; si toca reglas del juego, modelo de datos o alcance,
vuelve al ciclo de plan.

## 8. Resultado

El proceso terminó en una aplicación Flask + MySQL con:

- 5 estaciones, 14 temas y 80 preguntas (20 `inicial`, 30 `intermedio` y 30
  `avanzado`), con 3 opciones por pregunta.
- Juego completo con temporizadores, ayudas, envíos, eliminaciones y
  reanudación.
- Ranking público para el televisor, estadísticas públicas y panel de
  administración con cobertura y dificultades.
- 105 pruebas automatizadas.
- Contenido congelado el 14/11/2026 y feria preparada para el 16/11/2026 con
  `./scripts/feria.sh`.

Al cierre se generó también la documentación en PDF (`docs/pdf/`) para que todo
el material quede en un formato cómodo de leer, imprimir y compartir.

## 9. Qué se puede reutilizar de este proceso

- Empezar por los requisitos y las decisiones, no por el código.
- Escribir las reglas permanentes una vez y respetarlas en cada pedido.
- Separar el estado del proyecto (`MEMORY.md`) de las reglas (`AGENTS.md`).
- Trabajar en pasos chicos, verificables y con criterio de aceptación.
- Planificar antes de implementar y aprobar el plan antes de escribir.
- Verificar con pruebas y con la aplicación real, no solo con el código.
- Mantener la documentación sincronizada con lo que existe de verdad.
