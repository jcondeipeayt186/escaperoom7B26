-- ============================================================================
-- Escape Room 7°B 2026 - Base de datos completa (estructura + contenido)
-- ============================================================================
-- Archivo generado automáticamente a partir de bd/schema.sql y los seeds
-- bd/seeds/001_contenido_inicial.sql, 002_contenido_intermedio.sql y
-- 003_contenido_avanzado.sql. No editar a mano: si cambia el contenido,
-- regenerar el archivo.
--
-- Uso:
--   mysql -u <usuario> -p < bd/escape_room_7b2026_completa.sql
--
-- ATENCIÓN: elimina y vuelve a crear las 12 tablas de escape_room_7b2026.
-- Se pierden los equipos, intentos y respuestas registrados. Hacer un backup
-- antes de cargarlo sobre una base en uso.
--
-- Contenido:
--   * 5 estaciones, 14 temas, 80 preguntas y 240 respuestas.
--   * 9 claves de configuración.
--   * Dificultades inicial, intermedia y avanzada habilitadas.
--   * Sin equipos, intentos ni historial de partidas.
--
-- Para regenerarlo: cargar bd/schema.sql y los tres seeds en una base vacía,
-- habilitar intermedio y avanzado en configuracion y volcar la base con
-- mysqldump --databases.
-- ============================================================================


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `escape_room_7b2026` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;

USE `escape_room_7b2026`;
DROP TABLE IF EXISTS `configuracion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `configuracion` (
  `clave` varchar(80) COLLATE utf8mb4_unicode_ci NOT NULL,
  `valor` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`clave`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

LOCK TABLES `configuracion` WRITE;
/*!40000 ALTER TABLE `configuracion` DISABLE KEYS */;
INSERT INTO `configuracion` VALUES ('dificultad_avanzada_habilitada','1'),('dificultad_intermedia_habilitada','1'),('duracion_estacion_segundos','240'),('max_ayudas_estacion','2'),('max_envios_estacion','2'),('max_integrantes_equipo','4'),('max_respuestas_incorrectas','2'),('max_temas_por_estacion','4'),('preguntas_por_estacion','4');
/*!40000 ALTER TABLE `configuracion` ENABLE KEYS */;
UNLOCK TABLES;
DROP TABLE IF EXISTS `equipo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `equipo` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `nombre` varchar(120) COLLATE utf8mb4_unicode_ci NOT NULL,
  `cantidad_personas` tinyint unsigned NOT NULL,
  `fecha_creacion` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_equipo_nombre` (`nombre`),
  CONSTRAINT `chk_equipo_cantidad` CHECK ((`cantidad_personas` between 1 and 4))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

LOCK TABLES `equipo` WRITE;
/*!40000 ALTER TABLE `equipo` DISABLE KEYS */;
/*!40000 ALTER TABLE `equipo` ENABLE KEYS */;
UNLOCK TABLES;
DROP TABLE IF EXISTS `estacion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `estacion` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `nombre` varchar(80) COLLATE utf8mb4_unicode_ci NOT NULL,
  `descripcion` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  `orden` tinyint unsigned NOT NULL,
  `activo` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_estacion_orden` (`orden`),
  UNIQUE KEY `uq_estacion_nombre` (`nombre`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

LOCK TABLES `estacion` WRITE;
/*!40000 ALTER TABLE `estacion` DISABLE KEYS */;
INSERT INTO `estacion` VALUES (1,'Redes','Conceptos de redes, direccionamiento IP, router y conexión WiFi.',1,1),(2,'Hardware','Componentes físicos: procesador, memoria RAM y periféricos de entrada y salida.',2,1),(3,'Internet','Navegadores web, direcciones URL y acceso a Internet.',3,1),(4,'Ciberseguridad','Contraseñas seguras y reconocimiento de phishing.',4,1),(5,'Sistemas Operativos','Funciones del sistema operativo y sistemas operativos móviles.',5,1);
/*!40000 ALTER TABLE `estacion` ENABLE KEYS */;
UNLOCK TABLES;
DROP TABLE IF EXISTS `incorrecta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `incorrecta` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `pregunta_id` int unsigned NOT NULL,
  `respuesta_id` int unsigned NOT NULL,
  `fecha` datetime(3) NOT NULL,
  `intento_id` int unsigned NOT NULL,
  `intento_envio_id` int unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_incorrecta_intento` (`intento_id`),
  KEY `idx_incorrecta_envio` (`intento_envio_id`),
  KEY `fk_inc_pregunta` (`pregunta_id`),
  KEY `fk_inc_respuesta` (`respuesta_id`),
  CONSTRAINT `fk_inc_envio` FOREIGN KEY (`intento_envio_id`) REFERENCES `intento_envio` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `fk_inc_intento` FOREIGN KEY (`intento_id`) REFERENCES `intento` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `fk_inc_pregunta` FOREIGN KEY (`pregunta_id`) REFERENCES `pregunta` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `fk_inc_respuesta` FOREIGN KEY (`respuesta_id`) REFERENCES `respuesta` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

LOCK TABLES `incorrecta` WRITE;
/*!40000 ALTER TABLE `incorrecta` DISABLE KEYS */;
/*!40000 ALTER TABLE `incorrecta` ENABLE KEYS */;
UNLOCK TABLES;
DROP TABLE IF EXISTS `intento`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `intento` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `equipo_id` int unsigned NOT NULL,
  `dificultad` enum('inicial','intermedio','avanzado') COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'inicial',
  `fecha_inicio` datetime(3) NOT NULL,
  `fecha_fin` datetime(3) DEFAULT NULL,
  `se_completo_ok` tinyint(1) GENERATED ALWAYS AS (if((`finalizado` = _utf8mb4'completo'),1,0)) STORED,
  `cantidad_ayudas` smallint unsigned NOT NULL DEFAULT '0',
  `puntaje_obtenido` int unsigned DEFAULT NULL,
  `finalizado` enum('completo','abandono','por_respuestas_incorrectas','por_tiempo') COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `ultima_estacion_visitada` int unsigned NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`),
  KEY `idx_intento_equipo` (`equipo_id`),
  KEY `idx_intento_activo` (`fecha_fin`),
  KEY `idx_intento_ranking` (`finalizado`,`fecha_inicio`,`fecha_fin`,`cantidad_ayudas`),
  KEY `fk_intento_ultima_estacion` (`ultima_estacion_visitada`),
  CONSTRAINT `fk_intento_equipo` FOREIGN KEY (`equipo_id`) REFERENCES `equipo` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `fk_intento_ultima_estacion` FOREIGN KEY (`ultima_estacion_visitada`) REFERENCES `estacion` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

LOCK TABLES `intento` WRITE;
/*!40000 ALTER TABLE `intento` DISABLE KEYS */;
/*!40000 ALTER TABLE `intento` ENABLE KEYS */;
UNLOCK TABLES;
DROP TABLE IF EXISTS `intento_envio`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `intento_envio` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `intento_id` int unsigned NOT NULL,
  `estacion_id` int unsigned NOT NULL,
  `fecha` datetime(3) NOT NULL,
  `respuestas_correctas` tinyint unsigned NOT NULL DEFAULT '0',
  `respuestas_incorrectas` tinyint unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `idx_envio_intento_estacion` (`intento_id`,`estacion_id`,`fecha`),
  KEY `fk_envio_estacion` (`estacion_id`),
  CONSTRAINT `fk_envio_estacion` FOREIGN KEY (`estacion_id`) REFERENCES `estacion` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `fk_envio_intento` FOREIGN KEY (`intento_id`) REFERENCES `intento` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

LOCK TABLES `intento_envio` WRITE;
/*!40000 ALTER TABLE `intento_envio` DISABLE KEYS */;
/*!40000 ALTER TABLE `intento_envio` ENABLE KEYS */;
UNLOCK TABLES;
DROP TABLE IF EXISTS `intento_estacion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `intento_estacion` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `intento_id` int unsigned NOT NULL,
  `estacion_id` int unsigned NOT NULL,
  `fecha_inicio` datetime(3) NOT NULL,
  `fecha_fin` datetime(3) DEFAULT NULL,
  `ayudas` tinyint unsigned NOT NULL DEFAULT '0',
  `completada` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_intento_estacion` (`intento_id`,`estacion_id`),
  KEY `fk_ie_estacion` (`estacion_id`),
  CONSTRAINT `fk_ie_estacion` FOREIGN KEY (`estacion_id`) REFERENCES `estacion` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `fk_ie_intento` FOREIGN KEY (`intento_id`) REFERENCES `intento` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

LOCK TABLES `intento_estacion` WRITE;
/*!40000 ALTER TABLE `intento_estacion` DISABLE KEYS */;
/*!40000 ALTER TABLE `intento_estacion` ENABLE KEYS */;
UNLOCK TABLES;
DROP TABLE IF EXISTS `intento_pregunta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `intento_pregunta` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `intento_id` int unsigned NOT NULL,
  `estacion_id` int unsigned NOT NULL,
  `pregunta_id` int unsigned NOT NULL,
  `orden` tinyint unsigned NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_ip_intento_estacion_orden` (`intento_id`,`estacion_id`,`orden`),
  UNIQUE KEY `uq_ip_intento_estacion_pregunta` (`intento_id`,`estacion_id`,`pregunta_id`),
  KEY `fk_ip_estacion` (`estacion_id`),
  KEY `fk_ip_pregunta` (`pregunta_id`),
  CONSTRAINT `fk_ip_estacion` FOREIGN KEY (`estacion_id`) REFERENCES `estacion` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `fk_ip_intento` FOREIGN KEY (`intento_id`) REFERENCES `intento` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `fk_ip_pregunta` FOREIGN KEY (`pregunta_id`) REFERENCES `pregunta` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `chk_ip_orden` CHECK ((`orden` between 1 and 4))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

LOCK TABLES `intento_pregunta` WRITE;
/*!40000 ALTER TABLE `intento_pregunta` DISABLE KEYS */;
/*!40000 ALTER TABLE `intento_pregunta` ENABLE KEYS */;
UNLOCK TABLES;
DROP TABLE IF EXISTS `pregunta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pregunta` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `titulo` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `descripcion` text COLLATE utf8mb4_unicode_ci,
  `explicacion` text COLLATE utf8mb4_unicode_ci,
  `tema_id` int unsigned NOT NULL,
  `dificultad` enum('inicial','intermedio','avanzado') COLLATE utf8mb4_unicode_ci NOT NULL,
  `activo` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`),
  KEY `idx_pregunta_tema_dificultad` (`tema_id`,`dificultad`,`activo`),
  CONSTRAINT `fk_pregunta_tema` FOREIGN KEY (`tema_id`) REFERENCES `tema` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3031 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

LOCK TABLES `pregunta` WRITE;
/*!40000 ALTER TABLE `pregunta` DISABLE KEYS */;
INSERT INTO `pregunta` VALUES (1,'¿Qué significa IP?',NULL,'IP son las siglas de Internet Protocol, el protocolo que identifica cada dispositivo dentro de una red y permite que los datos sepan hacia dónde viajar. Cada equipo conectado recibe una dirección IP, como si fuera su número de casa.',1,'inicial',1),(2,'¿Qué dispositivo conecta diferentes redes?',NULL,'El router une redes distintas y decide por dónde enviar cada paquete de datos. En una casa, es el equipo que conecta la red interna con Internet. Un teclado o un monitor no cumplen esa función.',2,'inicial',1),(3,'¿Qué es una red informática?',NULL,'Una red informática es un conjunto de dispositivos conectados entre sí para compartir información y recursos. Pueden estar unidos por cables o por WiFi y sirven para intercambiar archivos, usar una impresora o navegar.',3,'inicial',1),(4,'¿Qué se necesita para conectarse a una red WiFi?',NULL,'Para entrar a una red WiFi protegida hay que conocer su contraseña o clave de seguridad. Esa clave evita que cualquier persona se conecte sin permiso. Los cables HDMI o las impresoras no tienen relación con esa conexión.',4,'inicial',1),(5,'¿Qué componente es considerado el cerebro de la computadora?',NULL,'El procesador, también llamado CPU, ejecuta las instrucciones y coordina las tareas del equipo. Por eso se lo compara con el cerebro de la computadora: sin él, el resto de los componentes no puede trabajar. El teclado y el monitor solo permiten entrar o ver información.',5,'inicial',1),(6,'¿Cuál es un dispositivo de entrada?',NULL,'Un dispositivo de entrada permite ingresar datos al equipo. El teclado lo hace cuando escribís y el ratón cuando movés el puntero. El monitor y el parlante son de salida, porque muestran o emiten el resultado.',6,'inicial',1),(7,'¿Para qué sirve la memoria RAM?',NULL,'La memoria RAM guarda los datos y los programas que se están usando en ese momento. Es muy rápida, pero al apagar el equipo su contenido se pierde. No sirve para imprimir ni para proteger la pantalla.',7,'inicial',1),(8,'¿Cuál es un dispositivo de salida?',NULL,'Un dispositivo de salida presenta al usuario el resultado del trabajo del equipo. El monitor muestra texto e imágenes y el parlante emite sonido. El ratón y el micrófono son de entrada.',6,'inicial',1),(9,'¿Qué es un navegador web?',NULL,'Un navegador web es el programa que pide las páginas a los servidores y las muestra en pantalla. Chrome, Firefox y Edge son ejemplos. No es una parte del procesador ni un cable de red.',8,'inicial',1),(10,'¿Cuál de estos es un navegador web?',NULL,'Google Chrome es un navegador web: sirve para abrir sitios y navegar por Internet. Windows es un sistema operativo y la calculadora es una aplicación de cálculo. Cada programa cumple una función distinta.',8,'inicial',1),(11,'¿Qué significa URL?',NULL,'URL son las siglas de Uniform Resource Locator y funcionan como la dirección de una página, una imagen o un archivo en Internet. Al escribirla en el navegador, el equipo sabe qué servidor buscar y qué recurso pedir.',9,'inicial',1),(12,'¿Qué se necesita para acceder a un sitio web público en internet?',NULL,'Para ver un sitio público hace falta una conexión que llegue hasta el servidor donde está alojado. Sin conexión a Internet, el navegador no puede pedir esa página. Un escáner o un pendrive no reemplazan esa conexión.',10,'inicial',1),(13,'¿Cómo debe ser una contraseña segura?',NULL,'Una contraseña segura combina mayúsculas, minúsculas, números y símbolos, y tiene suficiente longitud para que no se adivine fácilmente. Evitá datos obvios como 123456 o tu nombre. Cuanto más difícil de adivinar, mejor protege la cuenta.',11,'inicial',1),(14,'¿Qué deberías hacer con un enlace sospechoso?',NULL,'Antes de abrir un enlace dudoso conviene comprobar quién lo envió y por qué. Se puede consultar por otro canal, como una llamada o el sitio oficial. Abrirlo o compartirlo solo aumenta el riesgo.',12,'inicial',1),(15,'¿Qué es el phishing?',NULL,'El phishing es un engaño que imita a una empresa o a una persona conocida para que entregues contraseñas o datos. Suele llegar por correo, mensaje o llamada. No es un programa de fotos ni una clase de monitor.',12,'inicial',1),(16,'¿Qué conviene hacer con tus contraseñas?',NULL,'Las contraseñas son personales y no se comparten con nadie, ni con amigos ni con desconocidos. Usar la misma en todos lados multiplica el daño si una se filtra. Guardarlas de forma segura ayuda a no tener que recordarlas de memoria.',11,'inicial',1),(17,'¿Qué es un sistema operativo?',NULL,'Un sistema operativo es el software principal que administra el hardware y permite ejecutar los programas. Windows, Linux y Android son ejemplos. Sin él, el equipo no sabría cómo usar sus componentes.',13,'inicial',1),(18,'¿Cuál de estos es un sistema operativo?',NULL,'Windows es un sistema operativo: administra el equipo y sirve de base para los demás programas. Microsoft Word es un procesador de textos y Google Chrome es un navegador. Cada uno se apoya en el sistema operativo.',13,'inicial',1),(19,'¿Para qué sirve un sistema operativo?',NULL,'El sistema operativo reparte el procesador, la memoria y el almacenamiento entre los programas. También controla los permisos y la comunicación con los dispositivos. No se limita al color del monitor ni a escribir documentos.',13,'inicial',1),(20,'¿Cuál de estos es un sistema operativo para celulares?',NULL,'Android es un sistema operativo móvil, pensado para teléfonos y tabletas. PowerPoint y Excel son aplicaciones de oficina que funcionan sobre un sistema operativo. iOS es otro sistema móvil, de otra empresa.',14,'inicial',1),(1001,'¿Qué dirección IPv4 es una dirección de loopback?','El loopback es una dirección reservada para que el equipo se hable a sí mismo y pruebe su configuración de red.','La dirección 127.0.0.1 se conoce como loopback y siempre apunta al propio equipo. Sirve para probar si la configuración de red funciona sin salir a la LAN. Las direcciones 192.168 y 169.254 pertenecen a otros rangos.',1,'intermedio',1),(1002,'¿Cuál es la función principal de una máscara de subred?','Junto con la dirección IP se indica la máscara de subred, que define el tamaño de la red.','La máscara de subred indica cuántos bits de la dirección IP identifican la red y cuántos identifican al equipo. Con esa información, el equipo sabe si el destino está dentro de su red o fuera. No identifica al fabricante ni cambia la velocidad.',1,'intermedio',1),(1003,'¿Qué protocolo asigna direcciones IP automáticamente a los dispositivos de una red?','Cuando un dispositivo se conecta a una red, puede recibir su configuración automáticamente en lugar de cargarla a mano.','DHCP es el protocolo que entrega automáticamente dirección IP, máscara y puerta de enlace a los dispositivos. Así no hay que configurar cada equipo a mano. DNS traduce nombres y FTP transfiere archivos.',2,'intermedio',1),(1004,'¿Cuál es la función principal de un switch en una red LAN?','Dentro de una red local hay equipos que concentran las conexiones y deciden por dónde sale cada trama.','Un switch conecta varios equipos de una red local y envía cada trama al puerto del dispositivo correcto. Trabaja dentro de la LAN y no se ocupa de sacar el tráfico a Internet, tarea del router. Tampoco almacena los archivos de los usuarios.',3,'intermedio',1),(1005,'¿Qué función cumple un punto de acceso inalámbrico (Access Point)?','Los dispositivos inalámbricos necesitan un equipo que reciba su señal y la conecte con el resto de la red.','Un punto de acceso recibe la señal de los dispositivos inalámbricos y los integra a la red cableada. Es habitual en escuelas y oficinas para ampliar la cobertura WiFi. No reemplaza la RAM ni guarda archivos.',4,'intermedio',1),(1006,'¿Qué protocolo traduce nombres de dominio como ejemplo.com a direcciones IP?','Escribir un nombre es más fácil que recordar números y algún servicio tiene que hacer la traducción.','DNS es el servicio que traduce nombres como ejemplo.com a direcciones IP. Gracias a él no hace falta recordar números para entrar a un sitio. DHCP asigna direcciones y ARP las vincula con direcciones MAC.',3,'intermedio',1),(1007,'¿Qué función cumple la tecnología SMART en las unidades de almacenamiento?','Los discos modernos registran datos internos sobre su estado y su salud a lo largo del tiempo.','SMART es un sistema de autodiagnóstico que registra datos internos del disco, como errores o temperatura. Con esa información se pueden detectar señales de falla antes de que el disco deje de funcionar. No controla el WiFi ni cifra archivos.',6,'intermedio',1),(1008,'¿Qué puede indicar una pantalla azul recurrente en Windows?','Windows muestra una pantalla azul cuando no puede continuar funcionando por un problema serio.','La pantalla azul de Windows aparece cuando el sistema encuentra un error grave y no puede seguir funcionando. Suele estar relacionada con controladores, memoria o fallas de hardware. No indica que el monitor esté conectado ni que el router esté apagado.',5,'intermedio',1),(1009,'¿Cuál es la finalidad de realizar una copia de seguridad?','Los datos pueden perderse por fallas, robos o errores. Una copia permite volver atrás.','Una copia de seguridad guarda una versión adicional de los datos para poder recuperarlos si algo falla. Sirve ante borrados accidentales, fallas del disco o robos. No reemplaza al antivirus ni acelera Internet.',6,'intermedio',1),(1010,'¿Qué es la pasta térmica?','Entre el procesador y el disipador no deben quedar bolsas de aire: por eso se usa un compuesto especial.','La pasta térmica se coloca entre el procesador y el disipador para llenar las imperfecciones y mejorar el paso del calor. Sin ella quedarían bolsas de aire que calentarían de más. No es un aislante ni un adhesivo para la RAM.',5,'intermedio',1),(1011,'¿Qué tipo de mantenimiento busca evitar fallas futuras?','El mantenimiento puede hacerse antes de que aparezca la falla, después, o para mejorar el rendimiento.','El mantenimiento preventivo se hace antes de que aparezca la falla, con limpieza, revisiones y actualizaciones. El correctivo se aplica cuando el problema ya ocurrió. Prevenir suele ser más barato y evita cortes.',5,'intermedio',1),(1012,'¿Qué significa que la memoria RAM sea volátil?','La RAM es rápida y se usa como espacio de trabajo, pero no está pensada para conservar datos a largo plazo.','Decir que la RAM es volátil significa que necesita energía para conservar los datos. Al apagar o reiniciar el equipo, su contenido se borra. Por eso los archivos se guardan en el disco y no en la RAM.',7,'intermedio',1),(1013,'¿Para qué sirven las cookies de un navegador?','Los sitios necesitan recordar quién sos y qué preferís entre una página y otra. Para eso usan pequeños archivos.','Las cookies son pequeños archivos que el sitio guarda en el navegador para recordar la sesión, el idioma o las preferencias. Sin ellas habría que iniciar sesión en cada página. No aceleran el procesador ni impiden el uso de HTTPS.',8,'intermedio',1),(1014,'¿Qué hace el modo incógnito de un navegador?','El modo incógnito cambia lo que el navegador guarda en el dispositivo, no lo que ve la red ni el proveedor.','El modo incógnito evita que el navegador guarde el historial y las cookies de esa sesión en el equipo. No oculta la navegación al proveedor de Internet ni a la red WiFi, y tampoco cifra archivos. Sirve para no dejar rastro local, no para ser invisible.',8,'intermedio',1),(1015,'En la dirección https://www.escuela.edu.ar/aula/notas, ¿qué parte indica el protocolo?','Una URL tiene varias partes: el protocolo, el dominio, la ruta y, a veces, parámetros.','En una URL, el protocolo aparece antes de los dos puntos y las barras e indica cómo se pide el recurso. En https://www.escuela.edu.ar/aula/notas, el protocolo es https. El dominio es www.escuela.edu.ar y la ruta es /aula/notas.',9,'intermedio',1),(1016,'¿Qué indica el dominio en una dirección web?','El dominio es la parte de la URL que se registra y se escribe en el navegador para llegar a un sitio.','El dominio es la parte de la URL que se registra y se escribe para llegar a un sitio, como escuela.edu.ar. El sistema DNS lo traduce a una dirección IP. No es una contraseña ni el tipo de procesador del servidor.',9,'intermedio',1),(1017,'¿Qué es el ancho de banda?','No es lo mismo tener más velocidad que más capacidad: el ancho de banda habla de cuánto puede pasar a la vez.','El ancho de banda mide cuántos datos pueden pasar por segundo por una conexión. Una conexión con más ancho de banda puede mover más información a la vez. No mide la demora de cada dato ni la cantidad de dispositivos.',10,'intermedio',1),(1018,'¿Qué significa tener una latencia alta?','La latencia no mide cuántos datos pasan, sino cuánto tardan en llegar. Se nota en videollamadas y juegos en línea.','La latencia es el tiempo que tarda un dato en ir y volver. Cuando es alta, las videollamadas se cortan y los juegos en línea se sienten lentos aunque el ancho de banda sea bueno. No reduce el tamaño de los archivos.',10,'intermedio',1),(1019,'¿Qué es la autenticación de dos factores (2FA)?','Además de la contraseña, algunos servicios piden una segunda prueba para confirmar tu identidad.','La autenticación de dos factores agrega una segunda prueba además de la contraseña, como un código en el celular. Así, aunque alguien conozca la clave, no puede entrar sin ese segundo dato. No consiste en usar dos claves iguales.',11,'intermedio',1),(1020,'¿Para qué sirve un gestor de contraseñas?','Recordar decenas de claves distintas es difícil, por eso existen herramientas que las administran por vos.','Un gestor de contraseñas guarda las claves cifradas y puede generar nuevas y difíciles de adivinar. Así se usa una clave distinta en cada sitio sin tener que memorizarlas. No elimina la necesidad de contraseñas ni sirve para compartirlas.',11,'intermedio',1),(1021,'¿Por qué no conviene usar la misma contraseña en varios sitios?','Si una base de datos filtrada contiene tu clave, los atacantes la prueban en otros servicios.','Si una base de datos filtrada contiene tu clave, los atacantes la prueban en otros servicios. Usar la misma contraseña en todos lados les facilita el acceso a varias cuentas con un solo dato. El problema no es el espacio en disco.',11,'intermedio',1),(1022,'¿Qué es el smishing?','El prefijo sms- da una pista: el engaño usa mensajes de texto o de aplicaciones de mensajería.','El smishing es phishing enviado por mensajes de texto o de aplicaciones como WhatsApp. El mensaje suele pedir que hagas clic en un enlace o entregues datos. No es una contraseña ni un virus que borra archivos.',12,'intermedio',1),(1023,'¿Qué es el vishing?','El prefijo vishing viene de voz: el contacto se hace por teléfono.','El vishing es phishing por teléfono: alguien se hace pasar por una empresa o un banco para obtener datos. La voz y la urgencia son parte del engaño. No es una actualización ni un virus.',12,'intermedio',1),(1024,'Recibís un correo urgente con un enlace que pide tus datos. ¿Qué conviene hacer?','Los pedidos urgentes por correo suelen buscar que actúes sin pensar. Ante la duda, frená y verificá.','Un correo que pide datos con urgencia suele buscar que actúes sin pensar. Conviene no hacer clic y confirmar por un canal oficial, como el sitio o el teléfono de la empresa. Reenviarlo multiplica el riesgo.',12,'intermedio',1),(1025,'¿Qué es un proceso?','Un programa guardado en el disco no hace nada hasta que el sistema lo carga y lo pone a ejecutar.','Un proceso es un programa que el sistema operativo cargó en memoria y está ejecutando. El archivo guardado en el disco solo se convierte en proceso cuando se inicia. No es una pieza física del procesador.',13,'intermedio',1),(1026,'¿Qué hace el sistema de archivos?','El sistema operativo necesita una forma de ordenar los datos en el disco y de encontrarlos después.','El sistema de archivos organiza los datos en carpetas y archivos y registra dónde está cada cosa en el disco. También aplica permisos y controla el acceso. No aumenta la RAM ni conecta a Internet.',13,'intermedio',1),(1027,'¿Para qué sirven los permisos de usuario?','En un equipo pueden trabajar varias personas: el sistema decide quién puede hacer qué con cada archivo.','Los permisos indican qué puede hacer cada usuario con cada archivo: leerlo, modificarlo o ejecutarlo. Así se protege la información de un equipo compartido. No cambian el color de la pantalla ni miden la red.',13,'intermedio',1),(1028,'¿Por qué conviene instalar las actualizaciones del sistema?','El software cambia y aparecen fallas nuevas. Los fabricantes publican correcciones periódicamente.','Las actualizaciones corrigen fallas y cierran problemas de seguridad que se van descubriendo. También pueden mejorar el rendimiento. No borran los archivos del equipo ni agrandan el disco.',13,'intermedio',1),(1029,'¿Qué son los permisos de una aplicación móvil?','Las aplicaciones móviles piden acceso a funciones del teléfono y a datos personales.','Cuando una aplicación móvil pide permisos, está solicitando acceso a funciones del teléfono o a datos personales. Conviene revisar qué pide y darle solo lo necesario. No son las contraseñas del equipo ni el plan de datos.',14,'intermedio',1),(1030,'¿Cuál es la diferencia principal entre Android e iOS?','Android e iOS tienen interfaces, tiendas y formas de actualización diferentes.','Android es el sistema móvil de Google y iOS el de Apple. Cada uno tiene su tienda, sus actualizaciones y su forma de manejar permisos. Ninguno es un navegador ni un procesador.',14,'intermedio',1),(3001,'¿Qué protocolo permite asignar automáticamente direcciones IP a los dispositivos de una red?','Cuando un equipo se conecta a la red, puede pedir su configuración automáticamente en lugar de escribirla a mano.','DHCP permite que un dispositivo obtenga su dirección IP y otros datos de red automáticamente al conectarse. Un servidor DHCP administra el rango de direcciones disponibles. DNS traduce nombres y FTP transfiere archivos.',2,'avanzado',1),(3002,'¿Qué dispositivo trabaja principalmente en la capa 3 del modelo OSI?','El modelo OSI tiene siete capas y cada dispositivo trabaja principalmente en una de ellas.','El router trabaja en la capa 3 del modelo OSI, la de red, y decide por dónde enviar los paquetes entre redes distintas. Un hub y un switch tradicional operan en capas inferiores. Esa es la razón por la que el router conecta redes diferentes.',2,'avanzado',1),(3003,'¿Qué función cumple el protocolo ARP en una red IPv4?','En IPv4, para enviar datos dentro de la red local hay que conocer la dirección física (MAC) del destinatario.','ARP averigua qué dirección física (MAC) corresponde a una dirección IP dentro de la red local. Con ese dato, las tramas llegan al dispositivo correcto. No asigna contraseñas ni cifra la información.',1,'avanzado',1),(3004,'¿Cuál es la diferencia principal entre TCP y UDP?','TCP y UDP son dos formas de transportar datos: una prioriza la confiabilidad y la otra la velocidad.','TCP establece una conexión, ordena los paquetes y vuelve a pedir los que se pierden. UDP envía sin esas garantías, por eso es más rápido y se usa en video o juegos. Ambos funcionan de manera distinta.',3,'avanzado',1),(3005,'¿Qué hace NAT en una red?','Las redes domésticas usan direcciones privadas que no existen en Internet, y algo tiene que traducirlas al salir.','NAT cambia las direcciones privadas de la red interna por una dirección pública cuando el tráfico sale a Internet. Así varios equipos comparten una sola IP pública. No asigna nombres ni cifra el WiFi.',2,'avanzado',1),(3006,'¿Qué mejora WPA3 respecto de WPA2?','Las versiones de WPA se suceden para corregir debilidades de las anteriores.','WPA3 mejora la protección de las redes WiFi, entre otras cosas frente a intentos de adivinar la clave. También refuerza el cifrado de la conexión. No elimina la contraseña ni reduce la velocidad por diseño.',4,'avanzado',1),(3007,'¿Qué componente del procesador almacena datos e instrucciones de acceso frecuente para acelerar su funcionamiento?','Dentro del procesador hay memorias muy pequeñas y rápidas que guardan lo que se usa más seguido.','La caché L1 es una memoria pequeña y muy rápida dentro del procesador que guarda datos e instrucciones de uso frecuente. Al tenerlos cerca, el procesador espera menos. El disco, la fuente y los módulos externos no cumplen esa función.',5,'avanzado',1),(3008,'¿Qué diferencia principal existe entre la memoria SRAM y la DRAM?','SRAM y DRAM son dos tipos de memoria que se diferencian por cómo conservan la información y por su costo.','La SRAM conserva el dato mientras recibe energía y no necesita refrescarse, por eso es más rápida y cara. La DRAM debe refrescarse constantemente para no perder la información. Esa diferencia explica su uso en caché y en memoria principal.',7,'avanzado',1),(3009,'¿Qué tecnología utilizan los SSD para distribuir el desgaste entre sus celdas de memoria?','La memoria flash se desgasta con las escrituras, por eso los SSD aplican técnicas de administración interna.','Wear Leveling es la técnica que distribuye las escrituras entre las celdas del SSD para que no se desgasten todas en el mismo lugar. Así el disco dura más. Hyper-Threading y Overclocking pertenecen al procesador.',6,'avanzado',1),(3010,'¿Qué característica de PCI Express permite aumentar la velocidad de transferencia de datos?','PCI Express conecta placas y periféricos con varios carriles que pueden trabajar en paralelo.','PCI Express usa carriles que trabajan en paralelo, y una tarjeta puede usar más carriles para transferir más datos. Por eso existen configuraciones x1, x4, x8 y x16. No depende de la RAM ni de cables HDMI.',5,'avanzado',1),(3011,'¿Qué diferencia principal hay entre un HDD y un SSD?','Un HDD y un SSD guardan datos, pero usan tecnologías de almacenamiento distintas.','Un HDD guarda los datos en discos magnéticos que giran, mientras que un SSD usa memoria flash sin partes móviles. Por eso el SSD suele ser más rápido y resistente a golpes. Ninguno usa RAM como almacenamiento permanente.',6,'avanzado',1),(3012,'¿Qué es la memoria virtual?','El sistema operativo administra la memoria disponible y puede apoyarse en el almacenamiento cuando hace falta.','La memoria virtual es un espacio en el almacenamiento que el sistema operativo usa cuando la RAM no alcanza. Es más lenta que la RAM, pero evita que los programas se cierren por falta de memoria. No reemplaza al procesador ni es una conexión inalámbrica.',7,'avanzado',1),(3013,'¿Qué función cumple el sistema DNS?','Los equipos se comunican con números, pero las personas recuerdan mejor los nombres.','El sistema DNS traduce los nombres que escriben las personas a las direcciones IP que usan los equipos. Es como una guía telefónica de Internet. No protege servidores ni aumenta la memoria.',10,'avanzado',1),(3014,'¿Qué significa el código de estado HTTP 403?','Los códigos HTTP empiezan con 4 cuando el problema está del lado del cliente o de sus permisos.','El código 403 significa que el servidor recibió el pedido y lo entendió, pero no permite el acceso al recurso. Puede pasar por permisos o por una regla del sitio. No indica que la página no exista.',10,'avanzado',1),(3015,'¿Qué diferencia principal existe entre HTTP y HTTPS?','HTTP y HTTPS se parecen en la dirección, pero no en cómo viaja la información.','HTTPS usa TLS para cifrar los datos que viajan entre el navegador y el servidor. Así, quien intercepte la conexión no puede leer el contenido. HTTP viaja sin ese cifrado y no es más seguro.',10,'avanzado',1),(3016,'¿Qué significa el código de estado HTTP 404?','Los códigos 4xx indican que el pedido no pudo completarse, y el número exacto identifica el motivo.','El código 404 indica que el servidor no encontró el recurso pedido. Puede ser una dirección mal escrita o una página que ya no existe. No es un error de contraseña ni una confirmación de cifrado.',10,'avanzado',1),(3017,'¿Qué es la caché del navegador?','El navegador guarda copias de imágenes, estilos y scripts para no descargarlos de nuevo en cada visita.','El navegador guarda copias de imágenes, estilos y scripts para no descargarlos otra vez en cada visita. Eso acelera la carga y ahorra datos. No bloquea virus ni guarda contraseñas.',8,'avanzado',1),(3018,'En una dirección como https://tienda.com/productos?categoria=ofertas, ¿qué indica la parte que comienza con el signo de interrogación?','En una URL, después del signo de interrogación se envían datos adicionales al servidor.','En una URL, la parte que empieza con el signo de interrogación contiene parámetros que se envían al servidor. Allí pueden ir filtros, búsquedas o datos de una consulta. No es el nombre del servidor ni el protocolo de cifrado.',9,'avanzado',1),(3019,'¿Qué es un ataque de fuerza bruta?','Consiste en probar combinaciones una tras otra, muchas veces con programas automáticos.','Un ataque de fuerza bruta prueba combinaciones de claves una tras otra, muchas veces con programas automáticos. Si la contraseña es corta o común, puede encontrarla. No es un virus de impresoras ni un error de conexión.',11,'avanzado',1),(3020,'¿Qué es un ataque Man-in-the-Middle (MitM)?','En este ataque hay tres partes: la víctima, el destino y alguien que se coloca en el medio.','En un ataque Man-in-the-Middle, el atacante se coloca entre la víctima y el destino y puede leer o modificar lo que se envían. Suele apoyarse en redes WiFi falsas o en configuraciones inseguras. No es un olvido de contraseña ni un apagón.',12,'avanzado',1),(3021,'¿Qué caracteriza a una vulnerabilidad Zero-Day?','Las vulnerabilidades se descubren y se corrigen, pero algunas aparecen antes de que exista una solución.','Una vulnerabilidad Zero-Day es una falla que todavía no fue corregida por el fabricante y que puede ser aprovechada. El nombre alude a que no hubo tiempo de preparar una defensa. No es un error que aparece a las 24 horas ni una clave que vence.',12,'avanzado',1),(3022,'¿Qué propiedad de la seguridad informática garantiza que los datos no sean modificados sin autorización?','Además de evitar filtraciones, la seguridad busca que la información no se altere y que esté disponible cuando se la necesita.','La integridad garantiza que los datos no se modifiquen sin autorización. La confidencialidad evita que los lean y la disponibilidad asegura que estén accesibles. La velocidad no es una propiedad de seguridad.',12,'avanzado',1),(3023,'¿Qué es el ransomware?','Existen malware que buscan un beneficio económico directo y otros que solo causan daño.','El ransomware cifra los archivos de la víctima y pide un pago para devolverlos. Es un malware con fines económicos. No mejora el rendimiento ni es una copia de seguridad.',12,'avanzado',1),(3024,'¿Qué es la ingeniería social?','El eslabón más débil suele ser la persona: se la puede manipular con confianza, miedo o urgencia.','La ingeniería social engaña a las personas con confianza, miedo o urgencia para que entreguen datos o hagan algo riesgoso. Ataca al factor humano, no a un componente técnico. No es instalar un antivirus ni cambiar un nombre de usuario.',12,'avanzado',1),(3025,'¿Qué función cumple el kernel de un sistema operativo?','El sistema operativo tiene una parte central con permisos especiales sobre el hardware.','El kernel es el núcleo del sistema operativo y tiene permisos especiales para administrar el hardware. Coordina la memoria, el procesador y los dispositivos, y atiende a los procesos. No se limita a imágenes ni al navegador.',13,'avanzado',1),(3026,'¿Qué es un proceso zombie en Linux?','En Linux, la tabla de procesos también registra estados de procesos que ya no se están ejecutando.','Un proceso zombie ya terminó, pero su entrada sigue en la tabla de procesos hasta que el proceso padre lee su estado. No consume CPU ni memoria de trabajo. No es un proceso que usa toda la RAM ni uno sin Internet.',13,'avanzado',1),(3027,'¿Qué algoritmo de planificación asigna un intervalo de tiempo a cada proceso?','Los sistemas operativos reparten el procesador entre los procesos, y algunos algoritmos usan turnos.','Round Robin asigna a cada proceso un intervalo de tiempo y luego pasa al siguiente, en turnos. Así todos reciben atención y el sistema se siente fluido. First Come, First Served y Shortest Job First usan otros criterios.',13,'avanzado',1),(3028,'¿Qué ocurre cuando se produce un Deadlock o interbloqueo?','Cuando varios procesos comparten recursos, una mala coordinación puede dejar a todos esperando.','En un interbloqueo, cada proceso tiene un recurso y espera otro que tiene el anterior, y ninguno puede avanzar. El sistema queda trabado hasta que se libere la situación. No elimina programas ni acelera el procesador.',13,'avanzado',1),(3029,'¿Qué diferencia hay entre un proceso y un hilo?','Dentro de un programa puede haber varias tareas a la vez, y conviene distinguir cómo se agrupan.','Un proceso tiene su propio espacio de memoria y sus recursos. Los hilos son tareas dentro de un proceso y comparten esa memoria, por eso la comunicación entre ellos es más simple. No son lo mismo.',13,'avanzado',1),(3030,'¿Por qué es riesgoso instalar aplicaciones fuera de la tienda oficial?','Instalar desde fuera de la tienda oficial saltea la revisión de la empresa que fabrica el sistema.','Las aplicaciones que se instalan fuera de la tienda oficial no pasan por la revisión de la empresa que fabrica el sistema. Por eso pueden incluir malware o pedir permisos peligrosos. No ahorran batería por ser externas ni dejan de actualizarse.',14,'avanzado',1);
/*!40000 ALTER TABLE `pregunta` ENABLE KEYS */;
UNLOCK TABLES;
DROP TABLE IF EXISTS `respuesta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `respuesta` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `contenido` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `correcta` tinyint(1) NOT NULL DEFAULT '0',
  `pregunta_id` int unsigned NOT NULL,
  `activo` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`),
  KEY `idx_respuesta_pregunta` (`pregunta_id`,`activo`),
  CONSTRAINT `fk_respuesta_pregunta` FOREIGN KEY (`pregunta_id`) REFERENCES `pregunta` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4091 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

LOCK TABLES `respuesta` WRITE;
/*!40000 ALTER TABLE `respuesta` DISABLE KEYS */;
INSERT INTO `respuesta` VALUES (1,'Internet personal',0,1,1),(2,'Internet Protocol',1,1,1),(3,'Información privada',0,1,1),(4,'Teclado',0,2,1),(5,'Router',1,2,1),(6,'Monitor',0,2,1),(7,'Un conjunto de dispositivos conectados',1,3,1),(8,'Un programa para dibujar',0,3,1),(9,'Una pieza de la computadora',0,3,1),(10,'Una contraseña, si está protegida',1,4,1),(11,'Un cable HDMI obligatoriamente',0,4,1),(12,'Una impresora',0,4,1),(13,'Teclado',0,5,1),(14,'Procesador',1,5,1),(15,'Monitor',0,5,1),(16,'Monitor',0,6,1),(17,'Parlante',0,6,1),(18,'Teclado',1,6,1),(19,'Guardar datos temporalmente mientras se trabaja',1,7,1),(20,'Imprimir documentos',0,7,1),(21,'Proteger físicamente la pantalla',0,7,1),(22,'Ratón',0,8,1),(23,'Micrófono',0,8,1),(24,'Monitor',1,8,1),(25,'Un programa para visitar páginas web',1,9,1),(26,'Una parte del procesador',0,9,1),(27,'Un cable de red',0,9,1),(28,'Google Chrome',1,10,1),(29,'Windows',0,10,1),(30,'Calculadora',0,10,1),(31,'Una dirección de un recurso en internet',1,11,1),(32,'Una memoria de computadora',0,11,1),(33,'Un tipo de teclado',0,11,1),(34,'Una conexión a internet',1,12,1),(35,'Un escáner obligatoriamente',0,12,1),(36,'Un pendrive siempre',0,12,1),(37,'123456',0,13,1),(38,'Tu nombre solamente',0,13,1),(39,'Larga y difícil de adivinar',1,13,1),(40,'Abrirlo inmediatamente',0,14,1),(41,'Evitar abrirlo y verificar su origen',1,14,1),(42,'Compartirlo con todos',0,14,1),(43,'Un intento de engaño para robar información',1,15,1),(44,'Un programa para editar fotos',0,15,1),(45,'Una clase de monitor',0,15,1),(46,'Compartirlas con desconocidos',0,16,1),(47,'Usar la misma en todos lados',0,16,1),(48,'Mantenerlas privadas',1,16,1),(49,'El software que administra la computadora',1,17,1),(50,'Un cable de alimentación',0,17,1),(51,'Una aplicación para dibujar',0,17,1),(52,'Microsoft Word',0,18,1),(53,'Windows',1,18,1),(54,'Google Chrome',0,18,1),(55,'Administrar recursos y permitir ejecutar programas',1,19,1),(56,'Solo para cambiar el color del monitor',0,19,1),(57,'Solo para escribir documentos',0,19,1),(58,'Android',1,20,1),(59,'PowerPoint',0,20,1),(60,'Excel',0,20,1),(2001,'127.0.0.1',1,1001,1),(2002,'169.254.1.1',0,1001,1),(2003,'192.168.1.1',0,1001,1),(2004,'Identificar el fabricante del equipo',0,1002,1),(2005,'Diferenciar la parte de red y la parte de host de una dirección IP',1,1002,1),(2006,'Aumentar la velocidad de la conexión',0,1002,1),(2007,'DNS',0,1003,1),(2008,'DHCP',1,1003,1),(2009,'FTP',0,1003,1),(2010,'Conectar la red local a Internet obligatoriamente',0,1004,1),(2011,'Conectar dispositivos dentro de una red local y enviar los datos al dispositivo correspondiente',1,1004,1),(2012,'Convertir señales digitales en sonido',0,1004,1),(2013,'Almacenar los archivos de los usuarios',0,1005,1),(2014,'Conectar dispositivos inalámbricos a una red cableada',1,1005,1),(2015,'Reemplazar la memoria RAM del equipo',0,1005,1),(2016,'DNS',1,1006,1),(2017,'DHCP',0,1006,1),(2018,'ARP',0,1006,1),(2019,'Controlar las conexiones WiFi',0,1007,1),(2020,'Supervisar indicadores de estado y anticipar posibles fallas',1,1007,1),(2021,'Cifrar automáticamente todos los archivos',0,1007,1),(2022,'Que el monitor está conectado correctamente',0,1008,1),(2023,'Que el router está apagado',0,1008,1),(2024,'Un error crítico del sistema o del hardware',1,1008,1),(2025,'Recuperar información ante pérdida o daño',1,1009,1),(2026,'Eliminar la necesidad de antivirus',0,1009,1),(2027,'Aumentar la velocidad de Internet',0,1009,1),(2028,'Un aislante que impide el paso del calor',0,1010,1),(2029,'Un adhesivo para fijar la memoria RAM',0,1010,1),(2030,'Un material que mejora la transferencia de calor entre superficies',1,1010,1),(2031,'Correctivo',0,1011,1),(2032,'Preventivo',1,1011,1),(2033,'Destructivo',0,1011,1),(2034,'Que guarda los datos para siempre',0,1012,1),(2035,'Que pierde su contenido al apagarse el equipo',1,1012,1),(2036,'Que solo funciona con Internet',0,1012,1),(2037,'Para acelerar el procesador',0,1013,1),(2038,'Para que el sitio recuerde datos de la visita, como la sesión o las preferencias',1,1013,1),(2039,'Para impedir que el sitio use HTTPS',0,1013,1),(2040,'Cifra todos los archivos del equipo',0,1014,1),(2041,'Impide que el proveedor de Internet vea la navegación',0,1014,1),(2042,'No guarda el historial ni las cookies de esa sesión en el dispositivo',1,1014,1),(2043,'https',1,1015,1),(2044,'www.escuela.edu.ar',0,1015,1),(2045,'/aula/notas',0,1015,1),(2046,'La contraseña de la red WiFi',0,1016,1),(2047,'El nombre que identifica al sitio o servidor',1,1016,1),(2048,'El tipo de procesador del servidor',0,1016,1),(2049,'El tiempo que tarda un dato en llegar',0,1017,1),(2050,'La cantidad de dispositivos conectados a la red',0,1017,1),(2051,'La cantidad de datos que se pueden transmitir por segundo',1,1017,1),(2052,'Que los datos llegan más rápido',0,1018,1),(2053,'Que los datos tardan más en llegar a destino',1,1018,1),(2054,'Que se reduce el tamaño de los archivos',0,1018,1),(2055,'Usar dos contraseñas iguales en dos sitios',0,1019,1),(2056,'Un segundo paso de verificación además de la contraseña',1,1019,1),(2057,'Cambiar la contraseña dos veces por año',0,1019,1),(2058,'Para compartir las contraseñas con todos',0,1020,1),(2059,'Para eliminar la necesidad de usar contraseñas',0,1020,1),(2060,'Para guardar y generar contraseñas seguras sin memorizarlas todas',1,1020,1),(2061,'Porque si filtran una, pueden acceder a las demás cuentas',1,1021,1),(2062,'Porque ocupa más espacio en el disco',0,1021,1),(2063,'Porque el navegador la borra automáticamente',0,1021,1),(2064,'Un ataque que solo afecta impresoras',0,1022,1),(2065,'Un engaño por SMS o aplicación de mensajería',1,1022,1),(2066,'Un tipo de contraseña segura',0,1022,1),(2067,'Un virus que borra archivos',0,1023,1),(2068,'Una actualización del sistema operativo',0,1023,1),(2069,'Un engaño realizado por llamada telefónica',1,1023,1),(2070,'Hacer clic y completar los datos rápido',0,1024,1),(2071,'No hacer clic y verificar el pedido por un canal oficial',1,1024,1),(2072,'Reenviarlo a todos tus contactos',0,1024,1),(2073,'Un archivo guardado en el disco',0,1025,1),(2074,'Un programa que se está ejecutando',1,1025,1),(2075,'Un componente físico del procesador',0,1025,1),(2076,'Aumenta la memoria RAM',0,1026,1),(2077,'Conecta el equipo a Internet',0,1026,1),(2078,'Organiza y controla el acceso a archivos y carpetas',1,1026,1),(2079,'Para cambiar el color de la pantalla',0,1027,1),(2080,'Para medir la velocidad de la red',0,1027,1),(2081,'Para controlar quién puede leer, modificar o ejecutar archivos',1,1027,1),(2082,'Porque corrigen errores y mejoran la seguridad',1,1028,1),(2083,'Porque borran todos los archivos',0,1028,1),(2084,'Porque aumentan el tamaño del disco',0,1028,1),(2085,'Los datos del plan de Internet',0,1029,1),(2086,'Autorizaciones para acceder a cámara, ubicación, contactos y otros datos',1,1029,1),(2087,'Las contraseñas del equipo',0,1029,1),(2088,'Uno es un navegador y el otro un procesador',0,1030,1),(2089,'Android es un hardware y iOS un cable',0,1030,1),(2090,'Son dos sistemas operativos móviles de empresas distintas',1,1030,1),(4001,'DNS',0,3001,1),(4002,'DHCP',1,3001,1),(4003,'FTP',0,3001,1),(4004,'Hub',0,3002,1),(4005,'Switch tradicional',0,3002,1),(4006,'Router',1,3002,1),(4007,'Traducir direcciones IP a direcciones MAC',1,3003,1),(4008,'Asignar contraseñas a los dispositivos',0,3003,1),(4009,'Cifrar la información transmitida',0,3003,1),(4010,'UDP necesita una conexión previa y TCP no',0,3004,1),(4011,'TCP garantiza una comunicación confiable, mientras que UDP no garantiza la entrega de los datos',1,3004,1),(4012,'Ambos protocolos funcionan exactamente igual',0,3004,1),(4013,'Asigna nombres de dominio a los dispositivos',0,3005,1),(4014,'Traduce direcciones privadas a una pública para salir a Internet',1,3005,1),(4015,'Cifra el tráfico de la red WiFi',0,3005,1),(4016,'Mayor seguridad y protección contra ataques de fuerza bruta a la clave WiFi',1,3006,1),(4017,'Menor velocidad de conexión',0,3006,1),(4018,'Elimina la necesidad de usar contraseña',0,3006,1),(4019,'Memoria caché L1',1,3007,1),(4020,'Disco rígido HDD',0,3007,1),(4021,'Fuente de alimentación',0,3007,1),(4022,'La SRAM necesita refresco constante y la DRAM no',0,3008,1),(4023,'La SRAM no necesita refresco periódico, mientras que la DRAM sí',1,3008,1),(4024,'Ambas funcionan exactamente de la misma manera',0,3008,1),(4025,'Hyper-Threading',0,3009,1),(4026,'Wear Leveling',1,3009,1),(4027,'Overclocking',0,3009,1),(4028,'La incorporación de memoria RAM externa',0,3010,1),(4029,'La utilización de cables HDMI',0,3010,1),(4030,'La utilización de múltiples carriles de comunicación (x1, x4, x8, x16)',1,3010,1),(4031,'El HDD usa discos magnéticos y el SSD usa memoria flash',1,3011,1),(4032,'El HDD usa memoria flash y el SSD usa discos magnéticos',0,3011,1),(4033,'Ambos usan únicamente memoria RAM',0,3011,1),(4034,'Un espacio en disco que el sistema usa como extensión de la RAM',1,3012,1),(4035,'Una memoria que reemplaza al procesador',0,3012,1),(4036,'Un tipo de conexión inalámbrica',0,3012,1),(4037,'Traducir nombres de dominio en direcciones IP',1,3013,1),(4038,'Proteger físicamente los servidores',0,3013,1),(4039,'Aumentar la memoria RAM de una computadora',0,3013,1),(4040,'El sitio web no existe',0,3014,1),(4041,'El servidor entendió la solicitud, pero deniega el acceso',1,3014,1),(4042,'La página fue encontrada correctamente',0,3014,1),(4043,'HTTP es más seguro porque no utiliza cifrado',0,3015,1),(4044,'HTTPS utiliza cifrado mediante TLS para proteger la comunicación',1,3015,1),(4045,'HTTPS solamente funciona sin conexión a Internet',0,3015,1),(4046,'Error de autenticación del usuario',0,3016,1),(4047,'Recurso o página no encontrada',1,3016,1),(4048,'Conexión cifrada correctamente',0,3016,1),(4049,'Copias de recursos para cargar las páginas más rápido',1,3017,1),(4050,'Un programa que bloquea los virus',0,3017,1),(4051,'El historial de contraseñas del equipo',0,3017,1),(4052,'El nombre del servidor',0,3018,1),(4053,'El protocolo de cifrado',0,3018,1),(4054,'Los parámetros o la consulta que se envía al servidor',1,3018,1),(4055,'Un intento de descubrir contraseñas probando múltiples combinaciones',1,3019,1),(4056,'Un virus que solamente afecta a las impresoras',0,3019,1),(4057,'Un error de conexión a Internet',0,3019,1),(4058,'Una computadora se apaga automáticamente',0,3020,1),(4059,'Un atacante intercepta o altera la comunicación entre dos partes',1,3020,1),(4060,'Un usuario pierde su contraseña por olvidarla',0,3020,1),(4061,'Es una falla de seguridad desconocida o que todavía no tiene un parche disponible',1,3021,1),(4062,'Es un error que aparece después de 24 horas',0,3021,1),(4063,'Es una contraseña que vence diariamente',0,3021,1),(4064,'Disponibilidad',0,3022,1),(4065,'Integridad',1,3022,1),(4066,'Velocidad',0,3022,1),(4067,'Un malware que cifra datos y pide un rescate',1,3023,1),(4068,'Un programa que mejora el rendimiento del equipo',0,3023,1),(4069,'Un tipo de copia de seguridad automática',0,3023,1),(4070,'Manipular personas para que revelen información o realicen acciones',1,3024,1),(4071,'Instalar un antivirus en varios equipos',0,3024,1),(4072,'Cambiar el nombre de usuario del sistema',0,3024,1),(4073,'Gestionar la comunicación entre el hardware y los procesos',1,3025,1),(4074,'Administrar exclusivamente los archivos de imágenes',0,3025,1),(4075,'Controlar únicamente el navegador web',0,3025,1),(4076,'Un proceso que utiliza toda la memoria RAM',0,3026,1),(4077,'Un proceso finalizado cuya entrada todavía permanece en la tabla de procesos',1,3026,1),(4078,'Un proceso que no tiene conexión a Internet',0,3026,1),(4079,'Round Robin',1,3027,1),(4080,'First Come, First Served',0,3027,1),(4081,'Shortest Job First',0,3027,1),(4082,'El sistema operativo elimina todos los programas',0,3028,1),(4083,'Dos o más procesos quedan esperando indefinidamente recursos que están retenidos entre sí',1,3028,1),(4084,'La computadora aumenta automáticamente la velocidad del procesador',0,3028,1),(4085,'El proceso tiene su propio espacio de memoria, mientras que los hilos comparten el del proceso',1,3029,1),(4086,'Los hilos tienen su propio espacio de memoria y el proceso no',0,3029,1),(4087,'No existe ninguna diferencia entre ambos',0,3029,1),(4088,'Pueden contener malware y no estar verificadas por la tienda oficial',1,3030,1),(4089,'Siempre consumen menos batería que las de la tienda oficial',0,3030,1),(4090,'No se pueden actualizar nunca',0,3030,1);
/*!40000 ALTER TABLE `respuesta` ENABLE KEYS */;
UNLOCK TABLES;
DROP TABLE IF EXISTS `respuesta_elegida`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `respuesta_elegida` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `fecha_respondida` datetime(3) NOT NULL,
  `intento_id` int unsigned NOT NULL,
  `intento_envio_id` int unsigned NOT NULL,
  `respuesta_id` int unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_re_intento` (`intento_id`),
  KEY `idx_re_envio` (`intento_envio_id`),
  KEY `idx_re_respuesta` (`respuesta_id`),
  CONSTRAINT `fk_re_envio` FOREIGN KEY (`intento_envio_id`) REFERENCES `intento_envio` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `fk_re_intento` FOREIGN KEY (`intento_id`) REFERENCES `intento` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `fk_re_respuesta` FOREIGN KEY (`respuesta_id`) REFERENCES `respuesta` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

LOCK TABLES `respuesta_elegida` WRITE;
/*!40000 ALTER TABLE `respuesta_elegida` DISABLE KEYS */;
/*!40000 ALTER TABLE `respuesta_elegida` ENABLE KEYS */;
UNLOCK TABLES;
DROP TABLE IF EXISTS `tema`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tema` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `nombre` varchar(80) COLLATE utf8mb4_unicode_ci NOT NULL,
  `introduccion` text COLLATE utf8mb4_unicode_ci,
  `estacion_id` int unsigned NOT NULL,
  `activo` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_tema_estacion_nombre` (`estacion_id`,`nombre`),
  CONSTRAINT `fk_tema_estacion` FOREIGN KEY (`estacion_id`) REFERENCES `estacion` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

LOCK TABLES `tema` WRITE;
/*!40000 ALTER TABLE `tema` DISABLE KEYS */;
INSERT INTO `tema` VALUES (1,'IP','Una dirección IP identifica a cada dispositivo dentro de una red y permite que los datos lleguen a destino. Puede ser privada, pública o especial, como la de loopback. Conocerla ayuda a entender cómo se comunican los equipos.',1,1),(2,'Router','El router es el equipo que conecta redes distintas y decide por dónde sale cada paquete. En una casa suele unir la red interna con Internet. Su trabajo es distinto del de un switch o un punto de acceso.',1,1),(3,'Redes de computadoras','Una red de computadoras es un conjunto de dispositivos conectados para compartir datos y recursos. Puede ser cableada o inalámbrica y su tamaño va desde una casa hasta una empresa. Los protocolos son las reglas que ordenan esa comunicación.',1,1),(4,'WiFi','El WiFi permite conectar dispositivos sin cables mediante ondas de radio. Un punto de acceso recibe la señal y la integra a la red. La seguridad de esa conexión depende del cifrado y de la clave que se use.',1,1),(5,'Procesador','El procesador ejecuta las instrucciones y coordina el trabajo del equipo. Dentro tiene memorias muy rápidas y se comunica con el resto de los componentes. Su rendimiento depende de varios factores, no solo de la velocidad que muestra la caja.',2,1),(6,'Dispositivos de entrada/salida','Los dispositivos de entrada permiten ingresar datos y los de salida muestran el resultado. Algunos cumplen las dos funciones, como una pantalla táctil. El almacenamiento también forma parte del hardware y guarda la información.',2,1),(7,'Memoria RAM','La memoria RAM es el espacio de trabajo del equipo: guarda lo que se está usando en ese momento. Es rápida y volátil, por eso los datos se pierden al apagar. Cuando falta, el sistema puede apoyarse en el disco con la memoria virtual.',2,1),(8,'Navegadores Web','El navegador es el programa que pide las páginas y las muestra en pantalla. Guarda cookies, caché e historial para que la navegación sea más rápida y cómoda. También ofrece modos y opciones de privacidad que conviene conocer.',3,1),(9,'URL','Una URL es la dirección de un recurso en Internet y tiene varias partes. El protocolo indica cómo se pide, el dominio identifica al servidor y la ruta señala el recurso. Los parámetros agregan datos a la consulta.',3,1),(10,'Conectividad','La conectividad depende de varios factores: la velocidad, la latencia y la calidad de la red. El ancho de banda mide cuánto puede pasar y la latencia cuánto tarda. Los códigos HTTP, por su parte, informan cómo respondió el servidor.',3,1),(11,'Contraseña','Las contraseñas protegen las cuentas y deben ser largas, únicas y difíciles de adivinar. Un gestor y la autenticación de dos factores ayudan a cuidarlas. Compartirlas o repetirlas aumenta el riesgo.',4,1),(12,'Phishing','El phishing reúne engaños que buscan robar información haciéndose pasar por alguien confiable. Llega por correo, mensajes o llamadas y suele usar la urgencia. La ingeniería social ataca la confianza de las personas.',4,1),(13,'Sistema Operativo','El sistema operativo administra el hardware y permite ejecutar los programas. Su núcleo, el kernel, coordina la memoria, el procesador y los dispositivos. Los procesos y los hilos son parte de esa administración.',5,1),(14,'Dispositivos Móviles','Los teléfonos y las tabletas usan sistemas operativos móviles como Android e iOS. Cada aplicación pide permisos para acceder a funciones y datos. Instalar solo desde la tienda oficial reduce riesgos.',5,1);
/*!40000 ALTER TABLE `tema` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

