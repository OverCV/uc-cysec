from const import MAPEO_PROFE
from gramas import MONOGRAMAS_ESP, BIGRAMAS_ESP, TRIGRAMAS_ESP, PALABRAS_CORTAS


# Función para aplicar el descifrado con el mapeo del profesor
def descifrar_con_mapeo_profesor(texto):
    resultado = ""
    for caracter in texto:
        if caracter in MAPEO_PROFE:
            resultado += MAPEO_PROFE[caracter]
        else:
            resultado += caracter  # Mantener caracteres que no están en el mapeo
    return resultado


# Función para encontrar ngrams en el texto
def encontrar_ngrams(texto, n):
    # Eliminar espacios para ngrams continuos
    texto_sin_espacios = texto.replace(" ", "")
    ngrams = {}
    for i in range(len(texto_sin_espacios) - n + 1):
        ngram = texto_sin_espacios[i : i + n]
        if ngram in ngrams:
            ngrams[ngram] += 1
        else:
            ngrams[ngram] = 1
    return ngrams


# Función para encontrar palabras entre espacios
def encontrar_palabras(texto):
    palabras = {}
    for palabra in texto.split():
        if palabra in palabras:
            palabras[palabra] += 1
        else:
            palabras[palabra] = 1
    return palabras


# Función para analizar patrones útiles en el texto descifrado
def analizar_patrones(texto_descifrado):
    # Encontrar palabras
    palabras = encontrar_palabras(texto_descifrado)
    palabras_ordenadas = sorted(palabras.items(), key=lambda x: x[1], reverse=True)

    # Encontrar bigramas
    bigramas = encontrar_ngrams(texto_descifrado, 2)
    bigramas_ordenados = sorted(bigramas.items(), key=lambda x: x[1], reverse=True)

    # Encontrar trigramas
    trigramas = encontrar_ngrams(texto_descifrado, 3)
    trigramas_ordenados = sorted(trigramas.items(), key=lambda x: x[1], reverse=True)

    # Comprobar si encontramos palabras conocidas
    palabras_encontradas = []
    for palabra, _ in palabras_ordenadas[:30]:
        if palabra in PALABRAS_CORTAS:
            palabras_encontradas.append(palabra)

    # Comprobar si encontramos bigramas conocidos
    bigramas_encontrados = []
    for bigrama, _ in bigramas_ordenados[:30]:
        if bigrama in BIGRAMAS_ESP:
            bigramas_encontrados.append(bigrama)

    # Comprobar si encontramos trigramas conocidos
    trigramas_encontrados = []
    for trigrama, _ in trigramas_ordenados[:30]:
        if trigrama in TRIGRAMAS_ESP:
            trigramas_encontrados.append(trigrama)

    return {
        "palabras_frecuentes": palabras_ordenadas[:15],
        "bigramas_frecuentes": bigramas_ordenados[:15],
        "trigramas_frecuentes": trigramas_ordenados[:15],
        "palabras_conocidas": palabras_encontradas,
        "bigramas_conocidos": bigramas_encontrados,
        "trigramas_conocidos": trigramas_encontrados,
    }


# Simular la lectura del texto cifrado
texto = "Sin contenido"
with open("texto_cifrado.txt", "r") as file:
    texto = file.read().replace(" ", "")

# Reemplazar saltos de línea por espacios y eliminar espacios adicionales
texto = texto.replace("\n", " ")
# No eliminar espacios aún para conservar la estructura original

# Aplicar descifrado con el mapeo del profesor
texto_descifrado = descifrar_con_mapeo_profesor(texto)

# Analizar patrones en el texto descifrado
patrones = analizar_patrones(texto_descifrado)

# Mostrar resultados
print("Texto cifrado (primeros 100 caracteres):")
print(texto[:100])

print("\nTexto descifrado con el mapeo del profesor (primeros 100 caracteres):")
print(texto_descifrado[:100])

print("\nPalabras más frecuentes en el texto descifrado:")
for palabra, frecuencia in patrones["palabras_frecuentes"][:10]:
    print(f"{palabra}: {frecuencia}")

print("\nBigramas más frecuentes en el texto descifrado:")
for bigrama, frecuencia in patrones["bigramas_frecuentes"][:10]:
    conocido = " (Conocido en español)" if bigrama in BIGRAMAS_ESP else ""
    print(f"{bigrama}: {frecuencia}{conocido}")

print("\nTrigramas más frecuentes en el texto descifrado:")
for trigrama, frecuencia in patrones["trigramas_frecuentes"][:10]:
    conocido = " (Conocido en español)" if trigrama in TRIGRAMAS_ESP else ""
    print(f"{trigrama}: {frecuencia}{conocido}")

print("\nPalabras conocidas encontradas:")
print(patrones["palabras_conocidas"])

print("\nBigramas conocidos encontrados:")
print(patrones["bigramas_conocidos"])

print("\nTrigramas conocidos encontrados:")
print(patrones["trigramas_conocidos"])

# Intentar con un archivo de texto completo (comentado porque no tenemos el archivo)
try:
    # La lectura del texto cifrado
    with open("texto_cifrado.txt", "r") as file:
        texto_completo = file.read().replace(" ", "")

    # Preprocesamiento del texto
    texto_completo = texto_completo.replace("\n", " ")

    # Aplicar descifrado con el mapeo del profesor
    texto_completo_descifrado = descifrar_con_mapeo_profesor(texto_completo)

    print("\n\nTexto completo descifrado (primeros 500 caracteres):")
    print(texto_completo_descifrado[:500])

    # Analizar patrones en el texto completo descifrado
    patrones_completo = analizar_patrones(texto_completo_descifrado)

    print("\nPalabras conocidas encontradas en el texto completo:")
    print(patrones_completo["palabras_conocidas"])

    print("\nBigramas conocidos encontrados en el texto completo:")
    print(patrones_completo["bigramas_conocidos"])

    print("\nTrigramas conocidos encontrados en el texto completo:")
    print(patrones_completo["trigramas_conocidos"])

except FileNotFoundError:
    print("\nArchivo 'texto_cifrado.txt' no encontrado. Usando solo el ejemplo.")


# Función para probar ajustes manuales al mapeo
def probar_ajuste(texto, mapeo_original, cambios):
    mapeo_ajustado = mapeo_original.copy()
    for original, nuevo in cambios.items():
        # Intercambiar los valores
        for key, value in mapeo_original.items():
            if value == original:
                mapeo_ajustado[key] = nuevo
            elif value == nuevo:
                mapeo_ajustado[key] = original

    resultado = ""
    for caracter in texto:
        if caracter in mapeo_ajustado:
            resultado += mapeo_ajustado[caracter]
        else:
            resultado += caracter

    return resultado


# Probar algunos ajustes basados en observaciones
print("\nProbando algunos ajustes potenciales:")

# # Ajuste 1: Intercambiar E y A
# texto_ajustado1 = probar_ajuste(texto, MAPEO_PROFE, {'E': 'A', 'A': 'E'})
# print("\nIntercambiando E y A:")
# print(texto_ajustado1[:100])

# # Ajuste 2: Intercambiar S y N
# texto_ajustado2 = probar_ajuste(texto, MAPEO_PROFE, {'S': 'N', 'N': 'S'})
# print("\nIntercambiando S y N:")
# print(texto_ajustado2[:100])

# # Ajuste 3: Intercambiar D y L
# texto_ajustado3 = probar_ajuste(texto, MAPEO_PROFE, {'D': 'L', 'L': 'D'})
# print("\nIntercambiando D y L:")
# print(texto_ajustado3[:100])

# # Ajuste 4: Intercambiar I y O
# texto_ajustado4 = probar_ajuste(texto, MAPEO_PROFE, {'I': 'O', 'O': 'I'})
# print("\nIntercambiando I y O:")
# print(texto_ajustado4[:100])
