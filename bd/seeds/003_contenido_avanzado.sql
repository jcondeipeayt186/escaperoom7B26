-- ============================================================================
-- Escape Room 7°B 2026 - Contenido de nivel avanzado
-- ============================================================================
-- Requiere haber ejecutado bd/schema.sql y bd/seeds/001_contenido_inicial.sql.
--
-- Uso:
--   mysql -u <usuario> -p < bd/seeds/003_contenido_avanzado.sql
--
-- Es idempotente: ejecutarlo dos veces no duplica datos.
--   * Preguntas y respuestas usan ids fijos.
--     Al reejecutar se actualizan los textos, pero NO se cambia `activo`:
--     si el admin desactivó algo, sigue desactivado.
--   * Las descripciones no llevan punto y coma: el cargador de seeds de las
--     pruebas separa las sentencias con ese signo.
--   * No toca `configuracion` ni habilita el nivel.
--
-- Basado en docs/elaboradoChicos/ESCAPEROOM-avanzado.odt y completado con redacción propia.
-- ============================================================================

USE escape_room_7b2026;

SET NAMES utf8mb4;

START TRANSACTION;

-- ----------------------------------------------------------------------------
-- Preguntas (30 en total, 6 por estación)
-- ----------------------------------------------------------------------------
INSERT INTO pregunta (id, titulo, descripcion, explicacion, tema_id, dificultad, activo) VALUES
  (3001, '¿Qué protocolo permite asignar automáticamente direcciones IP a los dispositivos de una red?', 'Cuando un equipo se conecta a la red, puede pedir su configuración automáticamente en lugar de escribirla a mano.', 'DHCP permite que un dispositivo obtenga su dirección IP y otros datos de red automáticamente al conectarse. Un servidor DHCP administra el rango de direcciones disponibles. DNS traduce nombres y FTP transfiere archivos.', 2, 'avanzado', 1),
  (3002, '¿Qué dispositivo trabaja principalmente en la capa 3 del modelo OSI?', 'El modelo OSI tiene siete capas y cada dispositivo trabaja principalmente en una de ellas.', 'El router trabaja en la capa 3 del modelo OSI, la de red, y decide por dónde enviar los paquetes entre redes distintas. Un hub y un switch tradicional operan en capas inferiores. Esa es la razón por la que el router conecta redes diferentes.', 2, 'avanzado', 1),
  (3003, '¿Qué función cumple el protocolo ARP en una red IPv4?', 'En IPv4, para enviar datos dentro de la red local hay que conocer la dirección física (MAC) del destinatario.', 'ARP averigua qué dirección física (MAC) corresponde a una dirección IP dentro de la red local. Con ese dato, las tramas llegan al dispositivo correcto. No asigna contraseñas ni cifra la información.', 1, 'avanzado', 1),
  (3004, '¿Cuál es la diferencia principal entre TCP y UDP?', 'TCP y UDP son dos formas de transportar datos: una prioriza la confiabilidad y la otra la velocidad.', 'TCP establece una conexión, ordena los paquetes y vuelve a pedir los que se pierden. UDP envía sin esas garantías, por eso es más rápido y se usa en video o juegos. Ambos funcionan de manera distinta.', 3, 'avanzado', 1),
  (3005, '¿Qué hace NAT en una red?', 'Las redes domésticas usan direcciones privadas que no existen en Internet, y algo tiene que traducirlas al salir.', 'NAT cambia las direcciones privadas de la red interna por una dirección pública cuando el tráfico sale a Internet. Así varios equipos comparten una sola IP pública. No asigna nombres ni cifra el WiFi.', 2, 'avanzado', 1),
  (3006, '¿Qué mejora WPA3 respecto de WPA2?', 'Las versiones de WPA se suceden para corregir debilidades de las anteriores.', 'WPA3 mejora la protección de las redes WiFi, entre otras cosas frente a intentos de adivinar la clave. También refuerza el cifrado de la conexión. No elimina la contraseña ni reduce la velocidad por diseño.', 4, 'avanzado', 1),
  (3007, '¿Qué componente del procesador almacena datos e instrucciones de acceso frecuente para acelerar su funcionamiento?', 'Dentro del procesador hay memorias muy pequeñas y rápidas que guardan lo que se usa más seguido.', 'La caché L1 es una memoria pequeña y muy rápida dentro del procesador que guarda datos e instrucciones de uso frecuente. Al tenerlos cerca, el procesador espera menos. El disco, la fuente y los módulos externos no cumplen esa función.', 5, 'avanzado', 1),
  (3008, '¿Qué diferencia principal existe entre la memoria SRAM y la DRAM?', 'SRAM y DRAM son dos tipos de memoria que se diferencian por cómo conservan la información y por su costo.', 'La SRAM conserva el dato mientras recibe energía y no necesita refrescarse, por eso es más rápida y cara. La DRAM debe refrescarse constantemente para no perder la información. Esa diferencia explica su uso en caché y en memoria principal.', 7, 'avanzado', 1),
  (3009, '¿Qué tecnología utilizan los SSD para distribuir el desgaste entre sus celdas de memoria?', 'La memoria flash se desgasta con las escrituras, por eso los SSD aplican técnicas de administración interna.', 'Wear Leveling es la técnica que distribuye las escrituras entre las celdas del SSD para que no se desgasten todas en el mismo lugar. Así el disco dura más. Hyper-Threading y Overclocking pertenecen al procesador.', 6, 'avanzado', 1),
  (3010, '¿Qué característica de PCI Express permite aumentar la velocidad de transferencia de datos?', 'PCI Express conecta placas y periféricos con varios carriles que pueden trabajar en paralelo.', 'PCI Express usa carriles que trabajan en paralelo, y una tarjeta puede usar más carriles para transferir más datos. Por eso existen configuraciones x1, x4, x8 y x16. No depende de la RAM ni de cables HDMI.', 5, 'avanzado', 1),
  (3011, '¿Qué diferencia principal hay entre un HDD y un SSD?', 'Un HDD y un SSD guardan datos, pero usan tecnologías de almacenamiento distintas.', 'Un HDD guarda los datos en discos magnéticos que giran, mientras que un SSD usa memoria flash sin partes móviles. Por eso el SSD suele ser más rápido y resistente a golpes. Ninguno usa RAM como almacenamiento permanente.', 6, 'avanzado', 1),
  (3012, '¿Qué es la memoria virtual?', 'El sistema operativo administra la memoria disponible y puede apoyarse en el almacenamiento cuando hace falta.', 'La memoria virtual es un espacio en el almacenamiento que el sistema operativo usa cuando la RAM no alcanza. Es más lenta que la RAM, pero evita que los programas se cierren por falta de memoria. No reemplaza al procesador ni es una conexión inalámbrica.', 7, 'avanzado', 1),
  (3013, '¿Qué función cumple el sistema DNS?', 'Los equipos se comunican con números, pero las personas recuerdan mejor los nombres.', 'El sistema DNS traduce los nombres que escriben las personas a las direcciones IP que usan los equipos. Es como una guía telefónica de Internet. No protege servidores ni aumenta la memoria.', 10, 'avanzado', 1),
  (3014, '¿Qué significa el código de estado HTTP 403?', 'Los códigos HTTP empiezan con 4 cuando el problema está del lado del cliente o de sus permisos.', 'El código 403 significa que el servidor recibió el pedido y lo entendió, pero no permite el acceso al recurso. Puede pasar por permisos o por una regla del sitio. No indica que la página no exista.', 10, 'avanzado', 1),
  (3015, '¿Qué diferencia principal existe entre HTTP y HTTPS?', 'HTTP y HTTPS se parecen en la dirección, pero no en cómo viaja la información.', 'HTTPS usa TLS para cifrar los datos que viajan entre el navegador y el servidor. Así, quien intercepte la conexión no puede leer el contenido. HTTP viaja sin ese cifrado y no es más seguro.', 10, 'avanzado', 1),
  (3016, '¿Qué significa el código de estado HTTP 404?', 'Los códigos 4xx indican que el pedido no pudo completarse, y el número exacto identifica el motivo.', 'El código 404 indica que el servidor no encontró el recurso pedido. Puede ser una dirección mal escrita o una página que ya no existe. No es un error de contraseña ni una confirmación de cifrado.', 10, 'avanzado', 1),
  (3017, '¿Qué es la caché del navegador?', 'El navegador guarda copias de imágenes, estilos y scripts para no descargarlos de nuevo en cada visita.', 'El navegador guarda copias de imágenes, estilos y scripts para no descargarlos otra vez en cada visita. Eso acelera la carga y ahorra datos. No bloquea virus ni guarda contraseñas.', 8, 'avanzado', 1),
  (3018, 'En una dirección como https://tienda.com/productos?categoria=ofertas, ¿qué indica la parte que comienza con el signo de interrogación?', 'En una URL, después del signo de interrogación se envían datos adicionales al servidor.', 'En una URL, la parte que empieza con el signo de interrogación contiene parámetros que se envían al servidor. Allí pueden ir filtros, búsquedas o datos de una consulta. No es el nombre del servidor ni el protocolo de cifrado.', 9, 'avanzado', 1),
  (3019, '¿Qué es un ataque de fuerza bruta?', 'Consiste en probar combinaciones una tras otra, muchas veces con programas automáticos.', 'Un ataque de fuerza bruta prueba combinaciones de claves una tras otra, muchas veces con programas automáticos. Si la contraseña es corta o común, puede encontrarla. No es un virus de impresoras ni un error de conexión.', 11, 'avanzado', 1),
  (3020, '¿Qué es un ataque Man-in-the-Middle (MitM)?', 'En este ataque hay tres partes: la víctima, el destino y alguien que se coloca en el medio.', 'En un ataque Man-in-the-Middle, el atacante se coloca entre la víctima y el destino y puede leer o modificar lo que se envían. Suele apoyarse en redes WiFi falsas o en configuraciones inseguras. No es un olvido de contraseña ni un apagón.', 12, 'avanzado', 1),
  (3021, '¿Qué caracteriza a una vulnerabilidad Zero-Day?', 'Las vulnerabilidades se descubren y se corrigen, pero algunas aparecen antes de que exista una solución.', 'Una vulnerabilidad Zero-Day es una falla que todavía no fue corregida por el fabricante y que puede ser aprovechada. El nombre alude a que no hubo tiempo de preparar una defensa. No es un error que aparece a las 24 horas ni una clave que vence.', 12, 'avanzado', 1),
  (3022, '¿Qué propiedad de la seguridad informática garantiza que los datos no sean modificados sin autorización?', 'Además de evitar filtraciones, la seguridad busca que la información no se altere y que esté disponible cuando se la necesita.', 'La integridad garantiza que los datos no se modifiquen sin autorización. La confidencialidad evita que los lean y la disponibilidad asegura que estén accesibles. La velocidad no es una propiedad de seguridad.', 12, 'avanzado', 1),
  (3023, '¿Qué es el ransomware?', 'Existen malware que buscan un beneficio económico directo y otros que solo causan daño.', 'El ransomware cifra los archivos de la víctima y pide un pago para devolverlos. Es un malware con fines económicos. No mejora el rendimiento ni es una copia de seguridad.', 12, 'avanzado', 1),
  (3024, '¿Qué es la ingeniería social?', 'El eslabón más débil suele ser la persona: se la puede manipular con confianza, miedo o urgencia.', 'La ingeniería social engaña a las personas con confianza, miedo o urgencia para que entreguen datos o hagan algo riesgoso. Ataca al factor humano, no a un componente técnico. No es instalar un antivirus ni cambiar un nombre de usuario.', 12, 'avanzado', 1),
  (3025, '¿Qué función cumple el kernel de un sistema operativo?', 'El sistema operativo tiene una parte central con permisos especiales sobre el hardware.', 'El kernel es el núcleo del sistema operativo y tiene permisos especiales para administrar el hardware. Coordina la memoria, el procesador y los dispositivos, y atiende a los procesos. No se limita a imágenes ni al navegador.', 13, 'avanzado', 1),
  (3026, '¿Qué es un proceso zombie en Linux?', 'En Linux, la tabla de procesos también registra estados de procesos que ya no se están ejecutando.', 'Un proceso zombie ya terminó, pero su entrada sigue en la tabla de procesos hasta que el proceso padre lee su estado. No consume CPU ni memoria de trabajo. No es un proceso que usa toda la RAM ni uno sin Internet.', 13, 'avanzado', 1),
  (3027, '¿Qué algoritmo de planificación asigna un intervalo de tiempo a cada proceso?', 'Los sistemas operativos reparten el procesador entre los procesos, y algunos algoritmos usan turnos.', 'Round Robin asigna a cada proceso un intervalo de tiempo y luego pasa al siguiente, en turnos. Así todos reciben atención y el sistema se siente fluido. First Come, First Served y Shortest Job First usan otros criterios.', 13, 'avanzado', 1),
  (3028, '¿Qué ocurre cuando se produce un Deadlock o interbloqueo?', 'Cuando varios procesos comparten recursos, una mala coordinación puede dejar a todos esperando.', 'En un interbloqueo, cada proceso tiene un recurso y espera otro que tiene el anterior, y ninguno puede avanzar. El sistema queda trabado hasta que se libere la situación. No elimina programas ni acelera el procesador.', 13, 'avanzado', 1),
  (3029, '¿Qué diferencia hay entre un proceso y un hilo?', 'Dentro de un programa puede haber varias tareas a la vez, y conviene distinguir cómo se agrupan.', 'Un proceso tiene su propio espacio de memoria y sus recursos. Los hilos son tareas dentro de un proceso y comparten esa memoria, por eso la comunicación entre ellos es más simple. No son lo mismo.', 13, 'avanzado', 1),
  (3030, '¿Por qué es riesgoso instalar aplicaciones fuera de la tienda oficial?', 'Instalar desde fuera de la tienda oficial saltea la revisión de la empresa que fabrica el sistema.', 'Las aplicaciones que se instalan fuera de la tienda oficial no pasan por la revisión de la empresa que fabrica el sistema. Por eso pueden incluir malware o pedir permisos peligrosos. No ahorran batería por ser externas ni dejan de actualizarse.', 14, 'avanzado', 1)
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
  (4001, 'DNS', 0, 3001, 1),
  (4002, 'DHCP', 1, 3001, 1),
  (4003, 'FTP', 0, 3001, 1),
  (4004, 'Hub', 0, 3002, 1),
  (4005, 'Switch tradicional', 0, 3002, 1),
  (4006, 'Router', 1, 3002, 1),
  (4007, 'Traducir direcciones IP a direcciones MAC', 1, 3003, 1),
  (4008, 'Asignar contraseñas a los dispositivos', 0, 3003, 1),
  (4009, 'Cifrar la información transmitida', 0, 3003, 1),
  (4010, 'UDP necesita una conexión previa y TCP no', 0, 3004, 1),
  (4011, 'TCP garantiza una comunicación confiable, mientras que UDP no garantiza la entrega de los datos', 1, 3004, 1),
  (4012, 'Ambos protocolos funcionan exactamente igual', 0, 3004, 1),
  (4013, 'Asigna nombres de dominio a los dispositivos', 0, 3005, 1),
  (4014, 'Traduce direcciones privadas a una pública para salir a Internet', 1, 3005, 1),
  (4015, 'Cifra el tráfico de la red WiFi', 0, 3005, 1),
  (4016, 'Mayor seguridad y protección contra ataques de fuerza bruta a la clave WiFi', 1, 3006, 1),
  (4017, 'Menor velocidad de conexión', 0, 3006, 1),
  (4018, 'Elimina la necesidad de usar contraseña', 0, 3006, 1),
  (4019, 'Memoria caché L1', 1, 3007, 1),
  (4020, 'Disco rígido HDD', 0, 3007, 1),
  (4021, 'Fuente de alimentación', 0, 3007, 1),
  (4022, 'La SRAM necesita refresco constante y la DRAM no', 0, 3008, 1),
  (4023, 'La SRAM no necesita refresco periódico, mientras que la DRAM sí', 1, 3008, 1),
  (4024, 'Ambas funcionan exactamente de la misma manera', 0, 3008, 1),
  (4025, 'Hyper-Threading', 0, 3009, 1),
  (4026, 'Wear Leveling', 1, 3009, 1),
  (4027, 'Overclocking', 0, 3009, 1),
  (4028, 'La incorporación de memoria RAM externa', 0, 3010, 1),
  (4029, 'La utilización de cables HDMI', 0, 3010, 1),
  (4030, 'La utilización de múltiples carriles de comunicación (x1, x4, x8, x16)', 1, 3010, 1),
  (4031, 'El HDD usa discos magnéticos y el SSD usa memoria flash', 1, 3011, 1),
  (4032, 'El HDD usa memoria flash y el SSD usa discos magnéticos', 0, 3011, 1),
  (4033, 'Ambos usan únicamente memoria RAM', 0, 3011, 1),
  (4034, 'Un espacio en disco que el sistema usa como extensión de la RAM', 1, 3012, 1),
  (4035, 'Una memoria que reemplaza al procesador', 0, 3012, 1),
  (4036, 'Un tipo de conexión inalámbrica', 0, 3012, 1),
  (4037, 'Traducir nombres de dominio en direcciones IP', 1, 3013, 1),
  (4038, 'Proteger físicamente los servidores', 0, 3013, 1),
  (4039, 'Aumentar la memoria RAM de una computadora', 0, 3013, 1),
  (4040, 'El sitio web no existe', 0, 3014, 1),
  (4041, 'El servidor entendió la solicitud, pero deniega el acceso', 1, 3014, 1),
  (4042, 'La página fue encontrada correctamente', 0, 3014, 1),
  (4043, 'HTTP es más seguro porque no utiliza cifrado', 0, 3015, 1),
  (4044, 'HTTPS utiliza cifrado mediante TLS para proteger la comunicación', 1, 3015, 1),
  (4045, 'HTTPS solamente funciona sin conexión a Internet', 0, 3015, 1),
  (4046, 'Error de autenticación del usuario', 0, 3016, 1),
  (4047, 'Recurso o página no encontrada', 1, 3016, 1),
  (4048, 'Conexión cifrada correctamente', 0, 3016, 1),
  (4049, 'Copias de recursos para cargar las páginas más rápido', 1, 3017, 1),
  (4050, 'Un programa que bloquea los virus', 0, 3017, 1),
  (4051, 'El historial de contraseñas del equipo', 0, 3017, 1),
  (4052, 'El nombre del servidor', 0, 3018, 1),
  (4053, 'El protocolo de cifrado', 0, 3018, 1),
  (4054, 'Los parámetros o la consulta que se envía al servidor', 1, 3018, 1),
  (4055, 'Un intento de descubrir contraseñas probando múltiples combinaciones', 1, 3019, 1),
  (4056, 'Un virus que solamente afecta a las impresoras', 0, 3019, 1),
  (4057, 'Un error de conexión a Internet', 0, 3019, 1),
  (4058, 'Una computadora se apaga automáticamente', 0, 3020, 1),
  (4059, 'Un atacante intercepta o altera la comunicación entre dos partes', 1, 3020, 1),
  (4060, 'Un usuario pierde su contraseña por olvidarla', 0, 3020, 1),
  (4061, 'Es una falla de seguridad desconocida o que todavía no tiene un parche disponible', 1, 3021, 1),
  (4062, 'Es un error que aparece después de 24 horas', 0, 3021, 1),
  (4063, 'Es una contraseña que vence diariamente', 0, 3021, 1),
  (4064, 'Disponibilidad', 0, 3022, 1),
  (4065, 'Integridad', 1, 3022, 1),
  (4066, 'Velocidad', 0, 3022, 1),
  (4067, 'Un malware que cifra datos y pide un rescate', 1, 3023, 1),
  (4068, 'Un programa que mejora el rendimiento del equipo', 0, 3023, 1),
  (4069, 'Un tipo de copia de seguridad automática', 0, 3023, 1),
  (4070, 'Manipular personas para que revelen información o realicen acciones', 1, 3024, 1),
  (4071, 'Instalar un antivirus en varios equipos', 0, 3024, 1),
  (4072, 'Cambiar el nombre de usuario del sistema', 0, 3024, 1),
  (4073, 'Gestionar la comunicación entre el hardware y los procesos', 1, 3025, 1),
  (4074, 'Administrar exclusivamente los archivos de imágenes', 0, 3025, 1),
  (4075, 'Controlar únicamente el navegador web', 0, 3025, 1),
  (4076, 'Un proceso que utiliza toda la memoria RAM', 0, 3026, 1),
  (4077, 'Un proceso finalizado cuya entrada todavía permanece en la tabla de procesos', 1, 3026, 1),
  (4078, 'Un proceso que no tiene conexión a Internet', 0, 3026, 1),
  (4079, 'Round Robin', 1, 3027, 1),
  (4080, 'First Come, First Served', 0, 3027, 1),
  (4081, 'Shortest Job First', 0, 3027, 1),
  (4082, 'El sistema operativo elimina todos los programas', 0, 3028, 1),
  (4083, 'Dos o más procesos quedan esperando indefinidamente recursos que están retenidos entre sí', 1, 3028, 1),
  (4084, 'La computadora aumenta automáticamente la velocidad del procesador', 0, 3028, 1),
  (4085, 'El proceso tiene su propio espacio de memoria, mientras que los hilos comparten el del proceso', 1, 3029, 1),
  (4086, 'Los hilos tienen su propio espacio de memoria y el proceso no', 0, 3029, 1),
  (4087, 'No existe ninguna diferencia entre ambos', 0, 3029, 1),
  (4088, 'Pueden contener malware y no estar verificadas por la tienda oficial', 1, 3030, 1),
  (4089, 'Siempre consumen menos batería que las de la tienda oficial', 0, 3030, 1),
  (4090, 'No se pueden actualizar nunca', 0, 3030, 1)
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
-- WHERE p.dificultad = 'avanzado'
-- GROUP BY e.id, e.orden, e.nombre
-- ORDER BY e.orden;
