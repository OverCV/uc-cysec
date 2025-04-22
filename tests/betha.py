import re
import string
from collections import Counter
import numpy as np


class DecodificadorMonoalfabetico:
    def __init__(self):
        # Frecuencias aproximadas de las letras en castellano (en porcentaje)
        self.frecuencias_esp = {
            "E": 13.68,
            "A": 12.53,
            "O": 8.68,
            "L": 8.28,
            "S": 7.98,
            "N": 7.01,
            "D": 5.86,
            "R": 4.69,
            "U": 4.63,
            "I": 4.56,
            "T": 4.34,
            "C": 3.96,
            "P": 2.51,
            "M": 2.45,
            "Y": 1.54,
            "Q": 1.53,
            "B": 1.42,
            "H": 1.19,
            "G": 1.01,
            "F": 0.69,
            "V": 0.55,
            "J": 0.50,
            "Z": 0.47,
            "X": 0.13,
            "K": 0.01,
            "W": 0.01,
        }

        # Palabras comunes cortas en castellano (2-3 caracteres)
        self.palabras_comunes = [
            "DE",
            "LA",
            "EL",
            "EN",
            "Y",
            "A",
            "O",
            "QUE",
            "DEL",
            "LOS",
            "SE",
            "LAS",
            "POR",
            "UN",
            "NO",
            "UNA",
            "SU",
            "CON",
            "ES",
            "AL",
            "LO",
            "SI",
            "HA",
            "ME",
            "TE",
            "MI",
            "TU",
        ]

        # Para verificar coherencia, usamos bigramas y trigramas comunes
        self.bigramas_comunes = [
            "ES",
            "DE",
            "EN",
            "EL",
            "LA",
            "QU",
            "AR",
            "NT",
            "ER",
            "RA",
            "ON",
            "AL",
            "RE",
            "CO",
            "ST",
            "OR",
            "AN",
            "TA",
            "CA",
            "TE",
        ]

        self.trigramas_comunes = [
            "QUE",
            "EST",
            "CON",
            "ENT",
            "LOS",
            "ARA",
            "ACI",
            "NTE",
            "ION",
            "ESE",
            "NTO",
            "LAS",
            "RES",
            "TRA",
            "PRE",
            "ERE",
            "TEN",
            "FOR",
            "ORA",
            "POR",
        ]

    def leer_texto_cifrado(self, archivo=None, texto=None):
        """Lee el texto cifrado desde un archivo o directamente como string"""
        if archivo:
            with open(archivo, "r", encoding="utf-8") as f:
                return f.read()
        return texto

    def analizar_frecuencias(self, texto):
        """Analiza las frecuencias de caracteres en el texto cifrado"""
        # Filtramos solo caracteres que parecen ser parte del cifrado
        chars = re.findall(
            r"[a-zA-Z0-9\!\@\#\$\%\^\&\*\(\)\[\]\{\}\;\:\'\"\,\.\<\>\/\?\-\_\=\+\\]",
            texto,
        )
        conteo = Counter(chars)
        total = sum(conteo.values())

        # Convertimos a porcentajes
        frecuencias = {char: (count / total) * 100 for char, count in conteo.items()}
        return dict(sorted(frecuencias.items(), key=lambda x: x[1], reverse=True))

    def mapear_frecuencias_iniciales(self, frecuencias_cifrado):
        """Crea un mapeo inicial basado en frecuencias"""
        # Ordenamos las letras del español por frecuencia
        letras_esp_ordenadas = sorted(
            self.frecuencias_esp.keys(),
            key=lambda x: self.frecuencias_esp[x],
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

    def identificar_patrones(self, texto_cifrado):
        """Identifica patrones que podrían corresponder a palabras comunes"""
        palabras_cifradas = re.findall(
            r"[a-zA-Z0-9\!\@\#\$\%\^\&\*\(\)\[\]\{\}\;\:\'\"\,\.\<\>\/\?\-\_\=\+\\]+",
            texto_cifrado,
        )

        # Buscamos palabras de 1, 2 y 3 caracteres (posibles artículos, preposiciones, etc.)
        palabras_cortas = [p for p in palabras_cifradas if len(p) <= 3]

        # Contamos frecuencias de palabras cortas
        conteo_palabras = Counter(palabras_cortas)

        return dict(conteo_palabras.most_common(20))

    def refinar_mapeo_con_patrones(self, mapeo, patrones, texto_cifrado):
        """Refina el mapeo usando patrones de palabras comunes"""
        # Buscamos caracteres que aparecen en posiciones específicas de palabras cortas
        # Por ejemplo, en español, 'EL', 'LA', 'DE' son muy comunes

        mapeo_refinado = mapeo.copy()

        # Intentamos identificar patrones que podrían corresponder a palabras comunes
        for palabra_cifrada, frecuencia in patrones.items():
            if len(palabra_cifrada) == 2:
                # Posibles candidatos: DE, LA, EL, EN, Y, etc.
                candidatos = [p for p in self.palabras_comunes if len(p) == 2]
                for candidato in candidatos:
                    # Verificar si la asignación tiene sentido con el mapeo actual
                    compatible = True
                    for i, char in enumerate(palabra_cifrada):
                        if (
                            char in mapeo_refinado
                            and mapeo_refinado[char] != candidato[i]
                        ):
                            compatible = False
                            break

                    if compatible:
                        # Actualizar mapeo con este candidato
                        for i, char in enumerate(palabra_cifrada):
                            mapeo_refinado[char] = candidato[i]
                        break

            elif len(palabra_cifrada) == 1:
                # Posibles candidatos: Y, A, O
                candidatos = [p for p in self.palabras_comunes if len(p) == 1]
                for candidato in candidatos:
                    if (
                        palabra_cifrada in mapeo_refinado
                        and mapeo_refinado[palabra_cifrada] != candidato
                    ):
                        continue

                    mapeo_refinado[palabra_cifrada] = candidato
                    break

        return mapeo_refinado

    def descifrar_texto(self, texto_cifrado, mapeo):
        """Descifra el texto usando el mapeo actual"""
        texto_descifrado = ""
        for char in texto_cifrado:
            if char in mapeo:
                texto_descifrado += mapeo[char]
            else:
                texto_descifrado += char

        return texto_descifrado

    def calcular_coherencia(self, texto_descifrado):
        """Calcula la coherencia del texto descifrado basado en n-gramas comunes"""
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

        puntuacion_bi = sum(1 for bg in count_bi if bg in self.bigramas_comunes)
        puntuacion_tri = sum(1 for tg in count_tri if tg in self.trigramas_comunes)

        # Normalizar puntuación (0-100%)
        max_bi = min(len(self.bigramas_comunes), len(count_bi))
        max_tri = min(len(self.trigramas_comunes), len(count_tri))

        if max_bi == 0 or max_tri == 0:
            return 0

        coherencia = (puntuacion_bi / max_bi * 0.4) + (puntuacion_tri / max_tri * 0.6)
        return coherencia * 100

    def busqueda_hill_climbing(
        self, texto_cifrado, mapeo_inicial, max_iteraciones=1000
    ):
        """Mejora el mapeo usando hill climbing"""
        mejor_mapeo = mapeo_inicial.copy()
        mejor_coherencia = self.calcular_coherencia(
            self.descifrar_texto(texto_cifrado, mejor_mapeo)
        )

        letras_esp = list(string.ascii_uppercase)

        iteracion = 0
        while iteracion < max_iteraciones and mejor_coherencia < 90:
            # Seleccionar dos letras al azar del mapeo
            chars_cifrados = list(mejor_mapeo.keys())
            if len(chars_cifrados) >= 2:
                idx1, idx2 = np.random.choice(len(chars_cifrados), 2, replace=False)
                char1, char2 = chars_cifrados[idx1], chars_cifrados[idx2]

                # Intercambiar mapeo
                mapeo_nuevo = mejor_mapeo.copy()
                mapeo_nuevo[char1], mapeo_nuevo[char2] = (
                    mapeo_nuevo[char2],
                    mapeo_nuevo[char1],
                )

                # Evaluar coherencia
                texto_descifrado = self.descifrar_texto(texto_cifrado, mapeo_nuevo)
                coherencia = self.calcular_coherencia(texto_descifrado)

                # Si mejora, actualizar mejor mapeo
                if coherencia > mejor_coherencia:
                    mejor_mapeo = mapeo_nuevo
                    mejor_coherencia = coherencia

            iteracion += 1

        return mejor_mapeo, mejor_coherencia

    def verificar_con_diccionario(self, texto_descifrado, umbral=0.5):
        """Verifica cuántas palabras descifradas existen en un diccionario español"""
        # Simplificado - en una implementación real usaríamos un diccionario completo
        diccionario_basico = self.palabras_comunes + [
            "ACTUALMENTE",
            "DISPONEMOS",
            "GRAN",
            "CANTIDAD",
            "NAVEGADORES",
            "WEB",
            "PARA",
            "ELEGIR",
            "NUESTRO",
            "CONCEPTOS",
            "COMO",
            "SEGURIDAD",
            "CUMPLIMIENTO",
        ]

        palabras = re.findall(r"\b[A-Z]+\b", texto_descifrado.upper())
        total = len(palabras)

        if total == 0:
            return 0

        encontradas = sum(1 for p in palabras if p in diccionario_basico)
        return (encontradas / total) >= umbral

    def descifrar(self, texto_cifrado, max_iteraciones=75_00):
        """Proceso completo de descifrado"""
        print("Iniciando proceso de descifrado...")

        # Paso 1: Analizar frecuencias
        frecuencias = self.analizar_frecuencias(texto_cifrado)
        print("Frecuencias analizadas:", frecuencias)

        # Paso 2: Mapeo inicial basado en frecuencias
        mapeo_inicial = self.mapear_frecuencias_iniciales(frecuencias)
        print("Mapeo inicial:", mapeo_inicial)

        # Paso 3: Identificar patrones de palabras comunes
        patrones = self.identificar_patrones(texto_cifrado)
        print("Patrones identificados:", patrones)

        # Paso 4: Refinar mapeo con patrones
        mapeo_refinado = self.refinar_mapeo_con_patrones(
            mapeo_inicial, patrones, texto_cifrado
        )
        print("Mapeo refinado con patrones:", mapeo_refinado)

        # Paso 5: Buscar mejor solución mediante hill climbing
        mejor_mapeo, coherencia = self.busqueda_hill_climbing(
            texto_cifrado, mapeo_refinado, max_iteraciones
        )
        print(f"Mapeo final (coherencia: {coherencia:.2f}%):", mejor_mapeo)

        # Paso 6: Descifrar con el mejor mapeo
        texto_descifrado = self.descifrar_texto(texto_cifrado, mejor_mapeo)

        # Paso 7: Verificar resultado
        verificado = self.verificar_con_diccionario(texto_descifrado)

        if coherencia >= 90 or verificado:
            print("¡Descifrado exitoso!")
        else:
            print("Descifrado parcial (puede requerir ajustes manuales)")

        return texto_descifrado, mejor_mapeo, coherencia


# Función para ejecutar el decodificador
def descifrar_texto(texto_cifrado=None, archivo_cifrado=None, max_iteraciones=10_000):
    decodificador = DecodificadorMonoalfabetico()

    if archivo_cifrado:
        texto_cifrado = decodificador.leer_texto_cifrado(archivo=archivo_cifrado)
    elif texto_cifrado is None:
        raise ValueError("Debe proporcionar texto cifrado o ruta a un archivo")

    texto_descifrado, mapeo, coherencia = decodificador.descifrar(
        texto_cifrado, max_iteraciones
    )

    print("\n=== RESULTADO DEL DESCIFRADO ===")
    print(f"Coherencia: {coherencia:.2f}%")
    print("\nTexto descifrado:")
    print(texto_descifrado)
    print("\nMapeo utilizado:")
    for k, v in sorted(mapeo.items()):
        print(f"{k} -> {v}")

    return texto_descifrado, mapeo, coherencia


# Ejemplo de uso
if __name__ == "__main__":
    # Texto cifrado de ejemplo
    caracter_espacio = "n"
    texto_cifrado = ""
    with open("tests/texto_cifrado.txt", "r", encoding="utf-8") as f:
        texto_cifrado = f.read().replace("\n", "").replace(caracter_espacio, " ")

    # print(texto_cifrado)

    # Descifrar el texto
    res = descifrar_texto(texto_cifrado, max_iteraciones=10_000)
    print(f"{res=}")
