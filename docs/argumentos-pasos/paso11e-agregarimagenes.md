# Paso 11e — Imágenes institucionales en la interfaz

> **Origen:** pedido posterior al `paso11d`, antes del `paso12`.
> **Tipo:** feat (interfaz).
> **Requiere:** `paso11d` aprobado.
> **Commit:** `feat: imágenes institucionales en la interfaz`.
>
> **Antes de empezar:** leé `AGENTS.md` (stack, estilos y reglas de
> contenido), `app/templates/base.html`, `app/templates/bienvenida.html`,
> `app/templates/ranking.html` y `app/static/css/publico.css`.

## Estado

Pendiente.

## Contexto

El repositorio ya tiene las imágenes institucionales en `docs/img/`, pero
**no se sirven desde la aplicación**:

- `docs/` es material de referencia, no una carpeta estática de Flask.
- Los originales pesan varios megabytes y no están optimizados para la web.
- La app debe funcionar **sin Internet**, así que no se puede depender de un
  CDN ni de una URL externa.

En este paso se copian **derivados optimizados** a `app/static/img/` y se usan
desde las plantillas con `url_for('static', ...)`. Los originales de
`docs/img/` **no se mueven, no se editan y no se borran**.

Imágenes que se usan en este paso:

| Archivo de origen | Uso |
| --- | --- |
| `docs/img/LogoCasta.png` | Favicon, logo de la página principal, logo del ranking y logo del pie de página. |
| `docs/img/frente-cole.png` | Foto de portada en la página inicial. |

El resto de `docs/img/` (`cartel-cole.png`, `escuela_oscuro.png`,
`informatica.png`, `Foto_PC.png`, etc.) queda **fuera de este paso**.

> Las medidas y los recortes de abajo se calcularon a partir de las
> dimensiones reales de los archivos. La composición final se revisa en el
> navegador antes de dar el paso por terminado.

## Decisión de diseño

| Pantalla | Imagen | Ubicación |
| --- | --- | --- |
| Todas | `logo-casta.png` | Logo chico en el pie de página, junto al texto institucional. |
| Página inicial (`/`) | `logo-casta.png` | Arriba del título, como marca de la escuela. |
| Página inicial (`/`) | `frente-cole.jpg` | Foto enmarcada entre el encabezado y el formulario. |
| Ranking (`/ranking`) | `logo-casta.png` | A la izquierda del título, con tamaño legible desde el televisor. |
| Todas | `favicon.ico` y `favicon-32.png` | Ícono de la pestaña del navegador. |
| Todas | `apple-touch-icon.png` | Ícono al guardar el sitio en la pantalla de inicio de un móvil. |

Criterios:

- El pie de página aparece en **todas** las pantallas porque vive en
  `base.html`; también en la página inicial y en el ranking, donde el logo ya
  se ve arriba.
- El logo es decorativo cuando está acompañado por el texto que nombra a la
  escuela (`alt=""`). Cuando es la única identificación, lleva `alt`
  descriptivo.
- Nada de texto dentro de la imagen: los títulos siguen siendo HTML.
- Sin animaciones, sin carruseles y sin cambios de contenido.

## Inventario de origen

| Archivo | Dimensiones | Peso | Formato |
| --- | --- | --- | --- |
| `docs/img/LogoCasta.png` | 1746 × 1738 | ≈ 0,9 MB | PNG RGBA (con transparencia) |
| `docs/img/frente-cole.png` | 3840 × 2880 | ≈ 4,5 MB | PNG RGBA |

El logo es casi cuadrado (1746 × 1738). La foto del frente es 4:3.

## Archivos a generar

| Archivo destino | Origen | Dimensiones | Peso esperado | Uso |
| --- | --- | --- | --- | --- |
| `app/static/img/logo-casta.png` | `LogoCasta.png` | 256 × 255 | ≈ 56 KB | Encabezados y pie. |
| `app/static/img/favicon-32.png` | `LogoCasta.png` | 32 × 32 | ≈ 3 KB | Pestaña del navegador. |
| `app/static/img/favicon.ico` | `LogoCasta.png` | 16, 32 y 48 | ≈ 15 KB | Compatibilidad con navegadores viejos. |
| `app/static/img/apple-touch-icon.png` | `LogoCasta.png` | 180 × 180 | ≈ 30 KB | Pantalla de inicio en iOS. |
| `app/static/img/frente-cole.jpg` | `frente-cole.png` | 1600 × 1200 | ≈ 60 KB | Portada de la página inicial. |

Presupuesto total: **menos de 200 KB** para todas las imágenes nuevas. No se
copian los originales de 0,9 MB y 4,5 MB.

## Preparación de los archivos

Desde la raíz del proyecto, con **ImageMagick** instalado:

```bash
mkdir -p app/static/img

# Logo para encabezados y pie (conserva la transparencia).
convert docs/img/LogoCasta.png \
  -resize 256x256 \
  -strip -define png:compression-level=9 \
  app/static/img/logo-casta.png

# Favicon PNG de 32 px.
convert docs/img/LogoCasta.png \
  -resize 32x32 \
  -strip -define png:compression-level=9 \
  app/static/img/favicon-32.png

# Favicon .ico con tres tamaños.
convert docs/img/LogoCasta.png \
  -background white -alpha remove -alpha off \
  -define icon:auto-resize=48,32,16 \
  -strip \
  app/static/img/favicon.ico

# Ícono para iOS: cuadrado, con fondo blanco.
convert docs/img/LogoCasta.png \
  -resize '180x180^' -gravity center -extent 180x180 \
  -background white -alpha remove -alpha off \
  -strip -define png:compression-level=9 \
  app/static/img/apple-touch-icon.png

# Foto de portada: se achica a 1600 px de ancho y se convierte a JPEG.
convert docs/img/frente-cole.png \
  -resize '1600x1200>' \
  -background white -alpha remove -alpha off \
  -quality 82 -strip \
  app/static/img/frente-cole.jpg
```

Notas:

- En ImageMagick 7 el comando es `magick` en lugar de `convert`. El resto de
  los argumentos es igual.
- `-alpha remove -alpha off` aplana la transparencia sobre blanco. Es
  necesario para el `.ico`, el ícono de iOS y el JPEG: si no, el fondo puede
  quedar negro.
- El logo de encabezados **sí conserva** la transparencia.
- El original de la foto no se toca: solo se lee.

Si no hay ImageMagick, se pueden generar los mismos archivos con Pillow desde
un Python del sistema. **No agregar Pillow a `requirements.txt`**: es una
herramienta de preparación, no una dependencia de la aplicación.

```python
from PIL import Image

logo = Image.open("docs/img/LogoCasta.png").convert("RGBA")
logo.resize((256, 255), Image.LANCZOS).save(
    "app/static/img/logo-casta.png", optimize=True
)
logo.resize((32, 32), Image.LANCZOS).save(
    "app/static/img/favicon-32.png", optimize=True
)
logo.save(
    "app/static/img/favicon.ico",
    sizes=[(16, 16), (32, 32), (48, 48)],
)

cuadrado = Image.new("RGB", (180, 180), "white")
copia = logo.copy()
copia.thumbnail((180, 180), Image.LANCZOS)
cuadrado.paste(copia, ((180 - copia.width) // 2, (180 - copia.height) // 2), copia)
cuadrado.save("app/static/img/apple-touch-icon.png", optimize=True)

frente = Image.open("docs/img/frente-cole.png").convert("RGBA")
fondo = Image.new("RGB", frente.size, "white")
fondo.paste(frente, mask=frente.split()[3])
fondo.thumbnail((1600, 1200), Image.LANCZOS)
fondo.save("app/static/img/frente-cole.jpg", quality=82, optimize=True)
```

Comprobar los resultados:

```bash
ls -lh app/static/img
file app/static/img/*
```

## Cambios en las plantillas

### 1. `app/templates/base.html`

En el `<head>`, después del Bootstrap, agregar los íconos y la hoja de estilos
institucional:

```jinja
<link rel="icon" href="{{ url_for('static', filename='img/favicon.ico') }}" sizes="any">
<link rel="icon" type="image/png" sizes="32x32"
      href="{{ url_for('static', filename='img/favicon-32.png') }}">
<link rel="apple-touch-icon" sizes="180x180"
      href="{{ url_for('static', filename='img/apple-touch-icon.png') }}">
<link rel="stylesheet" href="{{ url_for('static', filename='css/institucional.css') }}">
```

Reemplazar el pie de página actual por:

```jinja
<footer class="container py-3 text-body-secondary small">
  <div class="d-flex flex-wrap align-items-center justify-content-center gap-2 text-center">
    <img
      src="{{ url_for('static', filename='img/logo-casta.png') }}"
      alt=""
      width="32"
      height="32"
      class="footer-logo"
      loading="lazy"
      decoding="async"
    >
    <span>Escape Room 7.º B 2026 · IPEATyM 186 Castagnari</span>
  </div>
</footer>
```

`alt=""` es correcto: el texto de al lado ya nombra a la escuela y repetirlo
en el lector de pantalla no aporta nada.

### 2. `app/templates/bienvenida.html`

En el encabezado centrado, antes del `<h1>`, agregar el logo:

```jinja
<img
  src="{{ url_for('static', filename='img/logo-casta.png') }}"
  alt="Logo del IPEATyM 186 Castagnari"
  width="128"
  height="128"
  class="bienvenida__logo mb-3"
  decoding="async"
>
```

Entre el encabezado y el primer aviso o tarjeta, agregar la foto:

```jinja
<figure class="bienvenida__frente mb-4">
  <img
    src="{{ url_for('static', filename='img/frente-cole.jpg') }}"
    alt="Frente del edificio del IPEATyM 186 Castagnari"
    width="1600"
    height="1200"
    class="img-fluid rounded shadow-sm"
    decoding="async"
  >
</figure>
```

La foto va **arriba del formulario** para que no empuje los campos fuera de
pantalla en el móvil. `width` y `height` evitan el salto de maquetado mientras
carga.

### 3. `app/templates/ranking.html`

Envolver el título con el logo:

```jinja
<header class="ranking__cabecera">
  <div class="ranking__marca">
    <img
      src="{{ url_for('static', filename='img/logo-casta.png') }}"
      alt=""
      width="96"
      height="96"
      class="ranking__logo"
      decoding="async"
    >
    <h1 class="ranking__titulo">Ranking Escape Room 7.º B</h1>
  </div>
  <p class="ranking__actualizacion" aria-live="polite">
    ...
  </p>
  <p class="ranking__vacio" id="ranking-vacio" {% if hay_filas %}hidden{% endif %}>
    ...
  </p>
</header>
```

No cambiar el resto de la cabecera ni el contenido de las tablas. En el
ejemplo, los `...` representan el contenido actual de esos párrafos. El polling
de `ranking.js` reemplaza solo las filas: el logo queda fijo.

## Estilos

Crear `app/static/css/institucional.css`:

```css
/* Imágenes institucionales compartidas por todas las pantallas. */

.footer-logo {
  height: 2rem;
  width: auto;
}

.bienvenida__logo {
  height: clamp(5rem, 14vw, 8rem);
  width: auto;
}

.bienvenida__frente {
  max-width: 42rem;
  margin-inline: auto;
}

.bienvenida__frente img {
  display: block;
  width: 100%;
  height: auto;
}
```

En `app/static/css/publico.css`, agregar el logo del ranking y alinear la
cabecera:

```css
.ranking__cabecera {
  align-items: center; /* antes: baseline */
}

.ranking__marca {
  display: flex;
  align-items: center;
  gap: clamp(0.6rem, 1.2vw, 1.25rem);
  min-width: 0;
}

.ranking__logo {
  flex-shrink: 0;
  height: clamp(3.5rem, 7vw, 7rem);
  width: auto;
}
```

El `clamp()` hace que el logo crezca en el televisor y no ocupe media pantalla
en el móvil. No hace falta un media query extra.

## Accesibilidad y rendimiento

- Toda imagen lleva `alt`. Es vacío solo cuando el texto de al lado ya
  identifica a la escuela.
- Todas llevan `width` y `height` para reservar el espacio y evitar saltos.
- La foto de portada y el logo del ranking se cargan sin `loading="lazy"`
  porque están arriba del pliegue. El logo del pie usa `loading="lazy"` y
  `decoding="async"`.
- Ninguna imagen es un botón ni tiene texto esencial: si no carga, la pantalla
  sigue siendo comprensible.
- No se usa `background-image` para contenido informativo.
- Los archivos se sirven desde `app/static/` con `url_for`, nunca desde
  `docs/` ni desde una URL absoluta.

## Pruebas

Agregar a `tests/test_publico.py`:

```python
def test_imagenes_institucionales_locales(cliente):
    inicio = cliente.get("/").get_data(as_text=True)
    assert "img/logo-casta.png" in inicio
    assert "img/frente-cole.jpg" in inicio

    ranking = cliente.get("/ranking").get_data(as_text=True)
    assert "img/logo-casta.png" in ranking

    for ruta in (
        "/static/img/logo-casta.png",
        "/static/img/favicon.ico",
        "/static/img/favicon-32.png",
        "/static/img/apple-touch-icon.png",
        "/static/img/frente-cole.jpg",
    ):
        respuesta = cliente.get(ruta)
        assert respuesta.status_code == 200
        assert respuesta.mimetype.startswith("image/")


def test_pie_con_logo_en_todas_las_pantallas(cliente):
    for ruta in ("/", "/ranking", "/estadisticas", "/admin", "/no-existe"):
        html = cliente.get(ruta).get_data(as_text=True)
        assert "footer-logo" in html
```

- No comparar bytes ni dimensiones exactas: alcanza con que el archivo exista,
  se sirva como imagen y la plantilla lo referencie.
- No agregar asserts sobre colores ni sobre el contenido visual.
- `pytest -q` debe pasar dos veces seguidas.

## Proceso

1. Generar los cinco archivos en `app/static/img/` con los comandos de arriba.
2. Revisar los pesos con `ls -lh`; si alguno se pasa del presupuesto, volver a
   comprimir antes de seguir.
3. Editar `base.html`, `bienvenida.html`, `ranking.html`,
   `app/static/css/institucional.css` y `publico.css`.
4. Agregar los tests a `tests/test_publico.py`.
5. Correr `pytest -q` dos veces.
6. Recorrer la app en el navegador y revisar el resultado en móvil y en
   pantalla grande (ver **Verificación**).
7. Actualizar `README.md` (árbol de `static/img/` y, si corresponde, la tabla
   de funcionalidad), `docs/navegacion-por-app.md` (elementos de bienvenida,
   ranking y pie) y `MEMORY.md`.
8. Si el docente lo aprueba, agregar a `AGENTS.md` una decisión: las imágenes
   institucionales viven en `app/static/img/`, se sirven localmente y los
   originales quedan en `docs/img/`.
9. Verificar que la fila de este paso ya está en
   `docs/argumentos-pasos/README.md`, marcarla como `hecho` al terminar y hacer
   el commit.

## Criterio de aceptación

- El ícono de la pestaña se ve en `/`, `/ranking` y `/admin` después de una
  recarga forzada.
- La página inicial muestra el logo de la escuela y la foto del frente sin
  desbordes ni recortes raros.
- El ranking muestra el logo a la izquierda del título y se lee bien desde la
  distancia del televisor; en el móvil no tapa el título ni la actualización.
- El pie de página muestra el logo chico en todas las pantallas que heredan de
  `base.html`.
- Las cinco imágenes responden `200` desde `/static/img/` y ninguna se carga
  desde un CDN o desde `docs/`.
- El peso total de las imágenes nuevas es menor a 200 KB.
- La app sigue funcionando sin Internet.
- `pytest -q` pasa dos veces seguidas.
- `docs/img/` queda intacto.

## Verificación

```bash
ls -lh app/static/img
file app/static/img/*

curl -I http://127.0.0.1:5000/static/img/logo-casta.png
curl -I http://127.0.0.1:5000/static/img/frente-cole.jpg
curl -I http://127.0.0.1:5000/static/img/favicon.ico

.venv/bin/python -m pytest -q
.venv/bin/python -m pytest -q
```

Recorrido manual:

| Pantalla | Qué mirar |
| --- | --- |
| `/` | Favicon en la pestaña, logo arriba del título, foto del frente antes del formulario. |
| `/ranking` | Logo junto al título, legible de lejos; tablas y polling sin cambios. |
| `/estadisticas` | Pie con logo. |
| Estación de juego | Pie con logo; no se tapa el HUD ni los contadores. |
| `/admin` | Pie con logo; el login y el panel se siguen viendo bien. |
| 404 | Pie con logo. |
| Móvil (360 px) | Logo y foto proporcionados; el formulario queda cerca del inicio. |
| TV (1920 px) | Logo del ranking grande y nítido, sin empujar la tabla. |
| Sin red | Recargar con DevTools en modo offline: las imágenes siguen apareciendo. |

Para el favicon, usar **Ctrl+Shift+R** o abrir una ventana nueva: el navegador
cachea el ícono con mucha insistencia.

## Fuera de alcance

- Usar el resto de `docs/img/` (`cartel-cole.png`, `escuela_oscuro.png`,
  `informatica.png`, etc.).
- Galerías, carruseles, videos o imágenes de fondo.
- Subir imágenes desde `/admin`.
- Cambiar el logo por nivel, por estación o por estado del juego.
- Generar imágenes con un paso de build o con un servicio externo.
- Modificar el esquema, las rutas, los servicios o las reglas del juego.
- Cambiar textos, colores de Bootstrap o el diseño general.
- Agregar dependencias a `requirements.txt` o usar un CDN.

## Ojo con

- **No** usar `docs/img/...` como `src` de una plantilla: Flask no sirve esa
  carpeta.
- **No** copiar los originales completos a `app/static/`: 5,4 MB entre los dos
  archivos es demasiado para la red del aula.
- El logo no es exactamente cuadrado (1746 × 1738). No forzar `width` y
  `height` distintos en el HTML sin dejar que el CSS mantenga la proporción.
- La transparencia del logo se ve bien sobre fondo claro; para `.ico`, iOS y
  JPEG hay que aplanarla sobre blanco.
- El pie de página se comparte con el admin: no agregar ahí datos del juego ni
  enlaces públicos nuevos.
- El polling del ranking no debe tocar la cabecera ni el logo.
- Mantener los `alt` en español rioplatense y sin nombres de archivo.
- Si se cambia una imagen más adelante, actualizar también el derivado y
  volver a correr los tests; el original de `docs/img/` no se toca.
- No romper la regla de funcionamiento sin Internet: todo tiene que estar en
  `app/static/`.
