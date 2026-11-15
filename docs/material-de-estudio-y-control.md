# Material de estudio y control — Escape Room 7.º B 2026

> Documento para estudiar y controlar el contenido del juego. Contiene las respuestas correctas: **no se enlaza desde la aplicación** y no se muestra durante la partida.

Generado el 15/11/2026 desde la base `escape_room_7b2026` con el contenido congelado: 5 estaciones, 14 temas y 80 preguntas (20 `inicial`, 30 `intermedio` y 30 `avanzado`). Si se edita contenido desde `/admin`, hay que regenerar este documento y los PDFs de `docs/pdf/`.

## Cómo usar este material

1. Leé primero la introducción del tema: explica de qué se trata antes de las preguntas.
2. Tapá la opción marcada, respondé y recién después leé la explicación. Así el material sirve para autoevaluarte.
3. Las pistas del juego no están acá: se leen en papel desde `docs/pistas-del-juego.md`.
4. Usá el anexo de cobertura para controlar que cada tema tenga preguntas en los tres niveles.

## Contenido

- Estación 1: Redes
- Estación 2: Hardware
- Estación 3: Internet
- Estación 4: Ciberseguridad
- Estación 5: Sistemas Operativos
- Anexo: cobertura

## Estación 1: Redes

*Conceptos de redes, direccionamiento IP, router y conexión WiFi.*

### Tema: IP

Una dirección IP identifica a cada dispositivo dentro de una red y permite que los datos lleguen a destino. Puede ser privada, pública o especial, como la de loopback. Conocerla ayuda a entender cómo se comunican los equipos.

#### Nivel inicial

**1. ¿Qué significa IP?**

- A. Internet personal
- B. **Internet Protocol** ✅
- C. Información privada

*Explicación:* IP son las siglas de Internet Protocol, el protocolo que identifica cada dispositivo dentro de una red y permite que los datos sepan hacia dónde viajar. Cada equipo conectado recibe una dirección IP, como si fuera su número de casa.

#### Nivel intermedio

**2. ¿Qué dirección IPv4 es una dirección de loopback?**

- A. **127.0.0.1** ✅
- B. 169.254.1.1
- C. 192.168.1.1

*Explicación:* La dirección 127.0.0.1 se conoce como loopback y siempre apunta al propio equipo. Sirve para probar si la configuración de red funciona sin salir a la LAN. Las direcciones 192.168 y 169.254 pertenecen a otros rangos.

**3. ¿Cuál es la función principal de una máscara de subred?**

- A. Identificar el fabricante del equipo
- B. **Diferenciar la parte de red y la parte de host de una dirección IP** ✅
- C. Aumentar la velocidad de la conexión

*Explicación:* La máscara de subred indica cuántos bits de la dirección IP identifican la red y cuántos identifican al equipo. Con esa información, el equipo sabe si el destino está dentro de su red o fuera. No identifica al fabricante ni cambia la velocidad.

#### Nivel avanzado

**4. ¿Qué función cumple el protocolo ARP en una red IPv4?**

- A. **Traducir direcciones IP a direcciones MAC** ✅
- B. Asignar contraseñas a los dispositivos
- C. Cifrar la información transmitida

*Explicación:* ARP averigua qué dirección física (MAC) corresponde a una dirección IP dentro de la red local. Con ese dato, las tramas llegan al dispositivo correcto. No asigna contraseñas ni cifra la información.

### Tema: Router

El router es el equipo que conecta redes distintas y decide por dónde sale cada paquete. En una casa suele unir la red interna con Internet. Su trabajo es distinto del de un switch o un punto de acceso.

#### Nivel inicial

**5. ¿Qué dispositivo conecta diferentes redes?**

- A. Teclado
- B. **Router** ✅
- C. Monitor

*Explicación:* El router une redes distintas y decide por dónde enviar cada paquete de datos. En una casa, es el equipo que conecta la red interna con Internet. Un teclado o un monitor no cumplen esa función.

#### Nivel intermedio

**6. ¿Qué protocolo asigna direcciones IP automáticamente a los dispositivos de una red?**

- A. DNS
- B. **DHCP** ✅
- C. FTP

*Explicación:* DHCP es el protocolo que entrega automáticamente dirección IP, máscara y puerta de enlace a los dispositivos. Así no hay que configurar cada equipo a mano. DNS traduce nombres y FTP transfiere archivos.

#### Nivel avanzado

**7. ¿Qué protocolo permite asignar automáticamente direcciones IP a los dispositivos de una red?**

- A. DNS
- B. **DHCP** ✅
- C. FTP

*Explicación:* DHCP permite que un dispositivo obtenga su dirección IP y otros datos de red automáticamente al conectarse. Un servidor DHCP administra el rango de direcciones disponibles. DNS traduce nombres y FTP transfiere archivos.

**8. ¿Qué dispositivo trabaja principalmente en la capa 3 del modelo OSI?**

- A. Hub
- B. Switch tradicional
- C. **Router** ✅

*Explicación:* El router trabaja en la capa 3 del modelo OSI, la de red, y decide por dónde enviar los paquetes entre redes distintas. Un hub y un switch tradicional operan en capas inferiores. Esa es la razón por la que el router conecta redes diferentes.

**9. ¿Qué hace NAT en una red?**

- A. Asigna nombres de dominio a los dispositivos
- B. **Traduce direcciones privadas a una pública para salir a Internet** ✅
- C. Cifra el tráfico de la red WiFi

*Explicación:* NAT cambia las direcciones privadas de la red interna por una dirección pública cuando el tráfico sale a Internet. Así varios equipos comparten una sola IP pública. No asigna nombres ni cifra el WiFi.

### Tema: Redes de computadoras

Una red de computadoras es un conjunto de dispositivos conectados para compartir datos y recursos. Puede ser cableada o inalámbrica y su tamaño va desde una casa hasta una empresa. Los protocolos son las reglas que ordenan esa comunicación.

#### Nivel inicial

**10. ¿Qué es una red informática?**

- A. **Un conjunto de dispositivos conectados** ✅
- B. Un programa para dibujar
- C. Una pieza de la computadora

*Explicación:* Una red informática es un conjunto de dispositivos conectados entre sí para compartir información y recursos. Pueden estar unidos por cables o por WiFi y sirven para intercambiar archivos, usar una impresora o navegar.

#### Nivel intermedio

**11. ¿Cuál es la función principal de un switch en una red LAN?**

- A. Conectar la red local a Internet obligatoriamente
- B. **Conectar dispositivos dentro de una red local y enviar los datos al dispositivo correspondiente** ✅
- C. Convertir señales digitales en sonido

*Explicación:* Un switch conecta varios equipos de una red local y envía cada trama al puerto del dispositivo correcto. Trabaja dentro de la LAN y no se ocupa de sacar el tráfico a Internet, tarea del router. Tampoco almacena los archivos de los usuarios.

**12. ¿Qué protocolo traduce nombres de dominio como ejemplo.com a direcciones IP?**

- A. **DNS** ✅
- B. DHCP
- C. ARP

*Explicación:* DNS es el servicio que traduce nombres como ejemplo.com a direcciones IP. Gracias a él no hace falta recordar números para entrar a un sitio. DHCP asigna direcciones y ARP las vincula con direcciones MAC.

#### Nivel avanzado

**13. ¿Cuál es la diferencia principal entre TCP y UDP?**

- A. UDP necesita una conexión previa y TCP no
- B. **TCP garantiza una comunicación confiable, mientras que UDP no garantiza la entrega de los datos** ✅
- C. Ambos protocolos funcionan exactamente igual

*Explicación:* TCP establece una conexión, ordena los paquetes y vuelve a pedir los que se pierden. UDP envía sin esas garantías, por eso es más rápido y se usa en video o juegos. Ambos funcionan de manera distinta.

### Tema: WiFi

El WiFi permite conectar dispositivos sin cables mediante ondas de radio. Un punto de acceso recibe la señal y la integra a la red. La seguridad de esa conexión depende del cifrado y de la clave que se use.

#### Nivel inicial

**14. ¿Qué se necesita para conectarse a una red WiFi?**

- A. **Una contraseña, si está protegida** ✅
- B. Un cable HDMI obligatoriamente
- C. Una impresora

*Explicación:* Para entrar a una red WiFi protegida hay que conocer su contraseña o clave de seguridad. Esa clave evita que cualquier persona se conecte sin permiso. Los cables HDMI o las impresoras no tienen relación con esa conexión.

#### Nivel intermedio

**15. ¿Qué función cumple un punto de acceso inalámbrico (Access Point)?**

- A. Almacenar los archivos de los usuarios
- B. **Conectar dispositivos inalámbricos a una red cableada** ✅
- C. Reemplazar la memoria RAM del equipo

*Explicación:* Un punto de acceso recibe la señal de los dispositivos inalámbricos y los integra a la red cableada. Es habitual en escuelas y oficinas para ampliar la cobertura WiFi. No reemplaza la RAM ni guarda archivos.

#### Nivel avanzado

**16. ¿Qué mejora WPA3 respecto de WPA2?**

- A. **Mayor seguridad y protección contra ataques de fuerza bruta a la clave WiFi** ✅
- B. Menor velocidad de conexión
- C. Elimina la necesidad de usar contraseña

*Explicación:* WPA3 mejora la protección de las redes WiFi, entre otras cosas frente a intentos de adivinar la clave. También refuerza el cifrado de la conexión. No elimina la contraseña ni reduce la velocidad por diseño.

## Estación 2: Hardware

*Componentes físicos: procesador, memoria RAM y periféricos de entrada y salida.*

### Tema: Procesador

El procesador ejecuta las instrucciones y coordina el trabajo del equipo. Dentro tiene memorias muy rápidas y se comunica con el resto de los componentes. Su rendimiento depende de varios factores, no solo de la velocidad que muestra la caja.

#### Nivel inicial

**17. ¿Qué componente es considerado el cerebro de la computadora?**

- A. Teclado
- B. **Procesador** ✅
- C. Monitor

*Explicación:* El procesador, también llamado CPU, ejecuta las instrucciones y coordina las tareas del equipo. Por eso se lo compara con el cerebro de la computadora: sin él, el resto de los componentes no puede trabajar. El teclado y el monitor solo permiten entrar o ver información.

#### Nivel intermedio

**18. ¿Qué puede indicar una pantalla azul recurrente en Windows?**

- A. Que el monitor está conectado correctamente
- B. Que el router está apagado
- C. **Un error crítico del sistema o del hardware** ✅

*Explicación:* La pantalla azul de Windows aparece cuando el sistema encuentra un error grave y no puede seguir funcionando. Suele estar relacionada con controladores, memoria o fallas de hardware. No indica que el monitor esté conectado ni que el router esté apagado.

**19. ¿Qué es la pasta térmica?**

- A. Un aislante que impide el paso del calor
- B. Un adhesivo para fijar la memoria RAM
- C. **Un material que mejora la transferencia de calor entre superficies** ✅

*Explicación:* La pasta térmica se coloca entre el procesador y el disipador para llenar las imperfecciones y mejorar el paso del calor. Sin ella quedarían bolsas de aire que calentarían de más. No es un aislante ni un adhesivo para la RAM.

**20. ¿Qué tipo de mantenimiento busca evitar fallas futuras?**

- A. Correctivo
- B. **Preventivo** ✅
- C. Destructivo

*Explicación:* El mantenimiento preventivo se hace antes de que aparezca la falla, con limpieza, revisiones y actualizaciones. El correctivo se aplica cuando el problema ya ocurrió. Prevenir suele ser más barato y evita cortes.

#### Nivel avanzado

**21. ¿Qué componente del procesador almacena datos e instrucciones de acceso frecuente para acelerar su funcionamiento?**

- A. **Memoria caché L1** ✅
- B. Disco rígido HDD
- C. Fuente de alimentación

*Explicación:* La caché L1 es una memoria pequeña y muy rápida dentro del procesador que guarda datos e instrucciones de uso frecuente. Al tenerlos cerca, el procesador espera menos. El disco, la fuente y los módulos externos no cumplen esa función.

**22. ¿Qué característica de PCI Express permite aumentar la velocidad de transferencia de datos?**

- A. La incorporación de memoria RAM externa
- B. La utilización de cables HDMI
- C. **La utilización de múltiples carriles de comunicación (x1, x4, x8, x16)** ✅

*Explicación:* PCI Express usa carriles que trabajan en paralelo, y una tarjeta puede usar más carriles para transferir más datos. Por eso existen configuraciones x1, x4, x8 y x16. No depende de la RAM ni de cables HDMI.

### Tema: Dispositivos de entrada/salida

Los dispositivos de entrada permiten ingresar datos y los de salida muestran el resultado. Algunos cumplen las dos funciones, como una pantalla táctil. El almacenamiento también forma parte del hardware y guarda la información.

#### Nivel inicial

**23. ¿Cuál es un dispositivo de entrada?**

- A. Monitor
- B. Parlante
- C. **Teclado** ✅

*Explicación:* Un dispositivo de entrada permite ingresar datos al equipo. El teclado lo hace cuando escribís y el ratón cuando movés el puntero. El monitor y el parlante son de salida, porque muestran o emiten el resultado.

**24. ¿Cuál es un dispositivo de salida?**

- A. Ratón
- B. Micrófono
- C. **Monitor** ✅

*Explicación:* Un dispositivo de salida presenta al usuario el resultado del trabajo del equipo. El monitor muestra texto e imágenes y el parlante emite sonido. El ratón y el micrófono son de entrada.

#### Nivel intermedio

**25. ¿Qué función cumple la tecnología SMART en las unidades de almacenamiento?**

- A. Controlar las conexiones WiFi
- B. **Supervisar indicadores de estado y anticipar posibles fallas** ✅
- C. Cifrar automáticamente todos los archivos

*Explicación:* SMART es un sistema de autodiagnóstico que registra datos internos del disco, como errores o temperatura. Con esa información se pueden detectar señales de falla antes de que el disco deje de funcionar. No controla el WiFi ni cifra archivos.

**26. ¿Cuál es la finalidad de realizar una copia de seguridad?**

- A. **Recuperar información ante pérdida o daño** ✅
- B. Eliminar la necesidad de antivirus
- C. Aumentar la velocidad de Internet

*Explicación:* Una copia de seguridad guarda una versión adicional de los datos para poder recuperarlos si algo falla. Sirve ante borrados accidentales, fallas del disco o robos. No reemplaza al antivirus ni acelera Internet.

#### Nivel avanzado

**27. ¿Qué tecnología utilizan los SSD para distribuir el desgaste entre sus celdas de memoria?**

- A. Hyper-Threading
- B. **Wear Leveling** ✅
- C. Overclocking

*Explicación:* Wear Leveling es la técnica que distribuye las escrituras entre las celdas del SSD para que no se desgasten todas en el mismo lugar. Así el disco dura más. Hyper-Threading y Overclocking pertenecen al procesador.

**28. ¿Qué diferencia principal hay entre un HDD y un SSD?**

- A. **El HDD usa discos magnéticos y el SSD usa memoria flash** ✅
- B. El HDD usa memoria flash y el SSD usa discos magnéticos
- C. Ambos usan únicamente memoria RAM

*Explicación:* Un HDD guarda los datos en discos magnéticos que giran, mientras que un SSD usa memoria flash sin partes móviles. Por eso el SSD suele ser más rápido y resistente a golpes. Ninguno usa RAM como almacenamiento permanente.

### Tema: Memoria RAM

La memoria RAM es el espacio de trabajo del equipo: guarda lo que se está usando en ese momento. Es rápida y volátil, por eso los datos se pierden al apagar. Cuando falta, el sistema puede apoyarse en el disco con la memoria virtual.

#### Nivel inicial

**29. ¿Para qué sirve la memoria RAM?**

- A. **Guardar datos temporalmente mientras se trabaja** ✅
- B. Imprimir documentos
- C. Proteger físicamente la pantalla

*Explicación:* La memoria RAM guarda los datos y los programas que se están usando en ese momento. Es muy rápida, pero al apagar el equipo su contenido se pierde. No sirve para imprimir ni para proteger la pantalla.

#### Nivel intermedio

**30. ¿Qué significa que la memoria RAM sea volátil?**

- A. Que guarda los datos para siempre
- B. **Que pierde su contenido al apagarse el equipo** ✅
- C. Que solo funciona con Internet

*Explicación:* Decir que la RAM es volátil significa que necesita energía para conservar los datos. Al apagar o reiniciar el equipo, su contenido se borra. Por eso los archivos se guardan en el disco y no en la RAM.

#### Nivel avanzado

**31. ¿Qué diferencia principal existe entre la memoria SRAM y la DRAM?**

- A. La SRAM necesita refresco constante y la DRAM no
- B. **La SRAM no necesita refresco periódico, mientras que la DRAM sí** ✅
- C. Ambas funcionan exactamente de la misma manera

*Explicación:* La SRAM conserva el dato mientras recibe energía y no necesita refrescarse, por eso es más rápida y cara. La DRAM debe refrescarse constantemente para no perder la información. Esa diferencia explica su uso en caché y en memoria principal.

**32. ¿Qué es la memoria virtual?**

- A. **Un espacio en disco que el sistema usa como extensión de la RAM** ✅
- B. Una memoria que reemplaza al procesador
- C. Un tipo de conexión inalámbrica

*Explicación:* La memoria virtual es un espacio en el almacenamiento que el sistema operativo usa cuando la RAM no alcanza. Es más lenta que la RAM, pero evita que los programas se cierren por falta de memoria. No reemplaza al procesador ni es una conexión inalámbrica.

## Estación 3: Internet

*Navegadores web, direcciones URL y acceso a Internet.*

### Tema: Navegadores Web

El navegador es el programa que pide las páginas y las muestra en pantalla. Guarda cookies, caché e historial para que la navegación sea más rápida y cómoda. También ofrece modos y opciones de privacidad que conviene conocer.

#### Nivel inicial

**33. ¿Qué es un navegador web?**

- A. **Un programa para visitar páginas web** ✅
- B. Una parte del procesador
- C. Un cable de red

*Explicación:* Un navegador web es el programa que pide las páginas a los servidores y las muestra en pantalla. Chrome, Firefox y Edge son ejemplos. No es una parte del procesador ni un cable de red.

**34. ¿Cuál de estos es un navegador web?**

- A. **Google Chrome** ✅
- B. Windows
- C. Calculadora

*Explicación:* Google Chrome es un navegador web: sirve para abrir sitios y navegar por Internet. Windows es un sistema operativo y la calculadora es una aplicación de cálculo. Cada programa cumple una función distinta.

#### Nivel intermedio

**35. ¿Para qué sirven las cookies de un navegador?**

- A. Para acelerar el procesador
- B. **Para que el sitio recuerde datos de la visita, como la sesión o las preferencias** ✅
- C. Para impedir que el sitio use HTTPS

*Explicación:* Las cookies son pequeños archivos que el sitio guarda en el navegador para recordar la sesión, el idioma o las preferencias. Sin ellas habría que iniciar sesión en cada página. No aceleran el procesador ni impiden el uso de HTTPS.

**36. ¿Qué hace el modo incógnito de un navegador?**

- A. Cifra todos los archivos del equipo
- B. Impide que el proveedor de Internet vea la navegación
- C. **No guarda el historial ni las cookies de esa sesión en el dispositivo** ✅

*Explicación:* El modo incógnito evita que el navegador guarde el historial y las cookies de esa sesión en el equipo. No oculta la navegación al proveedor de Internet ni a la red WiFi, y tampoco cifra archivos. Sirve para no dejar rastro local, no para ser invisible.

#### Nivel avanzado

**37. ¿Qué es la caché del navegador?**

- A. **Copias de recursos para cargar las páginas más rápido** ✅
- B. Un programa que bloquea los virus
- C. El historial de contraseñas del equipo

*Explicación:* El navegador guarda copias de imágenes, estilos y scripts para no descargarlos otra vez en cada visita. Eso acelera la carga y ahorra datos. No bloquea virus ni guarda contraseñas.

### Tema: URL

Una URL es la dirección de un recurso en Internet y tiene varias partes. El protocolo indica cómo se pide, el dominio identifica al servidor y la ruta señala el recurso. Los parámetros agregan datos a la consulta.

#### Nivel inicial

**38. ¿Qué significa URL?**

- A. **Una dirección de un recurso en internet** ✅
- B. Una memoria de computadora
- C. Un tipo de teclado

*Explicación:* URL son las siglas de Uniform Resource Locator y funcionan como la dirección de una página, una imagen o un archivo en Internet. Al escribirla en el navegador, el equipo sabe qué servidor buscar y qué recurso pedir.

#### Nivel intermedio

**39. En la dirección https://www.escuela.edu.ar/aula/notas, ¿qué parte indica el protocolo?**

- A. **https** ✅
- B. www.escuela.edu.ar
- C. /aula/notas

*Explicación:* En una URL, el protocolo aparece antes de los dos puntos y las barras e indica cómo se pide el recurso. En https://www.escuela.edu.ar/aula/notas, el protocolo es https. El dominio es www.escuela.edu.ar y la ruta es /aula/notas.

**40. ¿Qué indica el dominio en una dirección web?**

- A. La contraseña de la red WiFi
- B. **El nombre que identifica al sitio o servidor** ✅
- C. El tipo de procesador del servidor

*Explicación:* El dominio es la parte de la URL que se registra y se escribe para llegar a un sitio, como escuela.edu.ar. El sistema DNS lo traduce a una dirección IP. No es una contraseña ni el tipo de procesador del servidor.

#### Nivel avanzado

**41. En una dirección como https://tienda.com/productos?categoria=ofertas, ¿qué indica la parte que comienza con el signo de interrogación?**

- A. El nombre del servidor
- B. El protocolo de cifrado
- C. **Los parámetros o la consulta que se envía al servidor** ✅

*Explicación:* En una URL, la parte que empieza con el signo de interrogación contiene parámetros que se envían al servidor. Allí pueden ir filtros, búsquedas o datos de una consulta. No es el nombre del servidor ni el protocolo de cifrado.

### Tema: Conectividad

La conectividad depende de varios factores: la velocidad, la latencia y la calidad de la red. El ancho de banda mide cuánto puede pasar y la latencia cuánto tarda. Los códigos HTTP, por su parte, informan cómo respondió el servidor.

#### Nivel inicial

**42. ¿Qué se necesita para acceder a un sitio web público en internet?**

- A. **Una conexión a internet** ✅
- B. Un escáner obligatoriamente
- C. Un pendrive siempre

*Explicación:* Para ver un sitio público hace falta una conexión que llegue hasta el servidor donde está alojado. Sin conexión a Internet, el navegador no puede pedir esa página. Un escáner o un pendrive no reemplazan esa conexión.

#### Nivel intermedio

**43. ¿Qué es el ancho de banda?**

- A. El tiempo que tarda un dato en llegar
- B. La cantidad de dispositivos conectados a la red
- C. **La cantidad de datos que se pueden transmitir por segundo** ✅

*Explicación:* El ancho de banda mide cuántos datos pueden pasar por segundo por una conexión. Una conexión con más ancho de banda puede mover más información a la vez. No mide la demora de cada dato ni la cantidad de dispositivos.

**44. ¿Qué significa tener una latencia alta?**

- A. Que los datos llegan más rápido
- B. **Que los datos tardan más en llegar a destino** ✅
- C. Que se reduce el tamaño de los archivos

*Explicación:* La latencia es el tiempo que tarda un dato en ir y volver. Cuando es alta, las videollamadas se cortan y los juegos en línea se sienten lentos aunque el ancho de banda sea bueno. No reduce el tamaño de los archivos.

#### Nivel avanzado

**45. ¿Qué función cumple el sistema DNS?**

- A. **Traducir nombres de dominio en direcciones IP** ✅
- B. Proteger físicamente los servidores
- C. Aumentar la memoria RAM de una computadora

*Explicación:* El sistema DNS traduce los nombres que escriben las personas a las direcciones IP que usan los equipos. Es como una guía telefónica de Internet. No protege servidores ni aumenta la memoria.

**46. ¿Qué significa el código de estado HTTP 403?**

- A. El sitio web no existe
- B. **El servidor entendió la solicitud, pero deniega el acceso** ✅
- C. La página fue encontrada correctamente

*Explicación:* El código 403 significa que el servidor recibió el pedido y lo entendió, pero no permite el acceso al recurso. Puede pasar por permisos o por una regla del sitio. No indica que la página no exista.

**47. ¿Qué diferencia principal existe entre HTTP y HTTPS?**

- A. HTTP es más seguro porque no utiliza cifrado
- B. **HTTPS utiliza cifrado mediante TLS para proteger la comunicación** ✅
- C. HTTPS solamente funciona sin conexión a Internet

*Explicación:* HTTPS usa TLS para cifrar los datos que viajan entre el navegador y el servidor. Así, quien intercepte la conexión no puede leer el contenido. HTTP viaja sin ese cifrado y no es más seguro.

**48. ¿Qué significa el código de estado HTTP 404?**

- A. Error de autenticación del usuario
- B. **Recurso o página no encontrada** ✅
- C. Conexión cifrada correctamente

*Explicación:* El código 404 indica que el servidor no encontró el recurso pedido. Puede ser una dirección mal escrita o una página que ya no existe. No es un error de contraseña ni una confirmación de cifrado.

## Estación 4: Ciberseguridad

*Contraseñas seguras y reconocimiento de phishing.*

### Tema: Contraseña

Las contraseñas protegen las cuentas y deben ser largas, únicas y difíciles de adivinar. Un gestor y la autenticación de dos factores ayudan a cuidarlas. Compartirlas o repetirlas aumenta el riesgo.

#### Nivel inicial

**49. ¿Cómo debe ser una contraseña segura?**

- A. 123456
- B. Tu nombre solamente
- C. **Larga y difícil de adivinar** ✅

*Explicación:* Una contraseña segura combina mayúsculas, minúsculas, números y símbolos, y tiene suficiente longitud para que no se adivine fácilmente. Evitá datos obvios como 123456 o tu nombre. Cuanto más difícil de adivinar, mejor protege la cuenta.

**50. ¿Qué conviene hacer con tus contraseñas?**

- A. Compartirlas con desconocidos
- B. Usar la misma en todos lados
- C. **Mantenerlas privadas** ✅

*Explicación:* Las contraseñas son personales y no se comparten con nadie, ni con amigos ni con desconocidos. Usar la misma en todos lados multiplica el daño si una se filtra. Guardarlas de forma segura ayuda a no tener que recordarlas de memoria.

#### Nivel intermedio

**51. ¿Qué es la autenticación de dos factores (2FA)?**

- A. Usar dos contraseñas iguales en dos sitios
- B. **Un segundo paso de verificación además de la contraseña** ✅
- C. Cambiar la contraseña dos veces por año

*Explicación:* La autenticación de dos factores agrega una segunda prueba además de la contraseña, como un código en el celular. Así, aunque alguien conozca la clave, no puede entrar sin ese segundo dato. No consiste en usar dos claves iguales.

**52. ¿Para qué sirve un gestor de contraseñas?**

- A. Para compartir las contraseñas con todos
- B. Para eliminar la necesidad de usar contraseñas
- C. **Para guardar y generar contraseñas seguras sin memorizarlas todas** ✅

*Explicación:* Un gestor de contraseñas guarda las claves cifradas y puede generar nuevas y difíciles de adivinar. Así se usa una clave distinta en cada sitio sin tener que memorizarlas. No elimina la necesidad de contraseñas ni sirve para compartirlas.

**53. ¿Por qué no conviene usar la misma contraseña en varios sitios?**

- A. **Porque si filtran una, pueden acceder a las demás cuentas** ✅
- B. Porque ocupa más espacio en el disco
- C. Porque el navegador la borra automáticamente

*Explicación:* Si una base de datos filtrada contiene tu clave, los atacantes la prueban en otros servicios. Usar la misma contraseña en todos lados les facilita el acceso a varias cuentas con un solo dato. El problema no es el espacio en disco.

#### Nivel avanzado

**54. ¿Qué es un ataque de fuerza bruta?**

- A. **Un intento de descubrir contraseñas probando múltiples combinaciones** ✅
- B. Un virus que solamente afecta a las impresoras
- C. Un error de conexión a Internet

*Explicación:* Un ataque de fuerza bruta prueba combinaciones de claves una tras otra, muchas veces con programas automáticos. Si la contraseña es corta o común, puede encontrarla. No es un virus de impresoras ni un error de conexión.

### Tema: Phishing

El phishing reúne engaños que buscan robar información haciéndose pasar por alguien confiable. Llega por correo, mensajes o llamadas y suele usar la urgencia. La ingeniería social ataca la confianza de las personas.

#### Nivel inicial

**55. ¿Qué deberías hacer con un enlace sospechoso?**

- A. Abrirlo inmediatamente
- B. **Evitar abrirlo y verificar su origen** ✅
- C. Compartirlo con todos

*Explicación:* Antes de abrir un enlace dudoso conviene comprobar quién lo envió y por qué. Se puede consultar por otro canal, como una llamada o el sitio oficial. Abrirlo o compartirlo solo aumenta el riesgo.

**56. ¿Qué es el phishing?**

- A. **Un intento de engaño para robar información** ✅
- B. Un programa para editar fotos
- C. Una clase de monitor

*Explicación:* El phishing es un engaño que imita a una empresa o a una persona conocida para que entregues contraseñas o datos. Suele llegar por correo, mensaje o llamada. No es un programa de fotos ni una clase de monitor.

#### Nivel intermedio

**57. ¿Qué es el smishing?**

- A. Un ataque que solo afecta impresoras
- B. **Un engaño por SMS o aplicación de mensajería** ✅
- C. Un tipo de contraseña segura

*Explicación:* El smishing es phishing enviado por mensajes de texto o de aplicaciones como WhatsApp. El mensaje suele pedir que hagas clic en un enlace o entregues datos. No es una contraseña ni un virus que borra archivos.

**58. ¿Qué es el vishing?**

- A. Un virus que borra archivos
- B. Una actualización del sistema operativo
- C. **Un engaño realizado por llamada telefónica** ✅

*Explicación:* El vishing es phishing por teléfono: alguien se hace pasar por una empresa o un banco para obtener datos. La voz y la urgencia son parte del engaño. No es una actualización ni un virus.

**59. Recibís un correo urgente con un enlace que pide tus datos. ¿Qué conviene hacer?**

- A. Hacer clic y completar los datos rápido
- B. **No hacer clic y verificar el pedido por un canal oficial** ✅
- C. Reenviarlo a todos tus contactos

*Explicación:* Un correo que pide datos con urgencia suele buscar que actúes sin pensar. Conviene no hacer clic y confirmar por un canal oficial, como el sitio o el teléfono de la empresa. Reenviarlo multiplica el riesgo.

#### Nivel avanzado

**60. ¿Qué es un ataque Man-in-the-Middle (MitM)?**

- A. Una computadora se apaga automáticamente
- B. **Un atacante intercepta o altera la comunicación entre dos partes** ✅
- C. Un usuario pierde su contraseña por olvidarla

*Explicación:* En un ataque Man-in-the-Middle, el atacante se coloca entre la víctima y el destino y puede leer o modificar lo que se envían. Suele apoyarse en redes WiFi falsas o en configuraciones inseguras. No es un olvido de contraseña ni un apagón.

**61. ¿Qué caracteriza a una vulnerabilidad Zero-Day?**

- A. **Es una falla de seguridad desconocida o que todavía no tiene un parche disponible** ✅
- B. Es un error que aparece después de 24 horas
- C. Es una contraseña que vence diariamente

*Explicación:* Una vulnerabilidad Zero-Day es una falla que todavía no fue corregida por el fabricante y que puede ser aprovechada. El nombre alude a que no hubo tiempo de preparar una defensa. No es un error que aparece a las 24 horas ni una clave que vence.

**62. ¿Qué propiedad de la seguridad informática garantiza que los datos no sean modificados sin autorización?**

- A. Disponibilidad
- B. **Integridad** ✅
- C. Velocidad

*Explicación:* La integridad garantiza que los datos no se modifiquen sin autorización. La confidencialidad evita que los lean y la disponibilidad asegura que estén accesibles. La velocidad no es una propiedad de seguridad.

**63. ¿Qué es el ransomware?**

- A. **Un malware que cifra datos y pide un rescate** ✅
- B. Un programa que mejora el rendimiento del equipo
- C. Un tipo de copia de seguridad automática

*Explicación:* El ransomware cifra los archivos de la víctima y pide un pago para devolverlos. Es un malware con fines económicos. No mejora el rendimiento ni es una copia de seguridad.

**64. ¿Qué es la ingeniería social?**

- A. **Manipular personas para que revelen información o realicen acciones** ✅
- B. Instalar un antivirus en varios equipos
- C. Cambiar el nombre de usuario del sistema

*Explicación:* La ingeniería social engaña a las personas con confianza, miedo o urgencia para que entreguen datos o hagan algo riesgoso. Ataca al factor humano, no a un componente técnico. No es instalar un antivirus ni cambiar un nombre de usuario.

## Estación 5: Sistemas Operativos

*Funciones del sistema operativo y sistemas operativos móviles.*

### Tema: Sistema Operativo

El sistema operativo administra el hardware y permite ejecutar los programas. Su núcleo, el kernel, coordina la memoria, el procesador y los dispositivos. Los procesos y los hilos son parte de esa administración.

#### Nivel inicial

**65. ¿Qué es un sistema operativo?**

- A. **El software que administra la computadora** ✅
- B. Un cable de alimentación
- C. Una aplicación para dibujar

*Explicación:* Un sistema operativo es el software principal que administra el hardware y permite ejecutar los programas. Windows, Linux y Android son ejemplos. Sin él, el equipo no sabría cómo usar sus componentes.

**66. ¿Cuál de estos es un sistema operativo?**

- A. Microsoft Word
- B. **Windows** ✅
- C. Google Chrome

*Explicación:* Windows es un sistema operativo: administra el equipo y sirve de base para los demás programas. Microsoft Word es un procesador de textos y Google Chrome es un navegador. Cada uno se apoya en el sistema operativo.

**67. ¿Para qué sirve un sistema operativo?**

- A. **Administrar recursos y permitir ejecutar programas** ✅
- B. Solo para cambiar el color del monitor
- C. Solo para escribir documentos

*Explicación:* El sistema operativo reparte el procesador, la memoria y el almacenamiento entre los programas. También controla los permisos y la comunicación con los dispositivos. No se limita al color del monitor ni a escribir documentos.

#### Nivel intermedio

**68. ¿Qué es un proceso?**

- A. Un archivo guardado en el disco
- B. **Un programa que se está ejecutando** ✅
- C. Un componente físico del procesador

*Explicación:* Un proceso es un programa que el sistema operativo cargó en memoria y está ejecutando. El archivo guardado en el disco solo se convierte en proceso cuando se inicia. No es una pieza física del procesador.

**69. ¿Qué hace el sistema de archivos?**

- A. Aumenta la memoria RAM
- B. Conecta el equipo a Internet
- C. **Organiza y controla el acceso a archivos y carpetas** ✅

*Explicación:* El sistema de archivos organiza los datos en carpetas y archivos y registra dónde está cada cosa en el disco. También aplica permisos y controla el acceso. No aumenta la RAM ni conecta a Internet.

**70. ¿Para qué sirven los permisos de usuario?**

- A. Para cambiar el color de la pantalla
- B. Para medir la velocidad de la red
- C. **Para controlar quién puede leer, modificar o ejecutar archivos** ✅

*Explicación:* Los permisos indican qué puede hacer cada usuario con cada archivo: leerlo, modificarlo o ejecutarlo. Así se protege la información de un equipo compartido. No cambian el color de la pantalla ni miden la red.

**71. ¿Por qué conviene instalar las actualizaciones del sistema?**

- A. **Porque corrigen errores y mejoran la seguridad** ✅
- B. Porque borran todos los archivos
- C. Porque aumentan el tamaño del disco

*Explicación:* Las actualizaciones corrigen fallas y cierran problemas de seguridad que se van descubriendo. También pueden mejorar el rendimiento. No borran los archivos del equipo ni agrandan el disco.

#### Nivel avanzado

**72. ¿Qué función cumple el kernel de un sistema operativo?**

- A. **Gestionar la comunicación entre el hardware y los procesos** ✅
- B. Administrar exclusivamente los archivos de imágenes
- C. Controlar únicamente el navegador web

*Explicación:* El kernel es el núcleo del sistema operativo y tiene permisos especiales para administrar el hardware. Coordina la memoria, el procesador y los dispositivos, y atiende a los procesos. No se limita a imágenes ni al navegador.

**73. ¿Qué es un proceso zombie en Linux?**

- A. Un proceso que utiliza toda la memoria RAM
- B. **Un proceso finalizado cuya entrada todavía permanece en la tabla de procesos** ✅
- C. Un proceso que no tiene conexión a Internet

*Explicación:* Un proceso zombie ya terminó, pero su entrada sigue en la tabla de procesos hasta que el proceso padre lee su estado. No consume CPU ni memoria de trabajo. No es un proceso que usa toda la RAM ni uno sin Internet.

**74. ¿Qué algoritmo de planificación asigna un intervalo de tiempo a cada proceso?**

- A. **Round Robin** ✅
- B. First Come, First Served
- C. Shortest Job First

*Explicación:* Round Robin asigna a cada proceso un intervalo de tiempo y luego pasa al siguiente, en turnos. Así todos reciben atención y el sistema se siente fluido. First Come, First Served y Shortest Job First usan otros criterios.

**75. ¿Qué ocurre cuando se produce un Deadlock o interbloqueo?**

- A. El sistema operativo elimina todos los programas
- B. **Dos o más procesos quedan esperando indefinidamente recursos que están retenidos entre sí** ✅
- C. La computadora aumenta automáticamente la velocidad del procesador

*Explicación:* En un interbloqueo, cada proceso tiene un recurso y espera otro que tiene el anterior, y ninguno puede avanzar. El sistema queda trabado hasta que se libere la situación. No elimina programas ni acelera el procesador.

**76. ¿Qué diferencia hay entre un proceso y un hilo?**

- A. **El proceso tiene su propio espacio de memoria, mientras que los hilos comparten el del proceso** ✅
- B. Los hilos tienen su propio espacio de memoria y el proceso no
- C. No existe ninguna diferencia entre ambos

*Explicación:* Un proceso tiene su propio espacio de memoria y sus recursos. Los hilos son tareas dentro de un proceso y comparten esa memoria, por eso la comunicación entre ellos es más simple. No son lo mismo.

### Tema: Dispositivos Móviles

Los teléfonos y las tabletas usan sistemas operativos móviles como Android e iOS. Cada aplicación pide permisos para acceder a funciones y datos. Instalar solo desde la tienda oficial reduce riesgos.

#### Nivel inicial

**77. ¿Cuál de estos es un sistema operativo para celulares?**

- A. **Android** ✅
- B. PowerPoint
- C. Excel

*Explicación:* Android es un sistema operativo móvil, pensado para teléfonos y tabletas. PowerPoint y Excel son aplicaciones de oficina que funcionan sobre un sistema operativo. iOS es otro sistema móvil, de otra empresa.

#### Nivel intermedio

**78. ¿Qué son los permisos de una aplicación móvil?**

- A. Los datos del plan de Internet
- B. **Autorizaciones para acceder a cámara, ubicación, contactos y otros datos** ✅
- C. Las contraseñas del equipo

*Explicación:* Cuando una aplicación móvil pide permisos, está solicitando acceso a funciones del teléfono o a datos personales. Conviene revisar qué pide y darle solo lo necesario. No son las contraseñas del equipo ni el plan de datos.

**79. ¿Cuál es la diferencia principal entre Android e iOS?**

- A. Uno es un navegador y el otro un procesador
- B. Android es un hardware y iOS un cable
- C. **Son dos sistemas operativos móviles de empresas distintas** ✅

*Explicación:* Android es el sistema móvil de Google y iOS el de Apple. Cada uno tiene su tienda, sus actualizaciones y su forma de manejar permisos. Ninguno es un navegador ni un procesador.

#### Nivel avanzado

**80. ¿Por qué es riesgoso instalar aplicaciones fuera de la tienda oficial?**

- A. **Pueden contener malware y no estar verificadas por la tienda oficial** ✅
- B. Siempre consumen menos batería que las de la tienda oficial
- C. No se pueden actualizar nunca

*Explicación:* Las aplicaciones que se instalan fuera de la tienda oficial no pasan por la revisión de la empresa que fabrica el sistema. Por eso pueden incluir malware o pedir permisos peligrosos. No ahorran batería por ser externas ni dejan de actualizarse.

## Anexo: cobertura

Preguntas activas por estación, tema y nivel. Cada nivel necesita al menos una pregunta por tema activo y cuatro por estación.

| Estación | Tema | Inicial | Intermedio | Avanzado | Total |
| --- | --- | --: | --: | --: | --: |
| Redes | IP | 1 | 2 | 1 | 4 |
| Redes | Router | 1 | 1 | 3 | 5 |
| Redes | Redes de computadoras | 1 | 2 | 1 | 4 |
| Redes | WiFi | 1 | 1 | 1 | 3 |
| Hardware | Procesador | 1 | 3 | 2 | 6 |
| Hardware | Dispositivos de entrada/salida | 2 | 2 | 2 | 6 |
| Hardware | Memoria RAM | 1 | 1 | 2 | 4 |
| Internet | Navegadores Web | 2 | 2 | 1 | 5 |
| Internet | URL | 1 | 2 | 1 | 4 |
| Internet | Conectividad | 1 | 2 | 4 | 7 |
| Ciberseguridad | Contraseña | 2 | 3 | 1 | 6 |
| Ciberseguridad | Phishing | 2 | 3 | 5 | 10 |
| Sistemas Operativos | Sistema Operativo | 3 | 4 | 5 | 12 |
| Sistemas Operativos | Dispositivos Móviles | 1 | 2 | 1 | 4 |

**Totales:** 20 `inicial`, 30 `intermedio` y 30 `avanzado`; 80 preguntas en 14 temas de 5 estaciones.

---

Este documento se genera desde la base y no se edita a mano. Para actualizarlo después de un cambio en `/admin`, volver a generarlo y regenerar los PDFs con `./scripts/generar-pdfs.sh`.
