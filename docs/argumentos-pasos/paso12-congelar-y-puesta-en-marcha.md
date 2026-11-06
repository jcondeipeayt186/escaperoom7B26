# Paso 12 — Congelar, respaldar y poner en marcha

> **Origen:** Pedido 12 de `docs/primeros-pasos.md` (Paso 10).
> **Tipo:** infra (con partes manuales).
> **Requiere:** `paso11b` y `paso11c` aprobados y commiteados.
> **Commit:** `docs: puesta en marcha y respaldo`.
>
> **Antes de empezar:** leé `AGENTS.md` ("Checklist para el día de la feria"),
> `docs/instalacion-y-puesta-en-funcionamiento.md` y `MEMORY.md`.
>
> **Docker:** es una alternativa opcional posterior a la feria. Se trata en un
> paso 13 aparte y **no** reemplaza waitress/systemd.

## Contexto

La app y los tests están listos. Falta dejarla preparada para el aula, sin
cambios de último momento.

## Objetivo

Dejar la aplicación congelada, con backup probado y un procedimiento de
arranque que funcione sin Internet.

## Alcance

- Revisar y congelar el contenido.
- Generar un volcado de la base y probar la restauración en una base limpia.
- Documentar el arranque con waitress en `0.0.0.0`.
- Configurar `ADMIN_PASSWORD_HASH` y `FLASK_SECRET_KEY` reales.
- Probar desde 3 notebooks y el televisor.
- Verificar el funcionamiento sin Internet.
- Dejar scripts de backup y restauración.

No cambiar el esquema, no cargar contenido nuevo y no tocar la lógica del
juego en este paso. Si aparece un error bloqueante, se corrige en un commit
aparte y se vuelve a probar.

## Scripts

Crear `scripts/backup.sh` y `scripts/restaurar.sh`:

- `backup.sh`: `mysqldump` de `escape_room_7b2026` a un archivo con fecha.
- `restaurar.sh`: restaurar un volcado en una base indicada por parámetro.
- Ambos leen credenciales de `.env` o de variables de entorno.
- Nunca commitear el volcado ni el `.env`.
- Probar la restauración de verdad, no solo generar el archivo.

## Arranque

- Usar waitress, no el servidor de desarrollo.
- Escuchar en `0.0.0.0` para que se conecten las notebooks.
- Documentar la IP del servidor y el puerto.
- Dejar el proceso estable: systemd o el mecanismo elegido en
  `docs/instalacion-y-puesta-en-funcionamiento.md`.
- `.env` con valores reales, fuera de Git.

## Criterio de aceptación

- [ ] La app levanta desde cero con los comandos del `README.md`.
- [ ] El backup se restaura en una base limpia y los conteos coinciden.
- [ ] 3 notebooks juegan a la vez sin errores.
- [ ] El televisor muestra `/ranking` actualizándose.
- [ ] Sin Internet, todo sigue funcionando (Bootstrap, audio y gráficos
      locales).
- [ ] El contenido está congelado y anotado.
- [ ] Los scripts de backup y restauración funcionan.
- [ ] `ADMIN_PASSWORD_HASH` y `FLASK_SECRET_KEY` son reales y no están
      versionados.

## Verificación

Backup y restauración:

```bash
mysqldump --single-transaction -u <usuario> -p escape_room_7b2026 \
  > respaldo_$(date +%Y%m%d).sql

mysql -u <usuario> -p -e "CREATE DATABASE escape_room_restore_test"
mysql -u <usuario> -p escape_room_restore_test < respaldo_20260101.sql
```

Después, en la base restaurada:

```sql
SELECT COUNT(*) FROM estacion;
SELECT COUNT(*) FROM tema;
SELECT COUNT(*) FROM pregunta;
SELECT COUNT(*) FROM respuesta;
```

Esperado: los mismos conteos que la base original.

Simulacro:

1. Levantar waitress en el servidor.
2. Conectar 3 notebooks y un televisor.
3. Jugar con 3 equipos a la vez.
4. Cortar Internet y repetir una estación.
5. Reiniciar MySQL y confirmar que la app se reconecta.
6. Restaurar el backup en una base limpia.

## Trampas conocidas

- El backup no está probado hasta que se restaura.
- Guardar el backup en un pendrive y en la nube, no solo en el servidor.
- `mysqldump` puede incluir `CREATE DATABASE`; decidir y documentar cómo se
  restaura para no pisar la base buena por error.
- No dejar el servidor de desarrollo de Flask para la feria.
- No hacer cambios de código el día de la feria.
- Verificar que el audio y Bootstrap sean locales; un CDN que falla deja la
  pantalla rota.
- El reloj del servidor es la fuente de tiempo: revisar que esté bien.

## Al terminar

- Resumir el procedimiento, los comandos y el resultado del simulacro.
- Actualizar `MEMORY.md` con el estado final y la fecha de congelamiento.
- Commit: `docs: puesta en marcha y respaldo`.
