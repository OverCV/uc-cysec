"""
Implementación del algoritmo de hill climbing para optimizar el mapeo de descifrado.
"""

import numpy as np
from utils.texto import descifrar_texto
from algoritmos.coherencia import calcular_coherencia


def busqueda_hill_climbing(
    texto_cifrado,
    mapeo_inicial,
    max_iteraciones=500,
    umbral_coherencia=95,
):
    """Implementa el algoritmo de hill climbing para buscar el mejor mapeo de descifrado.

    Args:
        texto_cifrado: String con el texto cifrado.
        mapeo_inicial: Diccionario con el mapeo inicial.
        max_iteraciones: Número máximo de iteraciones.
        umbral_coherencia: Coherencia mínima a alcanzar para terminar anticipadamente.

    Returns:
        Tuple (mejor_mapeo, coherencia) con el mejor mapeo encontrado y su coherencia.
    """
    mejor_mapeo = mapeo_inicial.copy()
    mejor_coherencia = calcular_coherencia(descifrar_texto(texto_cifrado, mejor_mapeo))

    # Temperatura inicial (para simulated annealing)
    temperatura = 100.0
    enfriamiento = 0.95

    print(f"Iniciando búsqueda con coherencia inicial: {mejor_coherencia:.2f}%")
    print(f"Temperatura inicial: {temperatura:.2f}")

    # Para almacenar el progreso
    mejoras = 0
    mapeo_actual = mejor_mapeo.copy()
    coherencia_actual = mejor_coherencia

    iteracion = 0
    # Condiciones de parada: alcanzar máx iteraciones o coherencia superior al umbral
    while iteracion < max_iteraciones and mejor_coherencia < umbral_coherencia:
        # Actualizar temperatura (enfriamiento gradual)
        if iteracion % 100 == 0 and iteracion > 0:
            temperatura *= enfriamiento
            print(
                f"Iter {iteracion}: Temp={temperatura:.2f}, "
                f"Best Coher={mejor_coherencia:.2f}%, "
                f"Upgrades={mejoras}\n"
            )

        # Seleccionar dos letras al azar del mapeo
        chars_cifrados = list(mapeo_actual.keys())
        if len(chars_cifrados) >= 2:
            idx1, idx2 = np.random.choice(len(chars_cifrados), 2, replace=False)
            char1, char2 = chars_cifrados[idx1], chars_cifrados[idx2]

            # Intercambiar mapeo
            mapeo_nuevo = mapeo_actual.copy()
            mapeo_nuevo[char1], mapeo_nuevo[char2] = (
                mapeo_nuevo[char2],
                mapeo_nuevo[char1],
            )

            # Evaluar coherencia
            texto_descifrado = descifrar_texto(texto_cifrado, mapeo_nuevo)
            coherencia = calcular_coherencia(texto_descifrado)

            # Decidir si aceptar la nueva solución
            delta = coherencia - coherencia_actual

            # Siempre aceptar si mejora, o probabilísticamente si empeora (simulated annealing)
            if delta > 0 or (
                temperatura > 0.1 and np.random.random() < np.exp(delta / temperatura)
            ):
                mapeo_actual = mapeo_nuevo
                coherencia_actual = coherencia

                # Actualizar el mejor mapeo si corresponde
                if coherencia > mejor_coherencia:
                    mejor_mapeo = mapeo_nuevo.copy()  # Important: make a copy!
                    mejor_coherencia = coherencia
                    mejoras += 1

        # Incrementar contador de iteraciones
        iteracion += 1

    return mejor_mapeo, mejor_coherencia
