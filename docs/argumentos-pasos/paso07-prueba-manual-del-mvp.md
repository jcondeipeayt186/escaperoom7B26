# Paso 07 — Prueba manual del MVP

> **Origen:** Pedido 7 de `docs/primeros-pasos.md` (cierre del Paso 6).
> **Tipo:** **manual**. No lo ejecuta el agente.
> **Requiere:** `paso06` aprobado y commiteado.
> **Commit:** `fix: correcciones del MVP` (solo si hay correcciones).
>
> **Antes de empezar:** leé `AGENTS.md` ("Verificación manual antes de
> entregar") y `docs/navegacion-por-app.md` (sección 7, mensajes).

## Contexto

El MVP jugable está completo: 5 estaciones, temporizadores, ayudas, envíos,
eliminaciones, final y ranking básico.

## Objetivo

Probar el juego de punta a punta con personas reales y corregir solo lo que
rompe la experiencia.

## Cómo se usa este archivo

- **No lo lances con `/feature` para implementar.** El comando corre en modo
  plan y no puede jugar.
- Si querés, podés usar `/feature` una sola vez para que el agente prepare
  una planilla de observaciones o un checklist imprimible. Después, la
  prueba la hacen personas.
- Si aparece un error bloqueante, recién ahí pasás a un agente de
  implementación con el error concreto.
- Las correcciones de este paso no agregan funcionalidad.

## Preparación

- Base con el seed cargado y `duracion_estacion_segundos = 240`.
- App levantada en la red local.
- Dos o tres personas que no hayan visto el código.
- Una persona observa y anota, sin ayudar.
- Cronómetro real y las pistas impresas de `docs/ESCAPE ROOM.pdf`.

## Guion de prueba

1. **Bienvenida**
   - Nombre nuevo, cantidad de integrantes y dificultad.
   - Solo debe ofrecer `inicial`.
   - Probar cantidad 0 y 5: deben rechazarse.
2. **Identidad**
   - Salir y volver a entrar con el mismo nombre.
   - Debe pedir el ID; un ID incorrecto debe rechazarse.
   - Confirmar que no se duplica el equipo en MySQL.
3. **Estación 1**
   - Ver el HUD completo.
   - Confirmar que el contador general sube y el de estación baja.
   - Recargar: mismas preguntas, mismos tiempos.
   - Pedir las dos ayudas: al llegar a 2 se deshabilitan.
   - Probar un envío incompleto.
   - Probar un envío con 1 incorrecta.
   - Probar un envío con 2 incorrectas: eliminación.
4. **Aviso de 30 segundos**
   - Texto titilante y audio después del primer clic.
   - Con el audio bloqueado, el aviso visual debe verse igual.
5. **Recorrido**
   - Completar las 5 estaciones.
   - Confirmar el orden y que no se puede saltar por URL.
   - Ver la transición y el arranque del cronómetro de la estación
     siguiente.
6. **Abandono**
   - Probar el botón, la confirmación y la pantalla de eliminación.
7. **Final y ranking**
   - Completar un intento y ver tiempo total, ayudas y posición.
   - Confirmar que un intento eliminado no aparece en el ranking.
   - Confirmar el orden por tiempo y luego por ayudas.
8. **Pantalla chica y televisor**
   - Revisar el HUD en una notebook y en una pantalla grande.
   - Verificar que los textos se lean de pie.

## Planilla de observaciones

Anotar cada tropiezo con este formato:

| # | Paso | Qué esperaba | Qué pasó | ¿Bloquea? |
| --- | --- | --- | --- | --- |
| 1 | | | | sí / no |

## Criterio de aceptación

- [ ] Dos personas completan el recorrido sin ayuda técnica.
- [ ] Ninguna recarga rompe el intento ni reinicia tiempos.
- [ ] No hay ninguna pista de cuál es la respuesta correcta en el HTML.
- [ ] Los mensajes se entienden sin explicación previa.
- [ ] Las tres eliminaciones se distinguen con claridad.
- [ ] El ranking ordena bien y excluye los intentos no completados.

## Qué corregir y qué no

- **Sí:** errores de flujo, mensajes confusos, tiempos mal calculados,
  pantallas rotas, pérdida de estado al recargar.
- **No:** funcionalidad nueva, cambios de esquema, cambios de contenido, ni
  "mejoras" de estilo que no estaban pedidas.
- Cada corrección lleva su prueba manual y, si toca una regla crítica, se
  agrega al `paso11`.
- No tocar el seed salvo un error bloqueante.

## Al terminar

- Listar los errores encontrados, los corregidos y los que quedan.
- Actualizar `MEMORY.md` con el resultado de la prueba.
- Commit: `fix: correcciones del MVP` (si hubo correcciones).

Este paso es la puerta antes del `paso08`. No empezar el admin sin cerrarlo.
