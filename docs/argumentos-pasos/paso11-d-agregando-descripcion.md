# Paso 11d — Descripciones breves en las preguntas

> **Origen:** pedido posterior al `paso11c`, antes del `paso12`.
> **Tipo:** feat (contenido).
> **Requiere:** `paso11c` aprobado.
> **Commit:** `feat: descripciones de preguntas`.
>
> **Antes de empezar:** leé `AGENTS.md` (decisión 15 y reglas de contenido),
> `bd/schema.sql`, `app/templates/estacion.html` y
> `app/servicios/estaciones.py`.

## Estado

Implementado y verificado el 12/11/2026. Los seeds `002` y `003` cargan las 60
descripciones, los tests pasan dos veces seguidas con 90 casos y la base real
quedó cargada con respaldo previo.

## Contexto

La aplicación **ya tiene todo listo para mostrar una descripción debajo de cada
pregunta**; lo único que falta es el contenido:

- `bd/schema.sql` define `pregunta.descripcion TEXT NULL`.
- `app/servicios/estaciones.py` trae `p.descripcion` en la consulta de la
  estación y la entrega como `pregunta["descripcion"]`.
- `app/templates/estacion.html` la renderiza debajo del enunciado, dentro de la
  misma tarjeta:

  ```jinja
  {% if pregunta.descripcion %}
    <p class="text-body-secondary">{{ pregunta.descripcion }}</p>
  {% endif %}
  ```

- El panel de administración ya permite editarla
  (`/admin/preguntas/<id>/editar`, campo **Descripción**, hasta 2000
  caracteres).
- Los seeds `002` y `003` cargan las descripciones de `intermedio` y
  `avanzado`; el seed `001` mantiene `NULL` en las 20 preguntas de `inicial`.

La descripción es una **mini ayuda de contexto**, no una pista. Las pistas de
papel siguen viviendo en `docs/pistas-del-juego.md` y la app no muestra su
texto (decisión 15).

## Reglas de redacción

- Una o dos oraciones, entre 60 y 200 caracteres, en español rioplatense.
- Explica el concepto o da contexto; **no nombra la opción correcta ni la
  parafrasea**.
- No repite el enunciado ni usa listas, HTML, negritas ni comillas tipográficas.
  Tampoco usa punto y coma: el cargador de seeds de las pruebas separa las
  sentencias con `;`.
- Se muestra como texto escapado: escribir solo texto plano.
- `inicial` queda con `NULL` (vacía). No se completa en este paso.

## Alcance

| Archivo | Cambio |
| --- | --- |
| `bd/seeds/002_contenido_intermedio.sql` | Reemplazar el `NULL` de `descripcion` por el texto propuesto en las 30 preguntas de intermedio. |
| `bd/seeds/003_contenido_avanzado.sql` | Reemplazar el `NULL` de `descripcion` por el texto propuesto en las 30 preguntas de avanzado. |
| `bd/seeds/001_contenido_inicial.sql` | **No se toca**: las 20 preguntas de `inicial` quedan con `descripcion = NULL`. |

Detalles técnicos:

- No hay cambios de esquema, de rutas, de servicios ni de plantillas: el campo
  y el render ya existen.
- El `ON DUPLICATE KEY UPDATE` de los seeds 002 y 003 ya incluye
  `descripcion = VALUES(descripcion)`, así que no hace falta modificarlo.
- No se toca `configuracion`, no se habilitan niveles y no se modifican
  preguntas, respuestas ni cobertura.
- Los textos se cargan en el seed y también se aplican a la base real al
  reejecutarlo.

## Contenido cargado

### Intermedio — 30 descripciones

| ID | Estación | Tema | Pregunta | Descripción |
| --- | --- | --- | --- | --- |
| 1001 | Redes | IP | ¿Qué dirección IPv4 es una dirección de loopback? | El loopback es una dirección reservada para que el equipo se hable a sí mismo y pruebe su configuración de red. |
| 1002 | Redes | IP | ¿Cuál es la función principal de una máscara de subred? | Junto con la dirección IP se indica la máscara de subred, que define el tamaño de la red. |
| 1003 | Redes | Router | ¿Qué protocolo asigna direcciones IP automáticamente a los dispositivos de una red? | Cuando un dispositivo se conecta a una red, puede recibir su configuración automáticamente en lugar de cargarla a mano. |
| 1004 | Redes | Redes de computadoras | ¿Cuál es la función principal de un switch en una red LAN? | Dentro de una red local hay equipos que concentran las conexiones y deciden por dónde sale cada trama. |
| 1005 | Redes | WiFi | ¿Qué función cumple un punto de acceso inalámbrico (Access Point)? | Los dispositivos inalámbricos necesitan un equipo que reciba su señal y la conecte con el resto de la red. |
| 1006 | Redes | Redes de computadoras | ¿Qué protocolo traduce nombres de dominio como ejemplo.com a direcciones IP? | Escribir un nombre es más fácil que recordar números y algún servicio tiene que hacer la traducción. |
| 1007 | Hardware | Dispositivos de entrada/salida | ¿Qué función cumple la tecnología SMART en las unidades de almacenamiento? | Los discos modernos registran datos internos sobre su estado y su salud a lo largo del tiempo. |
| 1008 | Hardware | Procesador | ¿Qué puede indicar una pantalla azul recurrente en Windows? | Windows muestra una pantalla azul cuando no puede continuar funcionando por un problema serio. |
| 1009 | Hardware | Dispositivos de entrada/salida | ¿Cuál es la finalidad de realizar una copia de seguridad? | Los datos pueden perderse por fallas, robos o errores. Una copia permite volver atrás. |
| 1010 | Hardware | Procesador | ¿Qué es la pasta térmica? | Entre el procesador y el disipador no deben quedar bolsas de aire: por eso se usa un compuesto especial. |
| 1011 | Hardware | Procesador | ¿Qué tipo de mantenimiento busca evitar fallas futuras? | El mantenimiento puede hacerse antes de que aparezca la falla, después, o para mejorar el rendimiento. |
| 1012 | Hardware | Memoria RAM | ¿Qué significa que la memoria RAM sea volátil? | La RAM es rápida y se usa como espacio de trabajo, pero no está pensada para conservar datos a largo plazo. |
| 1013 | Internet | Navegadores Web | ¿Para qué sirven las cookies de un navegador? | Los sitios necesitan recordar quién sos y qué preferís entre una página y otra. Para eso usan pequeños archivos. |
| 1014 | Internet | Navegadores Web | ¿Qué hace el modo incógnito de un navegador? | El modo incógnito cambia lo que el navegador guarda en el dispositivo, no lo que ve la red ni el proveedor. |
| 1015 | Internet | URL | En la dirección https://www.escuela.edu.ar/aula/notas, ¿qué parte indica el protocolo? | Una URL tiene varias partes: el protocolo, el dominio, la ruta y, a veces, parámetros. |
| 1016 | Internet | URL | ¿Qué indica el dominio en una dirección web? | El dominio es la parte de la URL que se registra y se escribe en el navegador para llegar a un sitio. |
| 1017 | Internet | Conectividad | ¿Qué es el ancho de banda? | No es lo mismo tener más velocidad que más capacidad: el ancho de banda habla de cuánto puede pasar a la vez. |
| 1018 | Internet | Conectividad | ¿Qué significa tener una latencia alta? | La latencia no mide cuántos datos pasan, sino cuánto tardan en llegar. Se nota en videollamadas y juegos en línea. |
| 1019 | Ciberseguridad | Contraseña | ¿Qué es la autenticación de dos factores (2FA)? | Además de la contraseña, algunos servicios piden una segunda prueba para confirmar tu identidad. |
| 1020 | Ciberseguridad | Contraseña | ¿Para qué sirve un gestor de contraseñas? | Recordar decenas de claves distintas es difícil, por eso existen herramientas que las administran por vos. |
| 1021 | Ciberseguridad | Contraseña | ¿Por qué no conviene usar la misma contraseña en varios sitios? | Si una base de datos filtrada contiene tu clave, los atacantes la prueban en otros servicios. |
| 1022 | Ciberseguridad | Phishing | ¿Qué es el smishing? | El prefijo sms- da una pista: el engaño usa mensajes de texto o de aplicaciones de mensajería. |
| 1023 | Ciberseguridad | Phishing | ¿Qué es el vishing? | El prefijo vishing viene de voz: el contacto se hace por teléfono. |
| 1024 | Ciberseguridad | Phishing | Recibís un correo urgente con un enlace que pide tus datos. ¿Qué conviene hacer? | Los pedidos urgentes por correo suelen buscar que actúes sin pensar. Ante la duda, frená y verificá. |
| 1025 | Sistemas Operativos | Sistema Operativo | ¿Qué es un proceso? | Un programa guardado en el disco no hace nada hasta que el sistema lo carga y lo pone a ejecutar. |
| 1026 | Sistemas Operativos | Sistema Operativo | ¿Qué hace el sistema de archivos? | El sistema operativo necesita una forma de ordenar los datos en el disco y de encontrarlos después. |
| 1027 | Sistemas Operativos | Sistema Operativo | ¿Para qué sirven los permisos de usuario? | En un equipo pueden trabajar varias personas: el sistema decide quién puede hacer qué con cada archivo. |
| 1028 | Sistemas Operativos | Sistema Operativo | ¿Por qué conviene instalar las actualizaciones del sistema? | El software cambia y aparecen fallas nuevas. Los fabricantes publican correcciones periódicamente. |
| 1029 | Sistemas Operativos | Dispositivos Móviles | ¿Qué son los permisos de una aplicación móvil? | Las aplicaciones móviles piden acceso a funciones del teléfono y a datos personales. |
| 1030 | Sistemas Operativos | Dispositivos Móviles | ¿Cuál es la diferencia principal entre Android e iOS? | Android e iOS tienen interfaces, tiendas y formas de actualización diferentes. |

### Avanzado — 30 descripciones

| ID | Estación | Tema | Pregunta | Descripción |
| --- | --- | --- | --- | --- |
| 3001 | Redes | Router | ¿Qué protocolo permite asignar automáticamente direcciones IP a los dispositivos de una red? | Cuando un equipo se conecta a la red, puede pedir su configuración automáticamente en lugar de escribirla a mano. |
| 3002 | Redes | Router | ¿Qué dispositivo trabaja principalmente en la capa 3 del modelo OSI? | El modelo OSI tiene siete capas y cada dispositivo trabaja principalmente en una de ellas. |
| 3003 | Redes | IP | ¿Qué función cumple el protocolo ARP en una red IPv4? | En IPv4, para enviar datos dentro de la red local hay que conocer la dirección física (MAC) del destinatario. |
| 3004 | Redes | Redes de computadoras | ¿Cuál es la diferencia principal entre TCP y UDP? | TCP y UDP son dos formas de transportar datos: una prioriza la confiabilidad y la otra la velocidad. |
| 3005 | Redes | Router | ¿Qué hace NAT en una red? | Las redes domésticas usan direcciones privadas que no existen en Internet, y algo tiene que traducirlas al salir. |
| 3006 | Redes | WiFi | ¿Qué mejora WPA3 respecto de WPA2? | Las versiones de WPA se suceden para corregir debilidades de las anteriores. |
| 3007 | Hardware | Procesador | ¿Qué componente del procesador almacena datos e instrucciones de acceso frecuente para acelerar su funcionamiento? | Dentro del procesador hay memorias muy pequeñas y rápidas que guardan lo que se usa más seguido. |
| 3008 | Hardware | Memoria RAM | ¿Qué diferencia principal existe entre la memoria SRAM y la DRAM? | SRAM y DRAM son dos tipos de memoria que se diferencian por cómo conservan la información y por su costo. |
| 3009 | Hardware | Dispositivos de entrada/salida | ¿Qué tecnología utilizan los SSD para distribuir el desgaste entre sus celdas de memoria? | La memoria flash se desgasta con las escrituras, por eso los SSD aplican técnicas de administración interna. |
| 3010 | Hardware | Procesador | ¿Qué característica de PCI Express permite aumentar la velocidad de transferencia de datos? | PCI Express conecta placas y periféricos con varios carriles que pueden trabajar en paralelo. |
| 3011 | Hardware | Dispositivos de entrada/salida | ¿Qué diferencia principal hay entre un HDD y un SSD? | Un HDD y un SSD guardan datos, pero usan tecnologías de almacenamiento distintas. |
| 3012 | Hardware | Memoria RAM | ¿Qué es la memoria virtual? | El sistema operativo administra la memoria disponible y puede apoyarse en el almacenamiento cuando hace falta. |
| 3013 | Internet | Conectividad | ¿Qué función cumple el sistema DNS? | Los equipos se comunican con números, pero las personas recuerdan mejor los nombres. |
| 3014 | Internet | Conectividad | ¿Qué significa el código de estado HTTP 403? | Los códigos HTTP empiezan con 4 cuando el problema está del lado del cliente o de sus permisos. |
| 3015 | Internet | Conectividad | ¿Qué diferencia principal existe entre HTTP y HTTPS? | HTTP y HTTPS se parecen en la dirección, pero no en cómo viaja la información. |
| 3016 | Internet | Conectividad | ¿Qué significa el código de estado HTTP 404? | Los códigos 4xx indican que el pedido no pudo completarse, y el número exacto identifica el motivo. |
| 3017 | Internet | Navegadores Web | ¿Qué es la caché del navegador? | El navegador guarda copias de imágenes, estilos y scripts para no descargarlos de nuevo en cada visita. |
| 3018 | Internet | URL | En una dirección como https://tienda.com/productos?categoria=ofertas, ¿qué indica la parte que comienza con el signo de interrogación? | En una URL, después del signo de interrogación se envían datos adicionales al servidor. |
| 3019 | Ciberseguridad | Contraseña | ¿Qué es un ataque de fuerza bruta? | Consiste en probar combinaciones una tras otra, muchas veces con programas automáticos. |
| 3020 | Ciberseguridad | Phishing | ¿Qué es un ataque Man-in-the-Middle (MitM)? | En este ataque hay tres partes: la víctima, el destino y alguien que se coloca en el medio. |
| 3021 | Ciberseguridad | Phishing | ¿Qué caracteriza a una vulnerabilidad Zero-Day? | Las vulnerabilidades se descubren y se corrigen, pero algunas aparecen antes de que exista una solución. |
| 3022 | Ciberseguridad | Phishing | ¿Qué propiedad de la seguridad informática garantiza que los datos no sean modificados sin autorización? | Además de evitar filtraciones, la seguridad busca que la información no se altere y que esté disponible cuando se la necesita. |
| 3023 | Ciberseguridad | Phishing | ¿Qué es el ransomware? | Existen malware que buscan un beneficio económico directo y otros que solo causan daño. |
| 3024 | Ciberseguridad | Phishing | ¿Qué es la ingeniería social? | El eslabón más débil suele ser la persona: se la puede manipular con confianza, miedo o urgencia. |
| 3025 | Sistemas Operativos | Sistema Operativo | ¿Qué función cumple el kernel de un sistema operativo? | El sistema operativo tiene una parte central con permisos especiales sobre el hardware. |
| 3026 | Sistemas Operativos | Sistema Operativo | ¿Qué es un proceso zombie en Linux? | En Linux, la tabla de procesos también registra estados de procesos que ya no se están ejecutando. |
| 3027 | Sistemas Operativos | Sistema Operativo | ¿Qué algoritmo de planificación asigna un intervalo de tiempo a cada proceso? | Los sistemas operativos reparten el procesador entre los procesos, y algunos algoritmos usan turnos. |
| 3028 | Sistemas Operativos | Sistema Operativo | ¿Qué ocurre cuando se produce un Deadlock o interbloqueo? | Cuando varios procesos comparten recursos, una mala coordinación puede dejar a todos esperando. |
| 3029 | Sistemas Operativos | Sistema Operativo | ¿Qué diferencia hay entre un proceso y un hilo? | Dentro de un programa puede haber varias tareas a la vez, y conviene distinguir cómo se agrupan. |
| 3030 | Sistemas Operativos | Dispositivos Móviles | ¿Por qué es riesgoso instalar aplicaciones fuera de la tienda oficial? | Instalar desde fuera de la tienda oficial saltea la revisión de la empresa que fabrica el sistema. |

## Proceso

1. Reemplazar `NULL` por cada texto en la lista de preguntas de
   `bd/seeds/002_contenido_intermedio.sql` y `bd/seeds/003_contenido_avanzado.sql`.
2. Verificar que ningún texto nombre una opción ni coincida con la respuesta
   correcta.
3. Ajustar las pruebas (ver abajo).
4. Cargar los seeds en la base de test con `pytest` y en la base real con
   `mysql`, con respaldo previo.
5. Agregar el paso al índice de `docs/argumentos-pasos/README.md` y actualizar
   `MEMORY.md`.
6. Revisar una estación de `intermedio` y una de `avanzado` en el navegador:
   la descripción debe verse debajo del enunciado, antes de las opciones.

## Pruebas

- `tests/test_seed.py`:
  - 30 preguntas `intermedio` y 30 `avanzado` activas con `descripcion` no
    nula y no vacía.
  - Las 20 preguntas `inicial` siguen con `descripcion IS NULL`.
  - Reejecutar los seeds no duplica filas ni cambia `activo`.
- `tests/test_reglas_juego.py` (o el test de estación que corresponda):
  - Una estación de `intermedio` incluye el texto de la descripción en el HTML.
  - Una estación de `inicial` no muestra el párrafo de descripción.
  - El HTML no expone la respuesta correcta.
- `pytest -q` pasa dos veces seguidas (la suite actual es de 88 tests; con
  estos casos queda en 90 o los que resulten).

## Criterio de aceptación

- Las 30 preguntas de `intermedio` y las 30 de `avanzado` tienen descripción
  visible debajo del enunciado.
- Las 20 preguntas de `inicial` quedan sin descripción (`NULL`).
- Ninguna descripción nombra la opción correcta ni la parafrasea.
- Los seeds siguen siendo idempotentes y no cambian `activo`, respuestas ni
  `configuracion`.
- La estación se sigue viendo bien en el móvil y la tarjeta no crece de más.
- `pytest -q` pasa dos veces seguidas.

## Verificación

```bash
mysql -u <usuario> -p < bd/seeds/002_contenido_intermedio.sql
mysql -u <usuario> -p < bd/seeds/002_contenido_intermedio.sql
mysql -u <usuario> -p < bd/seeds/003_contenido_avanzado.sql
mysql -u <usuario> -p < bd/seeds/003_contenido_avanzado.sql
.venv/bin/python -m pytest -q
.venv/bin/python -m pytest -q
```

Consulta de control:

```sql
SELECT dificultad,
       COUNT(*) AS total,
       SUM(descripcion IS NOT NULL AND descripcion <> '') AS con_descripcion
FROM pregunta
WHERE activo = 1
GROUP BY dificultad
ORDER BY FIELD(dificultad, 'inicial', 'intermedio', 'avanzado');
```

Resultado esperado:

| dificultad | total | con_descripcion |
| --- | --- | --- |
| inicial | 20 | 0 |
| intermedio | 30 | 30 |
| avanzado | 30 | 30 |

## Fuera de alcance

- Cambiar el esquema: `pregunta.descripcion` ya existe.
- Tocar `estacion.html`, los servicios o las rutas.
- Mostrar el texto de las pistas en la aplicación.
- Agregar descripciones a `inicial`.
- Tooltips, modales, acordeones o cualquier componente nuevo.
- Cambiar preguntas, respuestas, cobertura, tiempos o reglas.
- Agregar dependencias o CDN.

## Ojo con

- La descripción **no es una pista**: no debe resolver la pregunta. Las pistas
  de papel siguen aparte y la app no las muestra.
- Reejecutar los seeds 002 y 003 **pisa** lo que se haya editado desde
  `/admin` en `descripcion`, igual que con el título. Si el docente quiere
  editar a mano, no se reejecutan los seeds.
- Mantener los textos por debajo de 200 caracteres: son una línea de contexto,
  no un párrafo.
- No usar comillas tipográficas ni HTML: se renderiza como texto escapado.
- No cargar en la base real sin respaldo previo ni con intentos activos.
- `inicial` queda vacía a propósito: el nivel se juega sin ayuda extra.
