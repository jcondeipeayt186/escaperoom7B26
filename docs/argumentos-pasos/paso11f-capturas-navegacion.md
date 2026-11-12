# Paso 11f — Capturas de navegación en tamaño móvil

> **Origen:** pedido posterior al `paso11e`, antes del `paso12`.
> **Tipo:** documentación y capturas (no toca código de la aplicación).
> **Requiere:** `paso11e` implementado y commiteado.
> **Commit de este plan:** `docs: paso11f de capturas de navegación`.
> **Commit del entregable:** `docs: capturas de navegación en tamaño móvil`.
>
> **Antes de empezar:** leé `AGENTS.md` (reglas, rutas y "Qué no hacer"),
> `docs/navegacion-por-app.md` (mapa de pantallas y estados),
> `docs/argumentos-pasos/paso11e-agregarimagenes.md` y las plantillas
> `base.html`, `bienvenida.html`, `estacion.html`, `_hud.html`,
> `transicion.html`, `final.html`, `eliminado.html` y `admin/*.html`.

## Estado

Pendiente de ejecución. La **viabilidad técnica ya está comprobada** el
12/11/2026 con `chrome-devtools`: el viewport `300x800x1,mobile,touch` deja
`innerWidth = 300`, sin desbordes horizontales, y `fullPage` genera PNG de
300 px de ancho (bienvenida 300 × 1259, ranking 300 × 800). No hace falta
tocar la aplicación para capturar.

## Contexto

La app ya está implementada y probada, pero no existe un recorrido visual
que muestre cómo se ve en un teléfono y qué pantallas aparecen en cada
situación. El `paso11e` dejó las imágenes institucionales en su lugar; este
paso usa la app real para producir un documento de navegación con capturas.

El pedido original es:

- Capturas de **cada página** de la app en un ancho de móvil.
- **Tres intentos completos**, uno por nivel (`inicial`, `intermedio`,
  `avanzado`), que llegan al final y completan el recorrido.
- Intentos que **no completan** por respuestas incorrectas, por abandono y
  por tiempo agotado.
- Un único documento Markdown con las capturas embebidas.

No se agregan funcionalidades, rutas ni pantallas. Si una pantalla no existe
en la app, no se inventa: se documenta la que existe.

## Objetivo

Producir dos entregables:

1. `docs/capturas-navegacion/*.png` — capturas individuales.
2. `docs/navegacion-capturas.md` — documento de navegación con las capturas
   embebidas, agrupadas por recorrido y por estado.

El documento final debe permitir que una persona que nunca vio el proyecto
entienda el recorrido completo, los estados posibles y qué botón sigue en
cada pantalla.

## Viabilidad comprobada

Prueba realizada con `chrome-devtools` contra la app levantada en
`http://127.0.0.1:5055`:

| Prueba | Resultado |
| --- | --- |
| `emulate({ viewport: "300x800x1,mobile,touch" })` | `innerWidth = 300`, `innerHeight = 800`, `matchMedia("(max-width: 575.98px)") = true`. |
| Desborde horizontal en `/` | `scrollWidth = 300`, `overflowX = false`. |
| Desborde horizontal en `/ranking` | `scrollWidth = 300`, `overflowX = false`. |
| Captura `fullPage` de `/` | PNG de **300 × 1259** (157 KB). |
| Captura de viewport de `/ranking` | PNG de **300 × 800** (55 KB). |
| Tablas de ranking a 300 px | Scroll horizontal **interno** del contenedor, sin desbordar la página. |

Conclusión: el ancho de 300 px es viable y no rompe ninguna pantalla. La app
ya es responsive; no se necesita un modo móvil especial.

### 300 × 800 no es el tamaño físico del Galaxy A55

El A55 tiene una pantalla física de 1080 × 2340 y un viewport CSS aproximado
de **384 × 854** con densidad ~2,8. Los **300 × 800** pedidos son un viewport
CSS más angosto, útil para una galería compacta y para forzar el peor caso de
ancho. En este paso se respeta **300 × 800** y se aclara en el documento que
es una emulación angosta, no la métrica exacta del teléfono.

Opcional: repetir una o dos capturas a **384 × 854** para comparar con el
tamaño real del A55. No es obligatorio y no reemplaza las de 300 px.

## Decisiones de este paso

| Tema | Decisión |
| --- | --- |
| Ancho | 300 px CSS, `deviceScaleFactor = 1`, `mobile` y `touch`. |
| Alto | `fullPage = true` en las páginas de contenido; el alto varía. |
| Formato | PNG. Es texto de interfaz: conviene nitidez, no JPEG. |
| Base de datos | Exclusiva `escape_room_7b2026_capturas`, creada desde `bd/escape_room_7b2026_completa.sql`. **Nunca** la base real. |
| Código | Cero cambios en `app/`, `tests/`, `bd/` ni `requirements.txt`. |
| Datos | Equipos sintéticos (`Equipo Demo …`); sin nombres reales. |
| Respuestas | Las correctas se leen por SQL solo en la base de capturas y **no se transcriben** al documento. |
| Horarios | Se usan los tiempos reales del recorrido. No se normalizan fechas. |
| Administración | Credenciales temporales por variables de entorno; nunca las reales. |
| Alcance | Público, juego, eliminación, final, admin y errores. |
| Duración | El paso termina cuando el `.md` se puede leer de punta a punta y las capturas existen. |

## Entorno seguro

### 1. Crear la base de capturas

El archivo `bd/escape_room_7b2026_completa.sql` crea y usa
`escape_room_7b2026`. Se genera una copia con el nombre reemplazado **fuera
del repositorio**:

```bash
sed 's/escape_room_7b2026/escape_room_7b2026_capturas/g' \
  bd/escape_room_7b2026_completa.sql > /tmp/opencode/capturas.sql

grep -n "CREATE DATABASE\|^USE " /tmp/opencode/capturas.sql

mysql -u <usuario> -p < /tmp/opencode/capturas.sql
```

Verificar que la base creada es la correcta y que tiene el contenido
esperado:

```bash
mysql -u <usuario> -p -N -e \
  "SELECT SCHEMA_NAME FROM information_schema.SCHEMATA
   WHERE SCHEMA_NAME LIKE 'escape_room_7b2026%';"

mysql -u <usuario> -p escape_room_7b2026_capturas -e \
  "SELECT COUNT(*) AS estaciones FROM estacion;
   SELECT COUNT(*) AS preguntas FROM pregunta;
   SELECT COUNT(*) AS respuestas FROM respuesta;
   SELECT * FROM configuracion ORDER BY clave;"
```

Debe dar **5 estaciones, 80 preguntas, 240 respuestas** y las 9 claves de
`configuracion` con `duracion_estacion_segundos = 240`,
`max_envios_estacion = 2`, `max_respuestas_incorrectas = 2` y las dos
dificultades en `1`.

### 2. Confirmar que la app apunta a la base de capturas

`app/__init__.py` llama a `load_dotenv()`, que **no pisa** variables de
entorno ya definidas. Por eso alcanza con prefijar `MYSQL_DB`:

```bash
MYSQL_DB=escape_room_7b2026_capturas .venv/bin/python - <<'PY'
from app import create_app
app = create_app()
assert app.config["MYSQL_DB"] == "escape_room_7b2026_capturas", app.config["MYSQL_DB"]
print("OK:", app.config["MYSQL_DB"])
PY
```

Si el resultado no es `escape_room_7b2026_capturas`, **no seguir**.

### 3. Levantar la app con credenciales temporales

No se usa la clave real del admin. Se genera un hash temporal y se pasa por
entorno, junto con la base de capturas:

```bash
export CAPTURAS_CLAVE="clave-solo-para-capturas"
export CAPTURAS_HASH="$(.venv/bin/python -c \
  'from werkzeug.security import generate_password_hash; import os;
   print(generate_password_hash(os.environ["CAPTURAS_CLAVE"]))')"

MYSQL_DB=escape_room_7b2026_capturas \
ADMIN_USER=demo_capturas \
ADMIN_PASSWORD_HASH="$CAPTURAS_HASH" \
.venv/bin/flask --app app run --port 5056
```

Comprobar:

```bash
curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:5056/salud
curl -s http://127.0.0.1:5056/salud
```

Debe responder `200` y `{"estado":"ok","base":"ok"}`. El puerto 5056 evita
chocar con el servidor de desarrollo habitual (5000 o 5055).

> **Nunca** cambiar el `.env` del repositorio para este paso. Las variables
> van en la línea de comandos y desaparecen al cerrar la terminal.

### 4. Limpieza al terminar

```bash
pkill -f "flask --app app run --port 5056"

mysql -u <usuario> -p -e "DROP DATABASE escape_room_7b2026_capturas;"
rm -f /tmp/opencode/capturas.sql
```

La base de capturas es descartable. No se versiona, no se respalda y no se
restaura sobre la base real.

## Herramienta de captura

La herramienta `browser.*` del entorno **no permite cambiar el viewport**.
Hay que usar `chrome-devtools`, que sí acepta emulación de dispositivo.

Pasos mínimos:

```js
// 1. Abrir una página nueva contra la app de capturas.
const p = await tools["chrome-devtools"].new_page({
  url: "http://127.0.0.1:5056/"
});
const pages = await tools["chrome-devtools"].list_pages();
// Tomar el pageId de la página recién abierta.

// 2. Emular 300 x 800, móvil y táctil.
await tools["chrome-devtools"].emulate({
  pageId,
  viewport: "300x800x1,mobile,touch"
});

// 3. Navegar y capturar.
await tools["chrome-devtools"].navigate_page({
  pageId,
  type: "url",
  url: "http://127.0.0.1:5056/"
});

await tools["chrome-devtools"].take_screenshot({
  pageId,
  fullPage: true,
  filePath: "docs/capturas-navegacion/00-publico-bienvenida.png"
});
```

Notas de la herramienta:

- `filePath` se interpreta relativo al **directorio de trabajo** o absoluto.
  Crear la carpeta antes de la primera captura.
- `fullPage: true` captura toda la página; el ancho sigue siendo 300 px.
  Para pantallas donde el pliegue es lo importante (ranking, TV) usar
  `fullPage: false`.
- Si el navegador se reinicia o se reconecta, los `pageId` cambian: volver a
  llamar a `list_pages()` y a `emulate()`.
- `emulate()` reemplaza **todos** los ajustes en cada llamada. Si hace falta
  tocar otro ajuste, repetir `viewport`.
- Para los diálogos nativos de `window.confirm` (ayudas, abandono, finalizar)
  usar `handle_dialog` con `action: "accept"` o pasar
  `dialogAction: "accept"` a `evaluate_script`.
- El audio de los 30 segundos no se ve en una captura. Documentar el texto y
  el estado visual.

Verificar el viewport y el desborde antes de la primera captura:

```js
() => {
  const de = document.documentElement;
  return {
    viewport: [innerWidth, innerHeight],
    scrollWidth: de.scrollWidth,
    scrollHeight: de.scrollHeight,
    overflowX: de.scrollWidth > de.clientWidth
  };
}
```

Debe devolver `viewport: [300, 800]` y `overflowX: false`.

## Inventario de pantallas

Mapa tomado de `docs/navegacion-por-app.md`. La columna **Captura** indica
qué se hace en este paso.

| # | Ruta | Pantalla | Captura |
| --- | --- | --- | --- |
| 1 | `/` GET | Bienvenida | Sí (`00`, `01`). |
| 2 | `/` POST | Validación de bienvenida | No hay pantalla propia; el error se ve en `01`. |
| 3 | `/equipo/identificar` | Identificación de equipo | Sí (`02`). |
| 4 | `/juego` | Redirección al juego | No; no tiene pantalla. |
| 5 | `/juego/estacion/<orden>` | Estación | Sí (todas en `10`–`14`, más `20` y `30`). |
| 6 | `/juego/estacion/<orden>/responder` | Envío | No hay pantalla propia; los estados se ven en `40` y `51`. |
| 7 | `/juego/estacion/<orden>/ayuda` | Ayuda | Estado del HUD; captura opcional `18`. |
| 8 | `/juego/estacion/<orden>/abandonar` | Confirmación de abandono | El diálogo nativo no se captura; resultado en `42`. |
| 9 | `/juego/transicion/<orden>` | Transición | Sí (`15`, `16`, `21`). |
| 10 | `/juego/final` | Final | Sí (`17`, `22`, `31`). |
| 11 | `/juego/eliminado` | Eliminación | Sí (`41`, `42`, `43`). |
| 12 | `/ranking` | Ranking público | Sí (`03`). |
| 13 | `/ranking/datos` | JSON del ranking | No; es JSON. |
| 14 | `/estadisticas` | Estadísticas públicas | Sí (`04`). |
| 15 | `/admin` | Login | Sí (`60`). |
| 16 | `/admin/login` | Validación de login | No hay pantalla propia. |
| 17 | `/admin/logout` | Cierre de sesión | No hay pantalla propia. |
| 18 | `/admin/` | Panel | Sí (`61`). |
| 19 | `/admin/<tabla>` | Listado | Sí (`62`). |
| 20 | `/admin/<tabla>/nuevo` | Alta | Sí (`63`). |
| 21 | `/admin/<tabla>/<id>` | Detalle | Sí (`64`). |
| 22 | `/admin/<tabla>/<id>/editar` | Edición | Sí (`65`). |
| 23 | `/admin/<tabla>/<id>/desactivar` | Baja lógica | No hay pantalla propia. |
| 24 | `/admin/cobertura` | Cobertura | Sí (`66`). |
| 25 | `/admin/dificultades` | Dificultades | Sí (`67` y `68`). |
| 26 | `/admin/intentos-activos` | Intentos activos | Sí (`69`). |
| 27 | `/admin/estadisticas` | Estadísticas del admin | Sí (`70`). |
| 28 | `/salud` | Salud | No; es JSON. |
| 29 | — | 404 | Sí (`90`). |
| 30 | — | 500 | No; exigiría romper la app. |
| 31 | `/juego/estado` | JSON de tiempos | No; es JSON, no figura en el mapa base. |

Rutas que **no** se capturan porque no producen una página visible:
`/juego`, `/ranking/datos`, `/salud`, `/juego/estado`, los POST de
`responder`, `ayuda`, `abandonar`, `finalizar`, `continuar`,
`/admin/login`, `/admin/logout` y `/admin/<tabla>/<id>/desactivar`.

## Matriz de capturas

Los nombres son sintéticos y van numerados para que el documento final los
ordene solo. La carpeta destino es `docs/capturas-navegacion/`.

| Archivo | Escenario | Ruta | Estado | Modo |
| --- | --- | --- | --- | --- |
| `00-publico-bienvenida.png` | Público | `/` | Formulario vacío, tres dificultades. | Página completa |
| `01-publico-bienvenida-error.png` | Público | `/` (POST inválido) | Error de validación inline. | Página completa |
| `02-publico-identificar.png` | Público | `/equipo/identificar` | Nombre existente, pide ID. | Página completa |
| `03-publico-ranking.png` | Público | `/ranking` | Tres niveles con datos. | Página completa |
| `04-publico-estadisticas.png` | Público | `/estadisticas` | Agregados de la feria. | Página completa |
| `05-publico-ranking-reconectando.png` | Público | `/ranking` | Polling caído, tablas conservadas. | Viewport (opcional) |
| `10-inicial-estacion-1.png` | Inicial | `/juego/estacion/1` | Estación 1 inicial, 4 preguntas. | Página completa |
| `11-inicial-estacion-2.png` | Inicial | `/juego/estacion/2` | Estación 2 inicial. | Página completa |
| `12-inicial-estacion-3.png` | Inicial | `/juego/estacion/3` | Estación 3 inicial. | Página completa |
| `13-inicial-estacion-4.png` | Inicial | `/juego/estacion/4` | Estación 4 inicial. | Página completa |
| `14-inicial-estacion-5.png` | Inicial | `/juego/estacion/5` | Estación 5 inicial. | Página completa |
| `15-inicial-transicion-1.png` | Inicial | `/juego/transicion/1` | Estación 1 superada. | Página completa |
| `16-inicial-transicion-5.png` | Inicial | `/juego/transicion/5` | Quinta superada, **Ver resultado**. | Página completa |
| `17-inicial-final.png` | Inicial | `/juego/final` | Intento completo inicial. | Página completa |
| `18-inicial-ayudas.png` | Inicial | `/juego/estacion/1` | Ayudas 2 de 2, botones deshabilitados. | Página completa (opcional) |
| `20-intermedio-estacion-1.png` | Intermedio | `/juego/estacion/1` | Estación 1 intermedia, con descripciones. | Página completa |
| `21-intermedio-transicion-1.png` | Intermedio | `/juego/transicion/1` | Estación 1 superada. | Página completa |
| `22-intermedio-final.png` | Intermedio | `/juego/final` | Intento completo intermedio. | Página completa |
| `30-avanzado-estacion-1.png` | Avanzado | `/juego/estacion/1` | Estación 1 avanzada, con descripciones. | Página completa |
| `31-avanzado-final.png` | Avanzado | `/juego/final` | Intento completo avanzado. | Página completa |
| `40-incorrectas-estacion.png` | Incorrectas | `/juego/estacion/1` | Incorrectas 1 de 2, envíos 1 de 2. | Página completa |
| `41-incorrectas-eliminado.png` | Incorrectas | `/juego/eliminado` | Eliminado por 2 incorrectas. | Página completa |
| `42-abandono-eliminado.png` | Abandono | `/juego/eliminado` | Eliminado por abandono. | Página completa |
| `43-tiempo-eliminado.png` | Tiempo | `/juego/eliminado` | Eliminado por tiempo agotado. | Página completa |
| `50-especial-aviso-30s.png` | Tiempo | `/juego/estacion/1` | Últimos 30 segundos, texto titilante. | Página completa |
| `51-especial-solo-finalizar.png` | Especial | `/juego/estacion/1` | Modo “solo finalizar”. | Página completa (opcional) |
| `52-especial-503.png` | Especial | `/juego/estacion/1` | Estación no disponible por cobertura. | Página completa |
| `53-especial-400.png` | Especial | `/juego/…` | POST sin CSRF. | Página completa |
| `60-admin-login.png` | Admin | `/admin` | Login sin sesión. | Página completa |
| `61-admin-panel.png` | Admin | `/admin/` | Panel con cards y estado. | Página completa |
| `62-admin-listado.png` | Admin | `/admin/pregunta` | Listado con filtros. | Página completa |
| `63-admin-nuevo.png` | Admin | `/admin/pregunta/nuevo` | Alta de pregunta. | Página completa |
| `64-admin-detalle.png` | Admin | `/admin/pregunta/<id>` | Detalle de una pregunta. | Página completa |
| `65-admin-editar.png` | Admin | `/admin/pregunta/<id>/editar` | Edición de una pregunta. | Página completa |
| `66-admin-cobertura.png` | Admin | `/admin/cobertura` | Estación × nivel en verde. | Página completa |
| `67-admin-dificultades.png` | Admin | `/admin/dificultades` | Sin intentos activos. | Página completa |
| `68-admin-dificultades-bloqueado.png` | Admin | `/admin/dificultades` | Con un intento activo, toggles bloqueados. | Página completa |
| `69-admin-intentos-activos.png` | Admin | `/admin/intentos-activos` | Un equipo jugando. | Página completa |
| `70-admin-estadisticas.png` | Admin | `/admin/estadisticas` | Gráficos con datos. | Página completa |
| `90-error-404.png` | Error | `/ruta-inexistente` | 404 amigable. | Página completa |
| `91-ranking-tv-1920.png` | Público | `/ranking` | Vista de TV, 1920 × 1080. | Viewport |

Presupuesto: **41 capturas** (38 obligatorias + 3 opcionales: `05`, `18` y
`51`), alrededor de 6 a 8 MB en total. Si se suman todas las variantes, no
superar los 10 MB.

## Guion de los intentos

Los nombres son sintéticos y únicos. Todos usan **3 integrantes** para que el
formulario no quede en el valor mínimo.

| Intento | Equipo | Nivel | Final |
| --- | --- | --- | --- |
| A | `Equipo Demo Inicial` | `inicial` | Completo |
| B | `Equipo Demo Intermedio` | `intermedio` | Completo |
| C | `Equipo Demo Avanzado` | `avanzado` | Completo |
| D | `Equipo Demo Incorrectas` | `inicial` | Por respuestas incorrectas |
| E | `Equipo Demo Abandono` | `intermedio` | Por abandono |
| F | `Equipo Demo Tiempo` | `avanzado` | Por tiempo |
| G | `Equipo Demo Solo Finalizar` | `inicial` | Por respuestas incorrectas (laboratorio) |
| H | `Equipo Demo Activo` | `inicial` | Queda en curso para el admin |
| I | `Equipo Demo Sin Cobertura` | `inicial` | No llega a jugar (503) |

### Leer las respuestas correctas

Solo en la base de capturas. Nunca en la base real.

```sql
-- Último intento creado y su equipo.
SELECT i.id AS intento_id, i.equipo_id, e.nombre, i.dificultad, i.finalizado
FROM intento i
JOIN equipo e ON e.id = i.equipo_id
ORDER BY i.id DESC
LIMIT 1;

-- Preguntas congeladas y respuesta correcta de cada una.
SELECT ip.orden, p.id AS pregunta_id, r.id AS respuesta_id, r.contenido
FROM intento_pregunta ip
JOIN pregunta p ON p.id = ip.pregunta_id
JOIN respuesta r ON r.pregunta_id = p.id AND r.correcta = 1
WHERE ip.intento_id = <INTENTO_ID>
ORDER BY ip.orden;
```

Para un envío con una incorrecta, cambiar **una** de las cuatro respuestas
por una opción falsa de la misma pregunta:

```sql
SELECT r.id
FROM respuesta r
WHERE r.pregunta_id = <PREGUNTA_ID> AND r.correcta = 0
ORDER BY r.id
LIMIT 1;
```

El resultado de estas consultas **no se copia** al documento final ni a las
capturas. Las capturas muestran las opciones, pero la app no marca cuál es la
correcta.

### Cargar las respuestas en el navegador

Con la estación abierta, se marcan los radios por `name` y `value` y se envía
el formulario real:

```js
() => {
  // Pegar el mapa {pregunta_id: respuesta_id} leído de la base de capturas.
  const elegidas = { /* "123": "456", ... */ };

  for (const [preguntaId, respuestaId] of Object.entries(elegidas)) {
    const radio = document.querySelector(
      `input[name="pregunta_${preguntaId}"][value="${respuestaId}"]`
    );
    if (!radio) throw new Error(`Falta la opción ${respuestaId} de ${preguntaId}`);
    radio.checked = true;
  }

  const formulario = document.querySelector("form[action$='/responder']");
  formulario.requestSubmit();
  return true;
}
```

Si el envío dispara un diálogo de confirmación, pasar
`dialogAction: "accept"` a `evaluate_script`. Para el abandono y para
**Finalizar juego** conviene hacer clic en el botón real y aceptar el
diálogo, así la captura posterior refleja el flujo real.

### Intento A — completo, nivel `inicial`

Objetivo: recorrer las cinco estaciones, capturar todas las pantallas de
estación y las transiciones, y terminar en el final.

1. En `/`, completar `Equipo Demo Inicial`, 3 integrantes y `inicial`.
   Presionar **Iniciar misión**.
2. **Estación 1**: capturar `10-inicial-estacion-1.png` antes de responder.
   Opcional: pedir **Ayuda 1** y **Ayuda 2** (aceptar los dos diálogos) y
   capturar `18-inicial-ayudas.png` con el HUD en “Ayudas 2 de 2” y los
   botones deshabilitados.
3. Responder las 4 preguntas correctas con el envío real. Debe aparecer la
   transición 1.
4. **Transición 1**: capturar `15-inicial-transicion-1.png`. Presionar
   **Continuar**.
5. **Estación 2**: capturar `11-inicial-estacion-2.png`, responder todas
   correctas y continuar.
6. **Estación 3**: capturar `12-inicial-estacion-3.png`, responder y
   continuar.
7. **Estación 4**: capturar `13-inicial-estacion-4.png`, responder y
   continuar.
8. **Estación 5**: capturar `14-inicial-estacion-5.png`, responder todas
   correctas.
9. **Transición 5**: capturar `16-inicial-transicion-5.png` con el tiempo de
   estación congelado y el botón **Ver resultado**. Presionar **Ver
   resultado**.
10. **Final**: capturar `17-inicial-final.png` con el encabezado oscuro, la
    posición de nivel, el top 10 y el ranking completo.

Las ayudas usadas quedan registradas en el intento y afectan el desempate.
Es correcto: el documento muestra el HUD con 2 ayudas y el final con ese
dato. Si se prefiere un final sin ayudas, hacer el recorrido sin pedirlas y
capturar `18` en un intento aparte.

### Intento B — completo, nivel `intermedio`

Objetivo: mostrar la estación con descripciones y el final del nivel.

1. Volver a `/`. Completar `Equipo Demo Intermedio`, 3 integrantes y
   `intermedio`. Presionar **Iniciar misión**.
2. **Estación 1**: capturar `20-intermedio-estacion-1.png`. Debe verse el HUD
   con **Dificultad: intermedio** y la descripción breve debajo de cada
   enunciado.
3. Responder las 4 correctas. **Transición 1**: capturar
   `21-intermedio-transicion-1.png`. Presionar **Continuar**.
4. Recorrer las estaciones 2 a 5 sin capturas, respondiendo todo correcto.
5. **Final**: capturar `22-intermedio-final.png`.

No se usan ayudas ni respuestas incorrectas para que el final quede limpio.

### Intento C — completo, nivel `avanzado`

Objetivo: mostrar la estación avanzada y el final del nivel.

1. Volver a `/`. Completar `Equipo Demo Avanzado`, 3 integrantes y
   `avanzado`. Presionar **Iniciar misión**.
2. **Estación 1**: capturar `30-avanzado-estacion-1.png`. Debe verse la
   dificultad **avanzado** y las descripciones.
3. Recorrer las 5 estaciones respondiendo todo correcto, sin capturas
   intermedias.
4. **Final**: capturar `31-avanzado-final.png`.

Las transiciones ya se mostraron en los intentos A y B; no hace falta
repetirlas.

### Intento D — no completa por respuestas incorrectas

Objetivo: mostrar el estado intermedio (1 incorrecta) y la eliminación por
llegar a 2.

1. Volver a `/`. Completar `Equipo Demo Incorrectas`, 3 integrantes y
   `inicial`.
2. **Estación 1**: enviar **3 correctas y 1 incorrecta**. El servidor
   registra el envío, suma 1 incorrecta y vuelve a mostrar el formulario.
3. Capturar `40-incorrectas-estacion.png`: el HUD debe mostrar
   **Incorrectas 1 de 2** y **Envíos 1 de 2**, con el aviso de envíos
   realizados.
4. Enviar otro envío con **1 incorrecta** (puede ser la misma u otra
   pregunta). Al acumular 2 incorrectas, el intento se cierra y redirige a
   la eliminación.
5. Capturar `41-incorrectas-eliminado.png`: la pantalla debe explicar
   “Llegaron a 2 respuestas incorrectas” y mostrar el resumen del intento.

### Intento E — no completa por abandono

Objetivo: mostrar la eliminación por abandono.

1. Volver a `/`. Completar `Equipo Demo Abandono`, 3 integrantes y
   `intermedio`.
2. **Estación 1**: presionar **Abandonar**. El navegador abre el diálogo
   nativo “¿Abandonar el juego? El intento quedará cerrado.”. Aceptar.
3. Capturar `42-abandono-eliminado.png`: la pantalla debe explicar “El equipo
   abandonó el juego”.

El diálogo nativo no forma parte del HTML y no se puede capturar con
`take_screenshot`. En el documento final se transcribe el texto y se muestra
la pantalla resultante.

Variante opcional: abandonar desde la transición 1 después de superar la
estación. El resultado es la misma pantalla de eliminación y el botón está
en `transicion.html`.

### Intento F — no completa por tiempo agotado

Objetivo: mostrar el aviso de los 30 segundos y la eliminación por tiempo.

1. Volver a `/`. Completar `Equipo Demo Tiempo`, 3 integrantes y `avanzado`.
   Entrar a la estación 1.
2. En la base de capturas, adelantar el inicio del intento y de la estación
   para que queden **30 segundos**:

   ```sql
   -- Solo en escape_room_7b2026_capturas.
   UPDATE intento
   SET fecha_inicio = NOW(3) - INTERVAL 220 SECOND
   WHERE id = <INTENTO_ID>;

   UPDATE intento_estacion
   SET fecha_inicio = NOW(3) - INTERVAL 210 SECOND
   WHERE intento_id = <INTENTO_ID> AND estacion_id = <ESTACION_ID>;
   ```

3. Recargar la estación. El HUD debe mostrar `00:30` y el texto titilante
   **“¡Quedan 30 segundos!”**. Capturar `50-especial-aviso-30s.png` de
   inmediato, antes de que baje el contador. Si la animación deja el texto
   invisible en la foto (`steps(2, start)` alterna la opacidad), congelar solo
   la animación en el DOM antes de capturar:

   ```js
   () => {
     const aviso = document.querySelector(".aviso-30");
     if (aviso) aviso.style.animation = "none";
     return Boolean(aviso);
   }
   ```

   Es un ajuste de la captura, no un cambio en la app.
4. Atrasarlo más que la duración para forzar el cierre:

   ```sql
   UPDATE intento
   SET fecha_inicio = NOW(3) - INTERVAL 320 SECOND
   WHERE id = <INTENTO_ID>;

   UPDATE intento_estacion
   SET fecha_inicio = NOW(3) - INTERVAL 300 SECOND
   WHERE intento_id = <INTENTO_ID> AND estacion_id = <ESTACION_ID>;
   ```

5. Recargar la estación o consultar `/juego/estado`. El servidor cierra el
   intento como `por_tiempo` y redirige a la eliminación.
6. Capturar `43-tiempo-eliminado.png`: la pantalla debe explicar “Se terminó
   el tiempo de la estación”.

No se toca `duracion_estacion_segundos`: se manipula solo el inicio de la
estación en la base de capturas.

### Intento G — modo “solo finalizar” (opcional)

Con la configuración de la feria (`max_envios_estacion = 2` y
`max_respuestas_incorrectas = 2`), el modo “solo finalizar” **no se alcanza**:
el segundo envío con una incorrecta llega antes a la eliminación. Para
mostrarlo hay que cambiar temporalmente **una** clave en la base de capturas.

Opción recomendada (un solo cambio y el HUD conserva “Incorrectas 1 de 2”):

```sql
UPDATE configuracion SET valor = '1'
WHERE clave = 'max_envios_estacion';
```

1. Crear el intento `Equipo Demo Solo Finalizar` (`inicial`).
2. En la estación 1, enviar 3 correctas y 1 incorrecta. Con un solo envío
   permitido, el estado pasa a `solo_finalizar`.
3. Capturar `51-especial-solo-finalizar.png`: se ocultan el formulario, las
   ayudas y el abandono; queda solo **Finalizar juego**.
4. Presionar **Finalizar juego** y aceptar el diálogo. El intento se cierra
   como `por_respuestas_incorrectas`.
5. Restaurar la configuración:

   ```sql
   UPDATE configuracion SET valor = '2'
   WHERE clave = 'max_envios_estacion';
   ```

Si se prefiere no alterar la configuración, **omitir esta captura** y
documentar en el `.md` que el modo existe en el código y en las pruebas, pero
no es alcanzable con los valores de la feria.

## Estados especiales

### Estación no disponible (503)

Se provoca dejando una estación sin cobertura **antes** de crear el intento,
porque una selección ya congelada se sigue mostrando (decisión 22).

1. En la base de capturas, desactivar una pregunta `inicial` de la estación
   1. Como `inicial` tiene exactamente 4 preguntas por estación, sacar una
   deja 3 y la estación queda sin cobertura:

   ```sql
   UPDATE pregunta SET activo = 0 WHERE id = <PREGUNTA_ID>;
   ```

2. En `/`, crear el intento `Equipo Demo Sin Cobertura` con nivel `inicial`.
   El redirect a `/juego` intenta preparar la estación 1 y devuelve `503`
   con `estacion_no_disponible.html`.
3. Capturar `52-especial-503.png`.
4. Restaurar la pregunta:

   ```sql
   UPDATE pregunta SET activo = 1 WHERE id = <PREGUNTA_ID>;
   ```

5. Cerrar el intento por SQL, porque nunca llegó a crear
   `intento_estacion`:

   ```sql
   UPDATE intento
   SET finalizado = 'abandono', fecha_fin = NOW(3), puntaje_obtenido = NULL
   WHERE id = <INTENTO_ID>;
   ```

Esta captura va al final del recorrido porque modifica contenido. Si se
prefiere, se recrea la base de capturas después.

### Solicitud no válida (400)

Sin token CSRF, cualquier POST devuelve `400` antes de ejecutar la ruta. No
crea filas ni modifica datos.

1. Abrir cualquier página de la app.
2. Inyectar y enviar un formulario sin `_csrf`:

   ```js
   () => {
     const formulario = document.createElement("form");
     formulario.method = "POST";
     formulario.action = "/juego/estacion/1/responder";
     document.body.appendChild(formulario);
     formulario.submit();
     return true;
   }
   ```

3. Capturar `53-especial-400.png`.

La página `500` **no** se captura: exigiría romper la app a propósito.

### Reanudación

No tiene una pantalla propia: se documenta con texto.

- Recargar una estación mantiene las mismas 4 preguntas y los mismos
  tiempos.
- Salir y volver a entrar con el mismo nombre deriva a
  `/equipo/identificar`.
- Con un intento activo, `GET /` muestra el formulario con el aviso y el
  botón **Continuar**.

La captura de ese estado no está en la matriz: se documenta con texto para
no sumar una imagen que repite el formulario de la bienvenida.

## Administración

Usar las credenciales temporales del entorno de capturas. No capturar la
clave ni el hash en ninguna imagen.

Orden recomendado:

1. `/admin` sin sesión → `60-admin-login.png`.
2. Ingresar con `demo_capturas` y la clave temporal → `/admin/` →
   `61-admin-panel.png`.
3. `/admin/pregunta` → `62-admin-listado.png`.
4. `/admin/pregunta/nuevo` → `63-admin-nuevo.png`. No guardar; cancelar.
5. `/admin/pregunta/<id>` de una pregunta usada en los intentos →
   `64-admin-detalle.png`.
6. `/admin/pregunta/<id>/editar` → `65-admin-editar.png`. No guardar;
   cancelar.
7. `/admin/cobertura` → `66-admin-cobertura.png`.
8. `/admin/dificultades` **sin** intentos activos → `67-admin-dificultades.png`.
9. Crear el intento `Equipo Demo Activo` (`inicial`) y dejarlo en la
   estación 1. Volver a `/admin/dificultades` →
   `68-admin-dificultades-bloqueado.png`, con el aviso de que no se puede
   cambiar mientras hay equipos jugando.
10. `/admin/intentos-activos` → `69-admin-intentos-activos.png`.
11. `/admin/estadisticas` → `70-admin-estadisticas.png`. Con el intento
    activo, el gráfico debe incluir **En curso**.

La sesión del admin no toca `equipo_id` ni `intento_id` (decisión 46), así
que se puede volver al juego con el mismo navegador sin perder la sesión
administrativa.

Al terminar, el intento `Equipo Demo Activo` puede quedar abierto: la base de
capturas se descarta. No hace falta abandonarlo.

## Tiempos de las capturas

Se usan los tiempos reales del recorrido. No se normalizan fechas: los
contadores y el ranking muestran lo que realmente tardó la prueba.

Si se quiere una demo con tiempos más largos y parejos, se puede editar
**solo la base de capturas**, con estas precauciones:

- Hacerlo **después** de completar el intento y **antes** de capturar su
  final.
- Actualizar `intento.fecha_inicio`, `intento.fecha_fin` y
  `puntaje_obtenido` de forma coherente.
- Ajustar también `intento_estacion.fecha_inicio` y `fecha_fin` si se van a
  mostrar transiciones, para que no queden tiempos imposibles.
- Aclarar en el documento que los tiempos son sintéticos.

Patrón, solo en `escape_room_7b2026_capturas`:

```sql
-- Ejemplo: intento completo de 03:12 (192 segundos).
SET @t0 = '2026-11-12 09:00:00';

UPDATE intento
SET fecha_inicio = @t0,
    fecha_fin = DATE_ADD(@t0, INTERVAL 192 SECOND),
    puntaje_obtenido = 192
WHERE id = <INTENTO_ID> AND finalizado = 'completo';
```

No usar `puntaje_obtenido` para ordenar: el ranking ordena por tiempo,
incorrectas, ayudas, `fecha_inicio` e `id`. La normalización es solo estética.

## Estructura del documento final

Archivo: `docs/navegacion-capturas.md`.

```markdown
# Navegación con capturas — Escape Room 7.º B 2026

> Capturas tomadas a 300 × 800 px CSS (emulación angosta de móvil),
> con la app real y datos sintéticos. Los tiempos son los del recorrido
> de prueba.

## 1. Cómo leer este documento
- Qué es una captura de página completa y qué es una de viewport.
- Aclaración de 300 × 800 frente al Galaxy A55 real.
- Los diálogos nativos y el audio no se capturan.

## 2. Recorrido público
### 2.1 Bienvenida
### 2.2 Identificación de equipo
### 2.3 Ranking público
### 2.4 Estadísticas públicas

## 3. Recorrido completo · nivel inicial
### 3.1 Estación 1
### 3.2 Estación 2
### 3.3 Estación 3
### 3.4 Estación 4
### 3.5 Estación 5
### 3.6 Transición
### 3.7 Final

## 4. Recorrido completo · nivel intermedio
## 5. Recorrido completo · nivel avanzado
## 6. Intentos no completados
### 6.1 Por respuestas incorrectas
### 6.2 Por abandono
### 6.3 Por tiempo agotado
## 7. Estados especiales
### 7.1 Aviso de 30 segundos
### 7.2 Modo “solo finalizar”
### 7.3 Estación no disponible
### 7.4 Solicitud no válida
## 8. Administración
## 9. Pantallas de error
## 10. Resumen de rutas y estados
## 11. Cómo se generaron las capturas
```

Cada captura se presenta con:

- Título de la pantalla y ruta.
- Intento y estado (por ejemplo, “inicial, 1 incorrecta”).
- Qué muestra y qué acción sigue.
- La imagen embebida con `alt` en español.

Modelo de bloque:

```html
### Estación 1 · inicial

- **Ruta:** `/juego/estacion/1`
- **Intento:** `Equipo Demo Inicial`, nivel `inicial`.
- **Estado:** cuatro preguntas, sin envíos.
- **Siguiente:** marcar una opción por pregunta y **Comprobar respuestas**.

<p>
  <img src="capturas-navegacion/10-inicial-estacion-1.png"
       alt="Estación 1 de 5 del nivel inicial con el HUD, las cuatro preguntas y sus opciones"
       width="300" loading="lazy">
</p>
```

Reglas del documento:

- Rutas relativas a `docs/capturas-navegacion/`, nunca absolutas.
- `alt` descriptivo, en español rioplatense, sin nombres de archivo.
- No transcribir respuestas correctas ni resultados de las consultas SQL.
- No incluir credenciales, hashes, nombres reales ni datos personales.
- Aclarar que los equipos y los tiempos son de prueba.
- Enlazar `docs/navegacion-por-app.md` como mapa textual complementario.

## Presupuesto y optimización

| Grupo | Capturas | Peso estimado |
| --- | --- | --- |
| Público | 6 | 1,2 MB (incluye `05`, opcional) |
| Inicial | 9 | 1,8 MB (incluye `18`, opcional) |
| Intermedio y avanzado | 5 | 0,8 MB |
| No completados | 4 | 0,8 MB |
| Especiales | 4 | 0,6 MB (incluye `51`, opcional) |
| Admin | 11 | 2,0 MB |
| Error y TV | 2 | 0,5 MB |
| **Total** | **41** | **≈ 7,7 MB** |

Criterios:

- PNG, sin pérdida. Es texto de interfaz.
- Si una captura supera los 400 KB, optimizarla con `pngquant` u `oxipng`.
  Son herramientas de preparación, **no** dependencias del proyecto.
- No reducir el ancho por debajo de 300 px: se perdería legibilidad.
- Si el total supera los 10 MB, revisar primero las capturas de página
  completa más altas (panel y estadísticas del admin) antes de tocar las
  demás.

## Riesgos y trampas

| Riesgo | Prevención |
| --- | --- |
| Ejecutar las consultas en la base real | Verificar `SELECT DATABASE();` y `app.config["MYSQL_DB"]` antes de cada paso. |
| Cambiar el `.env` del repo | Usar variables en la línea de comandos; no editar `.env`. |
| Mezclar el servidor de desarrollo con el de capturas | Puerto 5056 y `curl /salud` antes de empezar. |
| Commitear credenciales temporales | No incluir la clave ni el hash en el `.md` ni en capturas. |
| Commitear el SQL temporal o un dump | Mantener `/tmp/opencode/capturas.sql` fuera del repo. |
| Capturar con el viewport equivocado | Verificar `innerWidth = 300` antes de la primera imagen. |
| Desborde horizontal | Comprobar `overflowX = false` en cada pantalla nueva. |
| Perder la sesión del intento | No cerrar el navegador ni el servidor entre estaciones. |
| `pageId` viejo tras reconectar | Volver a `list_pages()` y `emulate()`. |
| Diálogo de confirmación bloqueado | `handle_dialog` o `dialogAction: "accept"`. |
| El ranking se actualiza durante la captura | Capturar inmediatamente después de cargar. |
| No poder volver a una transición ya pasada | Capturar la transición en el momento exacto. |
| El final solo muestra el último intento de la sesión | Capturar el final antes de empezar otro intento. |
| La captura 503 no se reproduce | Desactivar la cobertura **antes** de crear el intento. |
| El modo “solo finalizar” no aparece | Es un estado de laboratorio; cambiar una clave y restaurarla. |
| Tiempos inconsistentes | No normalizar; si se hace, ajustar intento y estaciones juntos. |
| Capturas enormes | Usar `fullPage` con criterio y optimizar las más pesadas. |

## Proceso

1. Crear `docs/capturas-navegacion/` y verificar que está vacía.
2. Crear la base `escape_room_7b2026_capturas` desde la instantánea.
3. Confirmar la base y levantar la app en el puerto 5056 con credenciales
   temporales.
4. Abrir `chrome-devtools`, emular 300 × 800 y verificar viewport y
   desborde.
5. Capturar las pantallas públicas sin datos (bienvenida, error de
   validación, login del admin, 404).
6. Ejecutar el intento A (`inicial`) y capturar estaciones, transiciones y
   final.
7. Ejecutar el intento B (`intermedio`) y capturar estación 1, transición 1
   y final.
8. Ejecutar el intento C (`avanzado`) y capturar estación 1 y final.
9. Ejecutar el intento D (`incorrectas`) y capturar el estado intermedio y
   la eliminación.
10. Ejecutar el intento E (`abandono`) y capturar la eliminación.
11. Ejecutar el intento F (`tiempo`) y capturar el aviso de 30 segundos y la
    eliminación.
12. Opcional: intento G (`solo finalizar`) con el cambio temporal de
    `max_envios_estacion`.
13. Capturar el ranking público y las estadísticas públicas.
14. Capturar el admin, incluyendo los estados con y sin intentos activos.
15. Capturar el 503 y el 400.
16. Capturar la vista de TV a 1920 × 1080.
17. Revisar todas las imágenes: ancho 300, sin desbordes, sin datos
    personales, sin respuestas marcadas.
18. Escribir `docs/navegacion-capturas.md` con la estructura de arriba.
19. Verificar enlaces relativos y que todas las imágenes existan.
20. Actualizar `docs/argumentos-pasos/README.md` (estado `hecho`),
    `MEMORY.md` y, si corresponde, el índice de documentación de
    `README.md`.
21. Cerrar la app, eliminar la base de capturas y hacer el commit del
    entregable.

## Criterio de aceptación

- Existe `docs/navegacion-capturas.md` y se lee de punta a punta sin enlaces
  rotos.
- Existen todas las capturas obligatorias de la matriz, con nombres y rutas
  coherentes.
- Todas las capturas tienen **300 px de ancho** y ninguna desborda
  horizontalmente la página.
- El documento muestra las **cinco estaciones**, la transición, el final,
  el ranking, las estadísticas, el admin y las pantallas de error.
- Hay **tres intentos completos**, uno por nivel, y los tres finales se ven
  en el documento.
- Hay **tres intentos no completados**: por respuestas incorrectas, por
  abandono y por tiempo agotado.
- Se ven los estados de **1 incorrecta**, **2 incorrectas**, **aviso de 30
  segundos**, **abandono** y **tiempo agotado**.
- El modo “solo finalizar” se muestra o se explica por qué no se alcanza con
  la configuración de la feria.
- No hay respuestas correctas transcritas, credenciales, hashes ni nombres
  reales en el documento ni en las imágenes.
- La base real `escape_room_7b2026` no se tocó.
- No hay cambios en `app/`, `tests/`, `bd/` ni `requirements.txt`.
- `pytest -q` sigue pasando dos veces seguidas (no debería cambiar nada).
- La base `escape_room_7b2026_capturas` se eliminó al terminar.
- El peso total de `docs/capturas-navegacion/` es menor a 10 MB.

## Verificación

Comprobar las imágenes sin depender de ImageMagick:

```bash
ls -lh docs/capturas-navegacion | head -50
file docs/capturas-navegacion/*.png
du -sh docs/capturas-navegacion
```

`file` debe informar `PNG image data, 300 x <alto>` en todas. Si alguna
tiene otro ancho, se capturó con el viewport equivocado.

Si hay ImageMagick:

```bash
identify -format '%f %wx%h\n' docs/capturas-navegacion/*.png
```

Verificar el documento:

```bash
grep -n "capturas-navegacion/" docs/navegacion-capturas.md | wc -l
grep -n "docs/img\|/home/\|http://\|https://" docs/navegacion-capturas.md
```

No deben aparecer rutas absolutas ni imágenes de `docs/img/`.

Verificar que no se filtraron datos sensibles:

```bash
grep -ni "clave\|password\|hash\|demo_capturas" docs/navegacion-capturas.md
```

Solo deberían aparecer menciones genéricas al entorno de capturas, nunca la
clave ni el hash.

Comprobar que la app no cambió:

```bash
git status --short
git diff --stat
```

Solo deben aparecer `docs/navegacion-capturas.md`,
`docs/capturas-navegacion/`, este paso, el índice y `MEMORY.md`.

Pruebas automatizadas (opcional, porque no hay cambios de código):

```bash
.venv/bin/python -m pytest -q
.venv/bin/python -m pytest -q
```

Recorrido manual del documento:

| Qué mirar | Dónde |
| --- | --- |
| Las tres dificultades se ven en la bienvenida. | `00`. |
| El error de validación se lee sin salir del formulario. | `01`. |
| La identificación pide el ID y no revela datos. | `02`. |
| Las cinco estaciones tienen HUD, 4 preguntas y opciones. | `10`–`14`. |
| La transición 5 muestra el tiempo congelado y **Ver resultado**. | `16`. |
| Los tres finales muestran posición de nivel y ranking. | `17`, `22`, `31`. |
| La eliminación explica la causa correcta en cada caso. | `41`–`43`. |
| El aviso de 30 segundos se ve aunque no haya audio. | `50`. |
| El ranking público conserva las tablas si falla el polling. | `05`. |
| El admin se ve sin enlaces desde las páginas públicas. | `60`–`70`. |
| La vista de TV se lee a distancia. | `91`. |

## Fuera de alcance

- Cambiar rutas, plantillas, estilos, servicios, seeds o esquema.
- Agregar una pantalla o un modo “móvil” especial.
- Grabar video, GIF o audio.
- Usar un servicio externo, CDN o un dispositivo físico.
- Capturar la base real o datos de la feria.
- Capturar la página 500 rompiendo la app.
- Publicar respuestas correctas, credenciales o nombres reales.
- Agregar dependencias a `requirements.txt`.
- Versionar la base de capturas, su dump o el SQL temporal.
- Modificar `docs/escape-room.md`, los PDF o los prototipos.

## Ojo con

- **No** usar la base real. Antes de cada `UPDATE`, confirmar
  `SELECT DATABASE();`.
- **No** editar `.env` para apuntar a la base de capturas: usar variables de
  entorno en la línea de comandos.
- **No** commitear `/tmp/opencode/capturas.sql`, la clave temporal ni el
  hash.
- **No** copiar al `.md` el resultado de las consultas que traen
  `respuesta_id` o `r.contenido` de la correcta.
- **No** capturar terminales, formularios de login con la clave escrita ni
  el panel de MySQL.
- **No** asumir que 300 × 800 es el A55 real: es una emulación angosta.
- **No** capturar la quinta transición dos veces: ya está en `16`.
- **No** volver a una transición ya pasada: el servidor redirige a la
  estación actual.
- **No** esperar que el diálogo nativo salga en la captura: no es HTML.
- **No** dejar el intento “activo” abierto después de eliminar la base de
  capturas: la base se descarta completa.
- **No** normalizar tiempos a mitad del recorrido: se rompe la coherencia de
  los contadores.
- **No** optimizar las capturas con una herramienta que agregue una
  dependencia al proyecto.
- **No** subir capturas con scroll horizontal de página: las tablas tienen
  scroll interno y eso es correcto, pero la página no debe desbordar.
- **No** olvidar restaurar `max_envios_estacion`, la pregunta desactivada ni
  la cobertura después de las capturas especiales.
