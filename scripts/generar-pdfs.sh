#!/usr/bin/env bash
# Genera docs/pdf/ a partir de los .md del proyecto.
#
# Uso:
#   ./scripts/generar-pdfs.sh                 # todos los .md de documentación
#   ./scripts/generar-pdfs.sh README.md docs/guia-de-estudio-para-estudiantes.md
#
# Requiere pandoc y Google Chrome (o Chromium) instalados. No usa Internet.
# Deja un PDF por cada .md, respetando la ruta, más docs/pdf/00-indice.pdf.
# Las imágenes relativas de los .md se resuelven con un <base href>.

set -euo pipefail

RAIZ="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SALIDA="$RAIZ/docs/pdf"

if ! command -v pandoc >/dev/null 2>&1; then
  echo "Falta pandoc. En Ubuntu/Debian: sudo apt install pandoc" >&2
  exit 1
fi

NAVEGADOR=""
for candidato in google-chrome chromium chromium-browser google-chrome-stable; do
  if command -v "$candidato" >/dev/null 2>&1; then
    NAVEGADOR="$candidato"
    break
  fi
done
if [ -z "$NAVEGADOR" ]; then
  echo "Falta Google Chrome o Chromium para imprimir los PDF." >&2
  exit 1
fi

if [ "$#" -gt 0 ]; then
  ARCHIVOS=()
  for archivo in "$@"; do
    if [[ "$archivo" = /* ]]; then
      ARCHIVOS+=("$archivo")
    else
      ARCHIVOS+=("$RAIZ/$archivo")
    fi
  done
else
  mapfile -t ARCHIVOS < <(
    find "$RAIZ" -name '*.md' \
      -not -path '*/.venv*' \
      -not -path '*/feria2026/*' \
      -not -path '*/.pytest_cache/*' \
      -not -path '*/.agents/*' \
      -not -path '*/.opencode/*' \
      -not -path "$RAIZ/docs/pdf/*" \
      | sort
  )
fi

if [ "${#ARCHIVOS[@]}" -eq 0 ]; then
  echo "No hay archivos .md para convertir." >&2
  exit 1
fi

TEMPORAL="$(mktemp -d)"
trap 'rm -rf "$TEMPORAL"' EXIT

cat > "$TEMPORAL/estilo.css" <<'CSS'
@page { size: A4; margin: 16mm 14mm 18mm; }
html { font-size: 10.5pt; }
body { font-family: "DejaVu Sans", "Liberation Sans", system-ui, sans-serif;
       line-height: 1.45; color: #1f2328; }
h1 { font-size: 20pt; margin: 0 0 .6em; padding-bottom: .3em;
     border-bottom: 2px solid #cfd8dc; }
h2 { font-size: 15pt; margin: 1.5em 0 .5em; padding-bottom: .15em;
     border-bottom: 1px solid #e1e4e8; page-break-after: avoid; }
h3 { font-size: 12.5pt; margin: 1.2em 0 .4em; page-break-after: avoid; }
h4 { font-size: 11pt; margin: 1em 0 .3em; page-break-after: avoid; }
h5, h6 { font-size: 10.5pt; page-break-after: avoid; }
p, li { orphans: 3; widows: 3; }
ul, ol { padding-left: 1.5em; }
table { border-collapse: collapse; width: 100%; margin: .9em 0;
        font-size: 8.5pt; }
thead { display: table-header-group; }
tr { page-break-inside: avoid; }
th, td { border: 1px solid #cfd8dc; padding: 3px 5px; text-align: left;
         vertical-align: top; }
th { background: #eef2f5; font-weight: 600; }
code { font-family: "DejaVu Sans Mono", monospace; font-size: 8.8pt;
       background: #f4f6f8; padding: 0 .2em; border-radius: 3px; }
pre { background: #f6f8fa; border: 1px solid #e1e4e8; padding: 8px;
      font-size: 8.4pt; white-space: pre-wrap; overflow-wrap: anywhere;
      page-break-inside: avoid; }
pre code { background: none; padding: 0; }
blockquote { margin: 1em 0; padding: .3em 1em; border-left: 4px solid #9bb7cc;
             background: #f7fafc; }
img { max-width: 100%; height: auto; }
a { color: #0b5394; text-decoration: none; }
hr { border: 0; border-top: 1px solid #d0d7de; margin: 1.5em 0; }
CSS

generar_pdf() {
  local origen="$1"
  local relativo="${origen#"$RAIZ"/}"
  local destino="$SALIDA/${relativo%.md}.pdf"
  local carpeta
  carpeta="$(dirname "$origen")"

  mkdir -p "$(dirname "$destino")"

  printf '<base href="file://%s/">\n' "$carpeta" > "$TEMPORAL/base.html"
  pandoc "$origen" \
    --from=gfm \
    --to=html5 \
    --standalone \
    --self-contained \
    --resource-path="$carpeta:$RAIZ" \
    --css "$TEMPORAL/estilo.css" \
    --include-in-header "$TEMPORAL/base.html" \
    --metadata lang=es-AR \
    --metadata title="$relativo" \
    --output "$TEMPORAL/doc.html"

  "$NAVEGADOR" \
    --headless=new \
    --disable-gpu \
    --no-sandbox \
    --allow-file-access-from-files \
    --user-data-dir="$TEMPORAL/chrome" \
    --no-pdf-header-footer \
    --virtual-time-budget=10000 \
    --print-to-pdf="$destino" \
    "file://$TEMPORAL/doc.html" >/dev/null 2>&1

  if [ ! -s "$destino" ]; then
    echo "ERROR: no se generó $destino" >&2
    return 1
  fi
  return 0
}

echo "Generando PDFs en $SALIDA ..."
FALLOS=0
for archivo in "${ARCHIVOS[@]}"; do
  if [ ! -f "$archivo" ]; then
    echo "ERROR: no existe $archivo" >&2
    FALLOS=$((FALLOS + 1))
    continue
  fi
  relativo="${archivo#"$RAIZ"/}"
  printf '  %s\n' "$relativo"
  if ! generar_pdf "$archivo"; then
    FALLOS=$((FALLOS + 1))
  fi
done

# Índice con enlaces a todos los PDF generados.
listar_pdfs() {
  find "$SALIDA" -name '*.pdf' -not -name '00-indice.pdf' | sort
}

{
  echo "# Documentación en PDF"
  echo
  echo "Documentación del proyecto en formato PDF. Se genera desde los"
  echo "archivos \`.md\` con \`./scripts/generar-pdfs.sh\`."
  echo
  echo "Generado el $(date +%d/%m/%Y)."
  echo
  echo "## Documentos"
  echo
  while IFS= read -r pdf; do
    relativo="${pdf#"$SALIDA"/}"
    origen="$RAIZ/${relativo%.pdf}.md"
    titulo=""
    if [ -f "$origen" ]; then
      titulo="$(sed -n 's/^# //p' "$origen" | head -n 1)"
    fi
    if [ -z "$titulo" ]; then
      titulo="$relativo"
    fi
    echo "- [$titulo]($relativo)"
  done < <(listar_pdfs)
  echo
} > "$TEMPORAL/indice.md"

printf '<base href="file://%s/">\n' "$SALIDA" > "$TEMPORAL/base.html"
pandoc "$TEMPORAL/indice.md" \
  --from=gfm \
  --to=html5 \
  --standalone \
  --self-contained \
  --css "$TEMPORAL/estilo.css" \
  --include-in-header "$TEMPORAL/base.html" \
  --metadata lang=es-AR \
  --metadata title="Documentación en PDF (índice)" \
  --output "$TEMPORAL/indice.html"

"$NAVEGADOR" \
  --headless=new \
  --disable-gpu \
  --no-sandbox \
  --allow-file-access-from-files \
  --user-data-dir="$TEMPORAL/chrome" \
  --no-pdf-header-footer \
  --virtual-time-budget=10000 \
  --print-to-pdf="$SALIDA/00-indice.pdf" \
  "file://$TEMPORAL/indice.html" >/dev/null 2>&1

TOTAL="$(listar_pdfs | wc -l)"
TAMANO="$(du -sh "$SALIDA" | cut -f1)"
echo
echo "PDFs generados: $TOTAL (+ índice) en docs/pdf/ ($TAMANO)."
if [ "$FALLOS" -gt 0 ]; then
  echo "Fallaron $FALLOS archivos." >&2
  exit 1
fi
