# Feria de Producción del IPEATyM 186 Castagnari - 2026

El curso de séptimo año B de la especialidad de Informatica Profesional y Personal va a presentar el proyecto denominado Escape Room, el cual consiste en abordar los conceptos de los espacios curriculares de la especialidad, y un enfoque sencillo y más general de la espacialidad y que este tipo de abordaje de los contenidos sea mediante un juego.

## El Juego de Escape Room

Escape Room es un juego donde de a grupos de no más de 4 integrantes puedan participar, responder diversas preguntas sobre 5 tematicas de la especialidad las cuales estarán organizadas por estaciones. Una vez respondan bien las 4 preguntas de una estación, podrán pasar a la siguiente estación.

En cada estación estarán acompañados por un par de estudiantes de 7mo B que pueden ayudarlos si desean obtener alguna pista. Tener en cuenta que si realizan 2 respuestas incorrectas de las 4 preguntas de una estación, el equipo participante queda afuera del juego.

Otra forma de quedar fuera del juego es si no logran avanzar de estación en el tiempo establecido para cada estación, que es de 4 minutos, o si deciden abandonar el mismo.

Una vez completan las 5 estaciones el sistema les otorgará un puntaje al equipo y mostrara en que ranking se encuentran.

### El Sistema de puntaje de Escape Room

El puntaje de los equipos que han logrado llegar al final estará dado por el tiempo que les resulto llegar a completar las 5 estaciones. Asi mismo, si han tenido ayudas, se registrarán, asi como las resuestas incorrectas y entre equipos que hayan demorado lo mismo, tiene mejor ranking el que menos respuestas incorrectas y ayudas haya tenido.

Reglas operativas:

1. Formen un equipo: trabajen juntos y escuchen las ideas de todos los integrantes.
2. Respeten el tiempo: tendrán un tiempo límite para resolver todos los desafíos.
3. Resuelvan las misiones en orden: cada desafío les permitirá avanzar en la historia.
4. Lean atentamente: analicen las preguntas y las pistas antes de elegir una respuesta .
5. Pidan pistas con cuidado: cada equipo podrá solicitar hasta 2 pistas por estación durante el juego.
6. Colaboren y respeten: todos los integrantes deben participar y respetar las opiniones de sus compañeros.
7. ¡Completen la misión!: gana el equipo que resuelva correctamente los desafíos en el menor tiempo establecido, ante empates, ganan quienes tengan menos ayudas y menos respuestas incorrecta.

## Escape Room en la Feria: Presentación y Metodologia de juego

Escape Room contara con una presentación en un stand, el mismo contara con una web explicativa e infografias sobre los temas: Redes de computadoras, Hardware, Internet, Ciberseguridad y Sistemas Operativos. Los estudiantes explicarán los temas y la propuesta de participar del juego. Quienes deseen participar del juego deben anotarse, los estudiantes de 7B iran registrando los equipos, y a medida que puedan ir al aula que se encuentra decorada con el escape room, iran participando. Al disponer de 5 estaciones, no podrán estar participando más de 3 equipos simultaneamente. Cuando un equipo paso a la tercer estación, recien ahi puede entrar otro equipo a participar, iniciando por la estación 1. Siempre es el recorrido por estaciones de la misma manera, de la estacion 1 a la 5.

Cada equipo participa utilizando una notebook que le daran los estudiantes de 7B.

Habra una notebook conectada al televisor del aula donde mostrará en todo momento la aplicación web de escape room, por lo general mostrando el ranking de los equipos.

## La aplicación de Escape Room

La aplicación de escape room es una aplicación web que posee el siguiente stack:

* html
* bootstrap como framework de estilos
* python y flask
* mysql como gestor de base de datos

La aplicación se basa en la primer idea bosquejo que se encuentra en docs/src/index.html y que contiene 5 formularios, 1 por cada estación. Cada formulario posee 4 preguntas y un control de que deben estar todas correctas para pasar al siguiente escenario.

La app debe ser lo más limpia de código posible, pocos estilos de bootstrap, los necesarios.

La aplicación debe ser considerando las siguientes pautas:

Mostrar siempre el tiempo general que va incrementando, y el tiempo del escenario que inicia en 4 minutos y va decrementando. Faltando 30 segundos para llegar a 0 el contador del escenario debe emitir un audio de aviso y dejar titilando un texto debajo del contador. En cada página de estación debe mostrarse cantidad de ayudas, cantidad de respuestas incorrectas, cantidad de intentos de envio del formulario (si llega a 2 solo se deja el boton de finalizar juego por respuestas incorrectas).

Debe haber una página por cada escenario, una página inicial de bienvenida a escape room donde se le pida en un formulario pequeño, el nombre del equipo y el nivel de dificultad utilizado (inicial, intermedio, avanzado). Además debe haber una página de finalización del juego que debe ser basada en la de ranking-puntajes/ranking-puntajes.html donde se muestre por orden los equipos desde el que mas puntos tiene (menor tiempo para completar los escenarios, y a igualdad de tiempo, el de menos ayuda e incorrectas). Y una página estadisticas del juego donde pueda mostrar algunos datos y/o graficos estadisticos como cantidad de participantes, cantidad de intentos, tiempo promedio por intento, cantidad de respuestas realizadas / cantidad de respuestas correctas.

La base de datos de la aplicación debe ser en mysql. Debe poder representar:
Equipos (id, nombre, cantidadPersonas), Intento (id, equipo, fechaInicio, FechaFin, seCompletoOK[boolean] , cantidadAyudas, puntajeObtenido, finalizado [completo, abandono, porRespuestasIncorrectas, porTiempo], ultimaEstacionVisitada), Estacion (id, nombre, descripcion), Temas dentro de una estación (id, nombre, estacion), preguntas vinculadas a cada tema (id, titulo, descripcion, tema, dificultad [inicial, intermedio, avanzado]), respuestas a cada pregunta (id, contenido, correcta[boolean], pregunta), y RespuestaElegida(id, fechaRespondida, intento, respuesta). Agregar una tabla para las respuestas incorrectas en una tabla incorrectas(id, pregunta, respuestaElegida, fecha, intento) que se registrara cuando se envie un formulario y la respuesta no sea correcta.

Por ejemplo: una estacion sera redes, un tema seria IP o router. Las preguntas sobre IP pueden ser de distintos niveles de dificultad. Un equipo puede realizar muchos intentos. El puntaje esta vinculado a un intento. Se guardan todas las elecciones de respuestas que realice un equipo en un intento (pensando en permitir que puedan avanzar con una respuesta incorrecta por ejemplo, cuestión que por el momento no es necesario).

La aplicación debe tener una parte administrativa que no es accesible de manera navegable desde el index de la app, sino que solo si uno escribe /admin. Alli se debe pedir usuario y clave, y esto permitira ingresar a un panel de control, donde mostrar en cards de bootstrap la gestión a las distintas tablas de la base de datos sumado a unos graficos estadisticos sobre equipos participantes, intentos finalizados, tiempo promedio de cada estacion y de los intentos finalizados, sobre las preguntas mostrar el % de utilización sobre el total de los intentos (completados o no), porcentaje de aciertos. Desde esta parte administrativa debe permitir el crud de cada tabla, y en la visualización de los datos, permitir filtros y ordenamientos de la tabla según id y algunos campos más. Asi, si se desea agregar más preguntas sobre cada tema, vinculadas a una dificultad, sea posible añadirlas.

La administración de la aplicación debe permitir habilitar o deshabilitar las dificultades intermedias y avanzadas. A su vez, la cantidad de las preguntas por tema por nivel deben ser minimo 4, pero si son más, deben mostrarse en los intentos como aleatorias.

#### Repositorio en git

escape-room-7B2026

Aplicación para Feria de Producciones - 13 de noviembre de 2026

---

## Anexo: contenido inicial (nivel inicial)

Este anexo detalla el contenido que se carga con `bd/seeds/001_contenido_inicial.sql`. El texto de las preguntas y opciones se tomó de `docs/ESCAPE ROOM.pdf`, corrigiendo tildes, mayúsculas y errores de tipeo.

Notas:

- Para esta edición se usa la regla operativa de `AGENTS.md`: **al menos 1 pregunta por tema activo y 4 preguntas por estación**. La regla literal de "mínimo 4 preguntas por tema" no se aplica porque el contenido disponible no alcanza para cubrirla.
- Solo se carga el nivel **`inicial`**. Los niveles `intermedio` y `avanzado` quedan deshabilitados en `configuracion` hasta que el admin cargue cobertura completa.
- Las pistas del PDF **no se cargan en la base ni se muestran en la aplicación**. Los estudiantes de 7.º las leen en papel; la app solo registra si el equipo pidió 1 o 2 ayudas por estación.
- Cada pregunta tiene 3 opciones y una sola respuesta correcta.

### Estación 1: Redes

Temas (4): IP, Router, Redes de computadoras, WiFi.


| # | Tema                  | Pregunta                                           | Opciones                                                                                        | Correcta                               |
| --- | ----------------------- | ---------------------------------------------------- | ------------------------------------------------------------------------------------------------- | ---------------------------------------- |
| 1 | IP                    | ¿Qué significa IP?                               | Internet personal / Internet Protocol / Información privada                                    | Internet Protocol                      |
| 2 | Router                | ¿Qué dispositivo conecta diferentes redes?       | Teclado / Router / Monitor                                                                      | Router                                 |
| 3 | Redes de computadoras | ¿Qué es una red informática?                    | Un conjunto de dispositivos conectados / Un programa para dibujar / Una pieza de la computadora | Un conjunto de dispositivos conectados |
| 4 | WiFi                  | ¿Qué se necesita para conectarse a una red WiFi? | Una contraseña, si está protegida / Un cable HDMI obligatoriamente / Una impresora            | Una contraseña, si está protegida    |

### Estación 2: Hardware

Temas (3): Procesador, Dispositivos de entrada/salida, Memoria RAM.


| # | Tema                           | Pregunta                                                       | Opciones                                                                                                  | Correcta                                        |
| --- | -------------------------------- | ---------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------- | ------------------------------------------------- |
| 5 | Procesador                     | ¿Qué componente es considerado el cerebro de la computadora? | Teclado / Procesador / Monitor                                                                            | Procesador                                      |
| 6 | Dispositivos de entrada/salida | ¿Cuál es un dispositivo de entrada?                          | Monitor / Parlante / Teclado                                                                              | Teclado                                         |
| 7 | Memoria RAM                    | ¿Para qué sirve la memoria RAM?                              | Guardar datos temporalmente mientras se trabaja / Imprimir documentos / Proteger físicamente la pantalla | Guardar datos temporalmente mientras se trabaja |
| 8 | Dispositivos de entrada/salida | ¿Cuál es un dispositivo de salida?                           | Ratón / Micrófono / Monitor                                                                             | Monitor                                         |

### Estación 3: Internet

Temas (3): Navegadores Web, URL, Conectividad.


| #  | Tema            | Pregunta                                                             | Opciones                                                                                   | Correcta                                 |
| ---- | ----------------- | ---------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- | ------------------------------------------ |
| 9  | Navegadores Web | ¿Qué es un navegador web?                                          | Un programa para visitar páginas web / Una parte del procesador / Un cable de red         | Un programa para visitar páginas web    |
| 10 | Navegadores Web | ¿Cuál de estos es un navegador web?                                | Google Chrome / Windows / Calculadora                                                      | Google Chrome                            |
| 11 | URL             | ¿Qué significa URL?                                                | Una dirección de un recurso en internet / Una memoria de computadora / Un tipo de teclado | Una dirección de un recurso en internet |
| 12 | Conectividad    | ¿Qué se necesita para acceder a un sitio web público en internet? | Una conexión a internet / Un escáner obligatoriamente / Un pendrive siempre              | Una conexión a internet                 |

### Estación 4: Ciberseguridad

Temas (2): Contraseña, Phishing.


| #  | Tema        | Pregunta                                         | Opciones                                                                                             | Correcta                                      |
| ---- | ------------- | -------------------------------------------------- | ------------------------------------------------------------------------------------------------------ | ----------------------------------------------- |
| 13 | Contraseña | ¿Cómo debe ser una contraseña segura?         | 123456 / Tu nombre solamente / Larga y difícil de adivinar                                          | Larga y difícil de adivinar                  |
| 14 | Phishing    | ¿Qué deberías hacer con un enlace sospechoso? | Abrirlo inmediatamente / Evitar abrirlo y verificar su origen / Compartirlo con todos                | Evitar abrirlo y verificar su origen          |
| 15 | Phishing    | ¿Qué es el phishing?                           | Un intento de engaño para robar información / Un programa para editar fotos / Una clase de monitor | Un intento de engaño para robar información |
| 16 | Contraseña | ¿Qué conviene hacer con tus contraseñas?      | Compartirlas con desconocidos / Usar la misma en todos lados / Mantenerlas privadas                  | Mantenerlas privadas                          |

### Estación 5: Sistemas Operativos

Temas (2): Sistema Operativo, Dispositivos Móviles.


| #  | Tema                  | Pregunta                                                 | Opciones                                                                                                                    | Correcta                                           |
| ---- | ----------------------- | ---------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------- |
| 17 | Sistema Operativo     | ¿Qué es un sistema operativo?                          | El software que administra la computadora / Un cable de alimentación / Una aplicación para dibujar                        | El software que administra la computadora          |
| 18 | Sistema Operativo     | ¿Cuál de estos es un sistema operativo?                | Microsoft Word / Windows / Google Chrome                                                                                    | Windows                                            |
| 19 | Sistema Operativo     | ¿Para qué sirve un sistema operativo?                  | Administrar recursos y permitir ejecutar programas / Solo para cambiar el color del monitor / Solo para escribir documentos | Administrar recursos y permitir ejecutar programas |
| 20 | Dispositivos Móviles | ¿Cuál de estos es un sistema operativo para celulares? | Android / PowerPoint / Excel                                                                                                | Android                                            |

### Resumen de cobertura


| Estación           | Temas  | Preguntas iniciales |
| --------------------- | -------- | --------------------- |
| Redes               | 4      | 4                   |
| Hardware            | 3      | 4                   |
| Internet            | 3      | 4                   |
| Ciberseguridad      | 2      | 4                   |
| Sistemas Operativos | 2      | 4                   |
| **Total**           | **14** | **20**              |

Configuración inicial cargada por el seed:


| Clave                              | Valor |
| ------------------------------------ | ------- |
| `dificultad_intermedia_habilitada` | `0`   |
| `dificultad_avanzada_habilitada`   | `0`   |
| `duracion_estacion_segundos`       | `240` |
| `max_ayudas_estacion`              | `2`   |
| `max_envios_estacion`              | `2`   |
| `max_respuestas_incorrectas`       | `2`   |
| `max_integrantes_equipo`           | `4`   |
| `max_temas_por_estacion`           | `4`   |
| `preguntas_por_estacion`           | `4`   |
