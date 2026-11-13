# Guía de estudio para estudiantes de 7.º B

> Para los equipos que van a jugar y para los estudiantes de 7.º B que
> acompañan el stand y leen las pistas. Feria de Producciones del
> **16/11/2026**, IPEATyM 186 Castagnari.

Esta guía te dice **qué estudiar** para jugar, **cómo está armado el proyecto**
y **cómo levantarlo en tu computadora**. También explica qué vas a encontrar en
cada archivo `.md` del repositorio y cuáles conviene evitar antes de jugar
porque tienen respuestas.

## Contenido

- [1. Empezá por acá](#1-empezá-por-acá)
- [2. Ruta de estudio según el nivel](#2-ruta-de-estudio-según-el-nivel)
- [3. Ruta para estudiantes de 7.º B que atienden el stand](#3-ruta-para-estudiantes-de-7º-b-que-atienden-el-stand)
- [4. Qué mirar en cada estación](#4-qué-mirar-en-cada-estación)
- [5. Plan sugerido de tres sesiones](#5-plan-sugerido-de-tres-sesiones)
- [6. Cómo está armado el proyecto](#6-cómo-está-armado-el-proyecto)
- [7. Cómo leer el código](#7-cómo-leer-el-código)
- [8. Mapa completo de archivos `.md`](#8-mapa-completo-de-archivos-md)
- [9. Instalación básica en tu computadora](#9-instalación-básica-en-tu-computadora)
- [10. Cómo estudiar mejor](#10-cómo-estudiar-mejor)
- [11. Antes de la feria: checklist](#11-antes-de-la-feria-checklist)
- [12. Material que no es `.md`](#12-material-que-no-es-md)

## 1. Empezá por acá

Antes de abrir archivos, definí tu rol:

- **Vas a jugar en un equipo:** estudiá los conceptos de las cinco estaciones.
  No memorices preguntas ni opciones.
- **Vas a estar en el stand como parte de 7.º B:** además de los conceptos,
  necesitás las reglas, el recorrido de la app y el texto de presentación.
- **Te toca explicar cómo está hecha la app:** sumá las secciones 6 y 7, que
  explican el scaffolding y cómo leer el código.

### Tres ideas que ordenan todo el estudio

1. **Las preguntas se sortean.** Cada intento arma 4 preguntas al azar entre
   las disponibles de ese nivel (20 en `inicial`, 30 en `intermedio` y 30 en
   `avanzado`). Estudiar de memoria una pregunta no sirve: hay que entender el
   concepto.
2. **Se estudia por estación, no por archivo.** Las cinco estaciones son Redes,
   Hardware, Internet, Ciberseguridad y Sistemas Operativos. Cada archivo de
   contenido está ordenado con esa misma estructura.
3. **Cuidado con los archivos que tienen respuestas.** Algunos documentos son
   para docentes u organización. Están marcados más abajo con 🔴.

## 2. Ruta de estudio según el nivel

| Nivel | Qué leer | Cómo practicar |
| --- | --- | --- |
| **Inicial** | Las reglas, el puntaje y la metodología de [`escape-room.md`](escape-room.md), todo antes del anexo. Las pistas del nivel inicial en [`pistas-del-juego.md`](pistas-del-juego.md). El **Glosario mínimo** de la guía intermedia. | Leé cada pista y respondé en voz alta antes de mirar las opciones. Explicá el concepto con tus palabras. |
| **Intermedio** | [`contenido-para-responder-nivel-intermedio.md`](contenido-para-responder-nivel-intermedio.md), de principio a fin. | Al terminar cada estación, cerrá el archivo y contá qué aprendiste. Después compará con las pistas de esa estación. |
| **Avanzado** | [`contenido-para-responder-nivel-avanzado.md`](contenido-para-responder-nivel-avanzado.md), de principio a fin. | Mismo método, pero poné el foco en comparar conceptos parecidos (por ejemplo, tipos de memoria, protocolos o estados). |

> ⚠️ **Si vas a jugar el nivel inicial, no leas el anexo de
> [`escape-room.md`](escape-room.md)** (desde "Anexo: contenido inicial"). Tiene
> la tabla con las respuestas correctas. Las secciones anteriores sí son útiles:
> explican las reglas del juego.

## 3. Ruta para estudiantes de 7.º B que atienden el stand

| Momento | Qué leer | Para qué |
| --- | --- | --- |
| Antes de la feria | [`escape-room.md`](escape-room.md), las secciones de reglas, puntaje y metodología (antes del anexo) | Explicar reglas, tiempos, ayudas, eliminación y ranking sin dudar. |
| Antes de la feria | Las dos guías de contenido: [intermedio](contenido-para-responder-nivel-intermedio.md) y [avanzado](contenido-para-responder-nivel-avanzado.md) | Responder preguntas de los visitantes y acompañar a los equipos. |
| Para presentar el proyecto | [`proyectoEscapeRoom-7B.md`](proyectoEscapeRoom-7B.md) | Tener un texto corto y claro sobre qué es el proyecto y cómo se juega. |
| Para conocer la app | [`navegacion-por-app.md`](navegacion-por-app.md) y [`navegacion-capturas.md`](navegacion-capturas.md) | Saber qué pantalla sigue, qué muestra el HUD y cómo se ve el recorrido completo. |
| Para explicar cómo está hecha | Esta guía, secciones 6 y 7 | Contar el scaffolding, las carpetas y el recorrido de una petición. |
| Durante la feria | [`pistas-del-juego.md`](pistas-del-juego.md), impreso | Leer la pista fácil o difícil cuando el equipo pide una ayuda. La app **no** muestra el texto. |
| Si te toca explicar la tecnología | [`tecnologias.md`](tecnologias.md) | Entender el stack y poder contarlo con ejemplos simples. |
| Si te toca armar el stand | [`ideas-escape-room.md`](ideas-escape-room.md) | Ideas de banner, redes y ping pong (no son requisitos de la app). |
| Si te toca probar o instalar | Esta guía §9, [`ayuda-al-probar.md`](ayuda-al-probar.md) y las guías de instalación | Levantar la app, probar el recorrido y revisar la base. |

**Regla de oro para el stand:** no reveles la respuesta correcta. Si el equipo
pide una ayuda, leé la pista en papel y dejá que decidan.

## 4. Qué mirar en cada estación

Esta tabla es el corazón del estudio. No contiene respuestas: solo los temas que
hay que poder explicar.

| Estación | Conceptos para estudiar | Dónde leerlos |
| --- | --- | --- |
| **1. Redes** | Dirección IP, loopback, máscara de subred, DHCP, switch y hub, DNS, punto de acceso WiFi, modelo OSI y capa 3, ARP, TCP y UDP, NAT, WPA3. | Guía intermedia (estación 1) y guía avanzada (estación 1). |
| **2. Hardware** | SMART y salud del disco, pantalla azul, copias de seguridad, pasta térmica y refrigeración, mantenimiento preventivo y correctivo, RAM volátil, memoria caché, SRAM y DRAM, SSD y desgaste, PCI Express, HDD y SSD, memoria virtual. | Guía intermedia (estación 2) y guía avanzada (estación 2). |
| **3. Internet** | Cookies, modo incógnito, partes de una URL y parámetros, ancho de banda y latencia, DNS, códigos de estado HTTP, HTTP y HTTPS, caché del navegador. | Guía intermedia (estación 3) y guía avanzada (estación 3). |
| **4. Ciberseguridad** | Autenticación de dos factores, gestores de contraseñas, reutilización de contraseñas, smishing y vishing, correos urgentes y enlaces, fuerza bruta, man-in-the-middle, zero-day, integridad/confidencialidad/disponibilidad, ransomware, ingeniería social. | Guía intermedia (estación 4) y guía avanzada (estación 4). |
| **5. Sistemas Operativos** | Procesos, sistema de archivos, permisos de usuario, actualizaciones, permisos en móviles, Android e iOS, kernel, procesos zombie, planificación Round Robin, deadlock, diferencia entre proceso e hilo, aplicaciones fuera de la tienda oficial. | Guía intermedia (estación 5) y guía avanzada (estación 5). |

### Cómo saber si un tema está estudiado

Podés explicarlo sin leer, dar un ejemplo propio y distinguirlo de un concepto
parecido. Por ejemplo: no alcanza con decir "la RAM guarda datos"; hay que poder
explicar **qué tipo de datos**, **por cuánto tiempo** y **en qué se diferencia
del disco**.

## 5. Plan sugerido de tres sesiones

| Sesión | Duración | Actividad |
| --- | --- | --- |
| **1** | 45 min | Leer las reglas del juego y las estaciones 1 y 2 de la guía de tu nivel. Cerrar el archivo y explicar cada tema a otra persona. |
| **2** | 45 min | Leer las estaciones 3, 4 y 5. Armar tres tarjetas por estación: concepto, ejemplo y error típico. |
| **3** | 45 min | Repasar el glosario, practicar con las pistas y simular una estación: 4 preguntas, 4 minutos, sin mirar el archivo. |
| **Extra para 7.º B** | 30 min | Leer el texto de presentación, recorrer las capturas de la app y practicar el discurso del stand. |

Si tenés menos tiempo, priorizá así: **reglas → estación 1 → estación 4 →
glosario → el resto**.

## 6. Cómo está armado el proyecto

El proyecto es una **aplicación web**: hay un servidor (Python + Flask) que
recibe pedidos, consulta una base de datos (MySQL) y devuelve HTML. No hay una
app aparte para el celular ni un framework de JavaScript como React o Vue.

### 6.1 El árbol del proyecto

```text
escaperoom7B26/
├── app/                  # la aplicación web
│   ├── __init__.py       # crea la app, lee .env y registra las rutas
│   ├── db.py             # conexión a MySQL y transacciones
│   ├── csrf.py           # protección de los formularios
│   ├── routes/           # qué responde cada URL
│   ├── servicios/        # reglas del juego, sin HTML
│   ├── templates/        # HTML que arma el servidor
│   └── static/           # CSS, JS, imágenes, audio y Bootstrap
├── bd/                   # estructura y contenido de la base
├── tests/                # pruebas automáticas
├── docs/                 # documentación y material de la feria
├── requirements.txt      # dependencias de Python
├── .env.example          # plantilla de configuración
└── README.md             # presentación y puesta en marcha
```

La estructura completa, archivo por archivo, está en la sección 4 de
[`README.md`](../README.md). No hace falta memorizarla: alcanza con entender
para qué sirve cada carpeta.

### 6.2 Qué hay en cada carpeta

| Carpeta o archivo | Qué contiene | Para qué te sirve |
| --- | --- | --- |
| `app/` | Todo el código de la aplicación. | Es el corazón del proyecto. |
| `app/__init__.py` | La función que crea la app, lee `.env`, registra las rutas y define `/salud`. | Punto de entrada para entender cómo arranca todo. |
| `app/db.py` | La conexión a MySQL y el helper de transacciones. | Ahí se ve cómo habla la app con la base. |
| `app/csrf.py` | El token que protege los formularios. | Explica por qué un POST sin token se rechaza. |
| `app/routes/` | Un archivo por grupo de pantallas: `juego.py`, `ranking.py`, `estadisticas.py` y `admin.py`. | Ahí se decide qué responde cada URL. |
| `app/servicios/` | Las reglas del juego: equipos, estaciones, selección, envíos, tiempos, ranking y administración. | Ahí vive la lógica; no hay HTML. |
| `app/templates/` | Las plantillas Jinja que arman el HTML. | Ahí se ve qué muestra cada pantalla. |
| `app/static/` | CSS, JavaScript, imágenes, audio y Bootstrap local. | Ahí está todo lo que usa el navegador. |
| `bd/` | `schema.sql` y los tres seeds. | Ahí se crea la base y se carga el contenido. |
| `tests/` | Las pruebas automáticas con pytest. | Ahí se comprueba que las reglas funcionen. |
| `docs/` | Requisitos, guías, pistas y material de la feria. | Ahí está todo lo que se lee y se imprime. |
| `requirements.txt` | Las dependencias de Python con sus versiones. | Se usa al crear el entorno virtual. |
| `.env.example` | La plantilla de configuración. | Se copia a `.env` para levantar la app. |
| `README.md` | La presentación del repositorio. | Es la primera lectura para quien llega. |
| `AGENTS.md` | Las reglas y decisiones del proyecto. | Es la referencia para quien desarrolla. |
| `MEMORY.md` | El estado actual del proyecto. | Sirve para saber qué está hecho. |

### 6.3 El recorrido de una petición

Cuando un equipo abre la estación 1, pasa esto:

```text
Navegador
   │  GET /juego/estacion/1
   ▼
app/routes/juego.py
   │  llama a
   ▼
app/servicios/estaciones.py, seleccion.py y tiempos.py
   │  consultan
   ▼
app/db.py  ──►  MySQL (bd/schema.sql)
   │
   ▼
app/templates/estacion.html + _hud.html
   │
   ▼
Navegador  ◄── HTML
   │  static/js/temporizadores.js
   ▼
GET /juego/estado  (cada 10 segundos)
```

En palabras:

1. El navegador pide una URL.
2. La ruta correspondiente en `app/routes/` atiende el pedido.
3. La ruta llama a uno o más servicios de `app/servicios/`.
4. Los servicios consultan MySQL a través de `app/db.py`.
5. La ruta arma una plantilla de `app/templates/` con los datos.
6. El navegador recibe el HTML y el JavaScript de `app/static/js/` sincroniza los
   contadores con `/juego/estado`.

### 6.4 La regla de oro: el servidor es la autoridad

Las respuestas correctas **no viajan al navegador**. El equipo solo envía qué
opción eligió; el servidor decide si es correcta, calcula los tiempos con las
fechas de MySQL y guarda todo. Por eso no se puede "hacer trampa" mirando el
código de la página.

Tampoco se puede saltar una estación escribiendo otra URL: la ruta valida el
orden y redirige a la estación actual.

### 6.5 Lo que el proyecto no usa

- No hay React, Vue ni otro framework de frontend.
- No hay Node.js ni un paso de build.
- No hay Docker en la feria.
- No hay CDN: Bootstrap, el audio, las imágenes y los gráficos son locales.
- No hay una app móvil: se juega desde el navegador.

## 7. Cómo leer el código

No hace falta leer todo el proyecto para entenderlo. Con este orden alcanza:

| Paso | Archivo | Qué mirar |
| --- | --- | --- |
| 1 | [`README.md`](../README.md), sección 4 | La estructura completa y qué hace cada servicio. |
| 2 | `app/__init__.py` | `create_app()`, la lectura de `.env`, `/salud` y el registro de rutas. |
| 3 | `app/routes/juego.py` | El recorrido: bienvenida, identificación, estación, transición y final. |
| 4 | `app/servicios/estaciones.py`, `seleccion.py` y `tiempos.py` | Cómo se elige la estación, cómo se sortean las 4 preguntas y cómo se calculan los contadores. |
| 5 | `app/servicios/envios.py` | Qué pasa al enviar respuestas: correctas, incorrectas, ayudas y cierre. |
| 6 | `app/templates/base.html`, `_hud.html` y `estacion.html` | Qué ve el equipo y qué datos muestra el HUD. |
| 7 | `app/static/js/temporizadores.js` | Cómo el navegador dibuja la cuenta y consulta `/juego/estado`. |
| 8 | `bd/schema.sql` y [`sql/descripcion-de-la-base-de-datos.md`](../sql/descripcion-de-la-base-de-datos.md) | Las tablas y cómo se relacionan. |
| 9 | `tests/test_reglas_juego.py` | Cómo se comprueban las reglas del juego. |

Si te trabás, volvé al README y a la sección 6 de esta guía. No hace falta
entender cada línea: alcanza con poder explicar **qué hace** cada archivo y
**con quién habla**.

### 7.1 Glosario de la aplicación

| Término | Qué significa |
| --- | --- |
| **Cliente** | El navegador que pide páginas. |
| **Servidor** | El programa Flask que responde y decide. |
| **Ruta o endpoint** | Una URL con una función que la atiende. |
| **Blueprint** | Un grupo de rutas relacionadas (`juego`, `ranking`, `admin`). |
| **App factory** | La función `create_app()` que arma la aplicación. |
| **Plantilla Jinja** | Un HTML con huecos que el servidor completa. |
| **Servicio** | Un módulo con reglas del juego, sin HTML. |
| **Request / response** | El pedido del navegador y la respuesta del servidor. |
| **Entorno virtual** | Una carpeta con las dependencias del proyecto, aisladas del sistema. |
| **Dependencia** | Una librería que el proyecto necesita para funcionar. |
| **Seed** | Un archivo SQL que carga contenido en la base. |
| **Transacción** | Un grupo de cambios que se guardan todos o ninguno. |
| **CSRF** | Un token que evita envíos de formularios desde otro sitio. |

### 7.2 ¿Entendés el proyecto?

- [ ] Puedo explicar qué hay en `app/` sin mirar.
- [ ] Sé qué archivo atiende `/juego/estacion/1`.
- [ ] Sé de dónde salen las preguntas y dónde se guardan las respuestas.
- [ ] Sé por qué el navegador no recibe las respuestas correctas.
- [ ] Sé dónde se guardan los tiempos y cómo se arma el ranking.
- [ ] Puedo levantar la app siguiendo la sección 9.

## 8. Mapa completo de archivos `.md`

### 8.1 ¿Qué documento busco?

| Si querés... | Leé... |
| --- | --- |
| Entender las reglas del juego | [`escape-room.md`](escape-room.md), antes del anexo. |
| Estudiar los conceptos de tu nivel | [`contenido-para-responder-nivel-intermedio.md`](contenido-para-responder-nivel-intermedio.md) o [`contenido-para-responder-nivel-avanzado.md`](contenido-para-responder-nivel-avanzado.md). |
| Practicar con pistas | [`pistas-del-juego.md`](pistas-del-juego.md). |
| Ver cómo se ve la app | [`navegacion-capturas.md`](navegacion-capturas.md). |
| Entender la estructura del código | [`README.md`](../README.md) §4 y [`tecnologias.md`](tecnologias.md). |
| Instalar y levantar la app | Esta guía §9 y [`dejar-funcionando-proyecto-luego-clone.md`](dejar-funcionando-proyecto-luego-clone.md). |
| Administrar el juego | [`navegacion-por-app.md`](navegacion-por-app.md) §5 y [`README.md`](../README.md) §8. |
| Presentar el proyecto | [`proyectoEscapeRoom-7B.md`](proyectoEscapeRoom-7B.md). |
| Organizar el stand | [`ideas-escape-room.md`](ideas-escape-room.md). |
| Saber qué se hizo | [`MEMORY.md`](../MEMORY.md) y [`argumentos-pasos/README.md`](argumentos-pasos/README.md). |

### 8.2 Leyenda

- 🟢 **Sin respuestas:** se puede leer antes de jugar.
- 🟡 **Con pistas:** no tiene la respuesta marcada, pero ayuda demasiado. Usalo
  para practicar después de estudiar.
- 🔴 **Con respuestas:** material para docentes u organización. No lo leas si
  vas a participar.
- 🟠 **Uso mixto:** una parte se puede leer y otra contiene respuestas. Fijate
  en la advertencia de cada fila.
- ⚙️ **Técnico:** sirve para instalar, desarrollar o entender el proyecto; no es
  material de estudio del juego.

### 8.3 Contenido para estudiar

| Archivo | Qué contiene | Cómo usarlo |
| --- | --- | --- |
| [`docs/contenido-para-responder-nivel-intermedio.md`](contenido-para-responder-nivel-intermedio.md) | 🟢 Guía con los conceptos del nivel intermedio, ordenados por estación, más un glosario mínimo. | Es el material principal del nivel intermedio. Leelo completo y usá el glosario para repasar. |
| [`docs/contenido-para-responder-nivel-avanzado.md`](contenido-para-responder-nivel-avanzado.md) | 🟢 Guía con los conceptos del nivel avanzado, ordenados por estación, más un glosario mínimo. | Es el material principal del nivel avanzado. Prestá atención a las comparaciones entre conceptos. |
| [`docs/pistas-del-juego.md`](pistas-del-juego.md) | 🟡 Las 160 pistas de las 80 preguntas cargadas (40 del nivel inicial, 60 del intermedio y 60 del avanzado), más un anexo con preguntas en reserva. | Para el stand: se imprime y se lee en papel. Para estudiar: tapá las opciones, leé la pista y respondé de memoria. |
| [`docs/banco-preguntas-intermedio-avanzado.md`](banco-preguntas-intermedio-avanzado.md) | 🔴 Las 60 preguntas de intermedio y avanzado con sus tres opciones, la correcta marcada y dos pistas por pregunta. | Material de revisión docente. **No lo leas si vas a jugar**: contiene las respuestas. |

### 8.4 Reglas, recorrido y presentación

| Archivo | Qué contiene | Cómo usarlo |
| --- | --- | --- |
| [`docs/escape-room.md`](escape-room.md) | 🟠 Documento fuente del proyecto: reglas, puntaje, ranking, metodología de la feria y un anexo con las 20 preguntas del nivel inicial **y sus respuestas**. | Leé las secciones de reglas, puntaje y metodología; evitá el anexo si vas a jugar el nivel inicial. |
| [`docs/navegacion-por-app.md`](navegacion-por-app.md) | 🟢 Mapa de pantallas, rutas, elementos y objetivos: bienvenida, estaciones, transición, final, ranking, estadísticas y administración. | Para entender qué ve el equipo en cada momento y qué no se puede hacer (por ejemplo, saltar estaciones). |
| [`docs/navegacion-capturas.md`](navegacion-capturas.md) | 🟢 Recorrido visual con 41 capturas en tamaño móvil: tres intentos completos y los casos de incorrectas, abandono y tiempo agotado. | Para conocer el flujo sin abrir la app. Muestra el HUD, las transiciones y las pantallas de error. |
| [`docs/proyectoEscapeRoom-7B.md`](proyectoEscapeRoom-7B.md) | 🟢 Presentación breve del proyecto en cinco párrafos: qué es, cómo se juega, cómo está hecho y qué busca. | Guion para el stand. Leelo dos veces y contalo con tus palabras. |
| [`docs/tecnologias.md`](tecnologias.md) | 🟢 El stack explicado con ejemplos: frontend, backend, MySQL, servidor, pruebas y glosario. | Para quienes explican cómo está hecha la app. No hace falta leerlo entero: usá el índice y el glosario. |
| [`docs/ideas-escape-room.md`](ideas-escape-room.md) | 🟢 Ideas para el stand: redes sociales, banner y un juego de ping pong con preguntas generales. | No son requisitos de la aplicación. Sirven para organizar la feria. |

### 8.5 Organización, pruebas e instalación

| Archivo | Qué contiene | Cómo usarlo |
| --- | --- | --- |
| [`docs/ayuda-al-probar.md`](ayuda-al-probar.md) | ⚙️ Comandos rápidos para levantar la app, comprobar `/salud`, probar desde otra notebook y revisar la base. | Para quienes hacen pruebas manuales antes de la feria. |
| [`docs/instalacion-y-puesta-en-funcionamiento.md`](instalacion-y-puesta-en-funcionamiento.md) | ⚙️ Instalación completa en Ubuntu, MySQL, waitress, systemd, firewall y acceso desde las notebooks. | Para el equipo que deja funcionando el servidor. |
| [`docs/instalacion-servidor-escuela.md`](instalacion-servidor-escuela.md) | ⚙️ Puesta en marcha en el servidor Linux de la escuela y variante con la base remota. | Solo si se usa el servidor de la escuela. |
| [`docs/dejar-funcionando-proyecto-luego-clone.md`](dejar-funcionando-proyecto-luego-clone.md) | ⚙️ Guía desde un repositorio recién clonado hasta la app funcionando, con verificación de conteos y pruebas. | Para quien clona el proyecto por primera vez. |
| [`docs/primeros-pasos.md`](primeros-pasos.md) | ⚙️ Hoja de ruta y guion de pedidos del desarrollo, paso a paso. | Para entender cómo se construyó el proyecto. No es material de estudio del juego. |
| [`docs/chatdeopencode.md`](chatdeopencode.md) | ⚙️ Registro de decisiones y dudas resueltas durante el desarrollo. | Contexto histórico. No hace falta leerlo para jugar ni para el stand. |

### 8.6 Documentación técnica y de desarrollo

| Archivo | Qué contiene | Cómo usarlo |
| --- | --- | --- |
| [`sql/descripcion-de-la-base-de-datos.md`](../sql/descripcion-de-la-base-de-datos.md) | ⚙️ Modelo de datos: tablas, relaciones y consultas de ejemplo. | Para entender cómo se guardan equipos, intentos, respuestas y ranking. |
| [`README.md`](../README.md) | ⚙️ Presentación general del repositorio: qué es, cómo se juega, stack, estructura, rutas, instalación y documentación. | Primera lectura para quien llega al proyecto. |
| [`AGENTS.md`](../AGENTS.md) | ⚙️ Reglas del proyecto, modelo de datos, decisiones registradas y convenciones para quienes desarrollan. | Referencia de desarrollo. No es material de estudio del juego. |
| [`MEMORY.md`](../MEMORY.md) | ⚙️ Estado actual del proyecto y verificaciones realizadas. | Para saber qué está hecho y qué falta. |
| [`docs/argumentos-pasos/README.md`](argumentos-pasos/README.md) | ⚙️ Índice de los pasos de desarrollo, con tipo, estado y commit de cada uno. | Para ubicar un paso puntual. |
| `.pytest_cache/README.md` | ⚙️ Archivo generado automáticamente por pytest. No se versiona. | Ignoralo: no es documentación del proyecto. |

### 8.7 Pasos de desarrollo (`docs/argumentos-pasos/`)

Son planes técnicos. No contienen las respuestas del juego, pero tampoco son
material de estudio: sirven para entender o repetir el desarrollo.

| Archivo | Tema |
| --- | --- |
| [`paso00-verificar-base-y-contenido.md`](argumentos-pasos/paso00-verificar-base-y-contenido.md) | Verificar la base y el contenido inicial. |
| [`paso01-esqueleto-flask.md`](argumentos-pasos/paso01-esqueleto-flask.md) | Esqueleto de la aplicación Flask. |
| [`paso02-bienvenida-e-identidad.md`](argumentos-pasos/paso02-bienvenida-e-identidad.md) | Bienvenida e identidad del equipo. |
| [`paso03-seleccion-de-preguntas.md`](argumentos-pasos/paso03-seleccion-de-preguntas.md) | Selección y congelamiento de preguntas. |
| [`paso04-envio-y-reglas-de-estacion.md`](argumentos-pasos/paso04-envio-y-reglas-de-estacion.md) | Envíos, ayudas y reglas de la estación. |
| [`paso05-temporizadores-y-reanudacion.md`](argumentos-pasos/paso05-temporizadores-y-reanudacion.md) | Temporizadores y reanudación. |
| [`paso06-recorrido-completo-y-finales.md`](argumentos-pasos/paso06-recorrido-completo-y-finales.md) | Recorrido completo y pantallas finales. |
| [`paso07-prueba-manual-del-mvp.md`](argumentos-pasos/paso07-prueba-manual-del-mvp.md) | Prueba manual del MVP con personas. |
| [`paso08-ranking-publico-y-estadisticas.md`](argumentos-pasos/paso08-ranking-publico-y-estadisticas.md) | Ranking público y estadísticas. |
| [`paso09-admin-login-y-crud.md`](argumentos-pasos/paso09-admin-login-y-crud.md) | Login y CRUD del panel de administración. |
| [`paso10-cobertura-y-dificultades.md`](argumentos-pasos/paso10-cobertura-y-dificultades.md) | Cobertura de niveles y toggles de dificultad. |
| [`paso11-pruebas-y-endurecimiento.md`](argumentos-pasos/paso11-pruebas-y-endurecimiento.md) | Suite de pruebas y endurecimiento. |
| [`paso11b-ranking-por-nivel.md`](argumentos-pasos/paso11b-ranking-por-nivel.md) | Ranking por nivel. |
| [`paso11c-contenido-intermedio.md`](argumentos-pasos/paso11c-contenido-intermedio.md) | Contenido de los niveles intermedio y avanzado. |
| [`paso11-d-agregando-descripcion.md`](argumentos-pasos/paso11-d-agregando-descripcion.md) | Descripciones breves en las preguntas. |
| [`paso11e-agregarimagenes.md`](argumentos-pasos/paso11e-agregarimagenes.md) | Imágenes institucionales en la interfaz. |
| [`paso11f-capturas-navegacion.md`](argumentos-pasos/paso11f-capturas-navegacion.md) | Capturas de navegación en tamaño móvil. |
| [`paso12-congelar-y-puesta-en-marcha.md`](argumentos-pasos/paso12-congelar-y-puesta-en-marcha.md) | Congelar el proyecto y dejarlo en marcha. |
| [`paso13-docker-taller-post-feria.md`](argumentos-pasos/paso13-docker-taller-post-feria.md) | Taller opcional de Docker después de la feria. |

## 9. Instalación básica en tu computadora

Esta sección es para **probar la app** o mostrarla en tu casa. En la feria el
servidor ya está armado: las notebooks y el televisor solo se conectan a la red
del aula. Si te toca dejar el servidor funcionando, después de esta sección
seguí con las guías completas.

> Los comandos de Linux son para **Ubuntu 22.04 o 24.04** (o Debian reciente).
> En Windows podés usar **WSL2** (recomendado) o instalar todo de forma nativa.

### 9.1 Lo básico en 6 pasos

| Paso | Qué hacés | Comando principal |
| --- | --- | --- |
| 1 | Descargar el proyecto | `git clone https://github.com/jcondeipeayt186/escaperoom7B26.git` |
| 2 | Instalar Python 3.10+, MySQL 8 y git | `sudo apt install -y python3 python3-venv python3-pip mysql-server git` (Linux; en Windows ver §9.3) |
| 3 | Crear el entorno virtual e instalar dependencias | `python3 -m venv .venv` y `pip install -r requirements.txt` |
| 4 | Configurar `.env` | `cp .env.example .env` y editar las claves |
| 5 | Crear la base y cargar el contenido | `sudo mysql < bd/schema.sql` y los tres seeds |
| 6 | Ejecutar Flask | `flask --app app run --debug` |

Abrí <http://127.0.0.1:5000> y comprobá <http://127.0.0.1:5000/salud>. Tiene que
responder `200` con `{"estado": "ok", "base": "ok"}`.

### 9.2 Ubuntu/Debian

#### Paso 1: descargar el proyecto

```bash
git clone https://github.com/jcondeipeayt186/escaperoom7B26.git
cd escaperoom7B26
```

Si el repositorio es privado, GitHub pide usuario y token, o el docente te pasa
el acceso. También podés recibir el proyecto como ZIP: se descomprime y se entra
a la carpeta.

#### Paso 2: instalar Python, MySQL y git

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip mysql-server git
sudo systemctl enable --now mysql
```

Verificá las versiones:

```bash
python3 --version   # 3.10 o superior
mysql --version     # 8.0 o superior
git --version
```

#### Paso 3: crear el entorno virtual

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

El prompt muestra `(.venv)` adelante. Cada vez que abras una terminal nueva,
volvé a activarlo con `source .venv/bin/activate`. Para salir: `deactivate`.

#### Paso 4: configurar `.env`

```bash
cp .env.example .env
chmod 600 .env

python -c "import secrets; print(secrets.token_hex(32))"
python -c "from werkzeug.security import generate_password_hash; print(generate_password_hash('CAMBIA-ESTA-CLAVE'))"

nano .env
```

Completá:

```dotenv
FLASK_SECRET_KEY=la-clave-generada
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_USER=escaperoom
MYSQL_PASSWORD=una-clave-larga-y-propia
MYSQL_DB=escape_room_7b2026
ADMIN_USER=admin
ADMIN_PASSWORD_HASH=el-hash-generado
```

- No dejes `FLASK_SECRET_KEY` con el valor de ejemplo: la app no arranca.
- `.env` no se versiona y no se comparte.

#### Paso 5: crear la base y cargar el contenido

```bash
sudo mysql < bd/schema.sql
sudo mysql < bd/seeds/001_contenido_inicial.sql
sudo mysql < bd/seeds/002_contenido_intermedio.sql
sudo mysql < bd/seeds/003_contenido_avanzado.sql
```

El esquema crea la base `escape_room_7b2026` y las 12 tablas; los seeds cargan
las 80 preguntas. Los seeds son idempotentes: se pueden volver a ejecutar sin
duplicar filas.

Después creá el usuario con el que se conecta la app (la misma clave que pusiste
en `MYSQL_PASSWORD`). Entrá a MySQL con `sudo mysql` y pegá:

```sql
CREATE USER 'escaperoom'@'localhost' IDENTIFIED BY 'una-clave-larga-y-propia';
CREATE USER 'escaperoom'@'127.0.0.1' IDENTIFIED BY 'una-clave-larga-y-propia';
GRANT ALL PRIVILEGES ON escape_room_7b2026.* TO 'escaperoom'@'localhost';
GRANT ALL PRIVILEGES ON escape_room_7b2026.* TO 'escaperoom'@'127.0.0.1';
FLUSH PRIVILEGES;
EXIT;
```

> Los permisos sobre `escape_room_7b2026_test` solo hacen falta para correr
> `pytest`. Están detallados en [`README.md`](../README.md) §7.2.

#### Paso 6: ejecutar Flask

```bash
source .venv/bin/activate
flask --app app run --debug
```

- App: <http://127.0.0.1:5000>
- Salud: <http://127.0.0.1:5000/salud>
- Panel: <http://127.0.0.1:5000/admin>

`flask run --debug` es solo para desarrollo. Para la feria se usa waitress
(ver §9.5).

### 9.3 Windows

#### Opción A: WSL2 (recomendado)

WSL2 instala un Ubuntu dentro de Windows y permite usar los mismos comandos que
en 9.2.

1. Abrí PowerShell como administrador y ejecutá:

   ```powershell
   wsl --install -d Ubuntu
   ```

2. Reiniciá si lo pide, abrí Ubuntu y creá tu usuario.
3. Cloná el proyecto **dentro del home de Linux** (no en `/mnt/c`, que es más
   lento y trae problemas de permisos):

   ```bash
   cd ~
   git clone https://github.com/jcondeipeayt186/escaperoom7B26.git
   cd escaperoom7B26
   ```

4. Seguí los pasos 2 a 6 de la sección 9.2 tal cual.

#### Opción B: Windows nativo

Instalá:

- **Python 3.10 o superior** desde <https://www.python.org/downloads/>. Marcá
  **"Add python.exe to PATH"** durante la instalación.
- **MySQL 8** desde <https://dev.mysql.com/downloads/installer/>. Anotá la clave
  de `root`.
- **Git for Windows** desde <https://git-scm.com/download/win>.

Abrí **PowerShell** en la carpeta donde querés el proyecto:

```powershell
git clone https://github.com/jcondeipeayt186/escaperoom7B26.git
cd escaperoom7B26

python -m venv .venv
.\.venv\Scripts\Activate.ps1
# Si PowerShell bloquea el script:
# Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

pip install --upgrade pip
pip install -r requirements.txt

Copy-Item .env.example .env
python -c "import secrets; print(secrets.token_hex(32))"
python -c "from werkzeug.security import generate_password_hash; print(generate_password_hash('CAMBIA-ESTA-CLAVE'))"
notepad .env
```

Completá `.env` igual que en 9.2. En Windows no existe `chmod`; el archivo
`.env` igual queda fuera de Git por el `.gitignore`.

Para la base, usá el cliente de MySQL. Si `mysql` no está en el PATH, abrí
**MySQL 8.0 Command Line Client** desde el menú Inicio y ejecutá `source`:

```sql
source bd/schema.sql;
source bd/seeds/001_contenido_inicial.sql;
source bd/seeds/002_contenido_intermedio.sql;
source bd/seeds/003_contenido_avanzado.sql;
```

O desde PowerShell, con `cmd` para que la redirección no rompa los acentos:

```powershell
cmd /c "mysql -u root -p < bd\schema.sql"
cmd /c "mysql -u root -p < bd\seeds\001_contenido_inicial.sql"
cmd /c "mysql -u root -p < bd\seeds\002_contenido_intermedio.sql"
cmd /c "mysql -u root -p < bd\seeds\003_contenido_avanzado.sql"
```

Después creá el usuario `escaperoom` con el mismo bloque SQL de 9.2, ejecutado
en el cliente de MySQL. Finalmente:

```powershell
flask --app app run --debug
```

### 9.4 Errores frecuentes

| Error | Causa probable | Solución |
| --- | --- | --- |
| `No module named flask` | El entorno virtual no está activado. | `source .venv/bin/activate` (Linux) o `.\.venv\Scripts\Activate.ps1` (Windows). |
| `Can't connect to MySQL server` | MySQL no está corriendo o el `.env` tiene otro host/puerto. | `sudo systemctl start mysql` y revisá `MYSQL_HOST` y `MYSQL_PORT`. |
| `Access denied for user 'escaperoom'` | El usuario no existe o la clave no coincide. | Repetí el bloque SQL de 9.2 con la misma clave de `.env`. |
| La app no arranca y habla de `FLASK_SECRET_KEY` | Quedó el valor de ejemplo. | Generá una clave real y pegala en `.env`. |
| `Address already in use` | El puerto 5000 está ocupado. | `flask --app app run --debug --port 5001`. |
| `mysql: command not found` (Windows) | El cliente no está en el PATH. | Usá **MySQL 8.0 Command Line Client** o agregá la carpeta `bin` al PATH. |

### 9.5 Para la feria

En la feria la app no se levanta con `flask run --debug`: se usa **waitress**
detrás de **systemd**, para que quede funcionando aunque se cierre la terminal.
El detalle está en:

- [`dejar-funcionando-proyecto-luego-clone.md`](dejar-funcionando-proyecto-luego-clone.md) — de clonar a navegar.
- [`instalacion-y-puesta-en-funcionamiento.md`](instalacion-y-puesta-en-funcionamiento.md) — servidor Ubuntu, waitress, systemd y firewall.
- [`instalacion-servidor-escuela.md`](instalacion-servidor-escuela.md) — servidor Linux de la escuela y base remota.
- [`ayuda-al-probar.md`](ayuda-al-probar.md) — comandos rápidos para probar.

## 10. Cómo estudiar mejor

- **Explicá en voz alta.** Si podés contarle el tema a alguien que no sabe,
  ya lo entendiste. Si te trabás, volvé a esa sección.
- **Usá ejemplos propios.** Un ejemplo de la escuela, de tu casa o de tu celular
  se recuerda mejor que una definición.
- **Compará conceptos parecidos.** Armá pares: hub y switch, TCP y UDP, RAM y
  disco, proceso e hilo, HTTP y HTTPS. Poder decir en qué se diferencian vale
  más que repetir la definición.
- **Practicá con las pistas, no con las respuestas.** Leé la pista fácil, pensá
  la respuesta y recién después mirá las opciones.
- **Simulá una estación.** Cuatro preguntas, cuatro minutos, sin material. Si no
  llegás, no es un problema: sirve para saber qué repasar.
- **Repasá el glosario.** Las dos guías terminan con un glosario mínimo: es el
  mejor resumen para el día anterior.
- **No memorices opciones.** Las preguntas se sortean y cambian entre intentos.
  Memorizar una opción no te prepara para otra pregunta del mismo tema.

## 11. Antes de la feria: checklist

Para quienes van a jugar:

- [ ] Sé explicar las reglas: cinco estaciones, cuatro preguntas, cuatro minutos.
- [ ] Sé qué pasa con dos respuestas incorrectas, con el tiempo agotado y si el
      equipo abandona.
- [ ] Sé cuántas ayudas hay por estación y que la app no muestra la pista.
- [ ] Puedo explicar los conceptos principales de las cinco estaciones.
- [ ] Practiqué al menos una estación con tiempo.

Para 7.º B, además:

- [ ] Puedo contar el proyecto en un minuto con el texto de presentación.
- [ ] Conozco el recorrido de la app y qué muestra el HUD.
- [ ] Tengo impresas las pistas y sé leerlas sin revelar la respuesta.
- [ ] Sé qué hacer si un equipo recarga la página, vuelve a entrar o pide el ID.
- [ ] Sé a quién avisar si aparece la pantalla de estación no disponible o un
      error.
- [ ] Puedo explicar qué hay en `app/` y cómo se recorre una petición.

## 12. Material que no es `.md`

- `docs/ESCAPE ROOM.pdf`: preguntas y pistas originales. Es la fuente del
  contenido; su transcripción está en los archivos `.md`.
- `docs/contenido-para-responder-nivel-intermedio.pdf` y
  `docs/contenido-para-responder-nivel-avanzado.pdf`: versiones imprimibles de
  las dos guías de estudio.
- `docs/banco-preguntas-intermedio-avanzado.pdf`, `docs/escape-room.pdf`,
  `docs/navegacion-por-app.pdf` y `docs/proyectoEscapeRoom-7B.pdf`: versiones
  PDF de esos documentos.
- `docs/src/`: prototipos visuales del juego y del ranking. **No son la
  aplicación final** y no se usan para estudiar las reglas.
- `docs/img/`: imágenes originales de la escuela. No se editan ni se usan
  directamente en la app.
- `bd/seeds/`: contenido cargado en MySQL. Ahí viven las preguntas y respuestas
  reales; no es un archivo pensado para leer y estudiar.

---

Si tenés que elegir un solo archivo para empezar, elegí la guía de tu nivel:
[intermedio](contenido-para-responder-nivel-intermedio.md) o
[avanzado](contenido-para-responder-nivel-avanzado.md). Si vas a jugar el nivel
inicial, empezá por las reglas de [`escape-room.md`](escape-room.md) y seguí con
las pistas del nivel inicial.
