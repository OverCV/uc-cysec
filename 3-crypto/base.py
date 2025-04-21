from const import MAPEO_PROFE, FREC_CIFRADO, FREC_ESPANOL
from gramas import MONOGRAMAS_ESP, BIGRAMAS_ESP, TRIGRAMAS_ESP, PALABRAS_CORTAS


# Función para encontrar bigramas y trigramas en el texto cifrado
def encontrar_ngrams(texto, n):
    # Eliminar espacios para buscar secuencias continuas
    texto = texto.replace(" ", "")
    ngrams = {}
    for i in range(len(texto) - n + 1):
        ngram = texto[i : i + n]
        if ngram in ngrams:
            ngrams[ngram] += 1
        else:
            ngrams[ngram] = 1
    return ngrams


# Función para identificar posibles espacio + palabra corta + espacio
def identificar_palabras_cortas(texto):
    palabras_candidatas = {}
    # Buscar patrones entre espacios
    palabras = texto.split(" ")
    for palabra in palabras:
        if 1 <= len(palabra) <= 4:  # Palabras cortas de 1-4 caracteres
            if palabra in palabras_candidatas:
                palabras_candidatas[palabra] += 1
            else:
                palabras_candidatas[palabra] = 1
    return sorted(palabras_candidatas.items(), key=lambda x: x[1], reverse=True)


# Función para aplicar descifrado
def descifrar(texto, mapeo):
    resultado = ""
    for caracter in texto:
        if caracter == " ":
            resultado += " "
        elif caracter in mapeo:
            resultado += mapeo[caracter]
        else:
            resultado += caracter
    return resultado


# Función para mejorar el descifrado usando pistas contextuales
def mejorar_descifrado(texto_cifrado, mapeo_inicial):
    # 1. Buscar bigramas frecuentes en el texto cifrado
    bigramas_cifrado = encontrar_ngrams(texto_cifrado, 2)
    top_bigramas = sorted(bigramas_cifrado.items(), key=lambda x: x[1], reverse=True)[
        :20
    ]

    # 2. Buscar trigramas frecuentes en el texto cifrado
    trigramas_cifrado = encontrar_ngrams(texto_cifrado, 3)
    top_trigramas = sorted(trigramas_cifrado.items(), key=lambda x: x[1], reverse=True)[
        :16
    ]

    # 3. Identificar posibles palabras cortas
    palabras_cortas_cifrado = identificar_palabras_cortas(texto_cifrado)

    print("\nBigramas más frecuentes en el texto cifrado:")
    for bigrama, freq in top_bigramas[:10]:
        print(f"{bigrama}: {freq}")

    print("\nTrigramas más frecuentes en el texto cifrado:")
    for trigrama, freq in top_trigramas[:10]:
        print(f"{trigrama}: {freq}")

    print("\nPosibles palabras cortas en el texto cifrado:")
    for palabra, freq in palabras_cortas_cifrado[:10]:
        print(f"{palabra}: {freq}")

    # 4. Primera aproximación usando el mapeo por frecuencia
    mapeo = mapeo_inicial.copy()

    # 5. Descifrar el texto usando el mapeo actual
    texto_descifrado = descifrar(texto_cifrado, mapeo)

    # 6. Sugerir posibles refinamientos basados en bigramas y trigramas
    print("\nPosibles refinamientos basados en bigramas:")
    for bigrama_cifrado, _ in top_bigramas[:5]:
        descifrado = descifrar(bigrama_cifrado, mapeo)
        es_conocido = descifrado in BIGRAMAS_ESP
        print(
            f"{bigrama_cifrado} -> {descifrado} {'(Conocido en español)' if es_conocido else ''}"
        )

    print("\nPosibles refinamientos basados en trigramas:")
    for trigrama_cifrado, _ in top_trigramas[:5]:
        descifrado = descifrar(trigrama_cifrado, mapeo)
        es_conocido = descifrado in TRIGRAMAS_ESP
        print(
            f"{trigrama_cifrado} -> {descifrado} {'(Conocido en español)' if es_conocido else ''}"
        )

    print("\nPosibles refinamientos basados en palabras cortas:")
    for palabra_cifrada, _ in palabras_cortas_cifrado[:5]:
        descifrado = descifrar(palabra_cifrada, mapeo)
        es_conocida = descifrado in PALABRAS_CORTAS
        print(
            f"{palabra_cifrada} -> {descifrado} {'(Conocida en español)' if es_conocida else ''}"
        )

    return texto_descifrado, mapeo


# Simular la lectura del texto cifrado
texto = "Sin contenido"
with open("texto_cifrado.txt", "r") as file:
    texto = file.read()


# Preprocesamiento del texto
texto = texto.replace("\n", " ").replace(" ", "")
texto = texto.replace("n", " ")  # Reemplazar 'n' por espacio

# Mapeo inicial basado en frecuencias
cifrado_ordenado = sorted(
    FREC_CIFRADO.keys(), key=lambda x: FREC_ESPANOL[x], reverse=True
)
espanol_ordenado = sorted(
    FREC_ESPANOL.keys(), key=lambda x: FREC_ESPANOL[x], reverse=True
)

mapeo_inicial = {}
for i in range(min(len(cifrado_ordenado), len(espanol_ordenado))):
    mapeo_inicial[cifrado_ordenado[i]] = espanol_ordenado[i]

# Aplicar mejoras al descifrado
texto_descifrado, mapeo_final = mejorar_descifrado(texto, mapeo_inicial)

print("\nTexto cifrado (primeros 100 caracteres):")
print(texto[:100])
print("\nTexto descifrado (primeros 100 caracteres):")
print(texto_descifrado[:100])

# Sugerir ajustes manuales para mejorar el descifrado
print("\nSugerencias para refinar manualmente el descifrado:")
print("1. Buscar patrones como 'QUE', 'DE', 'LA', 'EL' en el texto descifrado.")
print("2. Ajustar el mapeo para letras específicas basándose en estos patrones.")
print("3. Probar diferentes combinaciones para caracteres frecuentes.")

# Ejemplo de ajuste manual para probar
print("\nEjemplo de ajuste manual (intercambiando E y A):")
mapeo_ajustado = mapeo_final.copy()
for key, value in mapeo_final.items():
    if value == "E":
        mapeo_ajustado[key] = "A"
    elif value == "A":
        mapeo_ajustado[key] = "E"

texto_ajustado = descifrar(texto, mapeo_ajustado)
print(texto_ajustado[:100])
