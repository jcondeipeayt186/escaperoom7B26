# Paso 03 — Selección de preguntas y estación 1

> **Origen:** Pedido 3 de `docs/primeros-pasos.md` (Paso 4, primera parte).
> **Tipo:** código.
> **Requiere:** `paso02` aprobado y commiteado.
> **Commit:** `feat: selección persistida de preguntas`.
>
> **Antes de empezar:** leé `AGENTS.md` ("Selección de preguntas por
> estación"), `docs/escape-room.md`, `docs/navegacion-por-app.md` (pantalla
> 3.3) y `sql/descripcion-de-la-base-de-datos.md` (`intento_pregunta`,
> `intento_estacion`, `estacion`, `tema`, `pregunta`, `respuesta`).

## Contexto

La bienvenida ya crea equipo e intento, y `/juego` muestra una pantalla
provisoria. Todavía no se puede jugar una estación.

## Objetivo

Mostrar la estación 1 con 4 preguntas seleccionadas y persistidas, sin
enviar al cliente cuál es la correcta.

## Alcance

- Helper de selección en `app/servicios/seleccion.py` (o la carpeta de
  servicios que adopte el proyecto).
- `GET /juego/estacion/<orden>` en el blueprint `juego`.
- `templates/estacion.html` con el HUD, el título de la estación y las 4
  preguntas con sus 3 opciones como radios.
- Crear `intento_estacion` con `fecha_inicio` del servidor al entrar por
  primera vez a la estación.
- Persistir la selección y el orden en `intento_pregunta`.
- Cambiar `GET /juego` para redirigir a la estación que corresponde.

No implementar todavía el envío del formulario ni los temporizadores.

## Reglas

- Siempre 4 preguntas, todas del nivel del intento.
- Si la estación tiene más de 4 temas activos, elegir 4 temas al azar y una
  pregunta de cada uno.
- Si tiene 4 temas o menos, elegir al menos una pregunta de cada tema y
  completar los lugares restantes al azar con preguntas de la estación y del
  nivel.
- La selección se congela por intento: si ya hay filas en
  `intento_pregunta`, se usan esas y no se vuelve a sortear.
- Recargar no cambia las preguntas ni el orden.
- No permitir saltar estaciones por URL.
- No enviar al cliente la respuesta correcta ni un atributo que la delate.
  Las opciones se muestran todas; lo que no se revela es cuál es la correcta.
- No confiar en el `orden` que manda el cliente: se valida contra la base.
- Si una estación no tiene cobertura suficiente, mostrar un error claro y no
  romper con una excepción.

## Criterio de aceptación

- [ ] La estación 1 muestra 4 preguntas, cada una con 3 opciones.
- [ ] Recargar 5 veces muestra las mismas 4 preguntas y en el mismo orden.
- [ ] El HTML no contiene ningún atributo, clase o campo que indique cuál es
      la correcta.
- [ ] `intento_pregunta` tiene 4 filas para el intento y la estación.
- [ ] Entrar a `/juego/estacion/3` sin haber jugado la 2 redirige a la
      estación actual.
- [ ] El HUD muestra equipo, estación, ayudas, incorrectas y envíos.
- [ ] `intento_estacion.fecha_inicio` no cambia al recargar.

## Verificación

Selección persistida:

```sql
SELECT orden, pregunta_id
FROM intento_pregunta
WHERE intento_id = <id> AND estacion_id = <id>
ORDER BY orden;
```

Esperado: 4 filas con `orden` 1 a 4 y sin preguntas repetidas.

Cobertura usada:

```sql
SELECT t.nombre AS tema, COUNT(ip.id) AS seleccionadas
FROM intento_pregunta ip
JOIN pregunta p ON p.id = ip.pregunta_id
JOIN tema t ON t.id = p.tema_id
WHERE ip.intento_id = <id> AND ip.estacion_id = <id>
GROUP BY t.id, t.nombre;
```

Esperado: al menos 1 por tema activo y 4 en total.

Fuga de información:

```bash
curl -s http://127.0.0.1:5000/juego/estacion/1 | grep -iE "correcta|correcto|data-correcta"
```

Esperado: sin resultados que identifiquen la opción correcta. El texto de la
opción correcta **sí** aparece, porque es una de las opciones visibles.

## Trampas conocidas

- `intento.ultima_estacion_visitada` guarda `estacion.id`, no `orden`. Para
  comparar, hacer `JOIN estacion` y usar `estacion.orden`.
- No usar `ORDER BY RAND()` sin persistir: hay que guardar la selección.
- `intento_estacion` tiene una clave única por `(intento_id, estacion_id)`.
  Al reanudar se reutiliza la fila; no se crea otra ni se reinicia
  `fecha_inicio`.
- El orden de las opciones no hace falta que sea aleatorio. Si se mezcla, la
  mezcla no se persiste y puede cambiar al recargar; para el MVP, mantener el
  orden de la base.
- Validar que la estación esté activa y que el orden esté entre 1 y 5.

## No hagas todavía

Envío del formulario, ayudas, eliminaciones, temporizadores, estaciones 2 a 5,
ranking y admin.

## Al terminar

- Resumir archivos, comandos y pruebas.
- Actualizar `MEMORY.md` con el estado de la estación 1.
- Commit: `feat: selección persistida de preguntas`.
