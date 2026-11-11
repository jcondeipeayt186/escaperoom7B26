# Guía de estudio — nivel avanzado

Esta guía reúne los conceptos que aparecen en el nivel **avanzado** del Escape
Room. Está pensada para leer antes de jugar o para imprimir y consultar en el
stand. No reemplaza al banco de preguntas ni a las pistas: la partida siempre se
juega con las preguntas y opciones que están cargadas en la base de datos.

## Cómo se juega este nivel

- El equipo recorre cinco estaciones en orden: Redes, Hardware, Internet,
  Ciberseguridad y Sistemas Operativos.
- En cada estación hay cuatro preguntas con tres opciones cada una. Todas deben
  quedar correctas para avanzar.
- La estación dura cuatro minutos. Además, el equipo se elimina si acumula dos
  respuestas incorrectas o si abandona.
- Hay hasta dos ayudas por estación. La aplicación registra cuántas usaste, pero
  no muestra el texto de la pista: las pistas se leen en papel.
- Las preguntas de este nivel se sortean entre las 30 disponibles y quedan
  congeladas para ese intento. Recargar la página no cambia la selección.

## Estación 1: Redes

### DHCP: configuración automática

**DHCP** (Dynamic Host Configuration Protocol) asigna automáticamente una
dirección IP, la máscara de subred, la puerta de enlace y los servidores DNS a
los dispositivos que se conectan a una red. Sin DHCP, cada equipo tendría que
configurarse a mano. Un servidor DHCP mantiene un registro de las direcciones
que entrega y durante cuánto tiempo las presta.

### Modelo OSI y capa 3

El modelo **OSI** divide las comunicaciones de red en siete capas. La **capa 3**
o capa de red se ocupa del direccionamiento lógico y del enrutamiento de
paquetes entre redes distintas. El **router** es el dispositivo que trabaja
principalmente en esa capa: analiza la dirección IP de destino y decide por qué
camino enviar cada paquete. Un hub y un switch tradicional trabajan
principalmente en capas inferiores.

### ARP: de IP a MAC

En IPv4, para entregar una trama dentro de una red local hace falta conocer la
dirección física o **MAC** del dispositivo de destino. El protocolo **ARP**
(Address Resolution Protocol) relaciona una dirección IP conocida con la
dirección MAC correspondiente. El equipo pregunta "¿quién tiene esta IP?" y el
dispositivo responde con su MAC. Esa información se guarda temporalmente en una
tabla ARP.

### TCP y UDP

**TCP** y **UDP** son protocolos de transporte, pero ofrecen garantías
distintas:

- **TCP** orienta la conexión, confirma la recepción, reordena los datos y
  reenvía lo que se pierde. Se usa cuando no se puede tolerar la pérdida de
  información, por ejemplo en una transferencia de archivos o en una página
  web.
- **UDP** no garantiza la entrega ni el orden. Es más liviano y rápido, y se usa
  cuando importa más la velocidad que la confiabilidad, por ejemplo en
  transmisiones de audio o video en tiempo real.

Que UDP no garantice la entrega no significa que siempre se pierdan datos: la
aplicación que lo usa decide si necesita agregar su propio control.

### NAT: varias direcciones privadas, una pública

**NAT** (Network Address Translation) permite que varios dispositivos de una red
privada salgan a Internet usando una o pocas direcciones públicas. El router
traduce las direcciones privadas de origen a una dirección pública y mantiene
una tabla para saber a qué equipo interno pertenece cada respuesta. Por eso en
una casa pueden convivir muchos dispositivos conectados con una sola conexión.

### WPA3 y la seguridad WiFi

**WPA3** es la versión más reciente del protocolo de seguridad para redes
inalámbricas. Mejora la protección de la clave y dificulta los ataques de fuerza
bruta contra la contraseña WiFi. No elimina la necesidad de usar una clave ni
garantiza que la red sea segura por sí sola: también importan la configuración
del router y las actualizaciones del firmware.

## Estación 2: Hardware

### Memoria caché del procesador

El procesador no accede a la memoria principal todo el tiempo: eso sería lento
en comparación con su velocidad interna. Por eso incorpora memoria **caché** en
varios niveles:

- **L1:** la más pequeña y rápida, integrada en el núcleo.
- **L2:** más grande y algo más lenta.
- **L3:** compartida entre núcleos en muchos procesadores.

La caché almacena datos e instrucciones de acceso frecuente para reducir la
espera del procesador. No reemplaza a la RAM ni al disco: es una ayuda temporal
mucho más rápida y mucho más chica.

### SRAM y DRAM

Ambas son memorias volátiles, es decir, pierden su contenido al cortar la
energía, pero funcionan de manera distinta:

- **SRAM** (Static RAM) mantiene el dato mientras haya energía, sin necesidad de
  refrescarlo periódicamente. Es muy rápida y se usa en cachés.
- **DRAM** (Dynamic RAM) necesita refrescar constantemente sus celdas para no
  perder la información. Es más barata y densa, y se usa como memoria principal.

### SSD y desgaste de celdas

Las unidades **SSD** usan memoria flash. Cada celda tiene una cantidad limitada
de ciclos de escritura, por lo que el controlador aplica **Wear Leveling**: en
lugar de escribir siempre en las mismas celdas, distribuye las escrituras entre
todas para prolongar la vida útil del dispositivo.

### PCI Express y los carriles

**PCI Express** (PCIe) es un bus de alta velocidad que conecta componentes como
placas de video, discos NVMe o tarjetas de red. Utiliza **carriles** o líneas de
comunicación que se identifican como x1, x4, x8 o x16. Cuantos más carriles se
usan en paralelo, mayor es el ancho de banda disponible. No se necesitan cables
HDMI ni memoria RAM externa para aumentar esa velocidad.

### HDD y SSD

Un **HDD** (disco rígido) almacena los datos en discos magnéticos que giran y
usa un cabezal móvil para leerlos y escribirlos. Un **SSD** usa celdas de memoria
flash y no tiene partes mecánicas en movimiento. Por eso el SSD suele ser más
rápido, más silencioso y más resistente a los golpes, aunque su precio por
capacidad puede ser mayor.

### Memoria virtual

Cuando la memoria RAM no alcanza, el sistema operativo puede usar un espacio del
disco como extensión de la memoria principal. Ese espacio se llama **memoria
virtual** o archivo de intercambio. Permite seguir trabajando con más programas
abiertos, pero es mucho más lento que la RAM física: el disco no reemplaza al
procesador ni a la memoria real.

## Estación 3: Internet

### DNS: nombres en lugar de números

Los dispositivos se localizan mediante direcciones IP, pero las personas
recordamos mejor nombres como `www.escuela.edu.ar`. El **DNS** (Domain Name
System) traduce esos nombres de dominio a direcciones IP. Cuando escribís una
dirección en el navegador, primero se consulta al DNS para saber a qué servidor
hay que conectarse.

### Códigos de estado HTTP

El servidor responde a cada solicitud del navegador con un **código de estado**.
Algunos de los más conocidos son:

- **200:** la solicitud se resolvió correctamente.
- **403:** el servidor entendió la solicitud, pero deniega el acceso.
- **404:** el recurso o la página no se encontró.
- **500:** hubo un error interno en el servidor.

El 403 no significa que la página no exista: significa que no tenés permiso para
acceder a ella. El 404 sí indica que el recurso solicitado no está disponible en
esa dirección.

### HTTP y HTTPS

**HTTP** es el protocolo que usan el navegador y el servidor para intercambiar
peticiones y respuestas. **HTTPS** es HTTP protegido con **TLS**, que cifra la
comunicación. Gracias a ese cifrado, otra persona en la red no puede leer
fácilmente el contenido intercambiado ni modificarlo sin ser detectada. HTTPS no
hace que el sitio sea confiable por sí solo, pero protege el canal.

### Caché del navegador

La **caché** guarda copias locales de imágenes, estilos, scripts y otros
recursos. Cuando volvés a visitar una página, el navegador puede reutilizar esos
archivos en lugar de descargarlos otra vez, y así la página carga más rápido. No
es un antivirus ni el historial de contraseñas; se puede borrar desde la
configuración del navegador.

### Partes de una URL y parámetros

Una **URL** identifica un recurso en la web. En una dirección como
`https://tienda.com/productos?categoria=ofertas` se distinguen estas partes:

- `https`: el **protocolo**.
- `tienda.com`: el **dominio**.
- `/productos`: la **ruta** del recurso.
- `?categoria=ofertas`: la **consulta o parámetros** que se envían al servidor.

Los parámetros suelen ser pares `clave=valor` y el servidor los usa para
filtrar, ordenar o personalizar la respuesta. No forman parte del nombre del
servidor ni del protocolo de cifrado.

## Estación 4: Ciberseguridad

### Ataques de fuerza bruta

Un ataque de **fuerza bruta** intenta descubrir una contraseña probando muchas
combinaciones posibles. Puede ser lento, pero funciona mejor cuando la clave es
corta o predecible. Por eso conviene usar contraseñas largas, únicas y, cuando
está disponible, autenticación de dos factores. Los sistemas también pueden
limitar la cantidad de intentos para dificultar este ataque.

### Man-in-the-Middle (MitM)

En un ataque **Man-in-the-Middle**, un tercero se interpone en la comunicación
entre dos partes. Puede observar, interceptar o modificar los datos que se
intercambian. Un ejemplo clásico es una red WiFi falsa que se hace pasar por la
red legítima. El cifrado de HTTPS ayuda a proteger la comunicación, pero no
reemplaza la verificación del destino ni el cuidado con las redes desconocidas.

### Vulnerabilidades Zero-Day

Una vulnerabilidad **Zero-Day** es una falla de seguridad que todavía no tiene
un parche disponible o que era desconocida para el fabricante. Los atacantes
pueden aprovecharla antes de que exista una solución. Como no siempre se puede
prevenir con una actualización, importan las capas de defensa: antivirus,
permisos limitados, respaldos y monitoreo.

### Integridad, confidencialidad y disponibilidad

La seguridad informática se apoya en tres propiedades fundamentales:

- **Confidencialidad:** solo las personas autorizadas pueden acceder a la
  información.
- **Integridad:** los datos no se modifican sin autorización.
- **Disponibilidad:** los sistemas y datos están accesibles cuando se necesitan.

Si alguien altera un archivo sin permiso, está afectando la **integridad**. La
velocidad no es una propiedad de seguridad.

### Ransomware

El **ransomware** es un tipo de malware que cifra los datos y pide un rescate
para liberarlos. Puede llegar por un archivo adjunto, un enlace malicioso o una
vulnerabilidad sin actualizar. La mejor defensa incluye copias de seguridad
actualizadas y guardadas por separado, además de evitar abrir archivos
sospechosos.

### Ingeniería social

La **ingeniería social** manipula a las personas para que revelen información o
realicen una acción riesgosa. No depende solo de fallas técnicas: aprovecha la
confianza, la urgencia o el miedo. El phishing, el smishing y el vishing son
ejemplos de ataques de ingeniería social. Desconfiar de los mensajes que apuran
y verificar por un canal oficial es una buena defensa.

## Estación 5: Sistemas Operativos

### El kernel

El **kernel** es el núcleo del sistema operativo. Administra los recursos del
hardware y coordina la ejecución de los procesos: decide qué programa usa el
procesador, cómo se reparte la memoria y cómo se accede a los dispositivos. Sin
kernel, el software no podría comunicarse con el hardware de forma controlada.

### Procesos zombie en Linux

Un **proceso zombie** es un proceso que ya terminó de ejecutarse, pero cuya
entrada todavía permanece en la tabla de procesos. Ocurre cuando el proceso
padre no recoge su estado de finalización. No consume procesador ni memoria como
un proceso activo, pero ocupa una entrada en la tabla. Si se acumulan muchos,
pueden ser un síntoma de un problema en el programa que los creó.

### Planificación Round Robin

**Round Robin** es un algoritmo de planificación que asigna a cada proceso un
intervalo de tiempo o *quantum* y luego pasa al siguiente, en forma de turnos
rotativos. Todos los procesos listos reciben oportunamente un turno de CPU, lo
que da una sensación de funcionamiento simultáneo. No es lo mismo que First Come,
First Served ni que Shortest Job First.

### Deadlock o interbloqueo

Hay **deadlock** cuando dos o más procesos quedan esperando indefinidamente
recursos que están retenidos entre sí. Por ejemplo, el proceso A tiene el recurso
1 y espera el 2, mientras que el proceso B tiene el recurso 2 y espera el 1.
Ninguno puede avanzar y el sistema queda bloqueado en esa parte. Los sistemas
operativos aplican estrategias de prevención, detección o recuperación.

### Proceso e hilo

Un **proceso** es una instancia de un programa en ejecución y tiene su propio
espacio de memoria y sus propios recursos. Un **hilo** es una unidad de ejecución
dentro de un proceso: varios hilos comparten el espacio de memoria del proceso,
aunque cada uno tiene su propio estado de ejecución. Esa diferencia permite que
los hilos se comuniquen más fácilmente, pero también exige cuidado para que no
interfieran entre sí.

### Aplicaciones fuera de la tienda oficial

Instalar aplicaciones desde fuera de la tienda oficial es riesgoso porque pueden
contener malware y no estar verificadas por la tienda. En Android se suele hablar
de *sideloading*. Aunque a veces permite acceder a apps que no están publicadas,
conviene hacerlo solo con fuentes confiables y revisar los permisos que solicita
la aplicación.

## Glosario mínimo

- **ARP:** protocolo que relaciona direcciones IP con direcciones MAC.
- **Caché:** memoria rápida que guarda datos de uso frecuente.
- **Deadlock:** bloqueo de procesos que esperan recursos retenidos entre sí.
- **DHCP:** protocolo que asigna automáticamente la configuración de red.
- **DNS:** sistema que traduce nombres de dominio a direcciones IP.
- **DRAM:** memoria volátil que necesita refresco periódico.
- **HTTPS:** HTTP protegido con cifrado TLS.
- **Ingeniería social:** manipulación de personas para obtener información o acciones.
- **Kernel:** núcleo del sistema operativo que administra el hardware.
- **MitM:** ataque en el que un tercero intercepta la comunicación.
- **NAT:** traducción de direcciones privadas a una dirección pública.
- **Ransomware:** malware que cifra datos y pide un rescate.
- **Round Robin:** planificación por turnos de tiempo.
- **SRAM:** memoria volátil rápida que no necesita refresco periódico.
- **Wear Leveling:** técnica que distribuye el desgaste entre celdas de un SSD.
- **WPA3:** protocolo de seguridad para redes WiFi.
- **Zero-Day:** vulnerabilidad sin parche disponible.
