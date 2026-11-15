# Paso 15 — Escape room de Conexión de Redes Extendidas

> **Origen:** pedido posterior a la feria del 16/11/2026, para reutilizar la
> aplicación con el contenido del espacio curricular *Conexión de Redes
> Extendidas*.
> **Tipo:** contenido + documentación (post-feria, aislado).
> **Requiere:** la feria terminada y el `paso12` funcionando. El `paso14`
> (Docker) es independiente.
> **Commit propuesto:** `docs: paso15 escenario de redes extendidas`.
>
> **Antes de empezar:** leé `AGENTS.md`, `MEMORY.md`, `bd/schema.sql`,
> `bd/seeds/001_contenido_inicial.sql`, `bd/seeds/002_contenido_intermedio.sql`,
> `docs/pistas-del-juego.md` y este archivo completo.

## Importante

Este paso **no modifica el escape room existente**. La aplicación que se usa en
la feria sigue funcionando igual, con la base `escape_room_7b2026`, sus 80
preguntas y su contenido congelado.

Lo que se agrega es un **segundo contenido** en otra base de datos, para
probarlo después y, si sirve, jugarlo con otro grupo. Si algo de este paso sale
mal, se descarta la base `escape_room_redes_2026` y el juego original no se
enteró.

**Regla de oro:** ante la duda entre "tocar el juego" y "no tocar el juego", no
se toca.

## Aislamiento: qué se toca y qué no

### No se modifica bajo ninguna circunstancia

| Ruta | Motivo |
| --- | --- |
| `app/` (rutas, servicios, plantillas, estáticos) | El juego en producción depende de esto |
| `tests/` | La suite valida el juego actual |
| `scripts/feria.sh`, `scripts/generar-pdfs.sh`, `scripts/backup.sh`, `scripts/restaurar.sh` | Herramientas de la feria ya probadas |
| `bd/schema.sql` | Se **lee**, nunca se escribe |
| `bd/seeds/001–003` | Contenido congelado del juego original |
| `bd/escape_room_7b2026_completa.sql` | Instantánea del juego original |
| `bd/migraciones/` | Migraciones ya aplicadas |
| Base `escape_room_7b2026` y su contenido | Datos reales de la feria |
| `docs/material/conexiones-de-redes-extendidas/*.pdf` | Material de origen del docente |

### Archivos nuevos

```
bd/contenido/redes-extendidas/
  001_inicial.sql            # 5 estaciones, 10 temas, 200 preguntas, 800 respuestas
  002_intermedio.sql         # 200 preguntas y 800 respuestas
  003_avanzado.sql           # 200 preguntas y 800 respuestas
  README.md                  # cómo crear la base y cargar el contenido

docs/material/conexiones-de-redes-extendidas/
  material-de-estudio-y-control.md   # generado desde la base, con respuestas
  pistas-del-juego-redes.md          # 600 pistas para leer en papel

docs/material/
  como-adaptar-el-escape-room.md     # guía general de adaptación
```

### Archivos que se actualizan (solo cuando el contenido esté terminado y aprobado)

- `README.md`: una sección corta **Segundo contenido: Conexión de Redes
  Extendidas** con los comandos de carga y el arranque con `MYSQL_DB`. No se
  reescribe nada de lo existente.
- `AGENTS.md`: una decisión nueva (70) que registre el segundo contenido y su
  aislamiento.
- `MEMORY.md`: estado del paso.
- `docs/pdf/`: los PDF de los tres documentos nuevos. Se generan solo con esos
  argumentos, para no rehacer los 48 PDF actuales.

Si el contenido no llega a buen puerto, estos cuatro puntos no se hacen y el
paso se cierra sin rastro.

## Contexto

El espacio curricular *Conexión de Redes Extendidas* (7.º B, IPEATyM 186,
profesor Julián Conde) trabaja redes de computadoras y los modelos OSI y TCP/IP.
El material de origen está en `docs/material/conexiones-de-redes-extendidas/`:

- `PROGRAMA de CONEXION DE REDES EXTENDIDAS 2026 - CONDE JULIAN.pdf` (6 ejes
  temáticos y contenidos prioritarios).
- `Planificación Anual 2026 - Conexiones de redes extendidas - CONDE JULIAN.pdf`.
- `cuadernillos/`: 1, 2, 2.1 (capa transporte) y 3.
- `bibliografia/`: Kurose, transcripciones de Paulo Colomé (capa física, enlace,
  red, transporte, aplicación, HTTP/HTTPS, DNS, direccionamiento IPv4 e IPv6) y
  material de secundaria.

La aplicación ya es agnóstica al contenido: los nombres de estación, los temas,
las preguntas y las explicaciones salen de la base. Cambiando `MYSQL_DB` cambia
todo el escenario, sin tocar una línea de código.

## Objetivo

Tener un escape room completo y jugable sobre redes, con 5 estaciones, 10 temas y
600 preguntas, en una base propia, más la documentación para jugarlo y para
adaptar el juego a cualquier otro contenido.

## Estructura de contenido: 5 estaciones y 10 temas

Un escenario general y los cuatro niveles de TCP/IP.

| Orden | Estación | Descripción (`estacion.descripcion`, ≤ 255 caracteres) |
| --- | --- | --- |
| 1 | Redes de computadoras | Qué es una red, cómo se clasifica, qué topologías existen y con qué dispositivos se arma. |
| 2 | Acceso a la red | El viaje del bit por el medio físico y el de la trama por el switch. Capa de acceso al medio. |
| 3 | Internet | Direcciones, máscaras y el camino entre redes. Capa de red del modelo TCP/IP. |
| 4 | Transporte | Cómo llegan los datos completos y en orden de punta a punta. Capa de transporte. |
| 5 | Aplicación | Los servicios que se usan todos los días: web, nombres, correo y archivos. |

| Tema | Estación | Nombre del tema | Capas |
| --- | --- | --- | --- |
| 1 | 1 | Conceptos y tipos de redes | General |
| 2 | 1 | Dispositivos y medios de transmisión | General |
| 3 | 2 | Medios físicos y señalización | OSI física |
| 4 | 2 | Capa de enlace y Ethernet | OSI enlace |
| 5 | 3 | Direccionamiento IP | OSI red |
| 6 | 3 | Enrutamiento y servicios de red | OSI red |
| 7 | 4 | TCP y UDP | OSI transporte |
| 8 | 4 | Puertos, conexiones y control | OSI transporte |
| 9 | 5 | Servicios de aplicación | OSI sesión, presentación y aplicación |
| 10 | 5 | Web, nombres y seguridad | OSI aplicación |

### Contenidos por tema

**1. Conceptos y tipos de redes:** concepto de red, Internet/intranet/extranet,
evolución histórica, PAN/LAN/MAN/WAN, topologías (estrella, bus, anillo, malla,
híbrida), cliente, servidor y nodo, modelo OSI y modelo TCP/IP, para qué sirve
cada uno, correspondencia entre capas, ventajas de dividir en capas.

**2. Dispositivos y medios de transmisión:** router, switch, hub, repetidor,
punto de acceso, módem, NIC, medios guiados y no guiados, criterios para elegir
un dispositivo, diferencias entre dispositivos de capa 1, 2 y 3.

**3. Medios físicos y señalización:** par trenzado UTP/STP y categorías, fibra
óptica, coaxial, inalámbrico, estándares 802.3 y 802.11, señal analógica y
digital, atenuación, interferencia, ruido, ancho de banda, medio compartido y
full-duplex.

**4. Capa de enlace y Ethernet:** función de la capa de enlace, trama, dirección
MAC, unicast/broadcast/multicast, switch versus hub, tabla de direcciones MAC,
dominio de colisión y de broadcast, ARP, CSMA/CD, encapsulado y desencapsulado.

**5. Direccionamiento IP:** IPv4, estructura y octetos, IPv6, máscara de subred,
porción de red y de host, dirección de red y de broadcast, direcciones
utilizables, rangos privados y públicos, loopback, CIDR y subredes, puerta de
enlace predeterminada.

**6. Enrutamiento y servicios de red:** función del router, tabla de
enrutamiento, ruta por defecto, salto a salto, enrutamiento estático y dinámico,
NAT, ICMP, `ping`, `traceroute`, DHCP y su relación con la configuración
automática, resolución de nombres como servicio de red.

**7. TCP y UDP:** función de la capa de transporte, segmentación y
reensamblado, TCP orientado a conexión, confiabilidad, UDP no orientado a
conexión, comparación y casos de uso (streaming, DNS, transferencia de archivos,
juegos), puertos conocidos y su relación con los servicios.

**8. Puertos, conexiones y control:** puertos y sockets, three-way handshake,
cierre de conexión, ACK, retransmisión por pérdida, ventana y control de flujo,
control de congestión, números de secuencia, multiplexación por puertos.

**9. Servicios de aplicación:** modelos cliente-servidor y P2P, HTTP y HTTPS,
URL, métodos GET y POST, códigos de estado, DNS y su jerarquía, correo con
SMTP/POP3/IMAP, FTP y SFTP, diferencia entre protocolo y servicio.

**10. Web, nombres y seguridad:** resolución de nombres paso a paso, dominio,
subdominio y FQDN, servidores DNS, caché, TLS y certificados, candado del
navegador, diferencia entre cifrado y autenticación, navegación segura.

## Volumen total

| Concepto | Cantidad |
| --- | --- |
| Estaciones | 5 |
| Temas | 10 (2 por estación) |
| Preguntas por tema y nivel | 20 |
| Preguntas totales | 600 (200 por nivel) |
| Respuestas | 2400 (4 por pregunta, exactamente 1 correcta) |
| Introducciones de tema | 10 |
| Explicaciones | 600 |
| Pistas en papel | 600 (1 por pregunta) |

Con 40 preguntas por estación y por nivel, cada partida sortea 4 de un banco muy
grande: dos equipos que jueguen la misma estación casi no repiten preguntas.

## Base de datos nueva

- Nombre: `escape_room_redes_2026`.
- Esquema: **no se duplica** `bd/schema.sql`. Se aplica con el nombre
  reemplazado al vuelo.
- La base original no se toca ni se lee para esto.

Comandos (quedan documentados en `bd/contenido/redes-extendidas/README.md`,
donde se buscan de verdad, y repetidos en la guía de adaptación):

```bash
sed 's/escape_room_7b2026/escape_room_redes_2026/g' bd/schema.sql | mysql -u <usuario> -p
mysql -u <usuario> -p < bd/contenido/redes-extendidas/001_inicial.sql
mysql -u <usuario> -p < bd/contenido/redes-extendidas/002_intermedio.sql
mysql -u <usuario> -p < bd/contenido/redes-extendidas/003_avanzado.sql
```

Cada seed lleva su propio `USE escape_room_redes_2026;`, igual que los seeds
actuales, para que no haga falta pasar la base como argumento.

Para jugar:

```bash
MYSQL_DB=escape_room_redes_2026 ./scripts/feria.sh
```

Funciona sin tocar el script porque `load_dotenv()` corre con `override=False`:
la variable de entorno gana sobre el `.env`.

**No se crea ningún script nuevo** para esto. Cuatro líneas documentadas son
suficientes y no agregan superficie de mantenimiento.

### Advertencia de sesión

Al cambiar de base con la misma sesión de navegador, la cookie puede traer un
`intento_id` que no existe en la base nueva. Para probar el escenario de redes
conviene abrir una ventana privada o cerrar sesión antes. Va anotado en el README
del contenido porque es la clase de detalle que hace perder diez minutos en el
aula.

## Contrato de los seeds

Copiar el patrón de `bd/seeds/001_contenido_inicial.sql`:

- Encabezado con el uso, la aclaración de idempotencia y la fuente del contenido.
- `USE escape_room_redes_2026;` y `SET NAMES utf8mb4;`.
- Todo dentro de `START TRANSACTION; ... COMMIT;`.
- `INSERT INTO` con **ids fijos** y `ON DUPLICATE KEY UPDATE` de los textos
  (nunca de `activo`: si el admin desactivó algo, sigue desactivado).
- `configuracion` solo con `INSERT IGNORE`, y **solo en el seed 001**.
- Los seeds 002 y 003 no tocan `configuracion` ni habilitan el nivel.
- **Ningún texto lleva punto y coma** (`;`): el cargador de seeds de las pruebas
  separa las sentencias con ese signo. Tampoco HTML.
- Textos en español rioplatense, sin emojis y sin comillas problemáticas.

### Rangos de ids reservados

| Entidad | Rango |
| --- | --- |
| `estacion` | 1–5 |
| `tema` | 1–10 |
| `pregunta` inicial | 1–200 |
| `pregunta` intermedio | 201–400 |
| `pregunta` avanzado | 401–600 |
| `respuesta` | `pregunta_id * 4 - 3` a `pregunta_id * 4` (1–2400) |

Dentro de cada nivel, 40 preguntas por estación, 20 por tema:

| Estación | Tema A | Tema B |
| --- | --- | --- |
| 1 | 1–20 | 21–40 |
| 2 | 41–60 | 61–80 |
| 3 | 81–100 | 101–120 |
| 4 | 121–140 | 141–160 |
| 5 | 161–180 | 181–200 |

En intermedio, sumar 200; en avanzado, 400.

### Ejemplo completo de una pregunta

```sql
INSERT INTO pregunta (id, titulo, descripcion, explicacion, tema_id, dificultad, activo) VALUES
  (405, '¿Qué indica la máscara 255.255.255.0 junto a una dirección IPv4?', 'La máscara acompaña a la dirección IP y marca dónde termina la parte de red.', 'La máscara 255.255.255.0 tiene 24 bits en uno, así que los tres primeros octetos identifican la red y el último identifica al equipo. Por eso esa red admite 254 hosts utilizables. No indica si la dirección es privada ni limita la salida a Internet.', 5, 'avanzado', 1)
ON DUPLICATE KEY UPDATE
  titulo = VALUES(titulo),
  descripcion = VALUES(descripcion),
  explicacion = VALUES(explicacion),
  tema_id = VALUES(tema_id);

INSERT INTO respuesta (id, contenido, correcta, pregunta_id, activo) VALUES
  (1621, 'Que los tres primeros octetos identifican la red y el último al equipo', 1, 405, 1),
  (1622, 'Que el equipo puede usar cualquier dirección de Internet', 0, 405, 1),
  (1623, 'Que la red admite 254 redes distintas', 0, 405, 1),
  (1624, 'Que la dirección es privada y no sale a Internet', 0, 405, 1)
ON DUPLICATE KEY UPDATE
  contenido = VALUES(contenido),
  correcta = VALUES(correcta),
  pregunta_id = VALUES(pregunta_id);
```

## Reglas de redacción del contenido

1. **Una sola respuesta correcta** por pregunta, sin ambigüedad y sin discusión
   posible. Nada de "todas las anteriores" ni "ninguna de las anteriores".
2. **Cuatro opciones** por pregunta, todas verosímiles y de extensión parecida.
   Los distractores salen de confusiones reales del tema, no de inventos.
3. `pregunta.titulo`: la pregunta en sí, hasta 255 caracteres, en una sola línea.
4. `pregunta.descripcion`: ayuda de contexto para `intermedio` y `avanzado`, que
   se muestra debajo del enunciado. **No nombra ni parafrasea la respuesta
   correcta.** En `inicial` queda `NULL`, igual que el juego actual, para que ese
   nivel se juegue sin ayuda extra.
5. `pregunta.explicacion`: justifica la correcta y dice por qué los distractores
   no van. Dos o tres oraciones, hasta dos párrafos, texto plano.
6. `tema.introduccion`: un párrafo que presenta el tema para la card **Lo que
   aprendieron** de la transición. No es pista y no adelanta respuestas.
7. Nada de preguntas de memoria pura tipo "¿en qué año...?" salvo que el año sea
   parte del contenido del programa.
8. Cada pregunta tiene que poder responderse con los cuadernillos y la
   bibliografía de `docs/material/conexiones-de-redes-extendidas/`. Si no se
   puede, la pregunta no entra.
9. **Trazabilidad:** mantener fuera del SQL, en un archivo de trabajo descartable,
   qué eje del programa cubre cada tema. No se guarda en la base.

## Pistas en papel

Documento `docs/material/conexiones-de-redes-extendidas/pistas-del-juego-redes.md`,
con el mismo formato que `docs/pistas-del-juego.md`:

- Organizado por nivel, luego por estación y luego por pregunta, en el mismo
  orden de ids.
- **Una pista por pregunta**: 600 en total. Se decidió así para este escenario,
  aunque el juego original usa dos (fácil y difícil). Si más adelante se quieren
  dos, se agrega una segunda sin tocar la app.
- La pista orienta sin revelar: nombra el concepto o el procedimiento, nunca la
  opción correcta ni su texto.
- La aplicación **no** muestra este texto: solo registra cuántas ayudas se
  pidieron. Las pistas se leen en papel o en pantalla aparte.

## Documentos a escribir

### 1. `material-de-estudio-y-control.md`

**Generado desde la base**, no escrito a mano, siguiendo la decisión 69: un
script descartable en modo solo lectura que lee `escape_room_redes_2026` y
produce el Markdown. Contiene:

- Las 10 introducciones de tema.
- Las 600 preguntas con sus cuatro opciones, la correcta marcada con ✅ y la
  explicación.
- Anexo de cobertura estación × tema × nivel.

**Contiene las respuestas correctas:** es material de estudio y control docente.
No se enlaza desde la aplicación y no se muestra durante la partida. Si se edita
contenido desde `/admin`, hay que regenerarlo.

### 2. `pistas-del-juego-redes.md`

Las 600 pistas, según la sección anterior.

### 3. `como-adaptar-el-escape-room.md`

La guía de adaptación a cualquier contenido. Se escribe para un docente o un
estudiante avanzado y usa este escenario como ejemplo real. Debe cubrir:

1. **Qué es fijo** y no se negocia sin tocar código: 5 estaciones, 4 preguntas
   por estación, 4 minutos, 2 ayudas, 2 envíos, 2 incorrectas, ranking por tiempo.
2. **Qué es variable**: nombres y descripciones de estación, temas, preguntas,
   opciones, explicaciones, introducciones, pistas, dificultades habilitadas y
   parámetros del juego.
3. **Cómo se arma el contenido**: 5 estaciones, hasta 4 temas por estación,
   mínimo 1 pregunta por tema y nivel, mínimo 4 por estación y nivel.
4. **Cómo se escribe un seed** con el contrato de esta página, con ejemplo.
5. **Cómo se crea una base paralela** con `sed` y los seeds, y cómo se arranca
   con `MYSQL_DB`.
6. **Cómo se verifica** la cobertura en `/admin/cobertura` y en
   `/admin/dificultades`, y cómo se habilita un nivel.
7. **Cómo se prueba** una partida completa por nivel en una base descartable,
   antes de dar el contenido por bueno.
8. **Errores típicos**: `;` dentro de los textos, menos de 4 preguntas por
   estación, tema sin cobertura, ids repetidos, dificultad habilitada sin
   cobertura, cookie de sesión con un `intento_id` de otra base.
9. **Qué no se debe hacer**: no mostrar respuestas en el HTML, no guardar las
   pistas en la base, no tocar la base de la feria, no reejecutar seeds después
   de congelar el contenido.

Sin respuestas correctas en los ejemplos, salvo el ejemplo didáctico marcado como
tal.

## Etapas de implementación

Trabajar por tanda y verificar antes de seguir. Si una tanda no convence, se
corrige ahí y no se arrastra el error.

| # | Tanda | Contenido | Verificación |
| --- | --- | --- | --- |
| 1 | Infraestructura | Crear la base, cargar esquema, `README.md` del contenido, estaciones 1–5, temas 1–10, `configuracion` | `/admin/cobertura` responde y marca todo en rojo |
| 2 | Inicial, estación 1 | 40 preguntas (ids 1–40) y 160 respuestas | Estación jugable de punta a punta |
| 3 | Inicial, estaciones 2 a 5 | 160 preguntas (ids 41–200) | Nivel `inicial` completo y habilitable |
| 4 | Intermedio, estaciones 1 a 5 | 200 preguntas (ids 201–400) | Cobertura de intermedio completa |
| 5 | Avanzado, estaciones 1 a 5 | 200 preguntas (ids 401–600) | Cobertura de avanzado completa |
| 6 | Pistas | 600 pistas en el documento nuevo | Revisar que ninguna revele la respuesta |
| 7 | Documentos | Material de estudio generado, guía de adaptación, README/AGENTS/MEMORY, PDFs | PDFs nuevos y `pytest` en verde |

Las tandas 3, 4 y 5 son de 160 a 200 preguntas cada una y se pueden cortar por
estación si hace falta.

## Verificación

### Al terminar cada tanda de contenido

```bash
mysql -u <usuario> -p escape_room_redes_2026 -e "
SELECT e.orden, e.nombre, t.id AS tema, p.dificultad, COUNT(*) AS preguntas
FROM estacion e
JOIN tema t ON t.estacion_id = e.id AND t.activo = 1
JOIN pregunta p ON p.tema_id = t.id AND p.activo = 1
GROUP BY e.orden, e.nombre, t.id, p.dificultad
ORDER BY e.orden, t.id, p.dificultad"
```

Cada combinación tema × nivel tiene que dar 20.

### Al cerrar el paso

- [ ] `escape_room_redes_2026` existe con 5 estaciones, 10 temas, 600 preguntas,
      2400 respuestas y 9 claves de configuración.
- [ ] 200 preguntas por nivel y 20 por tema y nivel.
- [ ] Exactamente 1 respuesta correcta por pregunta, 4 opciones por pregunta.
- [ ] 10 temas activos con `introduccion` y 600 preguntas activas con
      `explicacion`.
- [ ] `/admin/cobertura` en verde para los tres niveles.
- [ ] `intermedio` y `avanzado` habilitados desde `/admin/dificultades`, sin
      intentos activos.
- [ ] Una partida completa por nivel, jugada de verdad, en la base nueva.
- [ ] El HTML de la estación no contiene la palabra de la respuesta correcta ni
      la explicación.
- [ ] La transición muestra las 10 introducciones y las explicaciones una sola
      vez por pregunta.
- [ ] Los seeds son idempotentes: ejecutarlos dos veces no duplica nada.
- [ ] Los 600 ítems del documento de pistas existen y ninguno revela la
      respuesta.
- [ ] `material-de-estudio-y-control.md` coincide con la base.
- [ ] Los PDF nuevos existen en `docs/pdf/` y los 48 anteriores siguen intactos.
- [ ] `pytest -q` sigue en verde y no toca la base de la feria.
- [ ] La base `escape_room_7b2026` y el juego original siguen funcionando igual.

## Fuera de alcance

- Cambios de código en `app/`, `tests/` o `scripts/`.
- Cambiar el título "Escape Room 7.º B 2026" de las plantillas: se decidió
  dejarlo como está.
- Cambiar la cantidad de estaciones, de preguntas por estación o las reglas del
  juego.
- Agregar dependencias, frameworks o pasos de build.
- Enlazar el material de estudio o las pistas desde la aplicación.
- Reemplazar la base de la feria por la nueva.
- Crear un script de carga: se decidió que sean comandos documentados.

## Riesgos

| Riesgo | Mitigación |
| --- | --- |
| Que el contenido se escriba sin revisar contra el programa | Trazabilidad por eje en un archivo de trabajo y revisión por tanda |
| Que un `;` en un texto rompa el cargador de pruebas | Regla explícita y búsqueda con `grep ";"` antes de cerrar cada seed |
| Que se habilite un nivel sin cobertura | Habilitar solo después de la tanda 5 y verificar en `/admin/dificultades` |
| Que se toque la base de la feria por error | Todo apunta a `escape_room_redes_2026` y los seeds llevan su propio `USE` |
| Que 600 preguntas queden desparejas en dificultad | Tanda por nivel, con revisión de una muestra antes de seguir |
| Que el trabajo quede a medias | Cada tanda deja el contenido cargado y verificable, sin estados rotos |

## Decisiones de este paso

1. Segundo contenido en base propia `escape_room_redes_2026`; la base de la feria
   no se toca.
2. 5 estaciones y 10 temas: un escenario general y los cuatro niveles de TCP/IP,
   con 2 temas por estación.
3. 20 preguntas por tema y nivel: 600 en total.
4. Una pista por pregunta: 600, en documento aparte.
5. El título de la aplicación queda como está.
6. Sin script nuevo: los comandos de carga se documentan.
7. El material de estudio se genera desde la base, no se escribe a mano.
