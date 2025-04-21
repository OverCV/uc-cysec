# Por ejemplo el HearthBeat. 

TLS/SSL son protocolos medianamente seguros, parametrizados.
- RP
- AR
- CCSP
- Handshake: Confidencialidad, no repudio y se garantiza emisor/receptor comunicados de forma segura.

RFC (Request For Content): Para que el protocolo sea portable e interoperable entonces si se ciñe sobre HTTP estándar pues se ciñe por la RFC de HTTP, así mismo para POP3 e IMAC, esas estructuras del protocolo y mensaes estandarizados que se usan, necesita compatibilidad, interoperabilidad, etc...

HTTPS hace un VPN que es un Túnel antes de la autenticación porque sino la primera vez que vaya el password pues secuestra la pss. Esto funciona sobre OpenSSL que va sobre casi cualquier cosa/entorno, es muy compatible porque genera el estándar del protocolo y los certificados, es open-source libre (el hecho de que algo sea open source es más inseguro? Porque pues uno piensa que son pruebasd de caja blanca. Digamos en WIN y se cierra algo de reprente, los core-dump que hacen que se cierre abruptamente (son violaciones de pareas de memoria, un hacker mira esas excepciones y se aprovecha para hacer un exploit. Pero en caja-blanca es fácil de encontrar el fallo y fácilmente la misma comunidad pues de una van a hallar una solución))

Entonces el servidor pregunta con un "HELLO" con 5 bytes para ver si la conexión sigue activa, un HearthBeat.
> Los crackers dijeron, no, no me responda con 5 sino con 500 bytes, de forma que el serevidor tiene un canal con el que retorna la información, no había una validación que daba ese tope, de forma que retornaba más información que realmente era sensible! Fue un escándalo tenáz! Porque una cosa son datos tráfico y otra en reposo, que son los de memoria. Eso porque no validaron este tope, tan básico, pero así millones de cosas quedaron expuestas en el protocolo más seguro de todos, eso dado que en C toca controlar todo, incluso esa validación. 

Log4J permitía crear una consola remota, había gente que no decía que tenía nada en Java, pero muchas otras tecnologías sí usaban dicho motor, que sobre todo tenía 


# Ataque Poodle
La ciberseguridad no es empática 

Del inglés Padding Oracle On Downgraded Legacy

Se puede instanciar un algoritmo criptográfico chiquito, este ataque se aprovechaba de cómo el proto TLS hacía una seguridad chiquita.

## Meltdown y Spectre

Son clásicos en los ciberataques porque antes vimos cómo se comprometía un recurso pero a la larga era una solución de software, estos son ataques que realmente atacaban más al hardware, por ejemplo STUXNET era un parche de software o similar, que interactúe con el sistema SCADA ya se tenía la firma que se identificaba y era una solución de software.
Al profe lo asusta más de lo que lo sorprende el nivel de destreza de los que crean ciberataques para descubrir fallos para vulnerar la seguridad.

Recuerdese la ejecución especulativa anticipada: Determina que si tenemos una función main y tenemos unas variables `x, i, a=20, b=30` y luego `x = suma(a, b)` y luego... Acá la máquina hace un análisis meramente estadístico, donde por ejemplo el boot PID0 hasta el que termina es un set de instrucciones siempre igual, de forma que el procesador siempre se va yendo por una instrucción de una línea en el código. Esta ejecución especulativa pues anticipa la ejecución y la ejecuta antes de que llegue, entonces este resultado lo pone en una `mem_cache`, de forma que ese resultado que sabe que va a calcular con gran certeza pues el resultado antes de calcularlo.
Acá todos los procesadores son vulnerables
El chiste es que hacer esto da un speed-up mejoraba del 40 al 70 porciento.

Pero entones mediante una instrucción remota lograron acceder a esa memoria, y así mismo escribir datos en esa área de memoria, y eso está está en lo VIP que incluso usa el kernel. Es el primer ataque a los procesadores, una estructura de datos que se carga en memoria, al final es una pila que se carga en memoria de forma que ese 

El BufferOverflow es el más común, desborda la dirección de retorno (algo muy común en las direcciones de retorno y manda una shell, enviar un archivo, poner un key-logger etc...), pero este está sobre-escribiendo datos.

Entonces llegó la dicotomía de que cómo parcheaban eso.. Pero entonces si se puede mirar la carga útil pero es una característica en acople con el OS.
La solución real es cambiar el microprocesador, la que nos dieron (una p*tada) es que se alinearon con los fabricantes de los OS para que haya un parche del OS que tiene esa característica, lo que hace es "deshabilite la ejecución especulativa", una grosería pues así bajaron el 50% prácicamente.

Entonces todos los usuarios se quejaban, que era un bot o algo así, pero no, era pues el parche. Pero bueno entonces el el mundo de los centros de datos facturan por tiempo de computación, por procesamiento, ej. allá en el Marenostrum, que modelados de resistencias de aviones (eq. diff. parc.) y compiten con China, BIOS, etc, porque necesita que de un resultado en minutos, no meses. La HTC (High Trouble Computing) se encargó por ejepmlo para lo del COVID. Pues bueno, no, no podían hacer eso, de forma que pidieron una reposición de los procesadores, era una solución compleja.
De forma que este ciberataque fue potente, en 2022. Se descubrió mediante un BugBounty y recompensas altas


Mucho cuidado cuando se compra software porque el licensiamientoy 

## RC4ya p
WPA que usa AES-256 (más robusto y reciente)
La gente con tizas marcaba si había una red abierta en el Google maps y pues uno con eso sabía cuáles eran más vulnerables, esto con el PSK (Private Shared Key).
En la uni pues por ejemplo propusieron que hagan lo mismo que en los aeropuertos, pero pues con el id de la uni pues se autentica y así.

Unos chicos encontraron que en WiFi hay un 3WayHandshake, puede haber un MITmiddle de forma que sin estar conectado puede sniffear la red, esto mediante este SSI sin autenticarse ni conectarse puede olfatear, interceptarla, esnifear sin conectarse, que es el tráfico, contraseñas, si no hay cifrado, mejor dicho de todo.
Entonces actualizaron WPA2 a WP3, pero no sabe si eso lo hicieron a todos los routers domiciliarios, cree que sí porque cree hay una política de actualización,  

## Ramsonware

La mejor forma de engañar es por el usuario.
WannaCry fue un ataque que tuvo un impacto muy fuerte en el mundo, Chema Alonso fue el maligno hacker español en Informática64 o ElevenPaths de forma que ambos se encontraron haciendo el doctorado, Chema le tocó este ciberataque, y le tiraron la bronca porque era el encargado, pero pues era un Zero-Day, pero el ataque pasaba con alguien que logre hacer click donde no debe, abrir el archivo que no debe..

Las políticas de seguridad por ejemplo son:
- BYOD: Bring Your Own Desktop, pero pues ud no puede traer su propia basura a la empresa, un foco de infección.

El problema de WannaCry es que era un fichero malicioso (mirar la ruta de origen del archivo, el profe never abre un ZIP/RAR, en un isntalador se pueden concatenar varios .exe o .bat que quedan en el mismo instalador) se propagaba por el protocolo SMB mimado por MS, usado para operaciones en red, una cosa es la pila TCP/IP y otar lo que uno haga por encima, que es lo de perifericos, impresoras, etc, si tiene una máquina en red pues el SMB es ineludible porque pues ahí se usa, por ejemplo el Active Directory, sin eso no funciona, en .NET acceden con SMB para un directorio con ficheros necesarios, eso es un mal necesario.
Entonces era un script basado en EternalBlue, originado de las CIA-Hacking-Tools, de forma que estas implementaciones están en python o ruby y al final hacían un ransom-ware, de forma que ponen un cifrado en AES-256 que es prácticamente, indescifrable.

Hay un proyecto de la Europol/Barracuda que tienen un criptosherif que analyza intentos de descifrado, el profe no conoce la primera empresa/persona que eso lo haya salvado

Cuando hackean es para meterle a uno un cryptominer, meterlo a una botnet o sacar datos sensibles

## Ataque a SolarWinds

Este abrió una consideración que uno es pesimista ante solución aboluta, el software es una cadena de sumunistros de 6 cadenas de separación, los devs en back front o lo que sea luego a EU y esos a CH, y quién asegura que en un punto de la cadena a un loco no le de por meter malware?
Entonces el profe dice que sólo SantoDomingo usa Solarwind, que monitorea todos los disp de todas las sedes para mirar rendimiento, seguridad, etc.
Detectaron el ataque en DEC2021 pero cuando vieron que envenenaron fue desde 2019, era una DLL, una librería maliciosa que permitia Comand&Control, que manejaba todo, pues terminó en ramsonware, en robos de seguridad, etc etc, robar información muy privada y muy sensible.

En esta industria se controla todo esto.
El XZ-Utils es para comprimir y todas las herramientas de compresión tienen eso, y uno de los programadores tuvo mala leche porque lo echó, se infiltó en el ecosistema con otro nombre y fue metiendo código malicioso y con eso remotamente podía tener acceso a las máquinas.
