# Paso 02 — Bienvenida e identidad del equipo

> **Origen:** Pedido 2 de `docs/primeros-pasos.md` (Paso 3).
> **Tipo:** código.
> **Requiere:** `paso01` aprobado y commiteado.
> **Commit:** `feat: bienvenida e identidad de equipo`.
>
> **Antes de empezar:** leé `AGENTS.md` (sobre todo "Identidad del equipo"),
> `docs/escape-room.md`, `docs/navegacion-por-app.md` (pantallas 3.1 y 3.2) y
> `sql/descripcion-de-la-base-de-datos.md` (`equipo`, `intento`,
> `configuracion`).

## Contexto

La app levanta, hay conexión a MySQL y blueprints vacíos. Todavía no se puede
registrar un equipo.

## Objetivo

Registrar un equipo, crear o reanudar su intento y permitir el reingreso con
el ID cuando el nombre ya existe.

## Alcance

- `GET /` y `POST /` en el blueprint `juego`, con nombre, cantidad de
  integrantes (1–4) y dificultad.
- `GET /equipo/identificar` y `POST /equipo/identificar`.
- `templates/bienvenida.html` y `templates/identificar.html`.
- Leer `configuracion` para mostrar solo las dificultades habilitadas.
- Normalizar el nombre: `trim`, colapsar espacios repetidos y máximo 120
  caracteres.
- Guardar `equipo_id` e `intento_id` en la sesión de Flask.
- HUD mínimo con `Equipo N.º <id> · <nombre>`.
- `GET /juego` provisoria: muestra el equipo, el intento y la estación a
  jugar. En el `paso03` pasa a redirigir a la estación real.

No crear estaciones, temporizadores ni admin.

## Reglas

- `equipo.nombre` es único. La colación compara sin distinguir mayúsculas ni
  acentos: "Los Tigres" y "los tigres" son el mismo equipo.
- Si el nombre no existe: crear `equipo` e `intento` en una transacción.
- Si el nombre existe: no crear nada, redirigir a identificar y pedir el ID.
- Un ID incorrecto se rechaza sin revelar datos del equipo.
- Si el equipo tiene un intento activo (`fecha_fin IS NULL`), se reanuda ese
  intento, sin importar la dificultad elegida en el formulario.
- Si no tiene intento activo, se crea uno nuevo con la dificultad elegida.
- La dificultad de un intento no cambia después de crearlo.
- Al crear el intento, asignar `ultima_estacion_visitada` a la estación
  activa con `orden = 1`. No confiar en el `DEFAULT 1` del esquema: el `id`
  de esa estación no tiene por qué ser 1.
- No se acepta una dificultad deshabilitada en `configuracion`, aunque el
  cliente la mande.
- No guardar el nombre como fuente de verdad: la sesión guarda IDs y el
  servidor vuelve a leer de la base.
- No hay autenticación de participantes ni registro público.

## Criterio de aceptación

- [ ] Un nombre nuevo crea `equipo` e `intento` y deja la sesión lista.
- [ ] El mismo nombre (aunque cambien mayúsculas o acentos) pide el ID y no
      duplica el equipo.
- [ ] El ID correcto reanuda el intento activo o crea uno nuevo.
- [ ] Un ID incorrecto muestra error y no revela el nombre del equipo.
- [ ] Cantidad `0` o `5` se rechaza antes de crear nada.
- [ ] Una dificultad deshabilitada no se ofrece ni se acepta por POST.
- [ ] Recargar o volver a `/juego` no pierde el intento.
- [ ] El HUD muestra `Equipo N.º X`.

## Verificación

1. Crear "Los Tigres" con 3 integrantes y dificultad `inicial`.
2. Anotar el ID que muestra el HUD.
3. Cerrar sesión o abrir una ventana nueva y volver a cargar "los tigres".
4. Confirmar que pide el ID y que un ID inventado se rechaza.
5. En MySQL:

```sql
SELECT id, nombre, cantidad_personas, fecha_creacion
FROM equipo ORDER BY id DESC LIMIT 5;

SELECT id, equipo_id, dificultad, fecha_inicio, fecha_fin, finalizado,
       ultima_estacion_visitada
FROM intento ORDER BY id DESC LIMIT 5;

SELECT clave, valor FROM configuracion WHERE clave LIKE 'dificultad%';
```

Esperado: un solo `equipo` con ese nombre y un intento por ingreso sin
intento activo.

## Trampas conocidas

- El nombre único no distingue mayúsculas ni acentos. No intentes "arreglarlo"
  con una comparación en Python: la base ya lo resuelve.
- Si dos pestañas crean el mismo nombre a la vez, la restricción `UNIQUE`
  gana. Capturar el error de duplicado y redirigir a identificar.
- No confiar en el `id` que manda el formulario de identificación sin
  comprobar que el equipo existe y que el nombre coincide.
- La sesión de Flask no es la fuente de verdad del intento: en cada request
  se valida que el `intento_id` exista, pertenezca al `equipo_id` y siga
  activo.

## No hagas todavía

Estaciones, selección de preguntas, temporizadores, ranking y admin.

## Al terminar

- Resumir archivos, comandos y pruebas.
- Actualizar `MEMORY.md` con el estado de la bienvenida.
- Commit: `feat: bienvenida e identidad de equipo`.
