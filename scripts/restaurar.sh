#!/usr/bin/env bash
# Restaura un respaldo del Escape Room 7.º B 2026 en una base elegida.
#
# Uso:
#   ./scripts/restaurar.sh <respaldo.sql> [base_destino] [--force]
#
# Sin base_destino, crea una nueva con el nombre:
#   <MYSQL_DB>_restore_AAAAMMDD-HHMMSS
#
# Por seguridad:
#   * No restaura sobre MYSQL_DB sin --force.
#   * No restaura sobre una base que ya existe sin --force.
#   * Rechaza volcados que traigan CREATE DATABASE o USE, salvo --force.
#
# Lee la conexión de .env (o de ENV_FILE). No usa `source` porque
# ADMIN_PASSWORD_HASH contiene `$` y rompería la shell.

set -euo pipefail

RAIZ="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ENV_FILE="${ENV_FILE:-$RAIZ/.env}"

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

uso() {
    echo "Uso: $0 <respaldo.sql> [base_destino] [--force]" >&2
    echo "" >&2
    echo "  base_destino  por defecto: \${MYSQL_DB}_restore_AAAAMMDD-HHMMSS" >&2
    echo "  --force       permite pisar MYSQL_DB o una base existente" >&2
}

if [[ $# -lt 1 ]]; then
    uso
    exit 1
fi

ARCHIVO="$1"
shift

BASE_DESTINO=""
FORZAR=0

for argumento in "$@"; do
    case "$argumento" in
        --force)
            FORZAR=1
            ;;
        -*)
            echo "Opción desconocida: $argumento" >&2
            uso
            exit 1
            ;;
        *)
            if [[ -n "$BASE_DESTINO" ]]; then
                echo "Sobra el argumento: $argumento" >&2
                uso
                exit 1
            fi
            BASE_DESTINO="$argumento"
            ;;
    esac
done

if [[ ! -f "$ARCHIVO" ]]; then
    echo "No existe el respaldo: $ARCHIVO" >&2
    exit 1
fi

if [[ ! -s "$ARCHIVO" ]]; then
    echo "El respaldo está vacío: $ARCHIVO" >&2
    exit 1
fi

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

if command -v mysql >/dev/null 2>&1; then
    MYSQL_CLIENT="mysql"
elif command -v mariadb >/dev/null 2>&1; then
    MYSQL_CLIENT="mariadb"
else
    echo "No se encontró mysql ni mariadb en el PATH." >&2
    exit 1
fi

if [[ -z "$BASE_DESTINO" ]]; then
    BASE_DESTINO="${MYSQL_DB}_restore_$(date +%Y%m%d-%H%M%S)"
fi

if [[ ! "$BASE_DESTINO" =~ ^[A-Za-z0-9_]+$ ]]; then
    echo "Nombre de base inválido: $BASE_DESTINO" >&2
    echo "Usá solo letras, números y guion bajo." >&2
    exit 1
fi

if [[ "$BASE_DESTINO" == "$MYSQL_DB" && "$FORZAR" -ne 1 ]]; then
    echo "Negado: la base destino es la base real ($MYSQL_DB)." >&2
    echo "Elegí otra base o usá --force si estás completamente seguro." >&2
    exit 1
fi

if grep -Eiq '^[[:space:]]*(CREATE[[:space:]]+DATABASE|USE[[:space:]]+)' "$ARCHIVO"; then
    echo "El volcado contiene CREATE DATABASE o USE." >&2
    echo "Restaurarlo podría crear o pisar otra base." >&2
    if [[ "$FORZAR" -ne 1 ]]; then
        echo "Se aborta. Usá --force solo si revisaste el archivo." >&2
        exit 1
    fi
fi

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

EXISTE="$("$MYSQL_CLIENT" --defaults-extra-file="$DEFAULTS" --batch --skip-column-names -e \
    "SELECT COUNT(*) FROM information_schema.schemata WHERE schema_name = '$BASE_DESTINO';")"

if [[ "$EXISTE" -ne 0 && "$FORZAR" -ne 1 ]]; then
    echo "La base $BASE_DESTINO ya existe." >&2
    echo "Elegí otro nombre, borrala a mano o usá --force." >&2
    exit 1
fi

"$MYSQL_CLIENT" --defaults-extra-file="$DEFAULTS" -e \
    "CREATE DATABASE IF NOT EXISTS \`$BASE_DESTINO\`
       CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

"$MYSQL_CLIENT" \
    --defaults-extra-file="$DEFAULTS" \
    --default-character-set=utf8mb4 \
    "$BASE_DESTINO" < "$ARCHIVO"

umask "$UMASK_ORIGINAL"

echo "Respaldo restaurado en: $BASE_DESTINO"
echo "Conteos:"

"$MYSQL_CLIENT" --defaults-extra-file="$DEFAULTS" --table "$BASE_DESTINO" -e "
SELECT 'estacion' AS tabla, COUNT(*) AS filas FROM estacion
UNION ALL SELECT 'tema', COUNT(*) FROM tema
UNION ALL SELECT 'pregunta', COUNT(*) FROM pregunta
UNION ALL SELECT 'respuesta', COUNT(*) FROM respuesta
UNION ALL SELECT 'configuracion', COUNT(*) FROM configuracion;"

echo ""
echo "Esperado con el contenido congelado: 5, 14, 80, 240 y 9."
