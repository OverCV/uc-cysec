"""
Utilidades para el procesamiento de texto cifrado y descifrado.
"""

import re


def leer_texto_cifrado(archivo=None, texto=None):
    """Lee el texto cifrado desde un archivo o directamente como string.

    Args:
        archivo: Ruta al archivo que contiene el texto cifrado.
        texto: String que contiene el texto cifrado.

    Returns:
        String con el texto cifrado.
    """
    if archivo:
        try:
            with open(archivo, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            print(f"Error al leer el archivo: {e}")
            return ""
    return texto


def descifrar_texto(texto_cifrado, mapeo):
    """Descifra el texto usando el mapeo proporcionado.

    Args:
        texto_cifrado: String con el texto cifrado.
        mapeo: Diccionario de mapeo de caracteres cifrados a caracteres descifrados.

    Returns:
        String con el texto descifrado.
    """
    texto_descifrado = ""
    for char in texto_cifrado:
        if char in mapeo:
            texto_descifrado += mapeo[char]
        else:
            texto_descifrado += char

    return texto_descifrado


def guardar_resultado(texto_descifrado, mapeo, coherencia, ruta_salida=None):
    """Guarda el resultado del descifrado en un archivo.

    Args:
        texto_descifrado: String con el texto descifrado.
        mapeo: Diccionario de mapeo utilizado.
        coherencia: Valor de coherencia obtenido.
        ruta_salida: Ruta donde guardar el archivo de salida.
    """
    if ruta_salida is None:
        ruta_salida = "descifrado/output/resultado_descifrado.txt"

    try:
        with open(ruta_salida, "w", encoding="utf-8") as f:
            f.write("=== RESULTADO DEL DESCIFRADO ===\n")
            f.write(f"Coherencia: {coherencia:.2f}%\n\n")
            f.write("Texto descifrado:\n")
            f.write(texto_descifrado)
            f.write("\n\nMapeo utilizado:\n")
            for k, v in sorted(mapeo.items()):
                f.write(f"{k} -> {v}\n")
        print(f"\nResultado guardado en '{ruta_salida}'")
    except Exception as e:
        print(f"No se pudo guardar el resultado: {e}")


def limpiar_texto(texto):
    """Limpia y normaliza un texto para su procesamiento.

    Args:
        texto: String con el texto a limpiar.

    Returns:
        String con el texto limpio.
    """
    return re.sub(r"[^A-ZÁÉÍÓÚÜÑa-záéíóúüñ\s]", " ", texto)


def extraer_palabras(texto):
    """Extrae palabras válidas de un texto.

    Args:
        texto: String con el texto del que extraer palabras.

    Returns:
        Lista de palabras extraídas.
    """
    texto_limpio = limpiar_texto(texto)
    return re.findall(r"\b[A-ZÁÉÍÓÚÜÑa-záéíóúüñ]{2,}\b", texto_limpio.upper())
