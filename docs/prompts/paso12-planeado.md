
# Plan del `paso12` — Feria con el servidor de Flask

No modifiqué ningún archivo. Solo hice verificaciones de lectura sobre el proyecto y la base real.

## 0. Estado actual verificado


| Control                        | Resultado                                                                                         |
| -------------------------------- | --------------------------------------------------------------------------------------------------- |
| Contenido                      | `5` estaciones, `14` temas, `80` preguntas, `240` respuestas, `9` claves de configuración        |
| Preguntas por nivel            | `inicial 20`, `intermedio 30`, `avanzado 30`                                                      |
| Niveles habilitados            | `intermedio = 1`, `avanzado = 1`; `inicial` siempre disponible                                    |
| Introducciones / explicaciones | `14/14` y `80/80`                                                                                 |
| Intentos activos               | `0`                                                                                               |
| `.env`                         | Existe, permisos `600`, valores reales: secreto de 64 caracteres, hash `scrypt`, usuario `jconde` |
| `.gitignore`                   | **No** incluye `feria2026/`                                                                       |
| `scripts/feria.sh`             | **No existe**                                                                                     |
| `feria2026/`                   | **No existe**                                                                                     |
| Entorno                        | MySQL `8.0.46`, Python `3.10.12`, Ubuntu 22.04                                                    |
| Git                            | **No hay repositorio Git**, así que el commit del paso no se puede crear                         |
| IP de este entorno             | `192.168.1.29` (puede no ser la IP de la notebook de la feria)                                    |
| Última suite                  | `105 passed` según `MEMORY.md`; se vuelve a correr al final                                      |

## 1. Enfoque general

El paso es **infra + documentación**, no de código de la app. La idea es:

1. Congelar el contenido que ya está cargado y verificado.
2. Probar de verdad el respaldo y la restauración.
3. Confirmar que el `.env` real está bien y no se versiona.
4. Crear `scripts/feria.sh` como único comando de arranque.
5. Probar el arranque local y dejar el ensayo de 3 notebooks + televisor como checklist manual.
6. Documentar el día de la feria.

**No se toca** `app/`, `tests/`, `bd/`, `requirements.txt`, el esquema ni la lógica del juego. Tampoco se reescriben `scripts/backup.sh` ni `scripts/restaurar.sh`: se usan y se prueban.

## 2. Fases de implementación

### Fase 1 — Congelar el contenido

- Reconfirmar por SQL los conteos `5/14/80/240/9` y que no haya intentos con `fecha_fin IS NULL`.
- Revisar en `/admin/cobertura` que las tres columnas estén en verde.
- Revisar en `/admin/dificultades` que estén habilitados los tres niveles.
- Revisar descripciones de `intermedio`/`avanzado` y las introducciones/explicaciones del `paso11g`.
- Jugar una partida completa de cada nivel y confirmar que cada una entra al ranking de su nivel.
- Anotar **fecha de congelamiento**, niveles habilitados y resultado.

**Regla importante:** después de congelar no se vuelven a ejecutar los seeds, porque pisan lo editado desde `/admin`. Si hay que cambiar contenido, se hace antes de congelar, con backup previo y volviendo a probar.

### Fase 2 — Backup y restauración reales

Usar los scripts existentes, sin reescribirlos:

```bash
./scripts/backup.sh /tmp/opencode/backups-feria
./scripts/restaurar.sh /tmp/opencode/backups-feria/respaldo-....sql
```

Verificar:

- El volcado se crea con permisos `600` y no está vacío.
- La restauración crea una base `_restore_...` y devuelve `5/14/80/240/9`.
- También se verifican `14` introducciones, `80` explicaciones y los niveles en `1`.
- `restaurar.sh` **se niega** a pisar `escape_room_7b2026` sin `--force`.
- La base temporal de prueba se elimina al terminar.
- El respaldo se copia además a un pendrive o a la nube. No alcanza con dejarlo solo en la notebook.

### Fase 3 — `.env` real

El `.env` actual ya parece real y tiene permisos `600`. El plan es **verificarlo, no sobreescribirlo**:

- Confirmar que `FLASK_SECRET_KEY` no es el placeholder y tiene longitud suficiente.
- Confirmar que `ADMIN_PASSWORD_HASH` es un hash `scrypt` y que el login de `/admin` funciona con la clave real.
- Confirmar que no está versionado (no hay Git, pero `.gitignore` ya lo excluye).
- Verificar que el usuario de MySQL tenga permisos para la base real, `_test` y `_restore_%`.

Si se decide rotar el secreto o el hash, se hace **antes** de la feria: rotar `FLASK_SECRET_KEY` invalida las sesiones de los equipos y los obliga a reingresar el ID.

### Fase 4 — Crear `scripts/feria.sh`

Archivo nuevo con el contenido del paso, más algunos refuerzos sin cambiar el comportamiento:

- Verificar que exista `python3` y que `python3 -m venv` funcione; si falla, mensaje claro sobre `python3-venv`.
- Crear `feria2026/` solo si no existe.
- Probar `import flask, pymysql, dotenv`; instalar `requirements.txt` solo si falta algo.
- Detectar la IP con `hostname -I` **sin que un fallo corte el script** (`|| true`).
- Mostrar todas las IPs o al menos la primera, con la aclaración de que hay que usar la de la red del aula.
- Avisar si `.env` no tiene permisos `600`.
- Ejecutar al final:
  ```bash
  exec "$PYTHON" -m flask --app app run --debug --host=0.0.0.0 "$@"
  ```
- Quedar ejecutable con `chmod 755`.

También:

- Agregar `feria2026/` a `.gitignore`.
- Crear el entorno **ahora**, con Internet, para que el día de la feria no haya que instalar nada.
- Verificar que una segunda ejecución **no reinstale** dependencias.
- Probar `bash -n scripts/feria.sh` y, si está disponible, `shellcheck`.

### Fase 5 — Prueba local de arranque

- Levantar con `./scripts/feria.sh`.
- Probar `/salud` en `127.0.0.1:5000` y en la IP de red.
- Probar `/ranking`, `/estadisticas` y el login de `/admin`.
- Reiniciar y confirmar que no reinstala y que la app vuelve a levantar.
- Correr `pytest -q` y confirmar que sigue en **105 tests**.
- Verificar que no haya referencias a CDN ni recursos externos.

### Fase 6 — Ensayo con 3 notebooks y televisor

Checklist manual:

- Notebook enchufada, sin suspensión ni apagado de pantalla.
- IP anotada y, si se puede, reserva DHCP o IP fija.
- Puerto `5000` permitido en la red del aula.
- Las 3 notebooks y el televisor en la misma red.
- Reloj y zona horaria correctos: MySQL es la fuente de tiempo.
- `.env` con permisos `600`.
- Sin Internet: Bootstrap, audio, imágenes y gráficos locales.
- 3 equipos jugando a la vez, idealmente uno por nivel.
- Televisor con `/ranking` en pantalla completa y actualizándose.
- Cortar Internet y repetir una estación.
- Reiniciar MySQL y confirmar que la app se reconecta.
- Cronometrar el arranque desde cero.

Si no se consiguen físicamente las 3 notebooks y el televisor, **no voy a declarar el criterio como cumplido**: queda documentado como verificación manual pendiente, con la prueba local y el checklist listos.

### Fase 7 — Cierre documental

- Actualizar `README.md`, la guía de instalación, la guía de estudiantes y `MEMORY.md`.
- Marcar el `paso12` como `hecho` en el índice y en su archivo.
- Dejar anotado que no se pudo hacer el commit por no haber repositorio Git.

## 3. Archivos que se van a modificar


| Archivo                                           | Tipo                       | Qué cambia                                                                                                                                                                                             |
| --------------------------------------------------- | ---------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `scripts/feria.sh`                                | **Nuevo**                  | Script de arranque con venv `feria2026/`, chequeo de `.env`, IP y Flask en `0.0.0.0:5000`.                                                                                                              |
| `.gitignore`                                      | Modificado                 | Agrega `feria2026/`.                                                                                                                                                                                    |
| `README.md`                                       | Modificado                 | Sección 9: `./scripts/feria.sh` como arranque recomendado, primer arranque con Internet, arranques posteriores sin Internet, terminal abierta, puerto `5000`. Sección 10: respaldo probado y destino. |
| `docs/instalacion-y-puesta-en-funcionamiento.md`  | Modificado                 | §10.3/§10.4 con la prueba real de backup/restauración, §10.5 con fecha de congelamiento, §13.5 y §15 con `./scripts/feria.sh` y el checklist del día.                                            |
| `docs/guia-de-estudio-para-estudiantes.md`        | Modificado                 | §9: mencionar `./scripts/feria.sh` como atajo, manteniendo el comando manual para entender qué hace.                                                                                                  |
| `docs/tecnologias.md`                             | Modificado, si corresponde | Agregar `./scripts/feria.sh` al comando de arranque de la feria.                                                                                                                                        |
| `docs/dejar-funcionando-proyecto-luego-clone.md`  | Modificado, si corresponde | Mencionar el script en la puesta en marcha de la feria.                                                                                                                                                 |
| `docs/argumentos-pasos/paso12-feria-con-flask.md` | Modificado                 | Agregar `## Estado`, marcar criterios cumplidos y anotar resultados reales (fecha, IP, niveles, backup, ensayo).                                                                                        |
| `docs/argumentos-pasos/README.md`                 | Modificado                 | `paso12` pasa de `pendiente` a `hecho`.                                                                                                                                                                 |
| `docs/primeros-pasos.md`                          | Modificado, opcional       | El Pedido 12 todavía dice “documentar el arranque con waitress”; corregirlo para que la feria sea con Flask y waitress quede post-feria.                                                             |
| `AGENTS.md`                                       | Modificado                 | Decisiones 67 y 68, comandos, estructura, pruebas y “Qué no hacer”.                                                                                                                                  |
| `MEMORY.md`                                       | Modificado                 | Entrada nueva del paso, fecha, estado de la feria, respaldo, IP, niveles y próximo paso.                                                                                                               |

**No se modifican:** `app/`, `tests/`, `bd/`, `requirements.txt`, `scripts/backup.sh`, `scripts/restaurar.sh`, `.env.example` ni la base real (salvo la prueba de restauración en una base temporal).

## 4. Casos límite y decisiones que necesito de vos

1. **¿Rotamos el secreto y el hash del `.env`?**
   Recomendación: **no**, porque ya son reales, el `.env` está en `600` y no está versionado. Rotar el secreto obliga a todos los equipos a reingresar el ID.
2. **¿Las partidas de congelamiento se juegan en la base real o en una base descartable?**
   Recomendación: en una base descartable restaurada del backup, para que el ranking real de la feria arranque limpio. Si se juegan en la real, quedan intentos históricos con un equipo de prueba.
3. **¿El equipo de prueba queda en el ranking?**
   Recomendación: dejarlo como intento histórico, con un nombre claro tipo `PRUEBA FERIA`, y no borrarlo. No conviene borrar filas históricas. Si querés que no aparezca, se juega en la base descartable.
4. **¿Se puede hacer el ensayo físico con 3 notebooks y el televisor?**
   Si no se puede, lo dejo como verificación manual pendiente y hago solo la prueba local + `curl` desde otra máquina. No voy a marcar ese criterio como cumplido sin haberlo hecho.
5. **¿Mantenemos `--debug` o agregamos `--no-reload`?**
   Recomendación: mantener exactamente `--debug`, como pide la decisión 65. `--no-reload` daría más estabilidad, pero se aparta del comando acordado.
6. **¿Creamos `feria2026/` ahora o el día de la feria?**
   Recomendación: crearlo ahora, con Internet, para que el día de la feria no dependa de `pip`. El script igualmente lo crea solo si falta.
7. **¿Dónde guardamos el backup?**
   Recomendación: `$HOME/backups-escaperoom` o `/tmp/opencode/backups-feria`, más una copia en pendrive/nube. Evitar `bd/backups/` como único lugar porque está ignorado y se puede perder con el proyecto.
8. **¿Seguimos con `MYSQL_USER=jconde` o creamos un usuario `escaperoom`?**
   Recomendación: para la feria, dejar `jconde` que ya funciona. Crear el usuario dedicado queda para la puesta en producción posterior.
9. **¿El `.gitignore` solo agrega `feria2026/` o también otros artefactos de la feria?**
   Recomendación: solo `feria2026/`. Los backups ya están cubiertos por `bd/backups/` y no se van a guardar ahí.
10. **¿Actualizamos el checklist en `docs/instalacion-y-puesta-en-funcionamiento.md` §15 o creamos `docs/checklist-feria.md`?**
    Recomendación: actualizar el §15 existente, para no sumar otro archivo.
11. **¿Corregimos `docs/primeros-pasos.md` (Pedido 12) que todavía habla de waitress?**
    Recomendación: sí, es una corrección mínima de coherencia con la decisión 65.

## 5. Qué actualizaría en `AGENTS.md`

- **Decisión 67 — Arranque de la feria con `scripts/feria.sh`:**

  - venv propio en `feria2026/`, ignorado por Git;
  - `.env` real con permisos `600`;
  - no usa `source .env` por los `$` del hash;
  - crea el entorno e instala solo si falta;
  - muestra la IP y levanta Flask en `0.0.0.0:5000`;
  - no usa waitress, systemd ni Docker;
  - primer arranque con Internet, siguientes sin Internet;
  - terminal abierta durante toda la feria.
- **Decisión 68 — Congelamiento y respaldo de la feria:**

  - fecha de congelamiento y conteos `5/14/80/240/9`;
  - los seeds no se reejecutan después de congelar;
  - backup generado y **restaurado** en base temporal antes de la feria;
  - el respaldo se guarda también fuera de la notebook;
  - no se restaura sobre la base real sin `--force` consciente;
  - las partidas de prueba quedan como históricas o se juegan en base descartable.
- **Comandos:** agregar

  ```bash
  chmod +x scripts/feria.sh
  ./scripts/feria.sh
  ```
- **Estructura:** agregar `scripts/feria.sh`, `scripts/backup.sh` y `scripts/restaurar.sh` al árbol sugerido.
- **Pruebas y verificación:** agregar bullets para:

  - arranque con `./scripts/feria.sh`;
  - `/salud` en local y en red;
  - segunda ejecución sin reinstalar;
  - `feria2026/` ignorado;
  - backup restaurado con `5/14/80/240/9`;
  - negativa de `restaurar.sh` a pisar la base real;
  - `./scripts/feria.sh` sin CDN ni recursos externos.
- **Qué no hacer:** agregar

  - no versionar `feria2026/`;
  - no reejecutar seeds después de congelar;
  - no dejar el único backup en la notebook;
  - no reemplazar el arranque de la feria por waitress ni Docker.

## 6. Qué actualizaría en `MEMORY.md`

Al principio, una entrada nueva con:

- Fecha del paso y fecha de congelamiento.
- Conteos `5/14/80/240/9`, niveles habilitados y `0` intentos activos.
- `.env` real, `600`, sin rotación (o con rotación, si se decide).
- `scripts/feria.sh` creado, `feria2026/` creado e ignorado.
- IP de la notebook, puerto `5000` y tiempo de arranque medido.
- Ruta del backup, base temporal usada y resultado de la restauración.
- Resultado del ensayo con 3 notebooks y televisor, o “pendiente manual”.
- `pytest` con 105 tests.
- Documentos actualizados.
- Aclaración de que no se pudo hacer el commit por no haber repositorio Git.

En **“Próximo paso”**, pasar al `paso13` (waitress y systemd post-feria), dejando claro que la feria del 16/11/2026 se corre con Flask y que la ficha del servidor de la escuela sigue pendiente para los escenarios B/C del `paso13`.

## 7. Orden de ejecución propuesto

1. Reconfirmar base y contenido.
2. Congelar y jugar las partidas de prueba.
3. Backup y restauración.
4. Verificar `.env`.
5. Crear `scripts/feria.sh` y `feria2026/`.
6. Prueba local de arranque y `/salud`.
7. Ensayo físico o checklist manual.
8. Actualizar documentación, `AGENTS.md` y `MEMORY.md`.
9. Correr `pytest -q` una última vez.

## 8. Lo que necesito antes de empezar

- Tu aprobación del plan.
- Respuesta a las decisiones 1 a 11, sobre todo:
  - rotar o no `.env`;
  - base real o descartable para las partidas de congelamiento;
  - si hay o no ensayo físico con 3 notebooks y televisor;
  - si mantengo `--debug` tal cual.

Con eso apruebo el arranque y recién ahí empiezo a crear `scripts/feria.sh` y a tocar los archivos de documentación.
