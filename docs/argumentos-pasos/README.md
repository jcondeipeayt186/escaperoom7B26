# Guion de pasos

Carpeta de trabajo derivada de `docs/primeros-pasos.md`. Hay un archivo por
bloque verificable, pensado para usarse como argumento del comando
`/feature`.

No reemplaza a las fuentes de verdad:

- `docs/escape-room.md` — requisitos funcionales y contenido.
- `AGENTS.md` — decisiones registradas y modelo de datos.
- `docs/navegacion-por-app.md` — pantallas, rutas y elementos.
- `sql/descripcion-de-la-base-de-datos.md` — tablas y columnas.

Si hay contradicción, manda `docs/escape-room.md` y después `AGENTS.md`.

---

## 1. Cómo se usa

Cada paso se trabaja en una sesión nueva:

1. Lanzar el comando con el archivo del paso:

   ```text
   /feature @docs/argumentos-pasos/paso01-esqueleto-flask.md
   ```

2. Leer el plan que devuelve. El comando corre con el agente `plan`, así que
   **no escribe código**: solo propone.
3. Corregir el plan si hace falta y pasar a un agente de implementación.
4. Verificar el **Criterio de aceptación** del archivo, a mano y con SQL.
5. Actualizar `MEMORY.md` con el estado real.
6. Hacer el commit indicado.
7. Recién ahí pasar al paso siguiente.

Reglas del ciclo:

- Un paso, un objetivo, un commit.
- Si el alcance crece, se para y se consulta.
- Un paso no está terminado porque "compila": está terminado cuando el
  criterio de aceptación se verificó de verdad.
- No se saltea el `paso07` (prueba manual del MVP) para arrancar el admin.

---

## 2. Tipos de paso

| Tipo | Qué significa | ¿Se usa `/feature`? | ¿Escribe código? |
| --- | --- | --- | --- |
| `código` | Implementa una parte de la app: rutas, plantillas, lógica. | Sí, es el uso principal. | Sí. |
| `test` | Agrega pruebas automatizadas y endurecimiento. | Sí. | Sí, pero solo tests y ajustes menores. |
| `infra` | Entorno, base, backup, puesta en marcha. | Opcional: sirve para armar el plan o el checklist. | Poco o nada; puede crear scripts. |
| `manual` | Lo ejecuta una persona: probar el juego con gente real. | **No** para implementar. Solo si querés que prepare el checklist. | No. |

Detalle:

- **código**: el agente planifica y después implementa. El commit es de
  código.
- **test**: igual que código, pero el foco son las reglas críticas y la
  ausencia de fugas de información.
- **infra**: son comandos y verificación. Si lo corrés con `/feature`, el
  agente devuelve un plan de verificación, no una funcionalidad. El `paso00`
  no lleva commit; el `paso12` sí, pero de documentación y scripts.
- **manual**: no se puede delegar. El `paso07` lo hacen dos o tres personas
  jugando. El agente solo puede preparar la planilla de observaciones o
  corregir errores bloqueantes después.

---

## 3. Duplicación con la sección 11

La sección 11 de `docs/primeros-pasos.md` ya tiene los pedidos redactados.
Estos archivos son una copia operativa, ampliada con contexto, verificación y
trampas.

Por qué se duplica:

- La sección 11 es la hoja de ruta legible, con fechas y orden.
- Los `pasoNN.md` son autocontenidos: se pasan como argumento y no dependen
  de que el agente lea media hoja de ruta.

Riesgo: si se edita uno y no el otro, quedan versiones distintas.

Regla de sincronización:

- Para **ejecutar**, manda el `pasoNN.md`.
- Para **replanificar fechas u orden**, manda `docs/primeros-pasos.md`.
- Si cambia el alcance de un pedido, actualizar los dos en el mismo commit.
- Más adelante, si la carpeta queda estable, se puede recortar la sección 11
  a un índice. Eso modifica un documento existente: se consulta antes.

---

## 4. Índice

| Archivo | Tipo | Origen | Requiere | Commit | Estado |
| --- | --- | --- | --- | --- | --- |
| `paso00-verificar-base-y-contenido.md` | infra | Paso 1 | — | sin commit | hecho |
| `paso01-esqueleto-flask.md` | código | Pedido 1 | paso00 | `feat: esqueleto flask y configuración` | hecho |
| `paso02-bienvenida-e-identidad.md` | código | Pedido 2 | paso01 | `feat: bienvenida e identidad de equipo` | hecho |
| `paso03-seleccion-de-preguntas.md` | código | Pedido 3 | paso02 | `feat: selección persistida de preguntas` | hecho |
| `paso04-envio-y-reglas-de-estacion.md` | código | Pedido 4 | paso03 | `feat: envío de respuestas y reglas de la estación` | hecho |
| `paso05-temporizadores-y-reanudacion.md` | código | Pedido 5 | paso04 | `feat: temporizadores y reanudación` | hecho |
| `paso06-recorrido-completo-y-finales.md` | código | Pedido 6 | paso05 | `feat: recorrido completo y pantallas de finalización` | hecho |
| `paso07-prueba-manual-del-mvp.md` | manual | Pedido 7 | paso06 | `fix: correcciones del MVP` | hecho |
| `paso08-ranking-publico-y-estadisticas.md` | código | Pedido 8 | paso07 | `feat: ranking público y estadísticas` | hecho |
| `paso09-admin-login-y-crud.md` | código | Pedido 9 | paso08 | `feat: panel de administración y CRUD` | hecho |
| `paso10-cobertura-y-dificultades.md` | código | Pedido 10 | paso09 | `feat: cobertura y control de dificultades` | hecho |
| `paso11-pruebas-y-endurecimiento.md` | test | Pedido 11 | paso10 | `test: reglas del juego y endurecimiento` | hecho |
| `paso11b-ranking-por-nivel.md` | feat | Pedido 11b | paso11 | `feat: ranking por nivel` | hecho |
| `paso11c-contenido-intermedio.md` | feat | Pedido 11c | paso11b | `feat: contenido intermedio y avanzado` | hecho |
| `paso11-d-agregando-descripcion.md` | feat | Pedido 11d | paso11c | `feat: descripciones de preguntas` | hecho |
| `paso11e-agregarimagenes.md` | feat | Pedido 11e | paso11d | `feat: imágenes institucionales en la interfaz` | hecho |
| `paso11f-capturas-navegacion.md` | infra | Pedido 11f | paso11e | `docs: capturas de navegación en tamaño móvil` | hecho |
| `paso12-congelar-y-puesta-en-marcha.md` | infra | Pedido 12 | paso11f | `docs: puesta en marcha y respaldo` | pendiente |
| `paso13-docker-taller-post-feria.md` | infra | Pedido 13 | paso12 | `build: docker compose para taller post-feria` | pendiente |

Estados posibles: `pendiente`, `en curso`, `hecho`.

`paso00` no lleva commit porque no crea archivos del repo. Si encuentra un
error bloqueante en el esquema o en el seed, se consulta antes de tocarlo.

---

## 5. Ruta sugerida para una prueba completa

Una prueba de creación completa en un solo día es ambiciosa. La prioridad es
llegar al **MVP jugable** (`paso06`) y recién después seguir.

| Bloque | Pasos | Qué se obtiene |
| --- | --- | --- |
| A | 00, 01 | Base verificada y app levantando. |
| B | 02, 03 | Bienvenida, identidad y estación 1 con preguntas congeladas. |
| C | 04, 05 | Envío, ayudas, eliminaciones y temporizadores. |
| D | 06 | Recorrido completo. **Corte: MVP jugable.** |
| E | 07 | Prueba manual con dos o tres personas. |
| F | 08, 09, 10 | Ranking público, estadísticas y admin. |
| G | 11, 11b, 11c, 11d, 11e, 11f, 12 | Tests, ranking por nivel, contenido intermedio y avanzado, descripciones breves, imágenes institucionales, capturas de navegación, backup y puesta en marcha. |
| H | 13 | Docker educativo, posterior a la feria. |

El paso 13 (Docker) es opcional y posterior a la feria. No reemplaza el camino
de waitress/systemd del paso 12 y no debe ejecutarse antes del 16/11.

Si el día no alcanza, cortar después del bloque D o E. No dejar el MVP a
medio hacer para empezar el admin.

---

## 6. Reglas de la carpeta

- Sin fechas dentro de los pasos: el orden y las dependencias ya están en el
  índice.
- Cada archivo lista solo las reglas propias del paso; las generales viven en
  `AGENTS.md`.
- La verificación incluye comandos y consultas SQL concretas.
- Si aparece una decisión nueva, no se inventa: se anota como duda y se
  actualiza `AGENTS.md` solo con aprobación.
- No se modifican `docs/` ni los prototipos para "acomodar" el código.
