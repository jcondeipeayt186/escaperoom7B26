# Paso 11g — Explicaciones e introducciones en la transición

> **Origen:** pedido posterior al `paso11f`, antes del `paso12`.
> **Tipo:** feat (contenido y pantalla).
> **Requiere:** `paso11f` aprobado.
> **Commit:** `feat: explicaciones e introducciones en la transición`.
>
> **Antes de empezar:** leé `AGENTS.md` (decisiones 15 y 61), `bd/schema.sql`,
> `bd/seeds/001_contenido_inicial.sql`, `app/servicios/estaciones.py`,
> `app/routes/juego.py` y `app/templates/transicion.html`.

## Estado

Pendiente. El contenido de este archivo (14 introducciones y 80 explicaciones)
se propone para revisión antes de implementar. No ejecutar el paso hasta que el
docente lo apruebe.

## Contexto

Hoy la pantalla intermedia entre estaciones solo confirma que la estación está
superada y muestra tiempos, ayudas, incorrectas y envíos. El equipo avanza sin
enterarse de **por qué** las respuestas eran correctas. En una feria escolar ese
es justamente el momento de aprendizaje: acaban de responder, tienen el tema
fresco y todavía no arrancó el cronómetro de la estación siguiente.

Este paso agrega dos campos de contenido y los muestra en la transición:

- `tema.introduccion`: un párrafo corto que presenta el tema.
- `pregunta.explicacion`: una explicación breve de por qué la respuesta correcta
  lo es.

La transición muestra, para cada una de las 4 preguntas de la estación, el
enunciado, la respuesta que eligió el equipo (que en una estación superada es
la correcta) y la explicación. Las introducciones aparecen antes, agrupadas por
tema.

Esto **no es una pista**: las pistas de papel siguen viviendo en
`docs/pistas-del-juego.md` y la app no muestra su texto (decisión 15). La
explicación se ve recién cuando la estación ya está completada, así que no
ayuda a resolver nada.

## Objetivo

Que cada equipo termine la feria habiendo leído una explicación breve de las 20
preguntas que respondió, sin cambiar las reglas del juego, los tiempos ni el
ranking.

## Modelo de datos

Dos columnas nuevas, ambas `TEXT NULL`:

| Tabla | Columna | Tipo | Null | Ubicación |
| --- | --- | --- | --- | --- |
| `tema` | `introduccion` | `TEXT` | Sí | después de `nombre` |
| `pregunta` | `explicacion` | `TEXT` | Sí | después de `descripcion` |

Detalles:

- Se agregan en `bd/schema.sql` para instalaciones nuevas.
- Se agrega una migración para bases existentes:
  `bd/migraciones/20261113_explicaciones-e-introducciones.sql`. Es la primera
  migración del proyecto, por eso se crea la carpeta `bd/migraciones/`.
- La migración es idempotente: usa `ADD COLUMN IF NOT EXISTS` (MySQL 8.0.29+) o
  consulta `information_schema.COLUMNS` antes de agregar, para que se pueda
  correr dos veces sin error.
- No se toca ninguna otra tabla ni ninguna clave.
- Los conteos de contenido **no cambian**: siguen siendo `5` estaciones, `14`
  temas, `80` preguntas, `240` respuestas y `9` filas de `configuracion`.
- `bd/escape_room_7b2026_completa.sql` se regenera para incluir las columnas y
  el contenido nuevo.
- Las columnas quedan editables desde `/admin`, como `pregunta.descripcion`.
  No se agregan validaciones nuevas de cobertura ni de dificultad.

## Reglas de redacción

Para las 14 introducciones y las 80 explicaciones:

- Texto plano, español rioplatense, sin HTML, sin Markdown, sin listas, sin
  negritas y sin comillas tipográficas.
- Sin punto y coma: el cargador de seeds de las pruebas separa las sentencias
  con `;`.
- Sin comillas simples: se cargan dentro de literales SQL.
- Una introducción: entre 2 y 4 oraciones, hasta 400 caracteres.
- Una explicación: uno o dos párrafos, hasta 600 caracteres. Si son dos
  párrafos, se separan con una línea en blanco (`\n\n` en el seed) y la
  plantilla los renderiza como párrafos distintos.
- La explicación dice **por qué** la respuesta correcta es correcta y por qué
  las otras no lo son, sin repetir textualmente las opciones incorrectas.
- La explicación no nombra la opción correcta entre comillas ni la parafrasea
  letra por letra: la app ya muestra la respuesta elegida arriba.
- No se escribe la respuesta correcta en la plantilla ni en el JavaScript: sale
  de la base, de la respuesta que el equipo eligió en el envío que completó la
  estación.
- Tono de explicación para estudiantes de 7.º, sin tecnicismos innecesarios.
- Nada de pistas: no se adelanta el contenido de `docs/pistas-del-juego.md`.

## Contenido propuesto

### Introducciones de temas — 14

| ID | Estación | Tema | Introducción |
| --- | --- | --- | --- |
| 1 | Redes | IP | Una dirección IP identifica a cada dispositivo dentro de una red y permite que los datos lleguen a destino. Puede ser privada, pública o especial, como la de loopback. Conocerla ayuda a entender cómo se comunican los equipos. |
| 2 | Redes | Router | El router es el equipo que conecta redes distintas y decide por dónde sale cada paquete. En una casa suele unir la red interna con Internet. Su trabajo es distinto del de un switch o un punto de acceso. |
| 3 | Redes | Redes de computadoras | Una red de computadoras es un conjunto de dispositivos conectados para compartir datos y recursos. Puede ser cableada o inalámbrica y su tamaño va desde una casa hasta una empresa. Los protocolos son las reglas que ordenan esa comunicación. |
| 4 | Redes | WiFi | El WiFi permite conectar dispositivos sin cables mediante ondas de radio. Un punto de acceso recibe la señal y la integra a la red. La seguridad de esa conexión depende del cifrado y de la clave que se use. |
| 5 | Hardware | Procesador | El procesador ejecuta las instrucciones y coordina el trabajo del equipo. Dentro tiene memorias muy rápidas y se comunica con el resto de los componentes. Su rendimiento depende de varios factores, no solo de la velocidad que muestra la caja. |
| 6 | Hardware | Dispositivos de entrada/salida | Los dispositivos de entrada permiten ingresar datos y los de salida muestran el resultado. Algunos cumplen las dos funciones, como una pantalla táctil. El almacenamiento también forma parte del hardware y guarda la información. |
| 7 | Hardware | Memoria RAM | La memoria RAM es el espacio de trabajo del equipo: guarda lo que se está usando en ese momento. Es rápida y volátil, por eso los datos se pierden al apagar. Cuando falta, el sistema puede apoyarse en el disco con la memoria virtual. |
| 8 | Internet | Navegadores Web | El navegador es el programa que pide las páginas y las muestra en pantalla. Guarda cookies, caché e historial para que la navegación sea más rápida y cómoda. También ofrece modos y opciones de privacidad que conviene conocer. |
| 9 | Internet | URL | Una URL es la dirección de un recurso en Internet y tiene varias partes. El protocolo indica cómo se pide, el dominio identifica al servidor y la ruta señala el recurso. Los parámetros agregan datos a la consulta. |
| 10 | Internet | Conectividad | La conectividad depende de varios factores: la velocidad, la latencia y la calidad de la red. El ancho de banda mide cuánto puede pasar y la latencia cuánto tarda. Los códigos HTTP, por su parte, informan cómo respondió el servidor. |
| 11 | Ciberseguridad | Contraseña | Las contraseñas protegen las cuentas y deben ser largas, únicas y difíciles de adivinar. Un gestor y la autenticación de dos factores ayudan a cuidarlas. Compartirlas o repetirlas aumenta el riesgo. |
| 12 | Ciberseguridad | Phishing | El phishing reúne engaños que buscan robar información haciéndose pasar por alguien confiable. Llega por correo, mensajes o llamadas y suele usar la urgencia. La ingeniería social ataca la confianza de las personas. |
| 13 | Sistemas Operativos | Sistema Operativo | El sistema operativo administra el hardware y permite ejecutar los programas. Su núcleo, el kernel, coordina la memoria, el procesador y los dispositivos. Los procesos y los hilos son parte de esa administración. |
| 14 | Sistemas Operativos | Dispositivos Móviles | Los teléfonos y las tabletas usan sistemas operativos móviles como Android e iOS. Cada aplicación pide permisos para acceder a funciones y datos. Instalar solo desde la tienda oficial reduce riesgos. |

### Explicaciones de `inicial` — 20

| ID | Estación | Pregunta | Explicación |
| --- | --- | --- | --- |
| 1 | Redes | ¿Qué significa IP? | IP son las siglas de Internet Protocol, el protocolo que identifica cada dispositivo dentro de una red y permite que los datos sepan hacia dónde viajar. Cada equipo conectado recibe una dirección IP, como si fuera su número de casa. |
| 2 | Redes | ¿Qué dispositivo conecta diferentes redes? | El router une redes distintas y decide por dónde enviar cada paquete de datos. En una casa, es el equipo que conecta la red interna con Internet. Un teclado o un monitor no cumplen esa función. |
| 3 | Redes | ¿Qué es una red informática? | Una red informática es un conjunto de dispositivos conectados entre sí para compartir información y recursos. Pueden estar unidos por cables o por WiFi y sirven para intercambiar archivos, usar una impresora o navegar. |
| 4 | Redes | ¿Qué se necesita para conectarse a una red WiFi? | Para entrar a una red WiFi protegida hay que conocer su contraseña o clave de seguridad. Esa clave evita que cualquier persona se conecte sin permiso. Los cables HDMI o las impresoras no tienen relación con esa conexión. |
| 5 | Hardware | ¿Qué componente es considerado el cerebro de la computadora? | El procesador, también llamado CPU, ejecuta las instrucciones y coordina las tareas del equipo. Por eso se lo compara con el cerebro de la computadora: sin él, el resto de los componentes no puede trabajar. El teclado y el monitor solo permiten entrar o ver información. |
| 6 | Hardware | ¿Cuál es un dispositivo de entrada? | Un dispositivo de entrada permite ingresar datos al equipo. El teclado lo hace cuando escribís y el ratón cuando movés el puntero. El monitor y el parlante son de salida, porque muestran o emiten el resultado. |
| 7 | Hardware | ¿Para qué sirve la memoria RAM? | La memoria RAM guarda los datos y los programas que se están usando en ese momento. Es muy rápida, pero al apagar el equipo su contenido se pierde. No sirve para imprimir ni para proteger la pantalla. |
| 8 | Hardware | ¿Cuál es un dispositivo de salida? | Un dispositivo de salida presenta al usuario el resultado del trabajo del equipo. El monitor muestra texto e imágenes y el parlante emite sonido. El ratón y el micrófono son de entrada. |
| 9 | Internet | ¿Qué es un navegador web? | Un navegador web es el programa que pide las páginas a los servidores y las muestra en pantalla. Chrome, Firefox y Edge son ejemplos. No es una parte del procesador ni un cable de red. |
| 10 | Internet | ¿Cuál de estos es un navegador web? | Google Chrome es un navegador web: sirve para abrir sitios y navegar por Internet. Windows es un sistema operativo y la calculadora es una aplicación de cálculo. Cada programa cumple una función distinta. |
| 11 | Internet | ¿Qué significa URL? | URL son las siglas de Uniform Resource Locator y funcionan como la dirección de una página, una imagen o un archivo en Internet. Al escribirla en el navegador, el equipo sabe qué servidor buscar y qué recurso pedir. |
| 12 | Internet | ¿Qué se necesita para acceder a un sitio web público en internet? | Para ver un sitio público hace falta una conexión que llegue hasta el servidor donde está alojado. Sin conexión a Internet, el navegador no puede pedir esa página. Un escáner o un pendrive no reemplazan esa conexión. |
| 13 | Ciberseguridad | ¿Cómo debe ser una contraseña segura? | Una contraseña segura combina mayúsculas, minúsculas, números y símbolos, y tiene suficiente longitud para que no se adivine fácilmente. Evitá datos obvios como 123456 o tu nombre. Cuanto más difícil de adivinar, mejor protege la cuenta. |
| 14 | Ciberseguridad | ¿Qué deberías hacer con un enlace sospechoso? | Antes de abrir un enlace dudoso conviene comprobar quién lo envió y por qué. Se puede consultar por otro canal, como una llamada o el sitio oficial. Abrirlo o compartirlo solo aumenta el riesgo. |
| 15 | Ciberseguridad | ¿Qué es el phishing? | El phishing es un engaño que imita a una empresa o a una persona conocida para que entregues contraseñas o datos. Suele llegar por correo, mensaje o llamada. No es un programa de fotos ni una clase de monitor. |
| 16 | Ciberseguridad | ¿Qué conviene hacer con tus contraseñas? | Las contraseñas son personales y no se comparten con nadie, ni con amigos ni con desconocidos. Usar la misma en todos lados multiplica el daño si una se filtra. Guardarlas de forma segura ayuda a no tener que recordarlas de memoria. |
| 17 | Sistemas Operativos | ¿Qué es un sistema operativo? | Un sistema operativo es el software principal que administra el hardware y permite ejecutar los programas. Windows, Linux y Android son ejemplos. Sin él, el equipo no sabría cómo usar sus componentes. |
| 18 | Sistemas Operativos | ¿Cuál de estos es un sistema operativo? | Windows es un sistema operativo: administra el equipo y sirve de base para los demás programas. Microsoft Word es un procesador de textos y Google Chrome es un navegador. Cada uno se apoya en el sistema operativo. |
| 19 | Sistemas Operativos | ¿Para qué sirve un sistema operativo? | El sistema operativo reparte el procesador, la memoria y el almacenamiento entre los programas. También controla los permisos y la comunicación con los dispositivos. No se limita al color del monitor ni a escribir documentos. |
| 20 | Sistemas Operativos | ¿Cuál de estos es un sistema operativo para celulares? | Android es un sistema operativo móvil, pensado para teléfonos y tabletas. PowerPoint y Excel son aplicaciones de oficina que funcionan sobre un sistema operativo. iOS es otro sistema móvil, de otra empresa. |

### Explicaciones de `intermedio` — 30

| ID | Estación | Pregunta | Explicación |
| --- | --- | --- | --- |
| 1001 | Redes | ¿Qué dirección IPv4 es una dirección de loopback? | La dirección 127.0.0.1 se conoce como loopback y siempre apunta al propio equipo. Sirve para probar si la configuración de red funciona sin salir a la LAN. Las direcciones 192.168 y 169.254 pertenecen a otros rangos. |
| 1002 | Redes | ¿Cuál es la función principal de una máscara de subred? | La máscara de subred indica cuántos bits de la dirección IP identifican la red y cuántos identifican al equipo. Con esa información, el equipo sabe si el destino está dentro de su red o fuera. No identifica al fabricante ni cambia la velocidad. |
| 1003 | Redes | ¿Qué protocolo asigna direcciones IP automáticamente a los dispositivos de una red? | DHCP es el protocolo que entrega automáticamente dirección IP, máscara y puerta de enlace a los dispositivos. Así no hay que configurar cada equipo a mano. DNS traduce nombres y FTP transfiere archivos. |
| 1004 | Redes | ¿Cuál es la función principal de un switch en una red LAN? | Un switch conecta varios equipos de una red local y envía cada trama al puerto del dispositivo correcto. Trabaja dentro de la LAN y no se ocupa de sacar el tráfico a Internet, tarea del router. Tampoco almacena los archivos de los usuarios. |
| 1005 | Redes | ¿Qué función cumple un punto de acceso inalámbrico (Access Point)? | Un punto de acceso recibe la señal de los dispositivos inalámbricos y los integra a la red cableada. Es habitual en escuelas y oficinas para ampliar la cobertura WiFi. No reemplaza la RAM ni guarda archivos. |
| 1006 | Redes | ¿Qué protocolo traduce nombres de dominio como ejemplo.com a direcciones IP? | DNS es el servicio que traduce nombres como ejemplo.com a direcciones IP. Gracias a él no hace falta recordar números para entrar a un sitio. DHCP asigna direcciones y ARP las vincula con direcciones MAC. |
| 1007 | Hardware | ¿Qué función cumple la tecnología SMART en las unidades de almacenamiento? | SMART es un sistema de autodiagnóstico que registra datos internos del disco, como errores o temperatura. Con esa información se pueden detectar señales de falla antes de que el disco deje de funcionar. No controla el WiFi ni cifra archivos. |
| 1008 | Hardware | ¿Qué puede indicar una pantalla azul recurrente en Windows? | La pantalla azul de Windows aparece cuando el sistema encuentra un error grave y no puede seguir funcionando. Suele estar relacionada con controladores, memoria o fallas de hardware. No indica que el monitor esté conectado ni que el router esté apagado. |
| 1009 | Hardware | ¿Cuál es la finalidad de realizar una copia de seguridad? | Una copia de seguridad guarda una versión adicional de los datos para poder recuperarlos si algo falla. Sirve ante borrados accidentales, fallas del disco o robos. No reemplaza al antivirus ni acelera Internet. |
| 1010 | Hardware | ¿Qué es la pasta térmica? | La pasta térmica se coloca entre el procesador y el disipador para llenar las imperfecciones y mejorar el paso del calor. Sin ella quedarían bolsas de aire que calentarían de más. No es un aislante ni un adhesivo para la RAM. |
| 1011 | Hardware | ¿Qué tipo de mantenimiento busca evitar fallas futuras? | El mantenimiento preventivo se hace antes de que aparezca la falla, con limpieza, revisiones y actualizaciones. El correctivo se aplica cuando el problema ya ocurrió. Prevenir suele ser más barato y evita cortes. |
| 1012 | Hardware | ¿Qué significa que la memoria RAM sea volátil? | Decir que la RAM es volátil significa que necesita energía para conservar los datos. Al apagar o reiniciar el equipo, su contenido se borra. Por eso los archivos se guardan en el disco y no en la RAM. |
| 1013 | Internet | ¿Para qué sirven las cookies de un navegador? | Las cookies son pequeños archivos que el sitio guarda en el navegador para recordar la sesión, el idioma o las preferencias. Sin ellas habría que iniciar sesión en cada página. No aceleran el procesador ni impiden el uso de HTTPS. |
| 1014 | Internet | ¿Qué hace el modo incógnito de un navegador? | El modo incógnito evita que el navegador guarde el historial y las cookies de esa sesión en el equipo. No oculta la navegación al proveedor de Internet ni a la red WiFi, y tampoco cifra archivos. Sirve para no dejar rastro local, no para ser invisible. |
| 1015 | Internet | En la dirección https://www.escuela.edu.ar/aula/notas, ¿qué parte indica el protocolo? | En una URL, el protocolo aparece antes de los dos puntos y las barras e indica cómo se pide el recurso. En https://www.escuela.edu.ar/aula/notas, el protocolo es https. El dominio es www.escuela.edu.ar y la ruta es /aula/notas. |
| 1016 | Internet | ¿Qué indica el dominio en una dirección web? | El dominio es la parte de la URL que se registra y se escribe para llegar a un sitio, como escuela.edu.ar. El sistema DNS lo traduce a una dirección IP. No es una contraseña ni el tipo de procesador del servidor. |
| 1017 | Internet | ¿Qué es el ancho de banda? | El ancho de banda mide cuántos datos pueden pasar por segundo por una conexión. Una conexión con más ancho de banda puede mover más información a la vez. No mide la demora de cada dato ni la cantidad de dispositivos. |
| 1018 | Internet | ¿Qué significa tener una latencia alta? | La latencia es el tiempo que tarda un dato en ir y volver. Cuando es alta, las videollamadas se cortan y los juegos en línea se sienten lentos aunque el ancho de banda sea bueno. No reduce el tamaño de los archivos. |
| 1019 | Ciberseguridad | ¿Qué es la autenticación de dos factores (2FA)? | La autenticación de dos factores agrega una segunda prueba además de la contraseña, como un código en el celular. Así, aunque alguien conozca la clave, no puede entrar sin ese segundo dato. No consiste en usar dos claves iguales. |
| 1020 | Ciberseguridad | ¿Para qué sirve un gestor de contraseñas? | Un gestor de contraseñas guarda las claves cifradas y puede generar nuevas y difíciles de adivinar. Así se usa una clave distinta en cada sitio sin tener que memorizarlas. No elimina la necesidad de contraseñas ni sirve para compartirlas. |
| 1021 | Ciberseguridad | ¿Por qué no conviene usar la misma contraseña en varios sitios? | Si una base de datos filtrada contiene tu clave, los atacantes la prueban en otros servicios. Usar la misma contraseña en todos lados les facilita el acceso a varias cuentas con un solo dato. El problema no es el espacio en disco. |
| 1022 | Ciberseguridad | ¿Qué es el smishing? | El smishing es phishing enviado por mensajes de texto o de aplicaciones como WhatsApp. El mensaje suele pedir que hagas clic en un enlace o entregues datos. No es una contraseña ni un virus que borra archivos. |
| 1023 | Ciberseguridad | ¿Qué es el vishing? | El vishing es phishing por teléfono: alguien se hace pasar por una empresa o un banco para obtener datos. La voz y la urgencia son parte del engaño. No es una actualización ni un virus. |
| 1024 | Ciberseguridad | Recibís un correo urgente con un enlace que pide tus datos. ¿Qué conviene hacer? | Un correo que pide datos con urgencia suele buscar que actúes sin pensar. Conviene no hacer clic y confirmar por un canal oficial, como el sitio o el teléfono de la empresa. Reenviarlo multiplica el riesgo. |
| 1025 | Sistemas Operativos | ¿Qué es un proceso? | Un proceso es un programa que el sistema operativo cargó en memoria y está ejecutando. El archivo guardado en el disco solo se convierte en proceso cuando se inicia. No es una pieza física del procesador. |
| 1026 | Sistemas Operativos | ¿Qué hace el sistema de archivos? | El sistema de archivos organiza los datos en carpetas y archivos y registra dónde está cada cosa en el disco. También aplica permisos y controla el acceso. No aumenta la RAM ni conecta a Internet. |
| 1027 | Sistemas Operativos | ¿Para qué sirven los permisos de usuario? | Los permisos indican qué puede hacer cada usuario con cada archivo: leerlo, modificarlo o ejecutarlo. Así se protege la información de un equipo compartido. No cambian el color de la pantalla ni miden la red. |
| 1028 | Sistemas Operativos | ¿Por qué conviene instalar las actualizaciones del sistema? | Las actualizaciones corrigen fallas y cierran problemas de seguridad que se van descubriendo. También pueden mejorar el rendimiento. No borran los archivos del equipo ni agrandan el disco. |
| 1029 | Sistemas Operativos | ¿Qué son los permisos de una aplicación móvil? | Cuando una aplicación móvil pide permisos, está solicitando acceso a funciones del teléfono o a datos personales. Conviene revisar qué pide y darle solo lo necesario. No son las contraseñas del equipo ni el plan de datos. |
| 1030 | Sistemas Operativos | ¿Cuál es la diferencia principal entre Android e iOS? | Android es el sistema móvil de Google y iOS el de Apple. Cada uno tiene su tienda, sus actualizaciones y su forma de manejar permisos. Ninguno es un navegador ni un procesador. |

### Explicaciones de `avanzado` — 30

| ID | Estación | Pregunta | Explicación |
| --- | --- | --- | --- |
| 3001 | Redes | ¿Qué protocolo permite asignar automáticamente direcciones IP a los dispositivos de una red? | DHCP permite que un dispositivo obtenga su dirección IP y otros datos de red automáticamente al conectarse. Un servidor DHCP administra el rango de direcciones disponibles. DNS traduce nombres y FTP transfiere archivos. |
| 3002 | Redes | ¿Qué dispositivo trabaja principalmente en la capa 3 del modelo OSI? | El router trabaja en la capa 3 del modelo OSI, la de red, y decide por dónde enviar los paquetes entre redes distintas. Un hub y un switch tradicional operan en capas inferiores. Esa es la razón por la que el router conecta redes diferentes. |
| 3003 | Redes | ¿Qué función cumple el protocolo ARP en una red IPv4? | ARP averigua qué dirección física (MAC) corresponde a una dirección IP dentro de la red local. Con ese dato, las tramas llegan al dispositivo correcto. No asigna contraseñas ni cifra la información. |
| 3004 | Redes | ¿Cuál es la diferencia principal entre TCP y UDP? | TCP establece una conexión, ordena los paquetes y vuelve a pedir los que se pierden. UDP envía sin esas garantías, por eso es más rápido y se usa en video o juegos. Ambos funcionan de manera distinta. |
| 3005 | Redes | ¿Qué hace NAT en una red? | NAT cambia las direcciones privadas de la red interna por una dirección pública cuando el tráfico sale a Internet. Así varios equipos comparten una sola IP pública. No asigna nombres ni cifra el WiFi. |
| 3006 | Redes | ¿Qué mejora WPA3 respecto de WPA2? | WPA3 mejora la protección de las redes WiFi, entre otras cosas frente a intentos de adivinar la clave. También refuerza el cifrado de la conexión. No elimina la contraseña ni reduce la velocidad por diseño. |
| 3007 | Hardware | ¿Qué componente del procesador almacena datos e instrucciones de acceso frecuente para acelerar su funcionamiento? | La caché L1 es una memoria pequeña y muy rápida dentro del procesador que guarda datos e instrucciones de uso frecuente. Al tenerlos cerca, el procesador espera menos. El disco, la fuente y los módulos externos no cumplen esa función. |
| 3008 | Hardware | ¿Qué diferencia principal existe entre la memoria SRAM y la DRAM? | La SRAM conserva el dato mientras recibe energía y no necesita refrescarse, por eso es más rápida y cara. La DRAM debe refrescarse constantemente para no perder la información. Esa diferencia explica su uso en caché y en memoria principal. |
| 3009 | Hardware | ¿Qué tecnología utilizan los SSD para distribuir el desgaste entre sus celdas de memoria? | Wear Leveling es la técnica que distribuye las escrituras entre las celdas del SSD para que no se desgasten todas en el mismo lugar. Así el disco dura más. Hyper-Threading y Overclocking pertenecen al procesador. |
| 3010 | Hardware | ¿Qué característica de PCI Express permite aumentar la velocidad de transferencia de datos? | PCI Express usa carriles que trabajan en paralelo, y una tarjeta puede usar más carriles para transferir más datos. Por eso existen configuraciones x1, x4, x8 y x16. No depende de la RAM ni de cables HDMI. |
| 3011 | Hardware | ¿Qué diferencia principal hay entre un HDD y un SSD? | Un HDD guarda los datos en discos magnéticos que giran, mientras que un SSD usa memoria flash sin partes móviles. Por eso el SSD suele ser más rápido y resistente a golpes. Ninguno usa RAM como almacenamiento permanente. |
| 3012 | Hardware | ¿Qué es la memoria virtual? | La memoria virtual es un espacio en el almacenamiento que el sistema operativo usa cuando la RAM no alcanza. Es más lenta que la RAM, pero evita que los programas se cierren por falta de memoria. No reemplaza al procesador ni es una conexión inalámbrica. |
| 3013 | Internet | ¿Qué función cumple el sistema DNS? | El sistema DNS traduce los nombres que escriben las personas a las direcciones IP que usan los equipos. Es como una guía telefónica de Internet. No protege servidores ni aumenta la memoria. |
| 3014 | Internet | ¿Qué significa el código de estado HTTP 403? | El código 403 significa que el servidor recibió el pedido y lo entendió, pero no permite el acceso al recurso. Puede pasar por permisos o por una regla del sitio. No indica que la página no exista. |
| 3015 | Internet | ¿Qué diferencia principal existe entre HTTP y HTTPS? | HTTPS usa TLS para cifrar los datos que viajan entre el navegador y el servidor. Así, quien intercepte la conexión no puede leer el contenido. HTTP viaja sin ese cifrado y no es más seguro. |
| 3016 | Internet | ¿Qué significa el código de estado HTTP 404? | El código 404 indica que el servidor no encontró el recurso pedido. Puede ser una dirección mal escrita o una página que ya no existe. No es un error de contraseña ni una confirmación de cifrado. |
| 3017 | Internet | ¿Qué es la caché del navegador? | El navegador guarda copias de imágenes, estilos y scripts para no descargarlos otra vez en cada visita. Eso acelera la carga y ahorra datos. No bloquea virus ni guarda contraseñas. |
| 3018 | Internet | En una dirección como https://tienda.com/productos?categoria=ofertas, ¿qué indica la parte que comienza con el signo de interrogación? | En una URL, la parte que empieza con el signo de interrogación contiene parámetros que se envían al servidor. Allí pueden ir filtros, búsquedas o datos de una consulta. No es el nombre del servidor ni el protocolo de cifrado. |
| 3019 | Ciberseguridad | ¿Qué es un ataque de fuerza bruta? | Un ataque de fuerza bruta prueba combinaciones de claves una tras otra, muchas veces con programas automáticos. Si la contraseña es corta o común, puede encontrarla. No es un virus de impresoras ni un error de conexión. |
| 3020 | Ciberseguridad | ¿Qué es un ataque Man-in-the-Middle (MitM)? | En un ataque Man-in-the-Middle, el atacante se coloca entre la víctima y el destino y puede leer o modificar lo que se envían. Suele apoyarse en redes WiFi falsas o en configuraciones inseguras. No es un olvido de contraseña ni un apagón. |
| 3021 | Ciberseguridad | ¿Qué caracteriza a una vulnerabilidad Zero-Day? | Una vulnerabilidad Zero-Day es una falla que todavía no fue corregida por el fabricante y que puede ser aprovechada. El nombre alude a que no hubo tiempo de preparar una defensa. No es un error que aparece a las 24 horas ni una clave que vence. |
| 3022 | Ciberseguridad | ¿Qué propiedad de la seguridad informática garantiza que los datos no sean modificados sin autorización? | La integridad garantiza que los datos no se modifiquen sin autorización. La confidencialidad evita que los lean y la disponibilidad asegura que estén accesibles. La velocidad no es una propiedad de seguridad. |
| 3023 | Ciberseguridad | ¿Qué es el ransomware? | El ransomware cifra los archivos de la víctima y pide un pago para devolverlos. Es un malware con fines económicos. No mejora el rendimiento ni es una copia de seguridad. |
| 3024 | Ciberseguridad | ¿Qué es la ingeniería social? | La ingeniería social engaña a las personas con confianza, miedo o urgencia para que entreguen datos o hagan algo riesgoso. Ataca al factor humano, no a un componente técnico. No es instalar un antivirus ni cambiar un nombre de usuario. |
| 3025 | Sistemas Operativos | ¿Qué función cumple el kernel de un sistema operativo? | El kernel es el núcleo del sistema operativo y tiene permisos especiales para administrar el hardware. Coordina la memoria, el procesador y los dispositivos, y atiende a los procesos. No se limita a imágenes ni al navegador. |
| 3026 | Sistemas Operativos | ¿Qué es un proceso zombie en Linux? | Un proceso zombie ya terminó, pero su entrada sigue en la tabla de procesos hasta que el proceso padre lee su estado. No consume CPU ni memoria de trabajo. No es un proceso que usa toda la RAM ni uno sin Internet. |
| 3027 | Sistemas Operativos | ¿Qué algoritmo de planificación asigna un intervalo de tiempo a cada proceso? | Round Robin asigna a cada proceso un intervalo de tiempo y luego pasa al siguiente, en turnos. Así todos reciben atención y el sistema se siente fluido. First Come, First Served y Shortest Job First usan otros criterios. |
| 3028 | Sistemas Operativos | ¿Qué ocurre cuando se produce un Deadlock o interbloqueo? | En un interbloqueo, cada proceso tiene un recurso y espera otro que tiene el anterior, y ninguno puede avanzar. El sistema queda trabado hasta que se libere la situación. No elimina programas ni acelera el procesador. |
| 3029 | Sistemas Operativos | ¿Qué diferencia hay entre un proceso y un hilo? | Un proceso tiene su propio espacio de memoria y sus recursos. Los hilos son tareas dentro de un proceso y comparten esa memoria, por eso la comunicación entre ellos es más simple. No son lo mismo. |
| 3030 | Sistemas Operativos | ¿Por qué es riesgoso instalar aplicaciones fuera de la tienda oficial? | Las aplicaciones que se instalan fuera de la tienda oficial no pasan por la revisión de la empresa que fabrica el sistema. Por eso pueden incluir malware o pedir permisos peligrosos. No ahorran batería por ser externas ni dejan de actualizarse. |

## Alcance

| Archivo | Cambio |
| --- | --- |
| `bd/schema.sql` | Agregar `tema.introduccion TEXT NULL` y `pregunta.explicacion TEXT NULL`. |
| `bd/migraciones/20261113_explicaciones-e-introducciones.sql` | Nuevo. Migración idempotente para bases existentes. |
| `bd/seeds/001_contenido_inicial.sql` | Cargar las 14 introducciones y las 20 explicaciones de `inicial`. Incluir las columnas nuevas en el `ON DUPLICATE KEY UPDATE`. |
| `bd/seeds/002_contenido_intermedio.sql` | Cargar las 30 explicaciones de `intermedio` y sumar `explicacion` al `ON DUPLICATE KEY UPDATE`. |
| `bd/seeds/003_contenido_avanzado.sql` | Cargar las 30 explicaciones de `avanzado` y sumar `explicacion` al `ON DUPLICATE KEY UPDATE`. |
| `bd/escape_room_7b2026_completa.sql` | Regenerar con el esquema y el contenido nuevos. |
| `app/servicios/estaciones.py` | Nueva función `obtener_aprendizaje_estacion(intento_id, estacion_id)`. |
| `app/servicios/admin_tablas.py` | Agregar `introduccion` al `select` y a los `campos` de `tema`, y `explicacion` al `select` y a los `campos` de `pregunta`, como `textarea` opcional. |
| `app/routes/juego.py` | Pasar `aprendizaje` a `transicion.html` en las dos ramas de `transicion()`: intento activo y intento ya completado. |
| `app/templates/transicion.html` | Nueva sección de aprendizaje debajo del resumen y arriba de los botones. |
| `tests/` | Pruebas de contenido y de pantalla (ver abajo). |
| `AGENTS.md` | Nueva decisión 66, columnas en el modelo de datos y regla de contenido. |
| `docs/guia-de-estudio-para-estudiantes.md` | Mencionar la pantalla de transición con explicaciones. |
| `MEMORY.md` | Estado del paso y conteos. |

## Detalle técnico

### Función de servicio

En `app/servicios/estaciones.py`:

```python
def obtener_aprendizaje_estacion(intento_id, estacion_id):
    """Introducciones de los temas y explicación de cada pregunta respondida.

    Solo se llama desde la transición, cuando la estación ya está completada.
    Devuelve ``{"temas": [...], "preguntas": [...]}``. Las preguntas salen del
    envío que completó la estación (``respuestas_correctas`` completo), así la
    respuesta mostrada es la que el equipo eligió y no la que esté marcada como
    correcta después.
    """
```

Pasos de la consulta:

1. Buscar el `intento_envio` que completó la estación:

   ```sql
   SELECT id
   FROM intento_envio
   WHERE intento_id = %s AND estacion_id = %s
     AND respuestas_correctas = %s
   ORDER BY fecha DESC, id DESC
   LIMIT 1
   ```

   `respuestas_correctas` se compara con
   `configuracion.preguntas_por_estacion` (4, con respaldo 4) para no
   hardcodearlo dos veces.

2. Si no hay envío, devolver listas vacías. La plantilla simplemente no muestra
   la sección. No es un error: una estación completada siempre tiene envío, pero
   la pantalla no debe romperse si los datos históricos están incompletos.

3. Traer las 4 preguntas congeladas, su explicación, su tema y la respuesta
   elegida en ese envío:

   ```sql
   SELECT ip.orden,
          p.id AS pregunta_id,
          p.titulo,
          p.explicacion,
          t.id AS tema_id,
          t.nombre AS tema,
          t.introduccion,
          r.contenido AS respuesta_elegida
   FROM intento_pregunta ip
   JOIN pregunta p ON p.id = ip.pregunta_id
   JOIN tema t ON t.id = p.tema_id
   LEFT JOIN respuesta_elegida re
          ON re.intento_id = ip.intento_id
         AND re.intento_envio_id = %s
         AND re.respuesta_id IN (
               SELECT r2.id FROM respuesta r2 WHERE r2.pregunta_id = p.id
             )
   LEFT JOIN respuesta r ON r.id = re.respuesta_id
   WHERE ip.intento_id = %s AND ip.estacion_id = %s
   ORDER BY ip.orden
   ```

   - No se filtra por `activo` en `pregunta`, `tema` ni `respuesta`: la selección
     está congelada y el historial manda.
   - El `IN` con subconsulta evita depender de una columna `pregunta_id` en
     `respuesta_elegida`. Si el equipo eligió una sola respuesta por pregunta
     (lo exige el envío), hay una fila por pregunta.
   - La consulta se puede simplificar con un `JOIN` a `respuesta` y
     `GROUP BY`, pero la versión simple es suficiente para 4 filas.

4. Armar `temas` recorriendo las preguntas y deduplicando por `tema_id`, en el
   orden en que aparecen las preguntas. Cada tema lleva `id`, `nombre` e
   `introduccion`. Así se muestran solo los temas de las preguntas jugadas.

5. Armar `preguntas` con `orden`, `titulo`, `explicacion`, `tema` y
   `respuesta_elegida`.

### Ruta

En `app/routes/juego.py`, dentro de `transicion()`, en las dos ramas que
renderizan `transicion.html`, agregar:

```python
aprendizaje = obtener_aprendizaje_estacion(
    contexto["intento"]["id"], actual["id"]
)
```

y pasarlo a la plantilla como `aprendizaje=aprendizaje`. En la rama del intento
ya completado se usa `finalizado["intento"]["id"]`.

No se agregan rutas nuevas ni se modifica `POST /juego/transicion/<orden>/continuar`.

### Plantilla

En `app/templates/transicion.html`, entre el resumen de 4 tarjetas y el bloque
de `{% if es_ultima %}`, agregar una sección con dos partes:

1. **Temas de la estación.** Si `aprendizaje.temas` tiene filas, por cada tema:
   nombre en un `h3` pequeño e introducción en un párrafo.
2. **Preguntas y respuestas.** Si `aprendizaje.preguntas` tiene filas, por cada
   pregunta, en el orden del intento:
   - el enunciado (`pregunta.titulo`),
   - la respuesta elegida con una etiqueta de éxito:
     `Respuesta correcta: <strong>{{ pregunta.respuesta_elegida }}</strong>`,
   - la explicación, partida en párrafos.

La explicación se renderiza como texto escapado:

```jinja
{% for parrafo in pregunta.explicacion.split('\n\n') %}
  <p class="mb-2">{{ parrafo }}</p>
{% endfor %}
```

Reglas de la sección:

- Debe quedar en una card aparte, con un título claro: **Lo que aprendieron
  en {{ estacion.nombre }}**.
- La card va **antes** de los botones **Continuar** y **Abandonar**, para que se
  lea aunque el equipo avance rápido.
- No se agrega JavaScript ni audio. Es contenido estático.
- Se ve bien en móvil: una columna, tipografía normal, sin tablas.
- Si `aprendizaje.temas` y `aprendizaje.preguntas` están vacíos, la card no se
  muestra.
- No se muestra la palabra "pista" ni se enlaza a `docs/`.

### Seguridad

- La respuesta correcta sigue ausente del HTML de la estación
  (`GET /juego/estacion/<orden>`). Recién aparece en la transición, cuando la
  estación ya está completada.
- La transición ya exige `resumen["completada"]`; no se puede pedir por URL una
  estación sin completar.
- La explicación tampoco debe aparecer en la estación: solo se consulta en
  `obtener_aprendizaje_estacion()`.
- No se agrega ninguna marca de "correcta" a las opciones de la estación.

## Proceso

1. Crear `bd/migraciones/20261113_explicaciones-e-introducciones.sql` con las dos
   columnas.
2. Actualizar `bd/schema.sql`.
3. Cargar las 14 introducciones en `bd/seeds/001_contenido_inicial.sql` y las 20
   explicaciones de `inicial`.
4. Cargar las 30 explicaciones en `bd/seeds/002_contenido_intermedio.sql` y las
   30 en `bd/seeds/003_contenido_avanzado.sql`.
5. Agregar `introduccion` y `explicacion` a los `ON DUPLICATE KEY UPDATE`
   correspondientes.
6. Implementar `obtener_aprendizaje_estacion()` y pasarla en las dos ramas de
   `transicion()`.
7. Extender `transicion.html`.
8. Sumar los dos campos al panel de administración en `admin_tablas.py`, sin
   agregarlos como columnas de listado para no ensanchar las tablas.
9. Regenerar `bd/escape_room_7b2026_completa.sql`.
10. Aplicar la migración y reejecutar los seeds en la base real, con respaldo
    previo y sin intentos activos.
11. Actualizar `AGENTS.md` (decisión 66 y modelo de datos), la guía de estudio y
    `MEMORY.md`.
12. Sumar el paso al índice de `docs/argumentos-pasos/README.md`.

## Pruebas

En `tests/test_seed.py`:

- 14 temas activos con `introduccion` no nula y no vacía.
- 80 preguntas activas con `explicacion` no nula y no vacía: 20 de `inicial`,
  30 de `intermedio` y 30 de `avanzado`.
- Ninguna introducción ni explicación contiene `;`, `'` ni etiquetas HTML.
- Reejecutar los seeds no duplica filas ni cambia `activo`.
- Los conteos siguen en `5/14/80/240/9`.

En `tests/test_reglas_juego.py` (o el archivo de transición que corresponda):

- Completar una estación de `inicial` y entrar a la transición: la respuesta
  correcta y la explicación de las 4 preguntas aparecen en el HTML.
- La introducción de cada tema involucrado aparece una sola vez.
- La respuesta correcta no aparece en el HTML de la estación antes de
  completarla.
- Entrar a la transición de una estación sin completar redirige a la estación,
  como hoy.
- Con un intento ya cerrado como `completo`, la última transición también
  muestra la sección.
- La sección no rompe si `explicacion` es `NULL`: simplemente no muestra el
  párrafo.

En `tests/test_admin.py`:

- Editar `pregunta.explicacion` desde `/admin/preguntas/<id>/editar` se guarda y
  se sigue viendo al volver a entrar.
- Editar `tema.introduccion` desde `/admin/temas/<id>/editar` se guarda y se
  sigue viendo al volver a entrar.

En `tests/test_ranking.py` o de estadísticas, solo como control de no regresión:

- Los conteos y el ranking no cambian.

`pytest -q` debe pasar dos veces seguidas. La suite actual tiene 96 casos; con
estos queda alrededor de 103.

## Criterio de aceptación

- [ ] La migración corre dos veces sin error y no toca datos.
- [ ] `bd/schema.sql` crea las dos columnas nuevas en una base limpia.
- [ ] Los 14 temas tienen introducción y las 80 preguntas tienen explicación.
- [ ] Los conteos siguen en `5/14/80/240/9`.
- [ ] La transición muestra los temas con su introducción.
- [ ] La transición muestra, por cada pregunta, el enunciado, la respuesta
      elegida y la explicación.
- [ ] La respuesta correcta sigue sin aparecer en la estación.
- [ ] La transición de la quinta estación y la de un intento ya completado
      también muestran la sección.
- [ ] `tema.introduccion` y `pregunta.explicacion` se pueden editar desde
      `/admin` y el valor persiste.
- [ ] No hay pistas, enlaces a `docs/` ni cambios en reglas, tiempos o ranking.
- [ ] La pantalla se ve bien en móvil y no tapa los botones.
- [ ] Los seeds son idempotentes y no cambian `activo`, respuestas ni
      `configuracion`.
- [ ] `pytest -q` pasa dos veces seguidas.

## Verificación

```bash
mysql -u <usuario> -p < bd/migraciones/20261113_explicaciones-e-introducciones.sql
mysql -u <usuario> -p < bd/migraciones/20261113_explicaciones-e-introducciones.sql
mysql -u <usuario> -p < bd/seeds/001_contenido_inicial.sql
mysql -u <usuario> -p < bd/seeds/002_contenido_intermedio.sql
mysql -u <usuario> -p < bd/seeds/003_contenido_avanzado.sql
.venv/bin/python -m pytest -q
.venv/bin/python -m pytest -q
```

Consulta de control:

```sql
SELECT 'temas con introduccion' AS control,
       COUNT(*) AS total,
       SUM(introduccion IS NOT NULL AND introduccion <> '') AS completos
FROM tema WHERE activo = 1
UNION ALL
SELECT CONCAT('preguntas ', dificultad),
       COUNT(*),
       SUM(explicacion IS NOT NULL AND explicacion <> '')
FROM pregunta WHERE activo = 1
GROUP BY dificultad;
```

Resultado esperado:

| control | total | completos |
| --- | --- | --- |
| temas con introduccion | 14 | 14 |
| preguntas inicial | 20 | 20 |
| preguntas intermedio | 30 | 30 |
| preguntas avanzado | 30 | 30 |

Revisión manual:

1. Jugar una estación de `inicial` y detenerse en la transición.
2. Confirmar que se ven los temas y las 4 explicaciones.
3. Ver el código fuente de la estación antes de completarla y confirmar que no
   aparece la respuesta correcta ni la explicación.
4. Repetir con una estación de `intermedio` y una de `avanzado`.
5. Probar desde el móvil.

## Fuera de alcance

- Mostrar explicaciones dentro de la estación o en el final.
- Mostrar explicaciones en `/ranking` o `/estadisticas`.
- Agregar pistas nuevas o cambiar `docs/pistas-del-juego.md`.
- Cambiar preguntas, respuestas, opciones, dificultad o cobertura.
- Cambiar los tiempos, las reglas de eliminación o el ranking.
- Agregar JavaScript, audio, modales, acordeones o tooltips.
- Agregar dependencias, CDN o pasos de build.
- Editar la pantalla final o la eliminación.

## Ojo con

- La respuesta correcta solo puede verse en la transición, nunca en la
  estación. Si aparece antes, el paso está mal.
- Reejecutar los seeds **pisa** lo editado desde `/admin` en `explicacion` e
  `introduccion`, igual que con el título y la descripción.
- La explicación no debe ser una pista: se lee después de responder, pero
  conviene que no anticipe la respuesta de otra pregunta de la misma estación.
- No usar `;` ni `'` en los textos: rompen el cargador de seeds de las pruebas.
- No hardcodear las 4 respuestas en la plantilla ni en el JS: salen del envío
  registrado.
- Si el administrador cambia después la respuesta correcta, la transición sigue
  mostrando la que el equipo eligió, porque es historial.
- La migración no reemplaza a los seeds: la columna se crea vacía y el contenido
  entra al reejecutarlos.
- No aplicar la migración en la base real con equipos jugando.
- Mantener el estilo de la pantalla: Bootstrap mínimo, sin componentes nuevos.
