
Terminé lo que quedaba del plan.

## Qué completé en esta última tanda

**`docs/guia-de-estudio-para-estudiantes.md`**

- §8.1: nueva fila “Entender cómo se hizo el proyecto”.
- §8.3: agregué `docs/material-de-estudio-y-control.md` marcado 🔴, con la advertencia de que contiene todas las respuestas y que no se lee si se va a jugar.
- §8.6: agregué `docs/como-se-hizo-el-proyecto.md` como documentación de proceso.
- §12: documenté `docs/pdf/` (un PDF por `.md` con la ruta espejada + `00-indice.pdf`), el script `./scripts/generar-pdfs.sh` y la aclaración de que incluye el material con respuestas.

**`MEMORY.md`**

- Fecha actualizada a 15/11/2026 y entrada nueva con el material de estudio, el documento de proceso, el pipeline de PDFs, las verificaciones y el resultado de `pytest`.
- “Próximo paso” ahora recuerda regenerar los PDFs si cambia un `.md` o el contenido desde `/admin`.

**PDFs regenerados** (los que habían quedado viejos por las ediciones): `AGENTS.pdf`, `README.pdf`, `guia-de-estudio-para-estudiantes.pdf`, `MEMORY.pdf` y el índice.

## Verificación

- **48 archivos en `docs/pdf/`**: 47 PDFs + `00-indice.pdf`, 16 MB.
- **Ningún PDF desactualizado** respecto de su `.md` de origen.
- **0 enlaces internos rotos** en todos los `.md` del proyecto.
- El índice lista los documentos nuevos (“Cómo se hizo el proyecto”, “Material de estudio y control…”).
- La app **no referencia** el material con respuestas ni el documento de proceso (`grep` en `app/` sin resultados).
- **`pytest -q`: 105 passed** (57 s).
- La base real no se tocó.

## Pendiente (no depende del código)

- **No hay repositorio Git**, así que no se pueden crear los commits (`docs: feria con flask y respaldo`, ni el de los documentos/PDFs).
- Copiar el respaldo `respaldo-escape_room_7b2026-20261114-233156.sql` a un pendrive o a la nube: hoy sigue solo en la notebook.
- La ficha del servidor de la escuela (distribución y versión) para el `paso13` posterior a la feria.
