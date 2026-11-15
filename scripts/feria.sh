#!/usr/bin/env bash
# Levanta la app para la feria del 16/11/2026 con el servidor de Flask.
#
# Uso:
#   ./scripts/feria.sh
#   ./scripts/feria.sh --port=5001
#
# Requiere python3 y el archivo .env en la raíz del proyecto.
# La primera vez crea el entorno virtual feria2026/ e instala dependencias.
# Después arranca sin instalar nada, aunque no haya Internet.

set -euo pipefail

RAIZ="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$RAIZ"

ENTORNO="$RAIZ/feria2026"
PYTHON="$ENTORNO/bin/python"

if [ ! -f "$RAIZ/.env" ]; then
  echo "Falta el archivo .env en $RAIZ." >&2
  echo "Copiá .env.example y completá los valores reales antes de arrancar." >&2
  exit 1
fi

PERMISOS="$(stat -c '%a' "$RAIZ/.env" 2>/dev/null || true)"
if [ -n "$PERMISOS" ] && [ "$PERMISOS" != "600" ]; then
  echo "Aviso: .env tiene permisos $PERMISOS. Se recomienda 600: chmod 600 .env" >&2
fi

if ! command -v python3 >/dev/null 2>&1; then
  echo "No se encontró python3. Instalalo antes de arrancar la feria." >&2
  exit 1
fi

if [ ! -x "$PYTHON" ]; then
  echo "Creando el entorno virtual en feria2026/ ..."
  if ! python3 -m venv "$ENTORNO"; then
    echo "No se pudo crear el entorno virtual." >&2
    echo "En Ubuntu/Debian instalá python3-venv: sudo apt install python3-venv" >&2
    exit 1
  fi
fi

if ! "$PYTHON" -c "import flask, pymysql, dotenv" >/dev/null 2>&1; then
  echo "Instalando dependencias en feria2026/ ..."
  "$PYTHON" -m pip install --upgrade pip
  "$PYTHON" -m pip install -r "$RAIZ/requirements.txt"
fi

IPS="$(hostname -I 2>/dev/null || true)"
IP="$(printf '%s\n' "$IPS" | awk '{print $1}')"

PUERTO="5000"
ARGUMENTO_ANTERIOR=""
for argumento in "$@"; do
  case "$argumento" in
    --port=*) PUERTO="${argumento#--port=}" ;;
  esac
  if [ "$ARGUMENTO_ANTERIOR" = "--port" ]; then
    PUERTO="$argumento"
  fi
  ARGUMENTO_ANTERIOR="$argumento"
done

echo "Servidor de la feria: http://${IP:-IP-DE-LA-NOTEBOOK}:${PUERTO}"
if [ -n "$IPS" ] && [ "$(printf '%s\n' "$IPS" | wc -w)" -gt 1 ]; then
  echo "Interfaces detectadas: $IPS (usá la de la red del aula)."
fi
echo "Abrí esa dirección desde las otras notebooks y el televisor."
echo "Para cerrar, presioná Ctrl+C en esta terminal."

exec "$PYTHON" -m flask --app app run --debug --host=0.0.0.0 "$@"
