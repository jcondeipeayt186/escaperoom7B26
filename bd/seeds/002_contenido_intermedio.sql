-- ============================================================================
-- Escape Room 7°B 2026 - Contenido de nivel intermedio
-- ============================================================================
-- Requiere haber ejecutado bd/schema.sql y bd/seeds/001_contenido_inicial.sql.
--
-- Uso:
--   mysql -u <usuario> -p < bd/seeds/002_contenido_intermedio.sql
--
-- Es idempotente: ejecutarlo dos veces no duplica datos.
--   * Preguntas y respuestas usan ids fijos.
--     Al reejecutar se actualizan los textos, pero NO se cambia `activo`:
--     si el admin desactivó algo, sigue desactivado.
--   * Las descripciones no llevan punto y coma: el cargador de seeds de las
--     pruebas separa las sentencias con ese signo.
--   * No toca `configuracion` ni habilita el nivel.
--
-- Basado en docs/elaboradoChicos/ESCAPEROOM-intermedio.odt y completado con redacción propia.
-- ============================================================================

USE escape_room_7b2026;

SET NAMES utf8mb4;

START TRANSACTION;

-- ----------------------------------------------------------------------------
-- Preguntas (30 en total, 6 por estación)
-- ----------------------------------------------------------------------------
INSERT INTO pregunta (id, titulo, descripcion, explicacion, tema_id, dificultad, activo) VALUES
  (1001, '¿Qué dirección IPv4 es una dirección de loopback?', 'El loopback es una dirección reservada para que el equipo se hable a sí mismo y pruebe su configuración de red.', 'La dirección 127.0.0.1 se conoce como loopback y siempre apunta al propio equipo. Sirve para probar si la configuración de red funciona sin salir a la LAN. Las direcciones 192.168 y 169.254 pertenecen a otros rangos.', 1, 'intermedio', 1),
  (1002, '¿Cuál es la función principal de una máscara de subred?', 'Junto con la dirección IP se indica la máscara de subred, que define el tamaño de la red.', 'La máscara de subred indica cuántos bits de la dirección IP identifican la red y cuántos identifican al equipo. Con esa información, el equipo sabe si el destino está dentro de su red o fuera. No identifica al fabricante ni cambia la velocidad.', 1, 'intermedio', 1),
  (1003, '¿Qué protocolo asigna direcciones IP automáticamente a los dispositivos de una red?', 'Cuando un dispositivo se conecta a una red, puede recibir su configuración automáticamente en lugar de cargarla a mano.', 'DHCP es el protocolo que entrega automáticamente dirección IP, máscara y puerta de enlace a los dispositivos. Así no hay que configurar cada equipo a mano. DNS traduce nombres y FTP transfiere archivos.', 2, 'intermedio', 1),
  (1004, '¿Cuál es la función principal de un switch en una red LAN?', 'Dentro de una red local hay equipos que concentran las conexiones y deciden por dónde sale cada trama.', 'Un switch conecta varios equipos de una red local y envía cada trama al puerto del dispositivo correcto. Trabaja dentro de la LAN y no se ocupa de sacar el tráfico a Internet, tarea del router. Tampoco almacena los archivos de los usuarios.', 3, 'intermedio', 1),
  (1005, '¿Qué función cumple un punto de acceso inalámbrico (Access Point)?', 'Los dispositivos inalámbricos necesitan un equipo que reciba su señal y la conecte con el resto de la red.', 'Un punto de acceso recibe la señal de los dispositivos inalámbricos y los integra a la red cableada. Es habitual en escuelas y oficinas para ampliar la cobertura WiFi. No reemplaza la RAM ni guarda archivos.', 4, 'intermedio', 1),
  (1006, '¿Qué protocolo traduce nombres de dominio como ejemplo.com a direcciones IP?', 'Escribir un nombre es más fácil que recordar números y algún servicio tiene que hacer la traducción.', 'DNS es el servicio que traduce nombres como ejemplo.com a direcciones IP. Gracias a él no hace falta recordar números para entrar a un sitio. DHCP asigna direcciones y ARP las vincula con direcciones MAC.', 3, 'intermedio', 1),
  (1007, '¿Qué función cumple la tecnología SMART en las unidades de almacenamiento?', 'Los discos modernos registran datos internos sobre su estado y su salud a lo largo del tiempo.', 'SMART es un sistema de autodiagnóstico que registra datos internos del disco, como errores o temperatura. Con esa información se pueden detectar señales de falla antes de que el disco deje de funcionar. No controla el WiFi ni cifra archivos.', 6, 'intermedio', 1),
  (1008, '¿Qué puede indicar una pantalla azul recurrente en Windows?', 'Windows muestra una pantalla azul cuando no puede continuar funcionando por un problema serio.', 'La pantalla azul de Windows aparece cuando el sistema encuentra un error grave y no puede seguir funcionando. Suele estar relacionada con controladores, memoria o fallas de hardware. No indica que el monitor esté conectado ni que el router esté apagado.', 5, 'intermedio', 1),
  (1009, '¿Cuál es la finalidad de realizar una copia de seguridad?', 'Los datos pueden perderse por fallas, robos o errores. Una copia permite volver atrás.', 'Una copia de seguridad guarda una versión adicional de los datos para poder recuperarlos si algo falla. Sirve ante borrados accidentales, fallas del disco o robos. No reemplaza al antivirus ni acelera Internet.', 6, 'intermedio', 1),
  (1010, '¿Qué es la pasta térmica?', 'Entre el procesador y el disipador no deben quedar bolsas de aire: por eso se usa un compuesto especial.', 'La pasta térmica se coloca entre el procesador y el disipador para llenar las imperfecciones y mejorar el paso del calor. Sin ella quedarían bolsas de aire que calentarían de más. No es un aislante ni un adhesivo para la RAM.', 5, 'intermedio', 1),
  (1011, '¿Qué tipo de mantenimiento busca evitar fallas futuras?', 'El mantenimiento puede hacerse antes de que aparezca la falla, después, o para mejorar el rendimiento.', 'El mantenimiento preventivo se hace antes de que aparezca la falla, con limpieza, revisiones y actualizaciones. El correctivo se aplica cuando el problema ya ocurrió. Prevenir suele ser más barato y evita cortes.', 5, 'intermedio', 1),
  (1012, '¿Qué significa que la memoria RAM sea volátil?', 'La RAM es rápida y se usa como espacio de trabajo, pero no está pensada para conservar datos a largo plazo.', 'Decir que la RAM es volátil significa que necesita energía para conservar los datos. Al apagar o reiniciar el equipo, su contenido se borra. Por eso los archivos se guardan en el disco y no en la RAM.', 7, 'intermedio', 1),
  (1013, '¿Para qué sirven las cookies de un navegador?', 'Los sitios necesitan recordar quién sos y qué preferís entre una página y otra. Para eso usan pequeños archivos.', 'Las cookies son pequeños archivos que el sitio guarda en el navegador para recordar la sesión, el idioma o las preferencias. Sin ellas habría que iniciar sesión en cada página. No aceleran el procesador ni impiden el uso de HTTPS.', 8, 'intermedio', 1),
  (1014, '¿Qué hace el modo incógnito de un navegador?', 'El modo incógnito cambia lo que el navegador guarda en el dispositivo, no lo que ve la red ni el proveedor.', 'El modo incógnito evita que el navegador guarde el historial y las cookies de esa sesión en el equipo. No oculta la navegación al proveedor de Internet ni a la red WiFi, y tampoco cifra archivos. Sirve para no dejar rastro local, no para ser invisible.', 8, 'intermedio', 1),
  (1015, 'En la dirección https://www.escuela.edu.ar/aula/notas, ¿qué parte indica el protocolo?', 'Una URL tiene varias partes: el protocolo, el dominio, la ruta y, a veces, parámetros.', 'En una URL, el protocolo aparece antes de los dos puntos y las barras e indica cómo se pide el recurso. En https://www.escuela.edu.ar/aula/notas, el protocolo es https. El dominio es www.escuela.edu.ar y la ruta es /aula/notas.', 9, 'intermedio', 1),
  (1016, '¿Qué indica el dominio en una dirección web?', 'El dominio es la parte de la URL que se registra y se escribe en el navegador para llegar a un sitio.', 'El dominio es la parte de la URL que se registra y se escribe para llegar a un sitio, como escuela.edu.ar. El sistema DNS lo traduce a una dirección IP. No es una contraseña ni el tipo de procesador del servidor.', 9, 'intermedio', 1),
  (1017, '¿Qué es el ancho de banda?', 'No es lo mismo tener más velocidad que más capacidad: el ancho de banda habla de cuánto puede pasar a la vez.', 'El ancho de banda mide cuántos datos pueden pasar por segundo por una conexión. Una conexión con más ancho de banda puede mover más información a la vez. No mide la demora de cada dato ni la cantidad de dispositivos.', 10, 'intermedio', 1),
  (1018, '¿Qué significa tener una latencia alta?', 'La latencia no mide cuántos datos pasan, sino cuánto tardan en llegar. Se nota en videollamadas y juegos en línea.', 'La latencia es el tiempo que tarda un dato en ir y volver. Cuando es alta, las videollamadas se cortan y los juegos en línea se sienten lentos aunque el ancho de banda sea bueno. No reduce el tamaño de los archivos.', 10, 'intermedio', 1),
  (1019, '¿Qué es la autenticación de dos factores (2FA)?', 'Además de la contraseña, algunos servicios piden una segunda prueba para confirmar tu identidad.', 'La autenticación de dos factores agrega una segunda prueba además de la contraseña, como un código en el celular. Así, aunque alguien conozca la clave, no puede entrar sin ese segundo dato. No consiste en usar dos claves iguales.', 11, 'intermedio', 1),
  (1020, '¿Para qué sirve un gestor de contraseñas?', 'Recordar decenas de claves distintas es difícil, por eso existen herramientas que las administran por vos.', 'Un gestor de contraseñas guarda las claves cifradas y puede generar nuevas y difíciles de adivinar. Así se usa una clave distinta en cada sitio sin tener que memorizarlas. No elimina la necesidad de contraseñas ni sirve para compartirlas.', 11, 'intermedio', 1),
  (1021, '¿Por qué no conviene usar la misma contraseña en varios sitios?', 'Si una base de datos filtrada contiene tu clave, los atacantes la prueban en otros servicios.', 'Si una base de datos filtrada contiene tu clave, los atacantes la prueban en otros servicios. Usar la misma contraseña en todos lados les facilita el acceso a varias cuentas con un solo dato. El problema no es el espacio en disco.', 11, 'intermedio', 1),
  (1022, '¿Qué es el smishing?', 'El prefijo sms- da una pista: el engaño usa mensajes de texto o de aplicaciones de mensajería.', 'El smishing es phishing enviado por mensajes de texto o de aplicaciones como WhatsApp. El mensaje suele pedir que hagas clic en un enlace o entregues datos. No es una contraseña ni un virus que borra archivos.', 12, 'intermedio', 1),
  (1023, '¿Qué es el vishing?', 'El prefijo vishing viene de voz: el contacto se hace por teléfono.', 'El vishing es phishing por teléfono: alguien se hace pasar por una empresa o un banco para obtener datos. La voz y la urgencia son parte del engaño. No es una actualización ni un virus.', 12, 'intermedio', 1),
  (1024, 'Recibís un correo urgente con un enlace que pide tus datos. ¿Qué conviene hacer?', 'Los pedidos urgentes por correo suelen buscar que actúes sin pensar. Ante la duda, frená y verificá.', 'Un correo que pide datos con urgencia suele buscar que actúes sin pensar. Conviene no hacer clic y confirmar por un canal oficial, como el sitio o el teléfono de la empresa. Reenviarlo multiplica el riesgo.', 12, 'intermedio', 1),
  (1025, '¿Qué es un proceso?', 'Un programa guardado en el disco no hace nada hasta que el sistema lo carga y lo pone a ejecutar.', 'Un proceso es un programa que el sistema operativo cargó en memoria y está ejecutando. El archivo guardado en el disco solo se convierte en proceso cuando se inicia. No es una pieza física del procesador.', 13, 'intermedio', 1),
  (1026, '¿Qué hace el sistema de archivos?', 'El sistema operativo necesita una forma de ordenar los datos en el disco y de encontrarlos después.', 'El sistema de archivos organiza los datos en carpetas y archivos y registra dónde está cada cosa en el disco. También aplica permisos y controla el acceso. No aumenta la RAM ni conecta a Internet.', 13, 'intermedio', 1),
  (1027, '¿Para qué sirven los permisos de usuario?', 'En un equipo pueden trabajar varias personas: el sistema decide quién puede hacer qué con cada archivo.', 'Los permisos indican qué puede hacer cada usuario con cada archivo: leerlo, modificarlo o ejecutarlo. Así se protege la información de un equipo compartido. No cambian el color de la pantalla ni miden la red.', 13, 'intermedio', 1),
  (1028, '¿Por qué conviene instalar las actualizaciones del sistema?', 'El software cambia y aparecen fallas nuevas. Los fabricantes publican correcciones periódicamente.', 'Las actualizaciones corrigen fallas y cierran problemas de seguridad que se van descubriendo. También pueden mejorar el rendimiento. No borran los archivos del equipo ni agrandan el disco.', 13, 'intermedio', 1),
  (1029, '¿Qué son los permisos de una aplicación móvil?', 'Las aplicaciones móviles piden acceso a funciones del teléfono y a datos personales.', 'Cuando una aplicación móvil pide permisos, está solicitando acceso a funciones del teléfono o a datos personales. Conviene revisar qué pide y darle solo lo necesario. No son las contraseñas del equipo ni el plan de datos.', 14, 'intermedio', 1),
  (1030, '¿Cuál es la diferencia principal entre Android e iOS?', 'Android e iOS tienen interfaces, tiendas y formas de actualización diferentes.', 'Android es el sistema móvil de Google y iOS el de Apple. Cada uno tiene su tienda, sus actualizaciones y su forma de manejar permisos. Ninguno es un navegador ni un procesador.', 14, 'intermedio', 1)
ON DUPLICATE KEY UPDATE
  titulo = VALUES(titulo),
  descripcion = VALUES(descripcion),
  explicacion = VALUES(explicacion),
  tema_id = VALUES(tema_id),
  dificultad = VALUES(dificultad);

-- ----------------------------------------------------------------------------
-- Respuestas (3 opciones por pregunta, una sola correcta)
-- ----------------------------------------------------------------------------
INSERT INTO respuesta (id, contenido, correcta, pregunta_id, activo) VALUES
  (2001, '127.0.0.1', 1, 1001, 1),
  (2002, '169.254.1.1', 0, 1001, 1),
  (2003, '192.168.1.1', 0, 1001, 1),
  (2004, 'Identificar el fabricante del equipo', 0, 1002, 1),
  (2005, 'Diferenciar la parte de red y la parte de host de una dirección IP', 1, 1002, 1),
  (2006, 'Aumentar la velocidad de la conexión', 0, 1002, 1),
  (2007, 'DNS', 0, 1003, 1),
  (2008, 'DHCP', 1, 1003, 1),
  (2009, 'FTP', 0, 1003, 1),
  (2010, 'Conectar la red local a Internet obligatoriamente', 0, 1004, 1),
  (2011, 'Conectar dispositivos dentro de una red local y enviar los datos al dispositivo correspondiente', 1, 1004, 1),
  (2012, 'Convertir señales digitales en sonido', 0, 1004, 1),
  (2013, 'Almacenar los archivos de los usuarios', 0, 1005, 1),
  (2014, 'Conectar dispositivos inalámbricos a una red cableada', 1, 1005, 1),
  (2015, 'Reemplazar la memoria RAM del equipo', 0, 1005, 1),
  (2016, 'DNS', 1, 1006, 1),
  (2017, 'DHCP', 0, 1006, 1),
  (2018, 'ARP', 0, 1006, 1),
  (2019, 'Controlar las conexiones WiFi', 0, 1007, 1),
  (2020, 'Supervisar indicadores de estado y anticipar posibles fallas', 1, 1007, 1),
  (2021, 'Cifrar automáticamente todos los archivos', 0, 1007, 1),
  (2022, 'Que el monitor está conectado correctamente', 0, 1008, 1),
  (2023, 'Que el router está apagado', 0, 1008, 1),
  (2024, 'Un error crítico del sistema o del hardware', 1, 1008, 1),
  (2025, 'Recuperar información ante pérdida o daño', 1, 1009, 1),
  (2026, 'Eliminar la necesidad de antivirus', 0, 1009, 1),
  (2027, 'Aumentar la velocidad de Internet', 0, 1009, 1),
  (2028, 'Un aislante que impide el paso del calor', 0, 1010, 1),
  (2029, 'Un adhesivo para fijar la memoria RAM', 0, 1010, 1),
  (2030, 'Un material que mejora la transferencia de calor entre superficies', 1, 1010, 1),
  (2031, 'Correctivo', 0, 1011, 1),
  (2032, 'Preventivo', 1, 1011, 1),
  (2033, 'Destructivo', 0, 1011, 1),
  (2034, 'Que guarda los datos para siempre', 0, 1012, 1),
  (2035, 'Que pierde su contenido al apagarse el equipo', 1, 1012, 1),
  (2036, 'Que solo funciona con Internet', 0, 1012, 1),
  (2037, 'Para acelerar el procesador', 0, 1013, 1),
  (2038, 'Para que el sitio recuerde datos de la visita, como la sesión o las preferencias', 1, 1013, 1),
  (2039, 'Para impedir que el sitio use HTTPS', 0, 1013, 1),
  (2040, 'Cifra todos los archivos del equipo', 0, 1014, 1),
  (2041, 'Impide que el proveedor de Internet vea la navegación', 0, 1014, 1),
  (2042, 'No guarda el historial ni las cookies de esa sesión en el dispositivo', 1, 1014, 1),
  (2043, 'https', 1, 1015, 1),
  (2044, 'www.escuela.edu.ar', 0, 1015, 1),
  (2045, '/aula/notas', 0, 1015, 1),
  (2046, 'La contraseña de la red WiFi', 0, 1016, 1),
  (2047, 'El nombre que identifica al sitio o servidor', 1, 1016, 1),
  (2048, 'El tipo de procesador del servidor', 0, 1016, 1),
  (2049, 'El tiempo que tarda un dato en llegar', 0, 1017, 1),
  (2050, 'La cantidad de dispositivos conectados a la red', 0, 1017, 1),
  (2051, 'La cantidad de datos que se pueden transmitir por segundo', 1, 1017, 1),
  (2052, 'Que los datos llegan más rápido', 0, 1018, 1),
  (2053, 'Que los datos tardan más en llegar a destino', 1, 1018, 1),
  (2054, 'Que se reduce el tamaño de los archivos', 0, 1018, 1),
  (2055, 'Usar dos contraseñas iguales en dos sitios', 0, 1019, 1),
  (2056, 'Un segundo paso de verificación además de la contraseña', 1, 1019, 1),
  (2057, 'Cambiar la contraseña dos veces por año', 0, 1019, 1),
  (2058, 'Para compartir las contraseñas con todos', 0, 1020, 1),
  (2059, 'Para eliminar la necesidad de usar contraseñas', 0, 1020, 1),
  (2060, 'Para guardar y generar contraseñas seguras sin memorizarlas todas', 1, 1020, 1),
  (2061, 'Porque si filtran una, pueden acceder a las demás cuentas', 1, 1021, 1),
  (2062, 'Porque ocupa más espacio en el disco', 0, 1021, 1),
  (2063, 'Porque el navegador la borra automáticamente', 0, 1021, 1),
  (2064, 'Un ataque que solo afecta impresoras', 0, 1022, 1),
  (2065, 'Un engaño por SMS o aplicación de mensajería', 1, 1022, 1),
  (2066, 'Un tipo de contraseña segura', 0, 1022, 1),
  (2067, 'Un virus que borra archivos', 0, 1023, 1),
  (2068, 'Una actualización del sistema operativo', 0, 1023, 1),
  (2069, 'Un engaño realizado por llamada telefónica', 1, 1023, 1),
  (2070, 'Hacer clic y completar los datos rápido', 0, 1024, 1),
  (2071, 'No hacer clic y verificar el pedido por un canal oficial', 1, 1024, 1),
  (2072, 'Reenviarlo a todos tus contactos', 0, 1024, 1),
  (2073, 'Un archivo guardado en el disco', 0, 1025, 1),
  (2074, 'Un programa que se está ejecutando', 1, 1025, 1),
  (2075, 'Un componente físico del procesador', 0, 1025, 1),
  (2076, 'Aumenta la memoria RAM', 0, 1026, 1),
  (2077, 'Conecta el equipo a Internet', 0, 1026, 1),
  (2078, 'Organiza y controla el acceso a archivos y carpetas', 1, 1026, 1),
  (2079, 'Para cambiar el color de la pantalla', 0, 1027, 1),
  (2080, 'Para medir la velocidad de la red', 0, 1027, 1),
  (2081, 'Para controlar quién puede leer, modificar o ejecutar archivos', 1, 1027, 1),
  (2082, 'Porque corrigen errores y mejoran la seguridad', 1, 1028, 1),
  (2083, 'Porque borran todos los archivos', 0, 1028, 1),
  (2084, 'Porque aumentan el tamaño del disco', 0, 1028, 1),
  (2085, 'Los datos del plan de Internet', 0, 1029, 1),
  (2086, 'Autorizaciones para acceder a cámara, ubicación, contactos y otros datos', 1, 1029, 1),
  (2087, 'Las contraseñas del equipo', 0, 1029, 1),
  (2088, 'Uno es un navegador y el otro un procesador', 0, 1030, 1),
  (2089, 'Android es un hardware y iOS un cable', 0, 1030, 1),
  (2090, 'Son dos sistemas operativos móviles de empresas distintas', 1, 1030, 1)
ON DUPLICATE KEY UPDATE
  contenido = VALUES(contenido),
  correcta = VALUES(correcta),
  pregunta_id = VALUES(pregunta_id);

COMMIT;

-- ----------------------------------------------------------------------------
-- Verificación rápida (opcional)
-- ----------------------------------------------------------------------------
-- SELECT e.orden, e.nombre, COUNT(p.id) AS preguntas
-- FROM estacion e
-- JOIN tema t ON t.estacion_id = e.id AND t.activo = 1
-- JOIN pregunta p ON p.tema_id = t.id AND p.activo = 1
-- WHERE p.dificultad = 'intermedio'
-- GROUP BY e.id, e.orden, e.nombre
-- ORDER BY e.orden;
