# Banco de preguntas — niveles intermedio y avanzado

Banco para revisión docente de las **60 preguntas** que cargan los seeds
`bd/seeds/002_contenido_intermedio.sql` y
`bd/seeds/003_contenido_avanzado.sql`. Cada pregunta tiene tres opciones,
una sola correcta y dos pistas (fácil y difícil) que se leen en papel.

Las pistas también están reunidas en `docs/pistas-del-juego.md`, junto con
las del nivel inicial y un anexo de reserva. La aplicación **no muestra**
ninguna pista: solo registra la cantidad de ayudas usadas.

> Los enunciados se adaptaron de `docs/elaboradoChicos/` y se completaron
> los temas que faltaban con redacción propia. No se agregaron temas nuevos:
> se usan los 14 temas existentes para no romper la cobertura de `inicial`.

## Nivel intermedio

### Estación 1: Redes

**1. ¿Qué dirección IPv4 es una dirección de loopback?**

- **Tema:** IP
- A. 127.0.0.1 ✅
- B. 169.254.1.1
- C. 192.168.1.1
- 🟢 **Fácil:** Es una dirección que permite que una computadora se comunique consigo misma.
- 🔴 **Difícil:** Pertenece a un rango reservado para pruebas internas, cuyo primer número es 127.

**2. ¿Cuál es la función principal de una máscara de subred?**

- **Tema:** IP
- A. Identificar el fabricante del equipo
- B. Diferenciar la parte de red y la parte de host de una dirección IP ✅
- C. Aumentar la velocidad de la conexión
- 🟢 **Fácil:** Se utiliza junto con la dirección IP.
- 🔴 **Difícil:** Permite determinar qué bits corresponden a la red y cuáles a los dispositivos (hosts).

**3. ¿Qué protocolo asigna direcciones IP automáticamente a los dispositivos de una red?**

- **Tema:** Router
- A. DNS
- B. DHCP ✅
- C. FTP
- 🟢 **Fácil:** Ayuda a que los dispositivos obtengan una dirección IP sin configurarla manualmente.
- 🔴 **Difícil:** Es un protocolo que asigna automáticamente parámetros de configuración de red.

**4. ¿Cuál es la función principal de un switch en una red LAN?**

- **Tema:** Redes de computadoras
- A. Conectar la red local a Internet obligatoriamente
- B. Conectar dispositivos dentro de una red local y enviar los datos al dispositivo correspondiente ✅
- C. Convertir señales digitales en sonido
- 🟢 **Fácil:** Permite conectar varias computadoras dentro de una red local.
- 🔴 **Difícil:** Utiliza direcciones MAC para enviar las tramas al puerto correspondiente.

**5. ¿Qué función cumple un punto de acceso inalámbrico (Access Point)?**

- **Tema:** WiFi
- A. Almacenar los archivos de los usuarios
- B. Conectar dispositivos inalámbricos a una red cableada ✅
- C. Reemplazar la memoria RAM del equipo
- 🟢 **Fácil:** Permite que los celulares y las computadoras se conecten a una red sin cables.
- 🔴 **Difícil:** Actúa como puente entre los dispositivos inalámbricos y la red cableada.

**6. ¿Qué protocolo traduce nombres de dominio como ejemplo.com a direcciones IP?**

- **Tema:** Redes de computadoras
- A. DNS ✅
- B. DHCP
- C. ARP
- 🟢 **Fácil:** Es como una agenda telefónica de Internet.
- 🔴 **Difícil:** Permite localizar la dirección numérica asociada a un nombre de dominio.

### Estación 2: Hardware

**1. ¿Qué función cumple la tecnología SMART en las unidades de almacenamiento?**

- **Tema:** Dispositivos de entrada/salida
- A. Controlar las conexiones WiFi
- B. Supervisar indicadores de estado y anticipar posibles fallas ✅
- C. Cifrar automáticamente todos los archivos
- 🟢 **Fácil:** Está relacionado con la salud del disco.
- 🔴 **Difícil:** Analiza datos internos de funcionamiento para anticipar posibles problemas.

**2. ¿Qué puede indicar una pantalla azul recurrente en Windows?**

- **Tema:** Procesador
- A. Que el monitor está conectado correctamente
- B. Que el router está apagado
- C. Un error crítico del sistema o del hardware ✅
- 🟢 **Fácil:** Puede ser una señal de que algo no funciona bien en la computadora.
- 🔴 **Difícil:** Suele aparecer cuando el sistema operativo encuentra un problema grave que le impide continuar normalmente.

**3. ¿Cuál es la finalidad de realizar una copia de seguridad?**

- **Tema:** Dispositivos de entrada/salida
- A. Recuperar información ante pérdida o daño ✅
- B. Eliminar la necesidad de antivirus
- C. Aumentar la velocidad de Internet
- 🟢 **Fácil:** Sirve para proteger tus archivos.
- 🔴 **Difícil:** Permite restaurar información si los datos originales dejan de estar disponibles.

**4. ¿Qué es la pasta térmica?**

- **Tema:** Procesador
- A. Un aislante que impide el paso del calor
- B. Un adhesivo para fijar la memoria RAM
- C. Un material que mejora la transferencia de calor entre superficies ✅
- 🟢 **Fácil:** Se utiliza entre el procesador y el sistema de refrigeración.
- 🔴 **Difícil:** Ayuda a reducir los espacios microscópicos entre dos superficies para facilitar el intercambio de calor.

**5. ¿Qué tipo de mantenimiento busca evitar fallas futuras?**

- **Tema:** Procesador
- A. Correctivo
- B. Preventivo ✅
- C. Destructivo
- 🟢 **Fácil:** Se realiza antes de que aparezcan problemas en la computadora.
- 🔴 **Difícil:** Consiste en revisiones y tareas periódicas para reducir la posibilidad de fallas futuras.

**6. ¿Qué significa que la memoria RAM sea volátil?**

- **Tema:** Memoria RAM
- A. Que guarda los datos para siempre
- B. Que pierde su contenido al apagarse el equipo ✅
- C. Que solo funciona con Internet
- 🟢 **Fácil:** Pensá en lo que pasa con los datos cuando apagás el equipo.
- 🔴 **Difícil:** Es una memoria temporal: su contenido se pierde al cortar la energía.

### Estación 3: Internet

**1. ¿Para qué sirven las cookies de un navegador?**

- **Tema:** Navegadores Web
- A. Para acelerar el procesador
- B. Para que el sitio recuerde datos de la visita, como la sesión o las preferencias ✅
- C. Para impedir que el sitio use HTTPS
- 🟢 **Fácil:** Son pequeños datos que el sitio guarda en tu navegador.
- 🔴 **Difícil:** Permiten recordar la sesión, el idioma o las preferencias entre visitas.

**2. ¿Qué hace el modo incógnito de un navegador?**

- **Tema:** Navegadores Web
- A. Cifra todos los archivos del equipo
- B. Impide que el proveedor de Internet vea la navegación
- C. No guarda el historial ni las cookies de esa sesión en el dispositivo ✅
- 🟢 **Fácil:** Es una ventana que no deja rastro en el historial del equipo.
- 🔴 **Difícil:** No guarda historial ni cookies de esa sesión, aunque no te vuelve invisible en Internet.

**3. En la dirección https://www.escuela.edu.ar/aula/notas, ¿qué parte indica el protocolo?**

- **Tema:** URL
- A. https ✅
- B. www.escuela.edu.ar
- C. /aula/notas
- 🟢 **Fácil:** Es la primera parte de la dirección, antes de los dos puntos.
- 🔴 **Difícil:** Indica cómo se comunican el navegador y el servidor; en este caso, mediante HTTPS.

**4. ¿Qué indica el dominio en una dirección web?**

- **Tema:** URL
- A. La contraseña de la red WiFi
- B. El nombre que identifica al sitio o servidor ✅
- C. El tipo de procesador del servidor
- 🟢 **Fácil:** Es la parte que está entre los dos puntos y la primera barra.
- 🔴 **Difícil:** Es el nombre registrado que identifica al sitio y se traduce a una dirección IP.

**5. ¿Qué es el ancho de banda?**

- **Tema:** Conectividad
- A. El tiempo que tarda un dato en llegar
- B. La cantidad de dispositivos conectados a la red
- C. La cantidad de datos que se pueden transmitir por segundo ✅
- 🟢 **Fácil:** Se suele medir en megabits por segundo.
- 🔴 **Difícil:** Indica cuánta información puede viajar por la conexión en un tiempo determinado.

**6. ¿Qué significa tener una latencia alta?**

- **Tema:** Conectividad
- A. Que los datos llegan más rápido
- B. Que los datos tardan más en llegar a destino ✅
- C. Que se reduce el tamaño de los archivos
- 🟢 **Fácil:** Está relacionada con el tiempo que tardan los datos en llegar.
- 🔴 **Difícil:** Se mide en milisegundos y representa el retraso de la comunicación.

### Estación 4: Ciberseguridad

**1. ¿Qué es la autenticación de dos factores (2FA)?**

- **Tema:** Contraseña
- A. Usar dos contraseñas iguales en dos sitios
- B. Un segundo paso de verificación además de la contraseña ✅
- C. Cambiar la contraseña dos veces por año
- 🟢 **Fácil:** Además de la contraseña, te pide un código.
- 🔴 **Difícil:** Combina algo que sabés con algo que tenés, como un código del celular.

**2. ¿Para qué sirve un gestor de contraseñas?**

- **Tema:** Contraseña
- A. Para compartir las contraseñas con todos
- B. Para eliminar la necesidad de usar contraseñas
- C. Para guardar y generar contraseñas seguras sin memorizarlas todas ✅
- 🟢 **Fácil:** Es un programa que guarda tus claves bajo una clave maestra.
- 🔴 **Difícil:** Genera y completa contraseñas únicas sin que tengas que memorizarlas todas.

**3. ¿Por qué no conviene usar la misma contraseña en varios sitios?**

- **Tema:** Contraseña
- A. Porque si filtran una, pueden acceder a las demás cuentas ✅
- B. Porque ocupa más espacio en el disco
- C. Porque el navegador la borra automáticamente
- 🟢 **Fácil:** Si una cuenta se filtra, las demás quedan expuestas.
- 🔴 **Difícil:** Un atacante puede probar la misma combinación en otros servicios.

**4. ¿Qué es el smishing?**

- **Tema:** Phishing
- A. Un ataque que solo afecta impresoras
- B. Un engaño por SMS o aplicación de mensajería ✅
- C. Un tipo de contraseña segura
- 🟢 **Fácil:** El nombre viene de SMS.
- 🔴 **Difícil:** Es una variante de phishing que llega por mensaje de texto o mensajería.

**5. ¿Qué es el vishing?**

- **Tema:** Phishing
- A. Un virus que borra archivos
- B. Una actualización del sistema operativo
- C. Un engaño realizado por llamada telefónica ✅
- 🟢 **Fácil:** El nombre viene de voz o llamada.
- 🔴 **Difícil:** Es una variante de phishing en la que el engaño ocurre por teléfono.

**6. Recibís un correo urgente con un enlace que pide tus datos. ¿Qué conviene hacer?**

- **Tema:** Phishing
- A. Hacer clic y completar los datos rápido
- B. No hacer clic y verificar el pedido por un canal oficial ✅
- C. Reenviarlo a todos tus contactos
- 🟢 **Fácil:** Desconfiá de los mensajes que apuran y piden datos.
- 🔴 **Difícil:** Verificá por un canal oficial antes de hacer clic o responder.

### Estación 5: Sistemas Operativos

**1. ¿Qué es un proceso?**

- **Tema:** Sistema Operativo
- A. Un archivo guardado en el disco
- B. Un programa que se está ejecutando ✅
- C. Un componente físico del procesador
- 🟢 **Fácil:** Pensá en un programa que ya está en marcha.
- 🔴 **Difícil:** Es una instancia de un programa en ejecución, con su propio estado y recursos.

**2. ¿Qué hace el sistema de archivos?**

- **Tema:** Sistema Operativo
- A. Aumenta la memoria RAM
- B. Conecta el equipo a Internet
- C. Organiza y controla el acceso a archivos y carpetas ✅
- 🟢 **Fácil:** Es lo que te permite ver carpetas y archivos.
- 🔴 **Difícil:** Organiza los datos en el disco y controla cómo se accede a ellos.

**3. ¿Para qué sirven los permisos de usuario?**

- **Tema:** Sistema Operativo
- A. Para cambiar el color de la pantalla
- B. Para medir la velocidad de la red
- C. Para controlar quién puede leer, modificar o ejecutar archivos ✅
- 🟢 **Fácil:** Definen qué puede hacer cada usuario con un archivo.
- 🔴 **Difícil:** Distinguen lectura, escritura y ejecución, y también quién es el propietario.

**4. ¿Por qué conviene instalar las actualizaciones del sistema?**

- **Tema:** Sistema Operativo
- A. Porque corrigen errores y mejoran la seguridad ✅
- B. Porque borran todos los archivos
- C. Porque aumentan el tamaño del disco
- 🟢 **Fácil:** Conviene instalarlas cuando el sistema avisa.
- 🔴 **Difícil:** Corrigen fallas y vulnerabilidades que podrían ser aprovechadas.

**5. ¿Qué son los permisos de una aplicación móvil?**

- **Tema:** Dispositivos Móviles
- A. Los datos del plan de Internet
- B. Autorizaciones para acceder a cámara, ubicación, contactos y otros datos ✅
- C. Las contraseñas del equipo
- 🟢 **Fácil:** Son los avisos que aparecen cuando una app quiere usar la cámara o la ubicación.
- 🔴 **Difícil:** Son autorizaciones granulares que podés revisar y quitar desde la configuración.

**6. ¿Cuál es la diferencia principal entre Android e iOS?**

- **Tema:** Dispositivos Móviles
- A. Uno es un navegador y el otro un procesador
- B. Android es un hardware y iOS un cable
- C. Son dos sistemas operativos móviles de empresas distintas ✅
- 🟢 **Fácil:** Son los dos sistemas de celulares más conocidos.
- 🔴 **Difícil:** Android lo desarrolla Google y iOS Apple; cada uno tiene su propia tienda y reglas.


## Nivel avanzado

### Estación 1: Redes

**1. ¿Qué protocolo permite asignar automáticamente direcciones IP a los dispositivos de una red?**

- **Tema:** Router
- A. DNS
- B. DHCP ✅
- C. FTP
- 🟢 **Fácil:** Sus siglas corresponden a cuatro palabras en inglés y permite que los dispositivos reciban una dirección IP sin configurarla manualmente.
- 🔴 **Difícil:** Es un protocolo que configura automáticamente los parámetros de conexión de los dispositivos.

**2. ¿Qué dispositivo trabaja principalmente en la capa 3 del modelo OSI?**

- **Tema:** Router
- A. Hub
- B. Switch tradicional
- C. Router ✅
- 🟢 **Fácil:** Es el aparato que generalmente permite conectar tu casa con Internet y distribuir la conexión.
- 🔴 **Difícil:** Trabaja en la capa de red y se encarga de dirigir paquetes entre diferentes redes.

**3. ¿Qué función cumple el protocolo ARP en una red IPv4?**

- **Tema:** IP
- A. Traducir direcciones IP a direcciones MAC ✅
- B. Asignar contraseñas a los dispositivos
- C. Cifrar la información transmitida
- 🟢 **Fácil:** Ayuda a encontrar la dirección física de un dispositivo a partir de su dirección IP.
- 🔴 **Difícil:** Relaciona dos tipos de direcciones utilizadas para identificar dispositivos dentro de una red.

**4. ¿Cuál es la diferencia principal entre TCP y UDP?**

- **Tema:** Redes de computadoras
- A. UDP necesita una conexión previa y TCP no
- B. TCP garantiza una comunicación confiable, mientras que UDP no garantiza la entrega de los datos ✅
- C. Ambos protocolos funcionan exactamente igual
- 🟢 **Fácil:** Uno busca garantizar que los datos lleguen correctamente y el otro prioriza la rapidez sin garantizar su entrega.
- 🔴 **Difícil:** Ambos permiten transmitir información, pero se diferencian en cómo gestionan la conexión y la entrega de los datos.

**5. ¿Qué hace NAT en una red?**

- **Tema:** Router
- A. Asigna nombres de dominio a los dispositivos
- B. Traduce direcciones privadas a una pública para salir a Internet ✅
- C. Cifra el tráfico de la red WiFi
- 🟢 **Fácil:** Es lo que permite que varios equipos de una casa salgan a Internet con una sola dirección pública.
- 🔴 **Difícil:** Traduce direcciones privadas a una dirección pública y mantiene el registro de las conexiones.

**6. ¿Qué mejora WPA3 respecto de WPA2?**

- **Tema:** WiFi
- A. Mayor seguridad y protección contra ataques de fuerza bruta a la clave WiFi ✅
- B. Menor velocidad de conexión
- C. Elimina la necesidad de usar contraseña
- 🟢 **Fácil:** Es la versión más reciente del protocolo de seguridad WiFi.
- 🔴 **Difícil:** Mejora la protección de la clave y dificulta los ataques de fuerza bruta contra la red inalámbrica.

### Estación 2: Hardware

**1. ¿Qué componente del procesador almacena datos e instrucciones de acceso frecuente para acelerar su funcionamiento?**

- **Tema:** Procesador
- A. Memoria caché L1 ✅
- B. Disco rígido HDD
- C. Fuente de alimentación
- 🟢 **Fácil:** Es una memoria muy rápida que está dentro del procesador y tiene diferentes niveles, como L1, L2 y L3.
- 🔴 **Difícil:** Es una memoria de alta velocidad que reduce el tiempo que necesita el procesador para acceder a información frecuente.

**2. ¿Qué diferencia principal existe entre la memoria SRAM y la DRAM?**

- **Tema:** Memoria RAM
- A. La SRAM necesita refresco constante y la DRAM no
- B. La SRAM no necesita refresco periódico, mientras que la DRAM sí ✅
- C. Ambas funcionan exactamente de la misma manera
- 🟢 **Fácil:** Una necesita refrescar sus datos constantemente y la otra puede mantenerlos sin ese proceso periódico.
- 🔴 **Difícil:** Ambas son memorias volátiles, pero utilizan mecanismos diferentes para conservar la información.

**3. ¿Qué tecnología utilizan los SSD para distribuir el desgaste entre sus celdas de memoria?**

- **Tema:** Dispositivos de entrada/salida
- A. Hyper-Threading
- B. Wear Leveling ✅
- C. Overclocking
- 🟢 **Fácil:** Su nombre en inglés significa «nivelación del desgaste» y evita que siempre se utilicen las mismas celdas.
- 🔴 **Difícil:** Es una técnica que distribuye las operaciones de escritura para prolongar la vida útil del almacenamiento.

**4. ¿Qué característica de PCI Express permite aumentar la velocidad de transferencia de datos?**

- **Tema:** Procesador
- A. La incorporación de memoria RAM externa
- B. La utilización de cables HDMI
- C. La utilización de múltiples carriles de comunicación (x1, x4, x8, x16) ✅
- 🟢 **Fácil:** Se identifica con números como x1, x4, x8 y x16. Cuantos más canales se utilizan, mayor ancho de banda puede haber.
- 🔴 **Difícil:** Esta tecnología permite utilizar varios canales de comunicación en paralelo entre los componentes.

**5. ¿Qué diferencia principal hay entre un HDD y un SSD?**

- **Tema:** Dispositivos de entrada/salida
- A. El HDD usa discos magnéticos y el SSD usa memoria flash ✅
- B. El HDD usa memoria flash y el SSD usa discos magnéticos
- C. Ambos usan únicamente memoria RAM
- 🟢 **Fácil:** Uno tiene partes mecánicas que giran y el otro no.
- 🔴 **Difícil:** El HDD usa discos magnéticos y el SSD usa celdas de memoria flash.

**6. ¿Qué es la memoria virtual?**

- **Tema:** Memoria RAM
- A. Un espacio en disco que el sistema usa como extensión de la RAM ✅
- B. Una memoria que reemplaza al procesador
- C. Un tipo de conexión inalámbrica
- 🟢 **Fácil:** Aparece cuando la RAM no alcanza y el sistema usa el disco.
- 🔴 **Difícil:** Es un espacio de almacenamiento que el sistema operativo usa como extensión de la memoria principal.

### Estación 3: Internet

**1. ¿Qué función cumple el sistema DNS?**

- **Tema:** Conectividad
- A. Traducir nombres de dominio en direcciones IP ✅
- B. Proteger físicamente los servidores
- C. Aumentar la memoria RAM de una computadora
- 🟢 **Fácil:** Gracias a él podés escribir el nombre de una página web sin tener que recordar su dirección numérica.
- 🔴 **Difícil:** Es un sistema que relaciona nombres fáciles de recordar con direcciones utilizadas por los dispositivos para localizar servidores.

**2. ¿Qué significa el código de estado HTTP 403?**

- **Tema:** Conectividad
- A. El sitio web no existe
- B. El servidor entendió la solicitud, pero deniega el acceso ✅
- C. La página fue encontrada correctamente
- 🟢 **Fácil:** Significa que el acceso está prohibido, aunque el servidor haya recibido correctamente tu solicitud.
- 🔴 **Difícil:** Es una respuesta del servidor que indica que comprendió la solicitud, pero no permite acceder al recurso.

**3. ¿Qué diferencia principal existe entre HTTP y HTTPS?**

- **Tema:** Conectividad
- A. HTTP es más seguro porque no utiliza cifrado
- B. HTTPS utiliza cifrado mediante TLS para proteger la comunicación ✅
- C. HTTPS solamente funciona sin conexión a Internet
- 🟢 **Fácil:** Es el protocolo que aparece en las páginas web seguras y utiliza TLS para proteger los datos transmitidos.
- 🔴 **Difícil:** Uno de estos protocolos incorpora un mecanismo de cifrado para proteger la comunicación entre el navegador y el servidor.

**4. ¿Qué significa el código de estado HTTP 404?**

- **Tema:** Conectividad
- A. Error de autenticación del usuario
- B. Recurso o página no encontrada ✅
- C. Conexión cifrada correctamente
- 🟢 **Fácil:** Aparece cuando intentás entrar a una página que no se encuentra disponible en esa dirección.
- 🔴 **Difícil:** Es una respuesta del servidor que indica que no pudo encontrar el recurso solicitado.

**5. ¿Qué es la caché del navegador?**

- **Tema:** Navegadores Web
- A. Copias de recursos para cargar las páginas más rápido ✅
- B. Un programa que bloquea los virus
- C. El historial de contraseñas del equipo
- 🟢 **Fácil:** Es lo que permite que una página ya visitada cargue más rápido.
- 🔴 **Difícil:** Guarda copias de imágenes, estilos y scripts para no descargarlos de nuevo.

**6. En una dirección como https://tienda.com/productos?categoria=ofertas, ¿qué indica la parte que comienza con el signo de interrogación?**

- **Tema:** URL
- A. El nombre del servidor
- B. El protocolo de cifrado
- C. Los parámetros o la consulta que se envía al servidor ✅
- 🟢 **Fácil:** Es la parte que sigue al signo de interrogación y suele tener pares clave=valor.
- 🔴 **Difícil:** Contiene parámetros que el servidor usa para filtrar o personalizar la respuesta.

### Estación 4: Ciberseguridad

**1. ¿Qué es un ataque de fuerza bruta?**

- **Tema:** Contraseña
- A. Un intento de descubrir contraseñas probando múltiples combinaciones ✅
- B. Un virus que solamente afecta a las impresoras
- C. Un error de conexión a Internet
- 🟢 **Fácil:** Consiste en intentar muchas contraseñas diferentes hasta encontrar la correcta.
- 🔴 **Difícil:** Es una técnica que intenta descubrir credenciales mediante la prueba sistemática de diferentes combinaciones.

**2. ¿Qué es un ataque Man-in-the-Middle (MitM)?**

- **Tema:** Phishing
- A. Una computadora se apaga automáticamente
- B. Un atacante intercepta o altera la comunicación entre dos partes ✅
- C. Un usuario pierde su contraseña por olvidarla
- 🟢 **Fácil:** Imaginá que alguien se mete en una conversación digital entre dos personas y puede observar o modificar lo que se envían.
- 🔴 **Difícil:** Es un ataque en el que un tercero se interpone en el intercambio de información entre dos partes.

**3. ¿Qué caracteriza a una vulnerabilidad Zero-Day?**

- **Tema:** Phishing
- A. Es una falla de seguridad desconocida o que todavía no tiene un parche disponible ✅
- B. Es un error que aparece después de 24 horas
- C. Es una contraseña que vence diariamente
- 🟢 **Fácil:** Es una vulnerabilidad que puede ser aprovechada antes de que los desarrolladores tengan tiempo de corregirla.
- 🔴 **Difícil:** Es una falla de seguridad para la cual todavía no existe una solución o parche disponible.

**4. ¿Qué propiedad de la seguridad informática garantiza que los datos no sean modificados sin autorización?**

- **Tema:** Phishing
- A. Disponibilidad
- B. Integridad ✅
- C. Velocidad
- 🟢 **Fácil:** Si alguien modifica un archivo sin permiso, está afectando esta propiedad de seguridad.
- 🔴 **Difícil:** Es uno de los tres principios fundamentales de la seguridad informática y protege la exactitud de la información.

**5. ¿Qué es el ransomware?**

- **Tema:** Phishing
- A. Un malware que cifra datos y pide un rescate ✅
- B. Un programa que mejora el rendimiento del equipo
- C. Un tipo de copia de seguridad automática
- 🟢 **Fácil:** Bloquea tus archivos y te pide dinero para liberarlos.
- 🔴 **Difícil:** Es un malware que cifra los datos y exige un rescate para recuperarlos.

**6. ¿Qué es la ingeniería social?**

- **Tema:** Phishing
- A. Manipular personas para que revelen información o realicen acciones ✅
- B. Instalar un antivirus en varios equipos
- C. Cambiar el nombre de usuario del sistema
- 🟢 **Fácil:** Aprovecha la confianza de las personas, no solo fallas técnicas.
- 🔴 **Difícil:** Manipula a una persona para que revele información o realice una acción riesgosa.

### Estación 5: Sistemas Operativos

**1. ¿Qué función cumple el kernel de un sistema operativo?**

- **Tema:** Sistema Operativo
- A. Gestionar la comunicación entre el hardware y los procesos ✅
- B. Administrar exclusivamente los archivos de imágenes
- C. Controlar únicamente el navegador web
- 🟢 **Fácil:** Es la parte central del sistema operativo que permite que el software se comunique con los componentes físicos de la computadora.
- 🔴 **Difícil:** Es el núcleo que administra los recursos del hardware y coordina la ejecución de los procesos.

**2. ¿Qué es un proceso zombie en Linux?**

- **Tema:** Sistema Operativo
- A. Un proceso que utiliza toda la memoria RAM
- B. Un proceso finalizado cuya entrada todavía permanece en la tabla de procesos ✅
- C. Un proceso que no tiene conexión a Internet
- 🟢 **Fácil:** Es un programa que ya terminó de funcionar, pero todavía aparece registrado en el sistema.
- 🔴 **Difícil:** Es un proceso que ya finalizó, pero cuya información todavía permanece registrada en la tabla de procesos.

**3. ¿Qué algoritmo de planificación asigna un intervalo de tiempo a cada proceso?**

- **Tema:** Sistema Operativo
- A. Round Robin ✅
- B. First Come, First Served
- C. Shortest Job First
- 🟢 **Fácil:** Su nombre en inglés significa «círculo rotativo» y permite que los procesos utilicen la CPU por turnos.
- 🔴 **Difícil:** Es un algoritmo de planificación que distribuye el tiempo del procesador mediante turnos de duración determinada.

**4. ¿Qué ocurre cuando se produce un Deadlock o interbloqueo?**

- **Tema:** Sistema Operativo
- A. El sistema operativo elimina todos los programas
- B. Dos o más procesos quedan esperando indefinidamente recursos que están retenidos entre sí ✅
- C. La computadora aumenta automáticamente la velocidad del procesador
- 🟢 **Fácil:** Imaginá dos procesos: cada uno tiene algo que el otro necesita y ninguno puede continuar hasta conseguirlo.
- 🔴 **Difícil:** Es una situación en la que varios procesos quedan bloqueados porque esperan recursos que están siendo retenidos entre ellos.

**5. ¿Qué diferencia hay entre un proceso y un hilo?**

- **Tema:** Sistema Operativo
- A. El proceso tiene su propio espacio de memoria, mientras que los hilos comparten el del proceso ✅
- B. Los hilos tienen su propio espacio de memoria y el proceso no
- C. No existe ninguna diferencia entre ambos
- 🟢 **Fácil:** Pensá en un programa con varias tareas que comparten datos.
- 🔴 **Difícil:** El proceso tiene su propio espacio de memoria, mientras que los hilos comparten el del proceso.

**6. ¿Por qué es riesgoso instalar aplicaciones fuera de la tienda oficial?**

- **Tema:** Dispositivos Móviles
- A. Pueden contener malware y no estar verificadas por la tienda oficial ✅
- B. Siempre consumen menos batería que las de la tienda oficial
- C. No se pueden actualizar nunca
- 🟢 **Fácil:** La tienda oficial revisa las apps antes de publicarlas.
- 🔴 **Difícil:** Una app instalada desde fuera de la tienda puede contener malware y no haber sido verificada.


## Anexo: preguntas de reserva

Preguntas del material que no se cargaron para no superar las 30 por
nivel. Sus pistas quedan en `docs/pistas-del-juego.md` por si se quieren
incorporar más adelante.

- **Intermedio · Redes:** ¿Cuántas direcciones IPv4 totales contiene una subred con prefijo /28?
  - 🟢 Fácil: No confundas la cantidad total con las direcciones disponibles para dispositivos.
  - 🔴 Difícil: IPv4 tiene 32 bits. Restá los bits del prefijo y calculá 2 elevado a la cantidad restante.
- **Intermedio · Redes:** ¿Qué puerto utiliza habitualmente SSH?
  - 🟢 Fácil: Es un número de puerto inferior a 30.
  - 🔴 Difícil: Es el puerto predeterminado para la administración remota segura mediante Secure Shell.
- **Intermedio · Redes:** ¿Qué diferencia existe entre un cable UTP y uno de fibra óptica?
  - 🟢 Fácil: Los dos sirven para transmitir información.
  - 🔴 Difícil: Uno utiliza impulsos eléctricos y el otro transmite información mediante pulsos luminosos.
- **Intermedio · Redes:** ¿Para qué sirve una dirección IP dentro de una red?
  - 🟢 Fácil: Es como el número de identificación de un dispositivo.
  - 🔴 Difícil: Es una dirección lógica que permite identificar y localizar un equipo dentro de una red.
- **Intermedio · Redes:** ¿Cuál es la principal ventaja de utilizar fibra óptica en una conexión de red?
  - 🟢 Fácil: Utiliza luz para transmitir información.
  - 🔴 Difícil: Permite transmitir datos a grandes velocidades y distancias, con poca pérdida de señal y sin interferencias electromagnéticas.
- **Intermedio · Redes:** ¿Qué herramienta se utiliza para colocar conectores RJ45 en un cable UTP?
  - 🟢 Fácil: Es una herramienta que se utiliza para trabajar con cables de red.
  - 🔴 Difícil: Permite fijar los conectores RJ45 a los extremos de los cables UTP.
- **Intermedio · Redes:** ¿Qué representa la dirección MAC de un dispositivo?
  - 🟢 Fácil: Es una identificación propia de la interfaz de red de un dispositivo.
  - 🔴 Difícil: Es una dirección de hardware que identifica una interfaz de red y está formada generalmente por 48 bits.
- **Avanzado · Internet:** ¿Qué función cumple un certificado TLS?
  - 🟢 Fácil: Aparece cuando la dirección empieza con https y el navegador muestra un candado.
  - 🔴 Difícil: Permite validar la identidad del servidor y establecer una conexión cifrada entre el navegador y el sitio.
