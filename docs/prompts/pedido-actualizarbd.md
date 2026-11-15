
Listo. Actualicé el documento y regeneré su PDF.

## Cambios en `sql/descripcion-de-la-base-de-datos.md`

**Parte 1 (cómo está pensada la base)**

- Nuevo párrafo: cada tema guarda `introduccion` y cada pregunta guarda `explicacion`; son texto plano, no son pistas, no se usan durante la partida y se leen solo en la card **Lo que aprendieron** de la transición, con la estación completada.

**Parte 2 (detalle de tablas)**

- `tema`: fila nueva `introduccion` · `TEXT` · nulo sí · `NULL` · “texto plano que presenta el tema en la transición… no se muestra en la estación”. Aclaración de que los 14 temas activos tienen introducción cargada.
- `pregunta`: fila nueva `explicacion` · `TEXT` · nulo sí · `NULL` · “justifica la respuesta correcta… no se envía a la estación”. Aclaración de las 80 preguntas con explicación (20/30/30).

**“Reglas que la base no impone”**

- La estación nunca recibe la explicación ni la respuesta correcta.
- La transición muestra la respuesta que el equipo eligió en `respuesta_elegida`, no la que hoy esté marcada como `correcta`.

Ambas columnas coinciden con `bd/schema.sql` y con la migración `bd/migraciones/20261113_explicaciones-e-introducciones.sql`.

## PDF

- `docs/pdf/sql/descripcion-de-la-base-de-datos.pdf` regenerado con `./scripts/generar-pdfs.sh`: **6 páginas, A4**, y el texto extraído ya incluye `introduccion` y `explicacion`.
- El índice `docs/pdf/00-indice.pdf` se regeneró en la misma corrida.
- No quedan PDFs desactualizados respecto de su `.md` y hay **0 enlaces internos rotos**.

También dejé registrada la actualización en `MEMORY.md` (y regeneré su PDF). No toqué código, base de datos ni tests; la suite sigue en 105 pruebas pasadas de la corrida anterior.

Nota: no pude leer el PDF que adjuntaste (no tengo soporte de entrada para PDFs), así que verifiqué contra el esquema real y regeneré el archivo desde el `.md` actualizado.
