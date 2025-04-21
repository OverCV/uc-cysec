RSA Diffy-Hellman

El DH es muy usado en IoT

Entonces el chiste es que se puso al receptor a trabajar

En el enfoqiue del principio de confidencialidad, pero una llave privada para firmar y verificar.

ENtonces tenemos un texto plano

$$P_i,i\in\{1,2,3,\cdots P_n\}$$

Entonces el emisor hace una codificación polinómica:

[C, A, S, A] se le hace un [3*27^3, 1*27^2, 14*27^1, 1*27^0]

Pero el chiste es que ese no se usó por coste energético para el futuro en IoT.


Uno de los retos en computación cuántica es hallar el primo más grande.


Entonces empiezaa trabajar el receptor Rx (B), hace el cálculo de las claves.
1. Escoge dos grandes números primos grandes (de al menos 256 dígitos).
2. Calcula $n=p\times x$
3. $\phi(n)=z=(p-1)(p-1)$
4. Tenemos q tal que 
   1. son coprimos si el MCD no es mayor a 1, tal que mcd(a, b) = 1
   > Por ejemplo 6 y 35, tal que 6=[3,2] y 35=[5,7]
   > Pero no son coprimos 6 y 27 porque 6=[3,2] y 27=[3,9] de forma que el MCD=3.
5. Calculamos $e$ tal que $e=1\mod z$ y eso hace que sea intractable el hacer un $e=d^{-1}\mod z$
    Eso vuelve el método de Euclides es algo para calcular el MCD y se usa mucho porque es rápido.

Las claves públicas entonces son $K_{pub}d, n$ y la clave privada $K_{priv}=e$, las diapositivas esa parte están al reves pero el resto si bien.

6. Entonces el emisor (B) emvía por el canal inseguro las claves públicas (PKI, infraestructura de clave pública, es cómo publicar claves públicas) y viajan por la red (protocolo) de forma que ahora el Tx (A) sabe que el criptograma $C_i=P_i^{K_{pub}(d)}\mod n $
7. Entonces el emisor (A) envía el criptograma $C_i$ al receptor (B) y el receptor (B) hace la operación inversa $P_i=C_i^{K_{priv}(e)}\mod n$ y eso es lo que se llama el cifrado RSA.

ENtonces el chiste es que la llave privada nunca viajó por la red, la tiene siempre el Rx.
La clave está entonces en poder tener:
- Factorización de números primos grandes.
- PLD (Problema Logaritmo Discreto): Su hay un ataque de MIM (Man in the middle) y pone un sniffer del Tx enviando la data, si este digamos tiene $C_i,d,n$ pues igual no pasa nada. Pero el chiste es que la falta la K_priv, pero si el $n$ es grande (pero pues depende de $e,n$) pues igual le falta el $z$ y eso es con logaritmos, el chiste es que eso es intractable. 

---

Lo que tienen es la estructura de 2 claves publicas d N y los bloques que so ncriptogramas.
EN ingeniería esta el TipsRetoRSA con la metodología de resolución, ha salido en muchos CTFs digamos una clave de una app web pero laclave está cifrada con RSA y toca hacer esto.
Entonces tiene las claves d N públicas, con un Sniffer tuvo esos criptogramas, cualquiera puede interceptarlos, y están los bloquecitos codifiacdo en números (plaintext > ASCII > RSA > Criptograma) y tuvo los bloques con una sustitución monoalfabética.
De una uno se ve que N es muy chiquito, entonces uno descompone ese N, digamos primos.html y si ponemos digamos 3431 tiene 43*77
Entonces luego z es p+1, q-1 y tiene todo para entonces calcular el E
Pero no lo hacemos con la inversa porque va para los pequeños pero grandes ya pailas. Entonces usamos el algorimo de Euclides que en principio:

Entonces ahí dice que es un ejemplo a la cosa azul, esos valores, pero sí las instrucciones que dice:
1. Se igualan los valores (podemos pedirle para saber si nos dio bien, el py de forma que ponemos os valres y listo)
2. Metemos los valores en una tablita g_0 g_1 ...
3. Entonces B=z=$\phi(n)$ y tenemos A=d, ahí dice y empezamos a llenar la matriz
4. Dice haga g_0 y ubicamos en la tabla  [0,g_i]=3152, bueno y llenamos esa parte de la tabla y el chiste es que el while para cuando g_i==0, 3 o 4 iteraciones. Cuando eso pasa pregunta si V_{i-1} es menor que 0, si es menor le suma `V_{i-1}<0` que en ese caso le suma Z, sino la salida `x` es V_{i-1} y esa instrucción de la `x` esta fuera del if, si no falla.

Entones seguimos, y se toma siempre la parte entera, así sea .999 periodico. Entonces luego dice hacer opraciones.
Entonces cuando tenga la `x` iguala por un lado dizque la E y ya tiene D, Z y con el algoritmo de euclides puede verificar para casos intractables.

Entonces, tiene los bloques criptográficos, el algoritmo dice que el texto plano son los bloquecitos cifrados elevado a la llave privada mod n.
De forma que tenemos E=2839 y n=3431
Entonces sería $114\mod 1$
Entonces el exponente da un número muy alto, de forma que usamos woframAlpha y ponemos digamos $114^2839 mod 3431=69$ y lo pone donde se repita, el chiste es ese, va reemplazando


$$
\begin{align}
\sum_{i=1}^{\infty} \left(\frac{1}{i} - \frac{1}{i+1}\right) &= \left(\frac{1}{1} - \frac{1}{2}\right) + \left(\frac{1}{2} - \frac{1}{3}\right) + \left(\frac{1}{3} - \frac{1}{4}\right) + \ldots \
&= 1 - \frac{1}{2} + \frac{1}{2} - \frac{1}{3} + \frac{1}{3} - \frac{1}{4} + \ldots
\end{align}
$$