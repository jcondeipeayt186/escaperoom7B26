#!/usr/bin/env bash
# Genera un respaldo de la base del Escape Room 7.º B 2026.
#
# Uso:
#   ./scripts/backup.sh [directorio_destino]
#
# Lee la conexión de .env (o de ENV_FILE). No evalúa el archivo con `source`
# porque ADMIN_PASSWORD_HASH contiene `$` y rompería la shell.
#
# El respaldo se genera sin `--databases`: no incluye CREATE DATABASE ni USE.
# Así se restaura siempre en una base elegida a mano.

set -euo pipefail

RAIZ="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ENV_FILE="${ENV_FILE:-$RAIZ/.env}"
DESTINO="${1:-$HOME/backups-escaperoom}"

leer_env() {
    local clave="$1"
    local valor
    valor="$(grep -E "^[[:space:]]*${clave}=" "$ENV_FILE" 2>/dev/null | tail -n 1 | cut -d= -f2- || true)"
    valor="${valor%$'\r'}"
    if [[ ${#valor} -ge 2 ]]; then
        if [[ "${valor:0:1}" == '"' && "${valor: -1}" == '"' ]]; then
            valor="${valor:1:${#valor}-2}"
        elif [[ "${valor:0:1}" == "'" && "${valor: -1}" == "'" ]]; then
            valor="${valor:1:${#valor}-2}"
        fi
    fi
    printf '%s' "$valor"
}

if [[ ! -f "$ENV_FILE" ]]; then
    echo "No existe $ENV_FILE. Copiá .env.example a .env y completalo." >&2
    exit 1
fi

MYSQL_HOST="$(leer_env MYSQL_HOST)"
MYSQL_PORT="$(leer_env MYSQL_PORT)"
MYSQL_USER="$(leer_env MYSQL_USER)"
MYSQL_PASSWORD="$(leer_env MYSQL_PASSWORD)"
MYSQL_DB="$(leer_env MYSQL_DB)"

: "${MYSQL_HOST:?Falta MYSQL_HOST en $ENV_FILE}"
: "${MYSQL_PORT:?Falta MYSQL_PORT en $ENV_FILE}"
: "${MYSQL_USER:?Falta MYSQL_USER en $ENV_FILE}"
: "${MYSQL_DB:?Falta MYSQL_DB en $ENV_FILE}"

if command -v mysqldump >/dev/null 2>&1; then
    MYSQLDUMP="mysqldump"
elif command -v mariadb-dump >/dev/null 2>&1; then
    MYSQLDUMP="mariadb-dump"
else
    echo "No se encontró mysqldump ni mariadb-dump en el PATH." >&2
    exit 1
fi

mkdir -p "$DESTINO"

UMASK_ORIGINAL="$(umask)"
umask 077
DEFAULTS="$(mktemp)"
trap 'rm -f "$DEFAULTS"' EXIT
chmod 600 "$DEFAULTS"

escapar_opcion() {
    printf '%s' "$1" | sed 's/\\/\\\\/g; s/"/\\"/g'
}

{
    echo "[client]"
    echo "host=$MYSQL_HOST"
    echo "port=$MYSQL_PORT"
    echo "user=$MYSQL_USER"
    echo "password=\"$(escapar_opcion "$MYSQL_PASSWORD")\""
} > "$DEFAULTS"

ARCHIVO="$DESTINO/respaldo-${MYSQL_DB}-$(date +%Y%m%d-%H%M%S).sql"

# --no-tablespaces existe en MySQL 8 y en las versiones recientes de MariaDB.
# Se agrega solo si la herramienta lo soporta.
TABLESPACES=""
if "$MYSQLDUMP" --help 2>/dev/null | grep -q -- "--no-tablespaces"; then
    TABLESPACES="--no-tablespaces"
fi

"$MYSQLDUMP" \
    --defaults-extra-file="$DEFAULTS" \
    --single-transaction \
    $TABLESPACES \
    --default-character-set=utf8mb4 \
    "$MYSQL_DB" > "$ARCHIVO"

if [[ ! -s "$ARCHIVO" ]]; then
    echo "El respaldo quedó vacío: $ARCHIVO" >&2
    exit 1
fi

chmod 600 "$ARCHIVO"
umask "$UMASK_ORIGINAL"

echo "Respaldo generado: $ARCHIVO"
echo "Tamaño: $(du -h "$ARCHIVO" | cut -f1)"
