# Paso 13 — Waitress y systemd después de la feria

> **Origen:** puesta en producción posterior a la feria del 16/11/2026.
> **Tipo:** infra (opcional, post-feria).
> **Requiere:** `paso12` aprobado y la feria terminada.
> **Commit:** `docs: waitress y systemd post-feria`.
>
> **Antes de empezar:** leé `AGENTS.md` (decisión 65),
> `docs/instalacion-y-puesta-en-funcionamiento.md`,
> `docs/instalacion-servidor-escuela.md` y `MEMORY.md`.

## Importante

Este paso **no forma parte de la feria**. La feria del 16/11/2026 se corre con
el servidor de desarrollo de Flask y el script `scripts/feria.sh` del `paso12`.
Acá se deja la aplicación como servicio permanente, recién cuando la feria ya
terminó.

No ejecutar este paso antes del 16/11. No reemplazar el arranque del `paso12`
mientras la feria esté en curso.

## Contexto

Terminada la feria, la app puede quedar funcionando todos los días en la
escuela. Para eso conviene:

- Servirla con **waitress**, un servidor WSGI de producción.
- Administrarla con **systemd**, para que arranque sola y se reinicie si falla.
- Dejar de depender de una terminal abierta.

Hay **dos equipos candidatos** para oficiar de servidor:

1. La notebook del docente con **Ubuntu 22.04**, la misma que se usó en la
   feria.
2. Un **servidor Linux de la escuela** con MySQL 8 y `sudo` completo. La
   distribución y la versión todavía no están confirmadas.

Existe además una tercera variante: dejar **solo la base de datos** en el
servidor de la escuela y la app en la notebook.

## Objetivo

Dejar la aplicación funcionando como servicio permanente, sin Internet, en los
tres escenarios posibles.

## Escenarios de despliegue

| | **A — Todo en la notebook** | **B — Todo en el servidor** | **C — Base en la escuela, app en la notebook** |
| --- | --- | --- | --- |
| Flask + waitress | Notebook Ubuntu 22.04 | Servidor de la escuela | Notebook Ubuntu 22.04 |
| MySQL 8 | Notebook | Servidor de la escuela | Servidor de la escuela |
| Dependencia de red entre app y base | Ninguna | Ninguna | Cada request depende de la LAN |
| Punto único de falla | La notebook | El servidor | Dos equipos |
| Permisos necesarios | Locales | `sudo` en el servidor | `sudo` en ambos y abrir `3306` en la LAN |
| Dónde se respalda | Notebook | Servidor | Servidor (o desde la notebook) |
| Complejidad | Baja, ya probada | Media | Alta |
| Riesgo principal | Suspensión o uso indebido de la notebook | Distro vieja, servidor compartido | Corte de red, reloj, MySQL expuesto |

Documentación de cada escenario:

- **A:** `docs/instalacion-y-puesta-en-funcionamiento.md`.
- **B y C:** `docs/instalacion-servidor-escuela.md`.

### Decisión tomada

- **A es el escenario principal**, porque ya está probado y no depende de la
  red entre la app y la base.
- **B es el respaldo**, porque el servidor tiene `sudo` completo y MySQL 8.
- **C se documenta, pero no se improvisa.** Solo se usa si se ensayó antes y
  hay una ventaja concreta, por ejemplo un UPS o respaldos centralizados.

### Restricciones técnicas comunes

| Requisito | Detalle |
| --- | --- |
| Python 3.10 o superior | `pytest 9.2` lo exige; Flask 3.1 acepta 3.9. |
| MySQL 8.0 o MariaDB 10.3 o superior | El ranking usa `ROW_NUMBER() OVER (...)`; el esquema usa columnas generadas y `CHECK`. |
| Misma red | Notebooks y televisor en la misma LAN que el servidor. |
| Puerto `8000` libre | Puerto de waitress. |
| Reloj y zona horaria correctos | La app inserta `NOW(3)` de MySQL: el reloj de la base es la autoridad. |
| `sudo` en el servidor | Sin permisos, B y C no son viables. |
| Sin Internet | Bootstrap, audio, imágenes y gráficos son locales. |

### Ficha del servidor de la escuela

Completar con los datos reales. La sección 2 de
`docs/instalacion-servidor-escuela.md` tiene los comandos para obtenerlos.

| Dato | Valor |
| --- | --- |
| Distribución y versión | |
| Arquitectura | |
| Python disponible | |
| Motor y versión | |
| Gestor de paquetes | |
| Usuario con `sudo` | |
| IP del servidor | |
| IP fija o DHCP | |
| Firewall | |
| ¿Servidor exclusivo o compartido? | |
| ¿Tiene UPS? | |
| ¿Tiene Internet o mirror interno? | |

Mientras la ficha esté incompleta, el procedimiento de B y C queda **a
validar**. No alcanza con que los comandos sean genéricos: hay que ejecutarlos
en el servidor.

## Alcance

- Documentar el arranque con waitress en `0.0.0.0:8000`.
- Crear el servicio systemd y habilitarlo.
- Configurar `ADMIN_PASSWORD_HASH` y `FLASK_SECRET_KEY` reales en `.env`.
- Probar desde 3 notebooks y el televisor en A y en B.
- Verificar el funcionamiento sin Internet.
- Usar los scripts de backup y restauración del `paso12` en A, B y C.
- Mantener el contenido congelado en `5/14/80/240/9`.

No cambiar el esquema, no cargar contenido nuevo y no tocar la lógica del
juego en este paso. Si aparece un error bloqueante, se corrige en un commit
aparte y se vuelve a probar.

## Arranque con waitress

Comando base:

```bash
feria2026/bin/python -m waitress --listen=0.0.0.0:8000 app:create_app
```

Detalles:

- Escuchar en `0.0.0.0` para que se conecten las notebooks.
- Usar el mismo entorno virtual `feria2026/` del `paso12` o el que corresponda
  en el servidor.
- `.env` con valores reales, permisos `600`, fuera de Git.
- El `.env` se carga con `python-dotenv` desde la app; no hace falta `source`.

### Servicio systemd de ejemplo

Archivo `/etc/systemd/system/escaperoom.service`:

```ini
[Unit]
Description=Escape Room 7 B 2026
After=network.target mysql.service

[Service]
User=escaperoom
WorkingDirectory=/opt/escaperoom7b2026
EnvironmentFile=/opt/escaperoom7b2026/.env
ExecStart=/opt/escaperoom7b2026/feria2026/bin/python -m waitress --listen=0.0.0.0:8000 app:create_app
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

Ajustar `User`, `WorkingDirectory` y la ruta del entorno virtual a la
instalación real. En B, ajustar también el nombre del motor en `After`
(`mysql.service` o `mysqld.service`) y la distribución.

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now escaperoom.service
sudo systemctl status escaperoom.service
```

### Escenario C

La notebook corre la app y apunta `MYSQL_HOST` a la IP del servidor de la
escuela. El puerto `3306` se abre solo para la IP de la notebook.

El procedimiento completo está en:

- A: `docs/instalacion-y-puesta-en-funcionamiento.md`, secciones 4 a 8.
- B y C: `docs/instalacion-servidor-escuela.md`, secciones 4 y 5.

## Criterios de aceptación

### Comunes a los tres escenarios

- [ ] La app levanta desde cero con los comandos documentados.
- [ ] `/salud` responde `200` con `{"estado": "ok", "base": "ok"}`.
- [ ] `/admin` entra con `ADMIN_USER` y la clave real.
- [ ] El contenido sigue congelado: `5/14/80/240/9`.
- [ ] `ADMIN_PASSWORD_HASH` y `FLASK_SECRET_KEY` son reales y no están
      versionados.
- [ ] El `.env` tiene permisos `600` y no está en Git.
- [ ] El backup del `paso12` se restaura en una base limpia y los conteos
      coinciden.
- [ ] Sin Internet, todo sigue funcionando: Bootstrap, audio, imágenes y
      gráficos locales.
- [ ] El reloj del equipo que corre MySQL está en hora.

### Escenario A — notebook

- [ ] Waitress responde en `0.0.0.0:8000`.
- [ ] El servicio systemd queda habilitado con `Restart=always`.
- [ ] 3 notebooks juegan a la vez sin errores.
- [ ] El televisor muestra `/ranking` actualizándose.
- [ ] Suspensión y tapa cerrada desactivadas.
- [ ] IP fija o reserva DHCP anotada.

### Escenario B — servidor de la escuela

- [ ] Ficha del servidor completa (sección anterior).
- [ ] Python 3.10+ y MySQL 8.0+ verificados.
- [ ] Servicio systemd habilitado con `Restart=always`.
- [ ] `8000` abierto solo para la red del aula.
- [ ] `3306` cerrado al exterior.
- [ ] 3 notebooks y el televisor funcionan contra el servidor.
- [ ] Reinicio del servidor: la app vuelve sola.

### Escenario C — base remota

- [ ] Usuario `'escaperoom'@'IP-NOTEBOOK'`, nunca `'%'`.
- [ ] `3306` abierto solo para la IP de la notebook.
- [ ] Conexión remota probada con `nc` y con `mysql`.
- [ ] Corte de red probado: la app falla de forma visible, no inventa
      resultados.
- [ ] Reinicio de MySQL probado: la app se reconecta.
- [ ] Procedimiento de vuelta a A escrito y probado.

## Verificación

### 1. Waitress en A

```bash
feria2026/bin/python -m waitress --listen=0.0.0.0:8000 app:create_app
curl -i http://127.0.0.1:8000/salud
```

### 2. Servicio systemd

```bash
sudo systemctl restart escaperoom.service
sudo systemctl status escaperoom.service
sudo reboot
```

Después del reinicio, `curl -i http://127.0.0.1:8000/salud` debe responder
`200` sin que nadie inicie sesión.

### 3. Simulacro A

1. Levantar la app con `systemctl`.
2. Conectar 3 notebooks y un televisor.
3. Jugar con 3 equipos a la vez.
4. Cortar Internet y repetir una estación.
5. Reiniciar MySQL y confirmar que la app se reconecta.
6. Restaurar el backup del `paso12` en una base limpia.

### 4. Simulacro B

1. Repetir los pasos anteriores contra el servidor de la escuela.
2. Reiniciar el servidor y confirmar que el servicio vuelve solo.
3. Probar desde una notebook con la IP real del servidor.

### 5. Simulacro C

Solo si se decide usar C:

1. Jugar una estación completa con la base remota.
2. Cortar la red de la notebook y confirmar que la app falla de forma visible.
3. Restaurar la red y continuar.
4. Reiniciar MySQL en el servidor y confirmar la reconexión.
5. Volver a A siguiendo el procedimiento escrito.

## Orden de trabajo posterior a la feria

```text
¿Se quiere dejar la app funcionando todos los días en la escuela?
├── No → no ejecutar este paso. El paso12 alcanza para la feria.
└── Sí
    ├── ¿La notebook queda como servidor permanente?
    │   ├── Sí → escenario A con waitress y systemd.
    │   └── No
    │       ├── ¿El servidor de la escuela tiene Python y MySQL compatibles?
    │       │   ├── Sí → escenario B.
    │       │   └── No → quedarse en A o actualizar el servidor.
    │       └── ¿Se necesita la base en la escuela y la app en la notebook?
    │           ├── Sí y se ensayó → escenario C.
    │           └── No → A o B.
```

## Trampas conocidas

- No usar este paso para la feria: la feria es Flask con `scripts/feria.sh`.
- No dejar el servidor de desarrollo de Flask como servicio permanente.
- `Restart=always` no reemplaza un backup probado.
- Una distribución vieja puede traer Python 3.6 u 8 y MySQL 5.7; verificar
  antes de prometer el escenario B.
- Abrir `3306` a toda la red es un riesgo innecesario: en C va solo la IP de la
  notebook.
- Un servidor compartido que se reinicia o actualiza solo puede cortar el
  servicio. Confirmar la política antes.
- Una IP por DHCP puede cambiar y romper el escenario C.
- En C, el respaldo debe quedar en el servidor y copiarse afuera; si se pierde
  el servidor, se pierde todo.
- No restaurar sobre la base real sin backup previo y sin `--force` consciente.
- El reloj del equipo que corre MySQL es la fuente de tiempo: revisarlo.

## Al terminar

- Resumir qué escenarios quedaron probados, en qué equipos y con qué
  resultados.
- Anotar la ficha del servidor de la escuela y la configuración del servicio.
- Actualizar `README.md` y `MEMORY.md` con el estado final.
- Commit: `docs: waitress y systemd post-feria`.
