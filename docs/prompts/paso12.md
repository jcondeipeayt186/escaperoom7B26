
Listo. Cerré el `paso12` y dejé todo verificado.

## Qué quedó hecho

**Estado y congelamiento**

- Base real `escape_room_7b2026` intacta: `5/14/80/240/9`, `inicial 20` / `intermedio 30` / `avanzado 30`, ambos niveles avanzados en `1`, `0` intentos activos, 14 introducciones y 80 explicaciones.
- Partidas de control por nivel jugadas en la base descartable `escape_room_7b2026_ensayo` (cada una entró a su ranking) y base eliminada. El ranking real quedó limpio.
- `.env` verificado: modo `600`, secreto de 64 caracteres, hash `scrypt` válido, `MYSQL_USER=jconde`, `MYSQL_DB=escape_room_7b2026`. No se rotó.

**Arranque de la feria**

- `scripts/feria.sh` (755): valida `.env` y `python3`, avisa si `.env` no está en `600`, crea `feria2026/`, instala solo si faltan `flask`/`pymysql`/`dotenv`, muestra la IP con el puerto real y ejecuta `python -m flask --app app run --debug --host=0.0.0.0`.
- Primer arranque: 13 s (instaló). Segundo: 2 s sin reinstalar.
- `/salud` `200` en `127.0.0.1` y en la IP de red; `/ranking` y `/estadisticas` `200`.
- `feria2026/` agregado a `.gitignore`.

**Respaldo y restauración**

- Respaldo real `respaldo-escape_room_7b2026-20261114-233156.sql` (68 KB, `600`) vía `scripts/backup.sh`.
- Restaurado en una base limpia: `5/14/80/240/9`, 14 introducciones, 80 explicaciones. `restaurar.sh` rechaza la base real sin `--force` (exit 1).
- **Bug corregido** en `scripts/restaurar.sh`: el nombre por defecto de la base temporal usaba guion (`AAAAMMDD-HHMMSS`) y la validación solo admite `[a-z0-9_]`. Ahora es `<MYSQL_DB>_restore_AAAAMMDD_HHMMSS`, con referencias actualizadas en `README.md`, `docs/instalacion-servidor-escuela.md` y el `paso12`. Los nombres de archivo de respaldo conservan el guion, que es correcto.

**Documentación**

- Actualizados: `README.md` (§7.4, §9, §10), `docs/instalacion-y-puesta-en-funcionamiento.md` (encabezado, respaldo, checklist y día de la feria), `docs/guia-de-estudio-para-estudiantes.md` (§9), `docs/tecnologias.md`, `docs/dejar-funcionando-proyecto-luego-clone.md`, `docs/primeros-pasos.md` (Pedido 12 y Paso 10), `docs/argumentos-pasos/paso12-feria-con-flask.md` (estado, resultado y aceptación), `docs/argumentos-pasos/README.md` (`paso12` = hecho), `AGENTS.md` (estructura, decisiones 67/68, comandos, pruebas y “Qué no hacer”) y `MEMORY.md` (fecha 14/11, entrada nueva y próximo paso).

**Verificación**

- `pytest -q` → **105 passed**.
- 0 enlaces relativos roto en los documentos tocados.
- No se tocaron `app/`, `tests/`, `bd/` ni el esquema.

## Pendiente operativo

1. Copiar el respaldo a un pendrive o a la nube (hoy está fuera del repo, en `/tmp/opencode/backups-feria/`).
2. Opcional: repetir `./scripts/feria.sh` en la notebook de la feria.
3. Sin repositorio Git en el directorio, **no se pudo crear el commit** `docs: feria con flask y respaldo`. Queda anotado en el `paso12` y en `MEMORY.md`.
4. El `paso13` (waitress + systemd) sigue esperando la ficha del servidor de la escuela (distro/versión).
