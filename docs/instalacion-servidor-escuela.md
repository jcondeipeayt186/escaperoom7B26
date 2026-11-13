# Instalación en el servidor de la escuela

Anexo de `docs/argumentos-pasos/paso12-congelar-y-puesta-en-marcha.md` para
dejar la aplicación funcionando en el **servidor Linux de la escuela**, que es
el respaldo de la notebook Ubuntu 22.04.

> **Para la feria del 16/11/2026** la notebook usa el servidor de desarrollo de
> Flask con `--host=0.0.0.0`; waitress y systemd son la puesta en producción
> posterior. Este anexo se conserva para ese momento y como respaldo.

> **Escenario principal:** notebook Ubuntu 22.04 con todo instalado (A). Se
> documenta en `docs/instalacion-y-puesta-en-funcionamiento.md`.
>
> **Este anexo:** servidor de la escuela con todo instalado (B) y la variante
> con la base en la escuela y la app en la notebook (C).
>
> La distribución y la versión exactas del servidor todavía no están
> confirmadas. La sección 2 permite averiguarlas y la 3 adapta los comandos.
> Hasta tenerlas, tratar este documento como **procedimiento a validar**, no
> como una receta probada.

## Contenido

- [1. Los tres escenarios](#1-los-tres-escenarios)
- [2. Recolectar los datos del servidor](#2-recolectar-los-datos-del-servidor)
- [3. Adaptar los comandos a la distribución](#3-adaptar-los-comandos-a-la-distribución)
- [4. Escenario B: todo en el servidor de la escuela](#4-escenario-b-todo-en-el-servidor-de-la-escuela)
- [5. Escenario C: MySQL en la escuela y la app en la notebook](#5-escenario-c-mysql-en-la-escuela-y-la-app-en-la-notebook)
- [6. Respaldos en B y C](#6-respaldos-en-b-y-c)
- [7. Problemas frecuentes](#7-problemas-frecuentes)
- [8. Checklists](#8-checklists)
- [9. Cómo decidir el día de la feria](#9-cómo-decidir-el-día-de-la-feria)

---

## 1. Los tres escenarios


|                                     | **A — Todo en la notebook**                            | **B — Todo en el servidor**                           | **C — Base en la escuela, app en la notebook**     |
| ------------------------------------- | --------------------------------------------------------- | -------------------------------------------------------- | ----------------------------------------------------- |
| Flask + waitress                    | Notebook Ubuntu 22.04                                   | Servidor de la escuela                                 | Notebook Ubuntu 22.04                               |
| MySQL 8                             | Notebook                                                | Servidor de la escuela                                 | Servidor de la escuela                              |
| Dependencia de red entre app y base | Ninguna                                                 | Ninguna                                                | Cada request depende de la LAN                      |
| Punto único de falla               | La notebook                                             | El servidor                                            | Dos equipos                                         |
| Permisos necesarios                 | Locales                                                 | `sudo` en el servidor                                  | `sudo` en ambos y abrir `3306` en la LAN            |
| Dónde se respalda                  | Notebook                                                | Servidor (o desde la notebook)                         | Servidor (o desde la notebook)                      |
| Complejidad                         | Baja, ya probada                                        | Media                                                  | Alta                                                |
| Riesgo principal                    | Suspensión, tapa cerrada o uso indebido de la notebook | Distro vieja, servidor compartido que se reinicia solo | Corte de red, reloj, seguridad de un MySQL expuesto |

Reglas para los tres:

- La app y la base deben quedar en la **misma red** que las notebooks y el
  televisor.
- El puerto de la app es `8000`; MySQL usa `3306` y **no se abre** salvo en C,
  con reglas restrictivas.
- La aplicación necesita **Python 3.10 o superior** en el equipo que la corre
  (`pytest 9.2` exige 3.10; Flask 3.1 acepta 3.9).
- La base necesita **MySQL 8.0 o superior** (o MariaDB 10.3 o superior). El
  ranking usa `ROW_NUMBER() OVER (...)` y el esquema usa columnas generadas y
  `CHECK`.
- Los tiempos del juego se calculan con `NOW(3)` de MySQL. **El reloj del
  motor de base es la autoridad**, no el de la notebook.

---

## 2. Recolectar los datos del servidor

Ejecutar **en el servidor de la escuela**. Algunos comandos piden `sudo`; si
alguno falla por permisos, anotarlo y seguir.

```bash
echo "=== Sistema ==="
cat /etc/os-release
uname -a
uname -m
nproc
free -h
df -h /

echo "=== Python ==="
python3 --version
command -v python3.10 python3.11 python3.12 2>/dev/null || true

echo "=== MySQL / MariaDB ==="
command -v mysql && mysql --version
command -v mariadb && mariadb --version
systemctl status mysql --no-pager 2>/dev/null || true
systemctl status mysqld --no-pager 2>/dev/null || true
systemctl status mariadb --no-pager 2>/dev/null || true

echo "=== systemd y permisos ==="
ps -p 1 -o comm=
systemctl --version | head -1
id
sudo -n true 2>/dev/null && echo "sudo sin clave: si" || echo "sudo sin clave: no"

echo "=== Red ==="
hostname -I
ip -4 addr show
ip route

echo "=== Firewall y puertos ==="
sudo ufw status verbose 2>/dev/null || true
sudo firewall-cmd --state 2>/dev/null || true
sudo ss -tlnp | grep -E ':(80|443|3306|8000)\b' || true

echo "=== Hora ==="
timedatectl 2>/dev/null || date

echo "=== Virtualización ==="
systemd-detect-virt 2>/dev/null || true
```

 El resultado es el siguiente:


```
echo "=== Sistema ==="
cat /etc/os-release
uname -a
uname -m
nproc
free -h
df -h /

echo "=== Python ==="
python3 --version
command -v python3.10 python3.11 python3.12 2>/dev/null || true

echo "=== MySQL / MariaDB ==="
command -v mysql && mysql --version
command -v mariadb && mariadb --version
systemctl status mysql --no-pager 2>/dev/null || true
systemctl status mysqld --no-pager 2>/dev/null || true
systemctl status mariadb --no-pager 2>/dev/null || true

echo "=== systemd y permisos ==="
ps -p 1 -o comm=
systemctl --version | head -1
id
sudo -n true 2>/dev/null && echo "sudo sin clave: si" || echo "sudo sin clave: no"

echo "=== Red ==="
hostname -I
ip -4 addr show
ip route

echo "=== Firewall y puertos ==="
sudo ufw status verbose 2>/dev/null || true
sudo firewall-cmd --state 2>/dev/null || true
sudo ss -tlnp | grep -E ':(80|443|3306|8000)\b' || true

echo "=== Hora ==="
timedatectl 2>/dev/null || date

echo "=== Virtualización ==="
systemd-detect-virt 2>/dev/null || true
=== Sistema ===
PRETTY_NAME="Ubuntu 26.04.1 LTS"
NAME="Ubuntu"
VERSION_ID="26.04"
VERSION="26.04.1 LTS (Resolute Raccoon)"
VERSION_CODENAME=resolute
ID=ubuntu
ID_LIKE=debian
HOME_URL="https://www.ubuntu.com/"
SUPPORT_URL="https://help.ubuntu.com/"
BUG_REPORT_URL="https://bugs.launchpad.net/ubuntu/"
PRIVACY_POLICY_URL="https://www.ubuntu.com/legal/terms-and-policies/privacy-policy"
UBUNTU_CODENAME=resolute
LOGO=ubuntu-logo
Linux ubuntu 7.0.0-43-generic #43-Ubuntu SMP PREEMPT_DYNAMIC Fri Oct 23 13:25:25 UTC 2026 x86_64 GNU/Linux
x86_64
6
               total        used        free      shared  buff/cache   available
Mem:            37Gi       1,6Gi        33Gi       248Mi       2,7Gi        35Gi
Swap:          8,0Gi          0B       8,0Gi
Filesystem                         Size  Used Avail Use% Mounted on
/dev/mapper/ubuntu--vg-ubuntu--lv  1,1T   23G  1,1T   3% /
=== Python ===
Python 3.14.4
=== MySQL / MariaDB ===
=== systemd y permisos ===
systemd
systemd 259 (259.9-0ubuntu0.1)
uid=1014(Profes) gid=1014(Profes) groups=1014(Profes),100(users)
sudo sin clave: no
=== Red ===
172.16.17.254 172.18.0.1 172.17.0.1 
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
2: enp2s0f0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP group default qlen 1000
    altname enx20283ee1f8ce
    inet 172.16.17.254/22 metric 100 brd 172.16.19.255 scope global dynamic enp2s0f0
       valid_lft 2407sec preferred_lft 2407sec
4: br-cfc2fa485f76: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default 
    inet 172.18.0.1/16 brd 172.18.255.255 scope global br-cfc2fa485f76
       valid_lft forever preferred_lft forever
5: docker0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN group default 
    inet 172.17.0.1/16 brd 172.17.255.255 scope global docker0
       valid_lft forever preferred_lft forever
default via 172.16.16.1 dev enp2s0f0 proto dhcp src 172.16.17.254 metric 100 
1.0.0.3 via 172.16.16.1 dev enp2s0f0 proto dhcp src 172.16.17.254 metric 100 
1.1.1.3 via 172.16.16.1 dev enp2s0f0 proto dhcp src 172.16.17.254 metric 100 
172.16.16.0/22 dev enp2s0f0 proto kernel scope link src 172.16.17.254 metric 100 
172.16.16.1 dev enp2s0f0 proto dhcp scope link src 172.16.17.254 metric 100 
172.17.0.0/16 dev docker0 proto kernel scope link src 172.17.0.1 linkdown 
172.18.0.0/16 dev br-cfc2fa485f76 proto kernel scope link src 172.18.0.1 
=== Firewall y puertos ===
sudo: I'm sorry Profes. I'm afraid I can't do that
=== Hora ===
               Local time: jue 2026-11-12 13:53:15 UTC
           Universal time: jue 2026-11-12 13:53:15 UTC
                 RTC time: jue 2026-11-12 13:53:15
                Time zone: Etc/UTC (UTC, +0000)
System clock synchronized: yes
              NTP service: active
          RTC in local TZ: no
=== Virtualización ===
none
```

### 2.1 Ficha del servidor

Completar con la salida anterior y guardarla junto al proyecto:


| Dato                                     | Valor                                      |
| ------------------------------------------ | -------------------------------------------- |
| Distribución y versión (`PRETTY_NAME`) |                                            |
| Arquitectura (`uname -m`)                |                                            |
| Python disponible                        |                                            |
| Motor y versión (`mysql --version`)     |                                            |
| Gestor de paquetes                       | `apt` / `dnf` / `zypper` / `pacman` / otro |
| Inicializa con systemd                   | sí / no                                   |
| Usuario con `sudo`                       |                                            |
| IP del servidor                          |                                            |
| IP fija o DHCP                           |                                            |
| Firewall activo                          | ufw / firewalld / nftables / ninguno       |
| Puertos `8000` y `3306` libres           | sí / no                                   |
| Reloj y zona horaria                     |                                            |
| ¿Servidor exclusivo o compartido?       |                                            |
| ¿Tiene UPS?                             |                                            |
| ¿Tiene Internet o mirror interno?       |                                            |

### 2.2 Criterios de viabilidad


| Verificación                                | Si falla                                                  |
| ---------------------------------------------- | ----------------------------------------------------------- |
| Python 3.10 o superior                       | Instalarlo o usar la notebook (A).                        |
| MySQL 8.0 o MariaDB 10.3 o superior          | Actualizar o instalar el motor compatible.                |
| `sudo` para paquetes y systemd               | Sin `sudo`, B y C no son viables.                         |
| Puerto `8000` libre                          | Elegir otro o liberar el existente.                       |
| Reloj correcto y zona horaria de Argentina   | Corregir antes de jugar.                                  |
| El servidor no se reinicia ni actualiza solo | Desactivar actualizaciones automáticas durante la feria. |
| Espacio suficiente (10 GB libres)            | Liberar espacio o usar otro equipo.                       |

---

## 3. Adaptar los comandos a la distribución

Los comandos de este anexo usan `apt` porque es el caso más probable y el ya
probado en la notebook. Si el servidor usa otro gestor, cambiar solo la
instalación de paquetes:


| Distribución                | Instalar base                                                                              | Firewall                |
| ------------------------------ | -------------------------------------------------------------------------------------------- | ------------------------- |
| Ubuntu / Debian              | `sudo apt install -y python3 python3-venv python3-pip mysql-server git`                    | `ufw`                   |
| Fedora / RHEL / Rocky / Alma | `sudo dnf install -y python3 python3-pip mysql-server git`                                 | `firewalld`             |
| openSUSE                     | `sudo zypper install -y python3 python3-pip python3-virtualenv mysql-community-server git` | `firewalld`             |
| Arch                         | `sudo pacman -S --needed python mysql git`                                                 | `nftables` / `iptables` |

Notas:

- En RHEL y derivados el servicio puede llamarse `mysqld` en lugar de `mysql`.
  Ajustar `systemctl` y el `After=` del servicio systemd.
- En openSUSE y Arch el paquete `mysql` puede instalar **MariaDB**. Verificar
  la versión con `mysql --version` antes de seguir.
- Si la distribución no trae `python3-venv`, el paquete puede llamarse
  `python3-virtualenv` o venir incluido en `python3`. Probar
  `python3 -m venv .venv` y, si falla, instalar el paquete correspondiente.
- En sistemas con **SELinux** (RHEL/Fedora), si el servicio no arranca, revisar
  `sudo ausearch -m avc -ts recent` antes de desactivar SELinux. No
  deshabilitarlo a ciegas.
- En sistemas con **AppArmor** (Ubuntu/openSUSE), el servicio en `/opt` suele
  funcionar sin cambios.

Verificar el gestor y la versión antes de instalar:

```bash
command -v apt dnf zypper pacman 2>/dev/null
cat /etc/os-release
```

---

## 4. Escenario B: todo en el servidor de la escuela

Flask, waitress y MySQL corren en el mismo servidor. Las notebooks solo abren
el navegador. Es el mismo esquema que la guía de Ubuntu, con los ajustes de
distribución de la sección 3.

### 4.1 Actualizar, zona horaria y paquetes

```bash
sudo timedatectl set-timezone America/Argentina/Buenos_Aires

# Ubuntu / Debian
sudo apt update
sudo apt install -y python3 python3-venv python3-pip mysql-server git

# Fedora / RHEL / Rocky / Alma
# sudo dnf install -y python3 python3-pip mysql-server git
```

Verificar versiones:

```bash
python3 --version
mysql --version
```

Se necesitan **Python 3.10+** y **MySQL 8.0+** (o MariaDB 10.3+).

Habilitar el motor:

```bash
sudo systemctl enable --now mysql
# En RHEL y derivados: sudo systemctl enable --now mysqld
sudo systemctl status mysql --no-pager
```

### 4.2 Copiar el proyecto

```bash
sudo mkdir -p /opt/escape-room-7b2026
sudo rsync -a --exclude .venv --exclude .venv2 --exclude .env \
  ./ /opt/escape-room-7b2026/
cd /opt/escape-room-7b2026
```

Si el proyecto se clona desde Git, usar la URL del repositorio en lugar de
`rsync`. No copiar `.venv` ni `.env` desde otra máquina: el entorno virtual no
es portable y el `.env` se arma de nuevo.

Crear el usuario del servicio:

```bash
sudo useradd --system --home /opt/escape-room-7b2026 \
  --shell /usr/sbin/nologin escaperoom
sudo chown -R escaperoom:escaperoom /opt/escape-room-7b2026
```

Si el usuario ya existe, omitir `useradd`.

### 4.3 Entorno virtual y dependencias

```bash
cd /opt/escape-room-7b2026
sudo -u escaperoom python3 -m venv .venv
sudo -u escaperoom .venv/bin/pip install --upgrade pip
sudo -u escaperoom .venv/bin/pip install -r requirements.txt
```

Comprobar que el entorno funciona:

```bash
sudo -u escaperoom .venv/bin/python -c "import flask, pymysql, dotenv, waitress; print('ok')"
```

### 4.4 Crear el `.env`

```bash
cd /opt/escape-room-7b2026
sudo -u escaperoom cp .env.example .env
sudo -u escaperoom chmod 600 .env
```

Generar los valores reales **con el entorno virtual**:

```bash
sudo -u escaperoom .venv/bin/python -c "import secrets; print(secrets.token_hex(32))"
sudo -u escaperoom .venv/bin/python -c "from werkzeug.security import generate_password_hash; print(generate_password_hash('LA-CLAVE-DEL-ADMIN'))"
```

Editar:

```bash
sudo -u escaperoom nano .env
```

Para el escenario B, `MYSQL_HOST` queda en `127.0.0.1` y `MYSQL_PORT` en
`3306`. La clave de `MYSQL_PASSWORD` debe coincidir con la del usuario de MySQL
que se crea en 4.6.

> `ADMIN_PASSWORD_HASH` contiene `$`. No usar `source .env` en scripts de
> shell: rompe la ejecución. Los scripts del proyecto leen el archivo línea por
> línea justamente por eso.

### 4.5 Crear la base y las tablas

```bash
cd /opt/escape-room-7b2026
sudo mysql < bd/schema.sql
```

### 4.6 Crear el usuario de MySQL

```bash
sudo mysql
```

```sql
CREATE USER 'escaperoom'@'localhost'
  IDENTIFIED BY 'una-clave-larga-y-propia';
CREATE USER 'escaperoom'@'127.0.0.1'
  IDENTIFIED BY 'una-clave-larga-y-propia';

GRANT ALL PRIVILEGES ON escape_room_7b2026.*
  TO 'escaperoom'@'localhost';
GRANT ALL PRIVILEGES ON escape_room_7b2026.*
  TO 'escaperoom'@'127.0.0.1';

GRANT ALL PRIVILEGES ON escape_room_7b2026_test.*
  TO 'escaperoom'@'localhost';
GRANT ALL PRIVILEGES ON escape_room_7b2026_test.*
  TO 'escaperoom'@'127.0.0.1';

GRANT ALL PRIVILEGES ON `escape\_room\_7b2026\_restore\_%`.*
  TO 'escaperoom'@'localhost';
GRANT ALL PRIVILEGES ON `escape\_room\_7b2026\_restore\_%`.*
  TO 'escaperoom'@'127.0.0.1';

FLUSH PRIVILEGES;
EXIT;
```

Usar la misma clave en `MYSQL_PASSWORD`. Si la clave tiene espacios, `#`, `$`
o comillas, escaparla según el motor. El permiso `_restore_` es el que usa
`scripts/restaurar.sh` para crear una base temporal sin tocar la real.

### 4.7 Cargar el contenido congelado

Opción 1, seeds separados (los tres son idempotentes):

```bash
cd /opt/escape-room-7b2026
mysql -u escaperoom -p < bd/seeds/001_contenido_inicial.sql
mysql -u escaperoom -p < bd/seeds/002_contenido_intermedio.sql
mysql -u escaperoom -p < bd/seeds/003_contenido_avanzado.sql
```

Cuando pida la clave, ingresar la misma de `MYSQL_PASSWORD`.

Opción 2, todo de una vez:

```bash
sudo mysql < bd/escape_room_7b2026_completa.sql
```

Ese archivo **elimina y vuelve a crear las 12 tablas**: usarlo solo en una base
nueva o con backup previo.

### 4.8 Verificar los conteos

```bash
mysql -u escaperoom -p -e "
USE escape_room_7b2026;
SELECT 'estacion' AS tabla, COUNT(*) AS filas FROM estacion
UNION ALL SELECT 'tema', COUNT(*) FROM tema
UNION ALL SELECT 'pregunta', COUNT(*) FROM pregunta
UNION ALL SELECT 'respuesta', COUNT(*) FROM respuesta
UNION ALL SELECT 'configuracion', COUNT(*) FROM configuracion;"
```

Esperado:


| Tabla           | Filas |
| ----------------- | ------- |
| `estacion`      | 5     |
| `tema`          | 14    |
| `pregunta`      | 80    |
| `respuesta`     | 240   |
| `configuracion` | 9     |

### 4.9 Probar a mano

```bash
cd /opt/escape-room-7b2026
sudo -u escaperoom .venv/bin/waitress-serve \
  --call --listen=127.0.0.1:8000 app:create_app
```

En otra terminal:

```bash
curl -i http://127.0.0.1:8000/salud
```

Esperado: `200` con `{"estado": "ok", "base": "ok"}`. Entrar a `/admin` con
`ADMIN_USER` y la clave elegida. Detener con `Ctrl+C`.

### 4.10 Servicio systemd

```bash
sudo nano /etc/systemd/system/escape-room.service
```

```ini
[Unit]
Description=Escape Room 7.º B 2026
After=network-online.target mysql.service
Wants=network-online.target

[Service]
Type=simple
User=escaperoom
Group=escaperoom
WorkingDirectory=/opt/escape-room-7b2026
EnvironmentFile=/opt/escape-room-7b2026/.env
ExecStart=/opt/escape-room-7b2026/.venv/bin/waitress-serve --call --listen=0.0.0.0:8000 app:create_app
Restart=always
RestartSec=5
NoNewPrivileges=true
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

En RHEL y derivados, cambiar `mysql.service` por `mysqld.service`.

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now escape-room
sudo systemctl status escape-room --no-pager
journalctl -u escape-room -f
```

### 4.11 Firewall, IP y acceso

Abrir `8000` solo para la red del aula.

**ufw:**

```bash
sudo ufw allow OpenSSH
sudo ufw allow from 192.168.1.0/24 to any port 8000 proto tcp
sudo ufw enable
sudo ufw status verbose
```

**firewalld:**

```bash
sudo firewall-cmd --permanent --add-service=ssh
sudo firewall-cmd --permanent --add-rich-rule='rule family="ipv4" source address="192.168.1.0/24" port port="8000" protocol="tcp" accept'
sudo firewall-cmd --reload
sudo firewall-cmd --list-all
```

Averiguar la IP:

```bash
hostname -I
ip -4 addr show
```

Dejar IP fija o reserva DHCP en el router. Con IP cambiante, las notebooks y el
televisor dejan de encontrar el servidor.

No abrir `3306` en B: MySQL escucha solo en `127.0.0.1`.

Probar desde una notebook:

```text
http://IP-DEL-SERVIDOR:8000
http://IP-DEL-SERVIDOR:8000/ranking
```

### 4.12 Desactivar suspensión y actualizaciones automáticas

Si el servidor es una notebook o un equipo de escritorio:

```bash
sudo systemctl mask sleep.target suspend.target hibernate.target hybrid-sleep.target
gsettings set org.gnome.settings-daemon.plugins.power sleep-inactive-ac-type 'nothing' 2>/dev/null || true
```

Antes de la feria, pausar actualizaciones automáticas según la distribución.
En Ubuntu, la guía principal tiene el procedimiento en la sección 13. En
Fedora/RHEL revisar `dnf-automatic`; en openSUSE, `zypper` y los timers de
`systemd`. No hace falta desinstalar nada: alcanza con no reiniciar durante la
feria y dejar los cambios para después.

---

## 5. Escenario C: MySQL en la escuela y la app en la notebook

La notebook corre Flask y waitress; el servidor de la escuela solo corre MySQL.
Cada request del juego viaja por la LAN hasta la base.

**Este escenario tiene más piezas y más formas de fallar.** Usarlo solo si hay
una ventaja concreta: por ejemplo, que el servidor tenga UPS y respaldos y la
notebook no pueda quedar dedicada. No improvisarlo el día de la feria.

### 5.1 Preparar MySQL en el servidor de la escuela

#### a) Escuchar en la red

Localizar el archivo de configuración:

```bash
mysql --help --verbose 2>/dev/null | grep -A1 "Default options"
ls /etc/mysql/mysql.conf.d/ 2>/dev/null
ls /etc/my.cnf /etc/my.cnf.d/ 2>/dev/null
```

En Ubuntu/Debian: `/etc/mysql/mysql.conf.d/mysqld.cnf`.
En RHEL y derivados: `/etc/my.cnf` o `/etc/my.cnf.d/mysql-server.cnf`.

Dejar la dirección de la LAN del servidor (mejor que `0.0.0.0`):

```ini
bind-address = 192.168.1.10
```

o, si no se conoce la IP fija:

```ini
bind-address = 0.0.0.0
```

Con `0.0.0.0`, el firewall es obligatorio.

```bash
sudo systemctl restart mysql
sudo ss -tlnp | grep 3306
```

Debe escuchar en la IP de la LAN (o en `0.0.0.0`).

#### b) Usuario restringido a la notebook

Reemplazar `192.168.1.50` por la IP real de la notebook. **No usar `'%'`**: eso
permite conexiones desde cualquier equipo de la red.

```bash
sudo mysql
```

```sql
CREATE USER 'escaperoom'@'192.168.1.50'
  IDENTIFIED BY 'una-clave-larga-y-propia';

GRANT ALL PRIVILEGES ON escape_room_7b2026.*
  TO 'escaperoom'@'192.168.1.50';

GRANT ALL PRIVILEGES ON escape_room_7b2026_test.*
  TO 'escaperoom'@'192.168.1.50';

GRANT ALL PRIVILEGES ON `escape\_room\_7b2026\_restore\_%`.*
  TO 'escaperoom'@'192.168.1.50';

FLUSH PRIVILEGES;
SHOW GRANTS FOR 'escaperoom'@'192.168.1.50';
EXIT;
```

Los permisos sobre `_test` son solo para poder correr `pytest` desde la
notebook. La base de test se crea y se borra en el servidor, nunca toca
`escape_room_7b2026`. El permiso `_restore_` permite que
`scripts/restaurar.sh` cree una base temporal desde la notebook.

#### c) Crear el esquema y cargar el contenido

En el servidor:

```bash
cd /opt/escape-room-7b2026   # o donde esté copiado el proyecto
sudo mysql < bd/schema.sql
sudo mysql < bd/seeds/001_contenido_inicial.sql
sudo mysql < bd/seeds/002_contenido_intermedio.sql
sudo mysql < bd/seeds/003_contenido_avanzado.sql
```

O todo de una vez:

```bash
sudo mysql < bd/escape_room_7b2026_completa.sql
```

En C no hace falta copiar toda la app al servidor: alcanza con los archivos de
`bd/`. También se pueden cargar los seeds desde la notebook, apuntando al
servidor:

```bash
mysql -h 192.168.1.10 -u escaperoom -p < bd/seeds/001_contenido_inicial.sql
mysql -h 192.168.1.10 -u escaperoom -p < bd/seeds/002_contenido_intermedio.sql
mysql -h 192.168.1.10 -u escaperoom -p < bd/seeds/003_contenido_avanzado.sql
```

#### d) Abrir `3306` solo para la notebook

**ufw:**

```bash
sudo ufw allow from 192.168.1.50 to any port 3306 proto tcp
sudo ufw status verbose
```

**firewalld:**

```bash
sudo firewall-cmd --permanent --add-rich-rule='rule family="ipv4" source address="192.168.1.50" port port="3306" protocol="tcp" accept'
sudo firewall-cmd --reload
```

No abrir `3306` para `192.168.1.0/24`: solo para la IP de la notebook.

#### e) Reloj

```bash
sudo timedatectl set-timezone America/Argentina/Buenos_Aires
timedatectl
```

El reloj del servidor es la autoridad de todos los tiempos del juego: la app
inserta `NOW(3)` de MySQL en cada fecha. Si el reloj está mal, el ranking y las
eliminaciones por tiempo quedan mal.

### 5.2 Preparar la notebook

La notebook ya debe tener el proyecto, Python 3.10+ y el entorno virtual
siguiendo `docs/instalacion-y-puesta-en-funcionamiento.md`, pero **sin**
instalar MySQL local.

Editar `.env`:

```dotenv
FLASK_SECRET_KEY=la-clave-generada
MYSQL_HOST=192.168.1.10
MYSQL_PORT=3306
MYSQL_USER=escaperoom
MYSQL_PASSWORD=la-clave-del-usuario
MYSQL_DB=escape_room_7b2026
ADMIN_USER=admin
ADMIN_PASSWORD_HASH=el-hash-generado
```

Probar la conexión remota antes de levantar la app:

```bash
mysql -h 192.168.1.10 -P 3306 -u escaperoom -p -e "SELECT VERSION(), NOW();"
nc -vz 192.168.1.10 3306
```

Si `mysql` no está instalado en la notebook, `nc` alcanza para comprobar que el
puerto llega. La app usa PyMySQL, no el cliente.

Levantar:

```bash
cd /opt/escape-room-7b2026
.venv/bin/waitress-serve --call --listen=0.0.0.0:8000 app:create_app
```

(usar la ruta real del entorno virtual de la notebook).

Comprobar:

```bash
curl -i http://127.0.0.1:8000/salud
```

Debe devolver `{"estado": "ok", "base": "ok"}`. Si devuelve `503`, el problema
está en la red, el firewall, el usuario o la clave de MySQL.

El servicio systemd de la notebook es el mismo de 4.10.

### 5.3 Probar y operar C

- Abrir `http://IP-DE-LA-NOTEBOOK:8000` desde otra máquina.
- Jugar una estación completa y confirmar que avanza.
- Cortar el cable o el Wi-Fi y comprobar qué pasa: la app debe mostrar un error
  de base, no un resultado falso. **No se puede jugar sin red en C.**
- Reiniciar MySQL en el servidor y confirmar que la app se reconecta.
- Correr `pytest` desde la notebook solo fuera del horario de la feria: usa la
  base de test remota y necesita crear y borrar bases.

### 5.4 Seguridad de C

- `'escaperoom'@'IP-NOTEBOOK'`, nunca `'%'`.
- `3306` abierto solo para esa IP.
- Clave larga y distinta de la de otros servicios.
- No exponer `3306` a Internet.
- Si el servidor y la notebook están en VLAN separadas, confirmar el ruteo
  antes de la feria.
- TLS entre la app y MySQL es opcional en una LAN cerrada; agregarlo exige
  certificados y configuración extra. No es parte de este plan.
- Respaldar en el servidor y copiar el archivo a un pendrive: si se pierde el
  servidor, se pierde todo el historial.

### 5.5 Revertir C

Si algo falla, volver a A:

1. Detener el servicio de la notebook.
2. Restaurar el último respaldo en el MySQL local de la notebook.
3. Cambiar `.env` a `MYSQL_HOST=127.0.0.1`.
4. Levantar de nuevo.

Tener este procedimiento escrito y probado **antes** de la feria.

---

## 6. Respaldos en B y C

Los scripts `scripts/backup.sh` y `scripts/restaurar.sh` funcionan en los tres
escenarios: leen `MYSQL_HOST`, `MYSQL_PORT`, `MYSQL_USER`, `MYSQL_PASSWORD` y
`MYSQL_DB` del `.env`.

### 6.1 Generar un respaldo

```bash
cd /opt/escape-room-7b2026
./scripts/backup.sh "$HOME/backups-escaperoom"
```

`/var/backups/escaperoom` también sirve si el usuario tiene permiso de
escritura; no ejecutar el script como `sudo` salvo que sea necesario, porque
cambia el `$HOME` y los permisos de los archivos.

En C, se puede ejecutar desde la notebook: el cliente `mysqldump` se conecta al
servidor remoto con los datos del `.env`. Para eso la notebook necesita el
paquete `mysql-client` (o `mariadb-client`) instalado. Si no lo tiene, ejecutar
el respaldo en el servidor.

El archivo no incluye `CREATE DATABASE` ni `USE`, así que se restaura siempre en
una base elegida a mano.

### 6.2 Probar la restauración

```bash
./scripts/restaurar.sh "$HOME/backups-escaperoom/respaldo-....sql"
```

Crea una base `<MYSQL_DB>_restore_AAAAMMDD-HHMMSS`, restaura y muestra los
conteos. Esperado: `5, 14, 80, 240 y 9`. El usuario del `.env` necesita el
permiso sobre `escape\_room\_7b2026\_restore\_%` que se otorga en 4.6 y 5.1.b.

El script se niega a restaurar sobre `MYSQL_DB` o sobre una base existente sin
`--force`. Esa protección evita pisar la base de la feria por error.

Cuando ya se verificaron los conteos, borrar la base temporal:

```bash
sudo mysql -e "DROP DATABASE escape_room_7b2026_restore_AAAAMMDD-HHMMSS;"
```

### 6.3 Frecuencia

- Antes de la feria.
- Al terminar cada día de feria.
- Antes de cualquier cambio de esquema o de contenido.
- Copiar cada respaldo a un pendrive **fuera** del servidor y de la notebook.

### 6.4 Restauración real

Solo si hay que reemplazar la base buena:

```bash
# Detener la app
sudo systemctl stop escape-room

# Restaurar con --force, con el nombre real
cd /opt/escape-room-7b2026
./scripts/restaurar.sh /ruta/al/respaldo.sql escape_room_7b2026 --force

# Verificar y volver a levantar
sudo systemctl start escape-room
```

Probar este procedimiento en un ensayo, no el día de la feria.

---

## 7. Problemas frecuentes


| Síntoma                                       | Causa probable                      | Solución                                                           |
| ------------------------------------------------ | ------------------------------------- | --------------------------------------------------------------------- |
| `python3 -m venv` falla                        | Falta el paquete `venv`             | Instalar `python3-venv` (Debian/Ubuntu) o `python3-virtualenv`.     |
| `pytest` no instala o falla al arrancar        | Python menor a 3.10                 | Instalar 3.10+ o usar la notebook.                                  |
| `ROW_NUMBER` no existe                         | MySQL 5.7 o MariaDB vieja           | Actualizar a MySQL 8.0+ / MariaDB 10.3+.                            |
| El servicio no arranca y `journalctl` no ayuda | SELinux o ruta equivocada           | Revisar `ausearch -m avc -ts recent`; confirmar `WorkingDirectory`. |
| `Can't connect to MySQL server` en C           | `bind-address`, firewall o IP mal   | Revisar 5.1.c, `ss -tlnp`, `ufw status`.                            |
| `Access denied for user ...@'IP'`              | Usuario creado para otro host       | Crear `'escaperoom'@'IP-NOTEBOOK'` y `FLUSH PRIVILEGES`.            |
| `Host ... is not allowed to connect`           | Falta el usuario para esa IP        | Igual que arriba.                                                   |
| La app anda local y no desde las notebooks     | waitress escucha en `127.0.0.1`     | Usar `--listen=0.0.0.0:8000` y abrir el firewall.                   |
| Se pierde la conexión a mitad del juego en C  | Wi-Fi o cable inestable             | Pasar a A o B; no hay modo offline en C.                            |
| El ranking muestra tiempos raros               | Reloj del servidor desfasado        | `timedatectl`, sincronizar y reiniciar MySQL.                       |
| El respaldo queda vacío                       | `mysqldump` falló por permisos     | Revisar `MYSQL_USER` y probar el cliente a mano.                    |
| `restaurar.sh` se niega                        | La base destino existe o es la real | Usar otro nombre o `--force` con cuidado.                           |

---

## 8. Checklists

### 8.1 Checklist del escenario B

- [ ]  Distribución y versión anotadas en la ficha (sección 2.1).
- [ ]  Python 3.10 o superior.
- [ ]  MySQL 8.0 o superior, activo y en `127.0.0.1:3306`.
- [ ]  Proyecto copiado en `/opt/escape-room-7b2026` y con dueño `escaperoom`.
- [ ]  `.venv` creado en el servidor y dependencias instaladas.
- [ ]  `.env` real, con permisos `600` y fuera de Git.
- [ ]  Esquema y contenido cargados; conteos `5/14/80/240/9`.
- [ ]  `/salud` responde `200` con `base: ok`.
- [ ]  `/admin` entra con el usuario y la clave reales.
- [ ]  Servicio systemd habilitado y con `Restart=always`.
- [ ]  `8000` abierto solo para la red del aula.
- [ ]  `3306` cerrado al exterior.
- [ ]  IP fija o reserva DHCP.
- [ ]  Suspensión y actualizaciones automáticas desactivadas.
- [ ]  Backup generado y **restaurado** en una base de prueba.
- [ ]  Simulacro con 3 notebooks y el televisor.
- [ ]  Funciona sin Internet.

### 8.2 Checklist del escenario C

Todo lo de B que aplique, más:

- [ ]  IP del servidor y de la notebook anotadas y fijas.
- [ ]  `bind-address` apunta a la LAN (o `0.0.0.0` con firewall).
- [ ]  Usuario `'escaperoom'@'IP-NOTEBOOK'`, sin `'%'`.
- [ ]  Permisos sobre la base real y la de test.
- [ ]  `3306` abierto solo para la IP de la notebook.
- [ ]  Conexión remota probada con `nc` y con `mysql`.
- [ ]  `.env` de la notebook apunta al servidor.
- [ ]  Reloj del servidor sincronizado.
- [ ]  Backup probado; copia fuera del servidor.
- [ ]  Procedimiento de vuelta a A escrito y probado.
- [ ]  Simulacro con corte de red y reinicio de MySQL.

---

## 9. Cómo decidir el día de la feria

Orden recomendado:

1. **Usar A (notebook) como principal.** Es el escenario ya probado y no
   depende de la red entre la app y la base.
2. **Tener B (servidor de la escuela) listo como respaldo.** Se activa si la
   notebook no arranca, se queda sin batería o se rompe.
3. **C solo si se ensayó antes** y hay una razón concreta: UPS, respaldos
   centralizados o una notebook que no puede quedar dedicada.

Árbol de decisión:

```text
¿La notebook arranca y tiene la app probada?
├── Sí → usar A.
└── No
    ├── ¿El servidor de la escuela tiene la app instalada y probada?
    │   ├── Sí → usar B.
    │   └── No → no hay plan C improvisado: reinstalar A en otra notebook
    │            o resolver el servidor con el procedimiento de este anexo.
    └── ¿Se ensayó C con corte de red y reloj?
        ├── Sí → usar C solo si A y B no son viables.
        └── No → no usar C.
```

Reglas para el día:

- No instalar paquetes ni actualizar el sistema.
- No cambiar el esquema ni cargar contenido.
- No restaurar sobre la base real sin backup previo.
- Anotar qué escenario se está usando y en qué equipo.
- Tener el backup en un pendrive y el `.env` en un lugar seguro.
