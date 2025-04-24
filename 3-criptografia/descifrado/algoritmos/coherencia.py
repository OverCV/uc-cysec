"""
Funciones para calcular la coherencia de un texto descifrado.
"""

from collections import Counter
from const import BIGRAMAS, TRIGRAMAS


def calcular_coherencia(texto_descifrado):
    """Calcula la coherencia del texto descifrado basado en n-gramas comunes.

    Esta función evalúa qué tan "español" suena un texto descifrado analizando
    los bigramas y trigramas (secuencias de 2 y 3 letras) y comparándolos con
    los más comunes del idioma español.

    Args:
        texto_descifrado: El texto descifrado a evaluar.

    Returns:
        Puntuación de coherencia (0-100%).
    """
    texto = texto_descifrado.upper()

    # Contamos bigramas y trigramas
    bigramas = []
    trigramas = []

    for i in range(len(texto) - 1):
        if texto[i : i + 2].isalpha():
            bigramas.append(texto[i : i + 2])

    for i in range(len(texto) - 2):
        if texto[i : i + 3].isalpha():
            trigramas.append(texto[i : i + 3])

    # Calculamos puntuación de coherencia
    count_bi = Counter(bigramas)
    count_tri = Counter(trigramas)

    # Agregamos bigramas y trigramas más comunes en español
    # Bigramas más frecuentes en español
    bigramas_esp = BIGRAMAS

    # Trigramas más frecuentes en español
    trigramas_esp = TRIGRAMAS

    # Combinamos con los que ya teníamos
    todos_bigramas = set(BIGRAMAS + bigramas_esp)
    todos_trigramas = set(TRIGRAMAS + trigramas_esp)

    # Calculamos cuántos de los bigramas/trigramas del texto están entre los comunes
    bigramas_encontrados = set(count_bi.keys()).intersection(todos_bigramas)
    trigramas_encontrados = set(count_tri.keys()).intersection(todos_trigramas)

    # Analizamos los bigramas/trigramas más frecuentes del texto
    bigramas_frecuentes = [bg for bg, _ in count_bi.most_common(20)]
    trigramas_frecuentes = [tg for tg, _ in count_tri.most_common(20)]

    # Calculamos puntuación por coincidencia con n-gramas comunes
    puntuacion_bi = len(bigramas_encontrados)
    puntuacion_tri = len(trigramas_encontrados)

    # Calculamos puntuación por frecuencia de n-gramas en el texto
    # (esto ayuda a detectar si las letras más comunes están bien mapeadas)
    puntuacion_bi_freq = sum(1 for bg in bigramas_frecuentes if bg in todos_bigramas)
    puntuacion_tri_freq = sum(1 for tg in trigramas_frecuentes if tg in todos_trigramas)

    # Normalizar puntuación (0-100%)
    max_bi = max(1, min(len(todos_bigramas), len(count_bi)))
    max_tri = max(1, min(len(todos_trigramas), len(count_tri)))
    max_bi_freq = max(1, min(20, len(bigramas_frecuentes)))
    max_tri_freq = max(1, min(20, len(trigramas_frecuentes)))

    # Calculamos coherencia combinando las puntuaciones
    coherencia = (
        (puntuacion_bi / max_bi * 0.3)
        + (puntuacion_tri / max_tri * 0.3)
        + (puntuacion_bi_freq / max_bi_freq * 0.2)
        + (puntuacion_tri_freq / max_tri_freq * 0.2)
    )

    # Mostrar información de diagnóstico
    print(f"BG: {puntuacion_bi}/{max_bi}")
    print(f"TG: {puntuacion_tri}/{max_tri}")
    print(f"BG-C: {puntuacion_bi_freq}/{max_bi_freq}")
    print(f"TG-C: {puntuacion_tri_freq}/{max_tri_freq}")

    return coherencia * 100
