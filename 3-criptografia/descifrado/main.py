"""
Punto de entrada principal para el decodificador monoalfabético.
"""

import os
from decodificador import DecodificadorMonoalfabetico
from utils.texto import guardar_resultado


def descifrar_texto(
    texto_cifrado=None,
    max_iteraciones=10_000,
    ruta_del_diccionario="data/diccionario_espanol.txt",
    archivo_cifrado="data/texto_cifrado.txt",
    ruta_salida="output/resultado_descifrado.txt",
):
    """
    Función principal para descifrar un texto cifrado por sustitución monoalfabética.

    Args:
        texto_cifrado: String con el texto cifrado.
        max_iteraciones: Número máximo de iteraciones para el algoritmo de optimización.
        ruta_del_diccionario: Ruta a un archivo de diccionario español (opcional).
        archivo_cifrado: Ruta al archivo con el texto cifrado.
        ruta_salida: Ruta donde guardar el resultado del descifrado.

    Returns:
        Tupla (texto_descifrado, mapeo, coherencia).
    """
    decodificador = DecodificadorMonoalfabetico()

    if texto_cifrado is None:
        texto_cifrado = decodificador.leer_texto_cifrado(archivo=archivo_cifrado)

    # Descifrar el texto
    texto_descifrado, mapeo, coherencia = decodificador.descifrar(
        texto_cifrado, max_iteraciones, ruta_del_diccionario
    )

    # Mostrar resultados
    print("\n=== RESULTADO DEL DESCIFRADO ===")
    print(f"Coherencia: {coherencia:.2f}%")
    print("\nTexto descifrado:")
    print(texto_descifrado)
    print("\nMapeo utilizado:")
    for k, v in sorted(mapeo.items()):
        print(f"{k} -> {v}")

    # Guardar resultado en archivo
    guardar_resultado(texto_descifrado, mapeo, coherencia, ruta_salida)

    # Informar al usuario sobre la opción de iteración
    print(
        "\nSugerencia: Si el resultado no es perfecto, puede ejecutar este script nuevamente"
    )
    print("utilizando el archivo de salida como entrada para refinarlo.")

    return texto_descifrado, mapeo, coherencia


# Ejemplo de uso
if __name__ == "__main__":
    # En el texto cifrado sabemos de antemano que la "n" es el espacio
    caracter_espacio = "i"

    ruta_cifrado = "data/texto_cifrado_27.txt"
    # ruta_cifrado = "output/resultado_descifrado.txt"

    try:
        with open(ruta_cifrado, "r", encoding="utf-8") as f:
            texto_cifrado = (
                f.read()
                .lower()
                .replace("\n", "")
                .replace(
                    caracter_espacio,
                    " ",
                )
            )

        # Descifrar el texto
        resultado = descifrar_texto(texto_cifrado, max_iteraciones=25_000)
        print(f"Resultado: {resultado}")

        # standar deviation > language statistic
        # mapping + ciphrated a

    except FileNotFoundError:
        print(f"No se encontró el archivo en {ruta_cifrado}")
    except Exception as e:
        print(f"Error al procesar el archivo: {e}")
