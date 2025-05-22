# PGP

Es para confidencialidad e integridad.
Acá pasa que el no-repudio parte del principio de pretty-good-privicy y lo bonito es que es un protocolo creado en los 90 y ha seguido igual

Define que cada usuario es su propio CA (Certificate Authority) porque lo normal es que una autoridad las de a usuarios, firewalls, otras CA, RA (Registration Authority) y demás.
Por qué? Porque se crea el concepto de llavero que tiene clave pública del que crea el dueño y otros en los que confío, como no hauy una CA uno importa las claves de los que va a confiar, existen lo que se llamaba las fiestas-pgp (pgp-party) que en una hackatón digamos creaban un llavero, es una telaraña de confianña, de forma que uno para uno quiera. El chiste  es que crean las llaves públicas y los que confíen importan las llaves públicas de los demás y crean así una telaraña de confianza.

Entonces el modelo es que tenemos un usuario, este tiene un mensaje que se hashea y ese resultado (H) se firma con mi llave privada (Kp)


```bash

gpg --gen-key

# nos pide unos datos, mail nombre y luego mail creo

GIzasaC2
gizasa@gg.com

# ponemos la contraseña para proteger la clave privada
qwerty-654

# Nos dice que la clave privada se guardó en ~/.gnupg/secring.gpg

gpg --list-keys

# Acá nos mostrará la clave, la reciente la última, dura 2 años, hay un flag para que sea por menos tiempo.

echo "Prueba pgp may2025" > mensaje.txt
echo "Prueba pgp may2025 cifrado" > cmensaje.txt.gpg

gpg -c cmensaje.txt

# Acá cifraría con AES porque es simétrico y eso nos da el cifrado con extensión .gpg
# podemos verlo con el CAT

gpg -d cmensaje.txt.gpg
# Acá nos pide la clave privada para desencriptar el mensaje, si no la tenemos no podemos desencriptar el mensaje. Pero pues en nuestro propio equipo no nos la pediría porque confiamos en nosotros mismos.

# Pero como esto es simétrico, para mí, pero con un usuario para otro lado pues tengo el problema de que debe ser asimetrica, entonces debe hacerse la importación de la llave publica, cifro el mensaje con su llave pub y descifra con su privada. Repito, cifro con su publica así que la debe de publicar, cifro con esa llave publica y la decufra con la privada.

# el -c es para el cifrado simétrico, el -d es para descifrado simétrico, el --encrypt es para cifrado asimétrico y el --decrypt es para descifrado asimétrico.


```


El término gpg significa GNU Privacy Guard, es un software de cifrado de datos y comunicaciones que utiliza el estándar OpenPGP. GPG permite cifrar y firmar datos y comunicaciones, proporcionando confidencialidad e integridad. Es una herramienta ampliamente utilizada para proteger la privacidad en la comunicación electrónica.

Donde el término GNU significa "GNU's Not Unix", es un sistema operativo libre que fue desarrollado por la Free Software Foundation (FSF) y que se basa en el principio de que el software debe ser libre para ser utilizado, modificado y distribuido por cualquier persona. GNU es un acrónimo recursivo que refleja la filosofía del proyecto de software libre.


Entonces para lo que es el asimétrico
```bash

gpg --encrypt --recipient "ultima-clave-generada" --output cmensaje.crypt cmensaje.txt

gpg --decrypt cmensaje.crypt cmensaje.decrypt.txt


```

Lo que hizo fue cifrar con llave publica del receptor y cifra con llave privada del emisor.


Ahora vamos a ver el firmado:

```bash	

gpg -u "ultima-clave-generada" --sign cmensaje.txt
# esto es para identificar el usuario pero firma con la privada, es para decir que el que va a firmar es un usuario

gpg --list-keys

gpg -u clave-

# el chiste, el crea el mensaje.txt.gpg y al hacerle un cat.

# entonces el chiste es que uno lo puede cifrar antes de cifrarlo, que sea tanto integro como confidencial.

# Entonces ya uno le pasa eso a la otra persona y si importó mi llave publica pues puede descifrarlo y dice de quién, eso con el
gpg --verify cmensaje.txt.gpg

```

Y si llega a modificar el archivo .pgp le modifica la integridad porque altera el hash y la firma con RSA.

```bash
# si hacemos un desadjuntar la firma
gpg -u clave-usuario-creador-creo --deatch-sign mensaje.txt.gpg
```

Entonces lo que uno hace es armonizar la firma para que quede en formato ASCII con

```bash
gpg --output mensaje.txt.gpg --armor --export "clave-usuario-creador-creo"
```


Podemos en pgp.mit.edu es un webserver pgp muy querido pero mantiene muy colapsado, que en vez de copiarla pues expoertar el archivo.
```bash
gpg --send-keys --keyserver pgp.mit.edu CLAVE-MIA-ESA-DE-ANTES

# Y listo toca esperar
# Para buscarla podemos hacer

gpg --keyserver pgp.mit.edu --recv-keys CLAVE-MIA-ESA-DE-ANTES"



```
De hecho es mejor keyserver.ubuntu.com porque es más rápido y no está colapsado.

Para buscar por correo en el sitio se debe hacer 



## Laboratorio

En el lab el 1:
Configurar y desplegar los webservers por al menos 3 opciones el de apache, python, nodejs o nginx.

2. A partir del uso del GPG cifrar y decifrar simétricamente y asimétricamente para un documento, o usar python para dicha tarea, el doc de GPGBasicCommands.
    También en el repo cryptography-python tiene un notebook llamado PgP creo que para hacer eso. Sirve para saber cómo cifra ficheros antes de enviarlos. LABProtocolo_SOC.txt



    
3. La siguiente semana nos explica tema y lua última semana de mayo da programación segura.