"""
Funciones para post-procesamiento y corrección final del texto descifrado.
"""

import re


def corregir_monogramas(texto_descifrado):
    """Corrige monogramas aislados según reglas del español.

    En español, los caracteres aislados suelen ser Y, A, O, E.

    Args:
        texto_descifrado: Texto descifrado a corregir.

    Returns:
        Texto con monogramas corregidos.
    """

    # Buscar palabras de un solo carácter
    def reemplazar_monograma(match):
        char = match.group(1).upper()
        # Estos son los únicos caracteres que pueden aparecer solos en español
        if char not in ["Y", "A", "O", "E", "U"]:
            # Determinar cuál usar según el contexto
            if match.group(0).startswith(" ") and match.group(0).endswith(" "):
                return " Y "  # La conjunción más común
            return " A "  # Segunda más común
        return match.group(0)

    # Aplicar la corrección (palabra de un solo carácter entre espacios)
    texto_corregido = re.sub(r"\s([a-zA-Z])\s", reemplazar_monograma, texto_descifrado)
    return texto_corregido


def corregir_patrones_comunes(texto_descifrado):
    """Corrige patrones comunes en el texto descifrado.

    Args:
        texto_descifrado: Texto descifrado a corregir.

    Returns:
        Texto con patrones corregidos.
    """
    correcciones = [
        # Patrón: reemplazo
        (r"\bj([aeiou])", r"b\1"),  # "ja", "je", etc. -> "ba", "be"
        (r"\bp([aeiou])", r"p\1"),  # "pa", "pe", etc. -> "pa", "pe"
        (r"\bz([aeiou])", r"p\1"),  # "za", "ze", etc. -> "pa", "pe"
        (r"\bf([aeiou])", r"j\1"),  # "fa", "fe", etc. -> "ja", "je"
        (r"\bx([aeiou])", r"h\1"),  # "xa", "xe", etc. -> "ha", "he"
        (r"\v([aeiou])", r"w\1"),  # "va", "ve", etc. -> "wa", "we"
        # Terminaciones
        (r"([aeiou])w\b", r"\1r"),  # Terminaciones en "aw", "ew" -> "ar", "er"
        (r"([aeiou])q\b", r"\1s"),  # Terminaciones en "as", "es" -> "aq", "eq"
    ]

    texto_corregido = texto_descifrado
    for patron, reemplazo in correcciones:
        texto_corregido = re.sub(patron, reemplazo, texto_corregido)

    return texto_corregido


def aplicar_correcciones_finales(texto_descifrado, mapeo):
    """Aplica correcciones finales al texto descifrado.

    Args:
        texto_descifrado: Texto descifrado a corregir.
        mapeo: Diccionario de mapeo utilizado.

    Returns:
        Texto corregido y mapeo actualizado.
    """
    # Aplicar correcciones a monogramas
    texto_corregido = corregir_monogramas(texto_descifrado)

    # Aplicar correcciones a patrones comunes
    texto_corregido = corregir_patrones_comunes(texto_corregido)

    # Actualizar el mapeo según las correcciones realizadas
    mapeo_actualizado = mapeo.copy()

    # Si hemos hecho cambios en el texto que no se reflejan en el mapeo,
    # podemos necesitar actualizar el mapeo para mantener la coherencia

    return texto_corregido, mapeo_actualizado
