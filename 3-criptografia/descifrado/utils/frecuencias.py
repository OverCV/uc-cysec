"""
Funciones para el análisis de frecuencias de caracteres en textos cifrados.
"""

import re
from collections import Counter


def analizar_frecuencias(texto):
    """Analiza las frecuencias de caracteres en el texto cifrado.

    Args:
        texto: String con el texto cifrado.

    Returns:
        Diccionario con los caracteres y sus frecuencias en porcentaje, ordenado por frecuencia.
    """
    # Filtramos solo caracteres que parecen ser parte del cifrado
    chars = re.findall(
        r"[a-zA-Z0-9\!\@\#\$\%\^\&\*\(\)\[\]\{\}\;\:\'\"\,\.\<\>\/\?\-\_\=\+\\]",
        texto,
    )
    conteo = Counter(chars)
    total = sum(conteo.values())

    # Evitar división por cero
    if total == 0:
        return {}

    # Convertimos a porcentajes
    frecuencias = {char: (count / total) * 100 for char, count in conteo.items()}
    return dict(sorted(frecuencias.items(), key=lambda x: x[1], reverse=True))


def identificar_patrones(texto_cifrado):
    """Identifica patrones que podrían corresponder a palabras comunes.

    Args:
        texto_cifrado: String con el texto cifrado.

    Returns:
        Diccionario con palabras cortas frecuentes en el texto cifrado.
    """
    palabras_cifradas = re.findall(
        r"[a-zA-Z0-9\!\@\#\$\%\^\&\*\(\)\[\]\{\}\;\:\'\"\,\.\<\>\/\?\-\_\=\+\\]+",
        texto_cifrado,
    )

    # Buscamos palabras de 1, 2 y 3 caracteres (posibles artículos, preposiciones, etc.)
    palabras_cortas = [p for p in palabras_cifradas if len(p) <= 3]

    # Contamos frecuencias de palabras cortas
    conteo_palabras = Counter(palabras_cortas)

    return dict(conteo_palabras.most_common(20))
