#!/usr/bin/env bash
# Vacía equipos, intentos y todo su detalle de una base del escape room.
#
# Uso:
#   ./scripts/vaciar-intentos.sh
#   ./scripts/vaciar-intentos.sh --base=escape_room_redes_2026
#   ./scripts/vaciar-intentos.sh --seco
#   ./scripts/vaciar-intentos.sh --si --sin-respaldo
#   ./scripts/vaciar-intentos.sh --forzar
#
# Ejecuta bd/vaciar-equipos-e-intentos.sql sobre la base elegida. Borra
# equipos, intentos, ranking y estadísticas, y NO toca el contenido:
# estaciones, temas, preguntas, respuestas y configuración quedan intactas.
#
# Lee la conexión de .env (o de la variable ENV_FILE). No evalúa el archivo con
# `source` porque ADMIN_PASSWORD_HASH contiene `$` y rompería la shell.

set -euo pipefail

RAIZ="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ENV_FILE="${ENV_FILE:-$RAIZ/.env}"
SQL="$RAIZ/bd/vaciar-equipos-e-intentos.sql"

TABLAS=(
    incorrecta
    respuesta_elegida
    intento_pregunta
    intento_envio
    intento_estacion
    intento
    equipo
)

BASE=""
CONFIRMAR=1
RESPALDAR=1
FORZAR=0
SECO=0

uso() {
    cat <<'TEXTO'
Vacía equipos, intentos y todo su detalle. Conserva el contenido y la
configuración de la base.

Uso:
  ./scripts/vaciar-intentos.sh [opciones]

Opciones:
  --base=<nombre>   Base a vaciar. Por defecto, MYSQL_DB del .env.
  --seco            Solo muestra qué se borraría. No borra ni respalda.
  --si              No pide confirmación.
  --sin-respaldo    No genera el respaldo previo con scripts/backup.sh.
  --forzar          Borra aunque haya equipos jugando (intentos sin fecha_fin).
  --ayuda, -h       Muestra esta ayuda.

La conexión (host, puerto, usuario y clave) sale de .env o de ENV_FILE.

Antes de borrar pide escribir el nombre de la base y genera un respaldo.
También se niega a borrar si hay intentos activos, salvo con --forzar.
TEXTO
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        --base=*)
            BASE="${1#*=}"
            ;;
        --seco)
            SECO=1
            ;;
        --si)
            CONFIRMAR=0
            ;;
        --sin-respaldo)
            RESPALDAR=0
            ;;
        --forzar)
            FORZAR=1
            ;;
        --ayuda | -h | --help)
            uso
            exit 0
            ;;
        *)
            echo "Opción desconocida: $1" >&2
            echo >&2
            uso >&2
            exit 2
            ;;
    esac
    shift
done

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

if [[ ! -f "$SQL" ]]; then
    echo "No se encontró $SQL." >&2
    exit 1
fi

MYSQL_HOST="$(leer_env MYSQL_HOST)"
MYSQL_PORT="$(leer_env MYSQL_PORT)"
MYSQL_USER="$(leer_env MYSQL_USER)"
MYSQL_PASSWORD="$(leer_env MYSQL_PASSWORD)"
MYSQL_DB_ENV="$(leer_env MYSQL_DB)"

: "${MYSQL_HOST:?Falta MYSQL_HOST en $ENV_FILE}"
: "${MYSQL_PORT:?Falta MYSQL_PORT en $ENV_FILE}"
: "${MYSQL_USER:?Falta MYSQL_USER en $ENV_FILE}"
: "${MYSQL_DB_ENV:?Falta MYSQL_DB en $ENV_FILE}"

BASE="${BASE:-${MYSQL_DB:-$MYSQL_DB_ENV}}"

if [[ ! "$BASE" =~ ^[A-Za-z0-9_]+$ ]]; then
    echo "Nombre de base inválido: '$BASE'." >&2
    echo "Solo se aceptan letras, números y guion bajo." >&2
    exit 2
fi

if command -v mysql >/dev/null 2>&1; then
    MYSQL_BIN="mysql"
elif command -v mariadb >/dev/null 2>&1; then
    MYSQL_BIN="mariadb"
else
    echo "No se encontró mysql ni mariadb en el PATH." >&2
    exit 1
fi

UMASK_ORIGINAL="$(umask)"
umask 077
DEFAULTS="$(mktemp)"
ENV_TEMPORAL=""
chmod 600 "$DEFAULTS"

limpia() {
    rm -f "$DEFAULTS"
    if [[ -n "$ENV_TEMPORAL" ]]; then
        rm -f "$ENV_TEMPORAL"
    fi
}
trap limpia EXIT

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

umask "$UMASK_ORIGINAL"

consulta() {
    "$MYSQL_BIN" \
        --defaults-extra-file="$DEFAULTS" \
        --batch \
        --skip-column-names \
        --default-character-set=utf8mb4 \
        "$BASE" \
        -e "$1"
}

SALIDA=""
if ! SALIDA="$(consulta "SELECT 1" 2>&1)"; then
    echo "No se pudo conectar a MySQL con los datos de $ENV_FILE." >&2
    echo "Base: $BASE  Servidor: $MYSQL_HOST:$MYSQL_PORT  Usuario: $MYSQL_USER" >&2
    echo "$SALIDA" >&2
    exit 1
fi

EXISTE="$(consulta "SELECT COUNT(*) FROM information_schema.schemata WHERE schema_name = '$BASE'")"
if [[ "$EXISTE" != "1" ]]; then
    echo "La base '$BASE' no existe en $MYSQL_HOST:$MYSQL_PORT." >&2
    exit 1
fi

LISTA=""
for tabla in "${TABLAS[@]}"; do
    if [[ -z "$LISTA" ]]; then
        LISTA="'$tabla'"
    else
        LISTA="$LISTA,'$tabla'"
    fi
done
FALTAN="$(consulta "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = '$BASE' AND table_name IN ($LISTA)")"
if [[ "$FALTAN" != "${#TABLAS[@]}" ]]; then
    echo "La base '$BASE' no tiene las ${#TABLAS[@]} tablas esperadas ($FALTAN encontradas)." >&2
    echo "Revisá que sea una base del escape room." >&2
    exit 1
fi

ACTIVOS="$(consulta "SELECT COUNT(*) FROM intento WHERE fecha_fin IS NULL")"

TOTAL=0
echo "Vaciar equipos e intentos"
echo
printf '  Base:     %s\n' "$BASE"
printf '  Servidor: %s:%s\n' "$MYSQL_HOST" "$MYSQL_PORT"
printf '  Usuario:  %s\n' "$MYSQL_USER"
printf '  Archivo:  %s\n' "bd/vaciar-equipos-e-intentos.sql"
if [[ "$ACTIVOS" != "0" ]]; then
    printf '  Aviso:    %s intento(s) sin terminar (equipos jugando)\n' "$ACTIVOS"
fi
echo
echo "Filas a borrar:"
for tabla in "${TABLAS[@]}"; do
    filas="$(consulta "SELECT COUNT(*) FROM \`$tabla\`")"
    TOTAL=$((TOTAL + filas))
    printf '  %-18s %s\n' "$tabla" "$filas"
done
printf '  %-18s %s\n' "total" "$TOTAL"
echo

if [[ "$SECO" -eq 1 ]]; then
    if [[ "$ACTIVOS" != "0" ]]; then
        echo "Modo seco: no se borró nada. Para borrar de verdad hace falta --forzar" >&2
        echo "mientras haya $ACTIVOS intento(s) sin terminar." >&2
    else
        echo "Modo seco: no se borró nada."
    fi
    exit 0
fi

if [[ "$ACTIVOS" != "0" && "$FORZAR" -eq 0 ]]; then
    echo "Hay $ACTIVOS intento(s) sin terminar: puede haber equipos jugando." >&2
    echo "Cerrá esas partidas o volvé a ejecutar con --forzar." >&2
    exit 2
fi

if [[ "$CONFIRMAR" -eq 1 ]]; then
    printf 'Escribí el nombre de la base para confirmar (%s): ' "$BASE"
    RESPUESTA=""
    if ! read -r RESPUESTA; then
        echo "Cancelado. No se borró nada." >&2
        exit 2
    fi
    if [[ "$RESPUESTA" != "$BASE" ]]; then
        echo "El nombre no coincide. No se borró nada." >&2
        exit 2
    fi
fi

if [[ "$RESPALDAR" -eq 1 ]]; then
    ENV_TEMPORAL="$(mktemp)"
    chmod 600 "$ENV_TEMPORAL"
    sed "s|^\([[:space:]]*MYSQL_DB=\).*|\1$BASE|" "$ENV_FILE" > "$ENV_TEMPORAL"
    if ! grep -qE "^[[:space:]]*MYSQL_DB=" "$ENV_TEMPORAL"; then
        printf '\nMYSQL_DB=%s\n' "$BASE" >> "$ENV_TEMPORAL"
    fi
    echo
    echo "Generando respaldo de '$BASE' ..."
    if ! ENV_FILE="$ENV_TEMPORAL" "$RAIZ/scripts/backup.sh"; then
        echo "El respaldo falló. No se borró nada." >&2
        exit 1
    fi
fi

echo
echo "Borrando ..."
if ! "$MYSQL_BIN" \
    --defaults-extra-file="$DEFAULTS" \
    --default-character-set=utf8mb4 \
    "$BASE" < "$SQL"; then
    echo "La eliminación falló. Revisá el respaldo y el estado de la base." >&2
    exit 1
fi

echo
echo "Filas restantes:"
RESTANTES=0
for tabla in "${TABLAS[@]}"; do
    filas="$(consulta "SELECT COUNT(*) FROM \`$tabla\`")"
    RESTANTES=$((RESTANTES + filas))
    printf '  %-18s %s\n' "$tabla" "$filas"
done
echo

if [[ "$RESTANTES" -ne 0 ]]; then
    echo "Quedaron $RESTANTES fila(s) sin borrar. Revisá la base." >&2
    exit 1
fi

echo "Listo: se borraron $TOTAL fila(s) de '$BASE'."
echo "El contenido (estaciones, temas, preguntas, respuestas y configuración) sigue intacto."
