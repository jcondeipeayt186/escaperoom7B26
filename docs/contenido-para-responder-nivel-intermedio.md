# Guía de estudio — nivel intermedio

Esta guía reúne los conceptos que aparecen en el nivel **intermedio** del Escape
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

### Direcciones IP y loopback

Una dirección IP identifica un dispositivo dentro de una red. En IPv4 se escribe
con cuatro números entre 0 y 255, separados por puntos. La dirección
`127.0.0.1` es especial: se llama **loopback** y permite que una computadora se
comunique consigo misma sin salir a la red. Es útil para probar servicios
locales.

### Máscara de subred

La máscara de subred acompaña a la dirección IP y permite separar dos partes:
la que identifica a la **red** y la que identifica al **host** o dispositivo.
Gracias a esa división, los equipos saben si otro dispositivo está en la misma
red local o si debe enviar el tráfico a un router.

### DHCP: direcciones automáticas

Cuando un dispositivo se conecta a una red, necesita una dirección IP, una
máscara, una puerta de enlace y un servidor DNS. El protocolo **DHCP** entrega
esos datos automáticamente. Sin DHCP habría que configurar cada equipo a mano,
algo poco práctico en una escuela o en una casa con varios dispositivos.

### Switch y red local

Un **switch** conecta varios dispositivos dentro de una red local (LAN). A
diferencia de un hub, que repite la señal por todos los puertos, el switch
aprende las direcciones MAC y envía cada trama al puerto del dispositivo
destinatario. Así se reduce el tráfico innecesario y mejora el rendimiento.

### DNS: la agenda de Internet

Las personas recordamos nombres como `www.escuela.edu.ar`, pero los equipos
trabajan con direcciones IP. El **DNS** (Domain Name System) traduce esos
nombres a direcciones numéricas. Si el DNS falla, el navegador puede mostrar un
error aunque la conexión a Internet funcione.

### Punto de acceso inalámbrico

Un **Access Point** o punto de acceso conecta dispositivos inalámbricos con una
red cableada. En una escuela suele ser el equipo que emite la red WiFi y que,
a su vez, está conectado por cable al switch o al router. No almacena archivos
ni reemplaza la memoria del equipo: su función es enlazar ambos mundos.

## Estación 2: Hardware

### SMART y la salud del disco

Las unidades de almacenamiento modernas incluyen la tecnología **SMART**, que
supervisa indicadores internos como la temperatura, los errores y el desgaste.
Cuando un valor se aleja de lo normal, SMART puede avisar antes de que el disco
falle. Ese aviso permite hacer una copia de seguridad a tiempo.

### Pantalla azul en Windows

La clásica **pantalla azul** aparece cuando Windows detecta un problema grave y
no puede continuar. Puede deberse a un controlador defectuoso, a un componente
de hardware que falla o a archivos del sistema dañados. Si se repite, conviene
revisar el equipo en lugar de ignorarla.

### Copias de seguridad

Una copia de seguridad permite recuperar la información si los archivos
originales se pierden por un accidente, una falla técnica o un problema de
software. No elimina la necesidad de un antivirus ni acelera Internet: su valor
está en poder restaurar los datos cuando algo sale mal.

### Pasta térmica y refrigeración

El procesador genera calor mientras trabaja. La **pasta térmica** se coloca
entre el procesador y el disipador para rellenar las microscópicas imperfecciones
de ambas superficies y mejorar la transferencia de calor. No es un aislante ni
un adhesivo: su función es conducir el calor hacia el sistema de refrigeración.

### Mantenimiento preventivo y correctivo

El mantenimiento **preventivo** se hace antes de que aparezca el problema:
limpieza, revisión de temperaturas, actualizaciones y copias de seguridad. El
mantenimiento **correctivo** se hace cuando el equipo ya falló. El preventivo
reduce la probabilidad de fallas futuras.

### Memoria RAM volátil

La memoria **RAM** guarda temporalmente los datos y programas que se están
usando. Es **volátil** porque pierde su contenido cuando se apaga el equipo.
Por eso los archivos deben guardarse en el disco; la RAM no es un almacenamiento
permanente.

## Estación 3: Internet

### Cookies del navegador

Las **cookies** son pequeños datos que un sitio guarda en el navegador. Sirven
para recordar la sesión, el idioma o las preferencias, y también para medir el
uso del sitio. No aceleran el procesador ni impiden HTTPS. Se pueden borrar o
limitar desde la configuración del navegador.

### Modo incógnito

El modo incógnito evita que el navegador guarde el historial y las cookies de
esa sesión en el dispositivo. No hace que la navegación sea invisible: el
proveedor de Internet, la red WiFi o el sitio visitado todavía pueden registrar
la actividad. Sirve para reducir rastros locales, no como anonimato completo.

### Partes de una URL

Una dirección web o **URL** tiene varias partes. En
`https://www.escuela.edu.ar/aula/notas`:

- `https` es el **protocolo**.
- `www.escuela.edu.ar` es el **dominio** o nombre del servidor.
- `/aula/notas` es la **ruta** del recurso.

El dominio identifica al sitio y el DNS lo traduce a una dirección IP.

### Ancho de banda y latencia

El **ancho de banda** indica cuánta información puede transmitirse por segundo;
se suele medir en megabits por segundo. La **latencia** indica cuánto tarda un
dato en llegar a destino y se mide en milisegundos. Una conexión puede tener
mucho ancho de banda y, aun así, una latencia alta: descargar un archivo grande
puede ser rápido, pero una videollamada se siente con retraso.

## Estación 4: Ciberseguridad

### Autenticación de dos factores (2FA)

La **2FA** agrega un segundo paso además de la contraseña, por ejemplo un código
temporal del celular. Combina algo que sabés con algo que tenés. Si alguien
consigue la contraseña, todavía necesita el segundo factor para entrar.

### Gestores de contraseñas

Un **gestor de contraseñas** guarda las claves cifradas bajo una contraseña
maestra y puede generar claves únicas y largas. Así no hace falta memorizar
todas ni repetirlas. La contraseña maestra sí debe ser fuerte y no debe
compartirse.

### No reutilizar contraseñas

Si usás la misma contraseña en varios sitios y uno de ellos sufre una filtración,
los atacantes pueden probar esa combinación en las demás cuentas. Cada servicio
debería tener una contraseña distinta. El gestor de contraseñas facilita esa
tarea.

### Smishing y vishing

El **phishing** es un engaño para obtener datos. Tiene variantes según el canal:

- **Smishing:** llega por SMS o aplicación de mensajería.
- **Vishing:** llega por una llamada telefónica.

En ambos casos el atacante se hace pasar por una entidad confiable y apura a la
víctima para que entregue contraseñas, datos bancarios o códigos.

### Correos urgentes y enlaces

Ante un mensaje que pide datos con urgencia, conviene no hacer clic y verificar
el pedido por un canal oficial: la web de la institución, un teléfono conocido o
una conversación presencial. Reenviar el mensaje o completar datos solo ayuda al
atacante.

## Estación 5: Sistemas Operativos

### Qué es un proceso

Un **proceso** es un programa que se está ejecutando. Tiene su propio estado,
su memoria y los recursos que el sistema le asignó. Un mismo programa puede dar
lugar a varios procesos, por ejemplo cuando se abren varias ventanas de un
navegador.

### Sistema de archivos

El **sistema de archivos** organiza los datos en el disco y controla el acceso a
archivos y carpetas. Define cómo se nombran, dónde se guardan y quién puede
leerlos o modificarlos. Sin él, el almacenamiento sería un conjunto de datos sin
estructura.

### Permisos de usuario

Los **permisos** indican qué puede hacer cada usuario con un archivo: leerlo,
modificarlo o ejecutarlo. También definen quién es el propietario. Los permisos
evitan que una cuenta común modifique archivos del sistema o datos de otra
persona.

### Actualizaciones del sistema

Las actualizaciones corrigen errores y vulnerabilidades, agregan compatibilidad
y mejoran el rendimiento. No borran los archivos ni agrandan el disco. Conviene
instalarlas cuando el sistema lo solicita, especialmente las de seguridad.

### Permisos en dispositivos móviles

Las aplicaciones móviles piden permisos para acceder a la cámara, el micrófono,
la ubicación, los contactos o los archivos. Conviene revisar esos permisos y
conceder solo los que la app realmente necesita. Se pueden cambiar o quitar
desde la configuración del teléfono.

### Android e iOS

**Android** e **iOS** son dos sistemas operativos móviles de empresas distintas:
Android lo desarrolla Google y iOS Apple. Cada uno tiene su propia tienda de
aplicaciones, sus reglas de seguridad y su forma de gestionar permisos. No son
navegadores ni componentes de hardware.

## Glosario mínimo

- **Access Point:** equipo que conecta dispositivos inalámbricos a una red cableada.
- **Ancho de banda:** cantidad de datos que se pueden transmitir por segundo.
- **Cookie:** dato que un sitio guarda en el navegador para recordar información.
- **DHCP:** protocolo que asigna automáticamente la configuración de red.
- **DNS:** sistema que traduce nombres de dominio a direcciones IP.
- **Latencia:** tiempo que tarda un dato en llegar a destino.
- **Loopback:** dirección `127.0.0.1`, usada para comunicarse con el propio equipo.
- **Máscara de subred:** valor que separa la parte de red y la de host de una IP.
- **Phishing:** engaño para obtener información o conseguir una acción de la víctima.
- **Proceso:** programa en ejecución con su propio estado y recursos.
- **SMART:** tecnología que supervisa el estado de una unidad de almacenamiento.
- **Switch:** dispositivo que conecta equipos dentro de una red local.
- **2FA:** segundo paso de verificación además de la contraseña.
