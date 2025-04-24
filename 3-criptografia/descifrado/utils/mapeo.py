"""
Funciones para la generación y refinamiento de mapeos entre caracteres cifrados y descifrados.
"""

from const import FREC_ESPANOL, PALABRAS_COMUNES_50
import re
from collections import Counter


def mapear_frecuencias_iniciales(frecuencias_cifrado):
    """Crea un mapeo inicial basado en frecuencias.

    Args:
        frecuencias_cifrado: Diccionario con frecuencias de caracteres en el texto cifrado.

    Returns:
        Diccionario con el mapeo inicial basado en frecuencias.
    """
    # Ordenamos las letras del español por frecuencia
    letras_esp_ordenadas = sorted(
        FREC_ESPANOL.keys(),
        key=lambda x: FREC_ESPANOL[x],
        reverse=True,
    )

    # Ordenamos los caracteres cifrados por frecuencia
    chars_cifrados_ordenados = [
        k
        for k, v in sorted(
            frecuencias_cifrado.items(), key=lambda x: x[1], reverse=True
        )
    ]

    # Creamos un mapeo inicial (puede ser incorrecto, pero es un punto de partida)
    mapeo_inicial = {}
    for i, char in enumerate(chars_cifrados_ordenados):
        if i < len(letras_esp_ordenadas):
            mapeo_inicial[char] = letras_esp_ordenadas[i]
        else:
            # Si hay más caracteres cifrados que letras, asignamos la última letra
            mapeo_inicial[char] = letras_esp_ordenadas[-1]

    return mapeo_inicial


def refinar_mapeo_con_patrones(mapeo, patrones, texto_cifrado):
    """Refina el mapeo usando patrones de palabras comunes.

    Args:
        mapeo: Diccionario con el mapeo inicial.
        patrones: Diccionario con palabras cortas frecuentes en el texto cifrado.
        texto_cifrado: String con el texto cifrado.

    Returns:
        Diccionario con el mapeo refinado.
    """
    # Buscamos caracteres que aparecen en posiciones específicas de palabras cortas
    # Por ejemplo, en español, 'EL', 'LA', 'DE' son muy comunes

    mapeo_refinado = mapeo.copy()

    # Intentamos identificar patrones que podrían corresponder a palabras comunes
    for palabra_cifrada, frecuencia in patrones.items():
        if len(palabra_cifrada) == 2:
            # Posibles candidatos: DE, LA, EL, EN, Y, etc.
            candidatos = [p for p in PALABRAS_COMUNES_50 if len(p) == 2]
            for candidato in candidatos:
                # Verificar si la asignación tiene sentido con el mapeo actual
                compatible = True
                for i, char in enumerate(palabra_cifrada):
                    if char in mapeo_refinado and mapeo_refinado[char] != candidato[i]:
                        compatible = False
                        break

                if compatible:
                    # Actualizar mapeo con este candidato
                    for i, char in enumerate(palabra_cifrada):
                        mapeo_refinado[char] = candidato[i]
                    break

        elif len(palabra_cifrada) == 1:
            # Posibles candidatos: Y, A, O
            candidatos = [p for p in PALABRAS_COMUNES_50 if len(p) == 1]
            for candidato in candidatos:
                if (
                    palabra_cifrada in mapeo_refinado
                    and mapeo_refinado[palabra_cifrada] != candidato
                ):
                    continue

                mapeo_refinado[palabra_cifrada] = candidato
                break

    return mapeo_refinado


def analizar_monogramas_especiales(texto_cifrado):
    """Identifica caracteres aislados que probablemente sean Y, A, O, etc.

    Args:
        texto_cifrado: String con el texto cifrado.

    Returns:
        Diccionario con mapeo sugerido para caracteres aislados.
    """
    # Buscar caracteres que aparecen como palabras de un solo carácter
    patron = r"\s([a-zA-Z])\s"
    monogramas = re.findall(patron, " " + texto_cifrado + " ")
    contador = Counter(monogramas)

    # Los caracteres aislados en español suelen ser Y, O, A, E
    candidatos = ["Y", "A", "O", "E"]

    mapeo_monogramas = {}
    if contador:
        # Ordenar por frecuencia
        monogramas_ordenados = [char for char, _ in contador.most_common()]

        # Asignar los más frecuentes a los candidatos más probables
        for i, char in enumerate(monogramas_ordenados):
            if i < len(candidatos):
                mapeo_monogramas[char] = candidatos[i]

    return mapeo_monogramas


def mejorar_mapeo_con_heuristicas(mapeo, texto_cifrado):
    """Mejora el mapeo aplicando reglas heurísticas específicas del español.

    Args:
        mapeo: Diccionario con el mapeo actual.
        texto_cifrado: String con el texto cifrado.

    Returns:
        Diccionario con el mapeo mejorado.
    """
    mapeo_mejorado = mapeo.copy()

    # 1. Analizar monogramas especiales (caracteres aislados que suelen ser Y, A, O)
    mapeo_monogramas = analizar_monogramas_especiales(texto_cifrado)
    for char, asignacion in mapeo_monogramas.items():
        mapeo_mejorado[char] = asignacion

    # 2. Analizar patrones de artículos y preposiciones
    # "de", "la", "el", "en", "un", "una", etc.
    palabras_en_texto = re.findall(r"\b\w+\b", texto_cifrado)

    # Identificar palabras de 2 letras más frecuentes
    palabras_2letras = [p for p in palabras_en_texto if len(p) == 2]
    contador_2letras = Counter(palabras_2letras)

    # Candidatos para palabras de 2 letras más comunes en español
    candidatos_2letras = ["DE", "LA", "EL", "EN", "ES"]

    # Las 3 palabras de 2 letras más frecuentes
    for i, (palabra, _) in enumerate(contador_2letras.most_common(3)):
        if i < len(candidatos_2letras):
            # Aplicar mapeo
            for j, char in enumerate(palabra):
                mapeo_mejorado[char] = candidatos_2letras[i][j]

    return mapeo_mejorado
