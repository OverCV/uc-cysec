"""
Funciones para verificar la calidad del texto descifrado mediante diccionario.
"""

import os
import re
import urllib.request
from const import PALABRAS_COMUNES_50


def descargar_diccionario_espanol(
    ruta_guardado="data/diccionario_espanol.txt",
):
    """Descarga un diccionario español si no existe localmente.

    Args:
        ruta_guardado: Ruta donde guardar el diccionario descargado.

    Returns:
        Ruta al diccionario descargado o None si falla la descarga.
    """
    if os.path.exists(ruta_guardado):
        print(f"Diccionario ya existe en {ruta_guardado}")
        return ruta_guardado

    try:
        # URL de un diccionario español (palabras comunes)
        url = "https://github.com/titoBouzout/Dictionaries/blob/master/Spanish.dic"
        print(f"Descargando diccionario desde {url}...")
        urllib.request.urlretrieve(url, ruta_guardado)
        print(f"Diccionario descargado correctamente en {ruta_guardado}")
        return ruta_guardado
    except Exception as e:
        print(f"Error al descargar el diccionario: {e}")
        print("Se utilizará el diccionario incorporado")
        return None


def cargar_diccionario(ruta_diccionario=None):
    """Carga un diccionario de palabras españolas.

    Args:
        ruta_diccionario: Ruta al archivo del diccionario.

    Returns:
        Conjunto con palabras del diccionario.
    """
    diccionario = set()

    # Intentar cargar diccionario externo si está disponible
    if ruta_diccionario and os.path.exists(ruta_diccionario):
        try:
            with open(ruta_diccionario, "r", encoding="utf-8") as f:
                diccionario = set(word.strip().upper() for word in f if word.strip())
            print(f"Diccionario cargado con {len(diccionario)} palabras")
            return diccionario
        except Exception as e:
            print(f"Error al cargar el diccionario: {e}")

    # Si no hay diccionario externo o falló la carga, usar diccionario incorporado
    print("Usando diccionario incorporado (limitado)")
    # Incluimos las palabras comunes que ya teníamos
    diccionario = set(PALABRAS_COMUNES_50)

    # Intenta cargar un diccionario básico incorporado
    try:
        with open(
            "data/diccionario_espanol.txt",
            "r",
            encoding="utf-8",
        ) as f:
            palabras = f.read().lower()
            # Agrega las palabras al diccionario
            for palabra in palabras.split():
                palabra = palabra.strip().upper()
                if palabra:
                    diccionario.add(palabra)
    except Exception as e:
        print(f"No se pudo cargar el diccionario básico: {e}")

    print(f"Diccionario interno creado con {len(diccionario)} palabras")
    return diccionario


def verificar_con_diccionario(texto_descifrado, umbral=0.5, ruta_diccionario=None):
    """Verifica cuántas palabras descifradas existen en un diccionario español.

    Args:
        texto_descifrado: Texto a verificar.
        umbral: Porcentaje mínimo de palabras que deben estar en el diccionario.
        ruta_diccionario: Ruta al archivo del diccionario.

    Returns:
        True si el porcentaje de palabras válidas supera el umbral.
    """
    # Cargar diccionario
    diccionario = cargar_diccionario(ruta_diccionario)

    # Limpiamos y normalizamos el texto descifrado
    texto_limpio = re.sub(r"[^A-ZÁÉÍÓÚÜÑa-záéíóúüñ\s]", " ", texto_descifrado)
    palabras = re.findall(r"\b[A-ZÁÉÍÓÚÜÑa-záéíóúüñ]{2,}\b", texto_limpio.upper())

    if not palabras:
        print("No se encontraron palabras válidas para verificar")
        return False

    # Verificamos cuántas palabras están en el diccionario
    encontradas = sum(1 for p in palabras if p in diccionario)
    porcentaje = (encontradas / len(palabras)) * 100

    print(
        f"Verificación: {encontradas}/{len(palabras)} palabras encontradas ({porcentaje:.2f}%)"
    )

    # Para depuración, mostrar palabras no encontradas
    no_encontradas = [p for p in palabras if p not in diccionario]
    if no_encontradas:
        print(
            f"Palabras no encontradas: {', '.join(no_encontradas[:10])}"
            + ("..." if len(no_encontradas) > 10 else "")
        )

    return porcentaje >= (umbral * 100)
