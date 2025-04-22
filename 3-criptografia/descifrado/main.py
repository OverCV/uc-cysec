import re
import string
import os
from collections import Counter
import numpy as np
import urllib.request

from const import (
    FREC_ESPANOL,
    PALABRAS_COMUNES_50,
    BIGRAMAS,
    TRIGRAMAS,
)


class DecodificadorMonoalfabetico:
    def __init__(self):
        # Frecuencias aproximadas de las letras en castellano (en porcentaje)
        self.frecuencias_esp = FREC_ESPANOL

        # Palabras comunes cortas en castellano (2-3 caracteres)
        self.palabras_comunes = PALABRAS_COMUNES_50

        # Para verificar coherencia, usamos bigramas y trigramas comunes
        self.bigramas_comunes = BIGRAMAS

        self.trigramas_comunes = TRIGRAMAS

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
        """Calcula la coherencia del texto descifrado basado en n-gramas comunes

        Esta función evalúa qué tan "español" suena un texto descifrado analizando
        los bigramas y trigramas (secuencias de 2 y 3 letras) y comparándolos con
        los más comunes del idioma español.

        Args:
            texto_descifrado: El texto descifrado a evaluar

        Returns:
            Puntuación de coherencia (0-100%)
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
        todos_bigramas = set(self.bigramas_comunes + bigramas_esp)
        todos_trigramas = set(self.trigramas_comunes + trigramas_esp)

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
        puntuacion_bi_freq = sum(
            1 for bg in bigramas_frecuentes if bg in todos_bigramas
        )
        puntuacion_tri_freq = sum(
            1 for tg in trigramas_frecuentes if tg in todos_trigramas
        )

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

    def busqueda_hill_climbing(
        self,
        texto_cifrado,
        mapeo_inicial,
        max_iteraciones=500,
    ):
        mejor_mapeo = mapeo_inicial.copy()
        mejor_coherencia = self.calcular_coherencia(
            self.descifrar_texto(texto_cifrado, mejor_mapeo)
        )

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
        # Change from "or" to "and" - we want BOTH conditions to be true
        while iteracion < max_iteraciones and mejor_coherencia < 95:
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
                texto_descifrado = self.descifrar_texto(texto_cifrado, mapeo_nuevo)
                coherencia = self.calcular_coherencia(texto_descifrado)

                # Decidir si aceptar la nueva solución
                delta = coherencia - coherencia_actual

                # Siempre aceptar si mejora, o probabilísticamente si empeora (simulated annealing)
                if delta > 0 or (
                    temperatura > 0.1
                    and np.random.random() < np.exp(delta / temperatura)
                ):
                    mapeo_actual = mapeo_nuevo
                    coherencia_actual = coherencia

                    # Actualizar el mejor mapeo si corresponde
                    if coherencia > mejor_coherencia:
                        mejor_mapeo = mapeo_nuevo.copy()  # Important: make a copy!
                        mejor_coherencia = coherencia
                        mejoras += 1

            # Don't forget to increment the counter!
            iteracion += 1

        # Add a return statement at the end
        return mejor_mapeo, mejor_coherencia

    def verificar_con_diccionario(
        self, texto_descifrado, umbral=0.5, ruta_diccionario=None
    ):
        """Verifica cuántas palabras descifradas existen en un diccionario español

        Args:
            texto_descifrado: Texto a verificar
            umbral: Porcentaje mínimo de palabras que deben estar en el diccionario
            ruta_diccionario: Ruta al archivo del diccionario (opcional)

        Returns:
            True si el porcentaje de palabras válidas supera el umbral
        """
        # Diccionario de español
        # Si no se proporciona un archivo externo, intentamos usar un diccionario predefinido
        diccionario = set()

        if ruta_diccionario and os.path.exists(ruta_diccionario):
            try:
                with open(ruta_diccionario, "r", encoding="utf-8") as f:
                    diccionario = set(
                        word.strip().upper() for word in f if word.strip()
                    )
                print(f"Diccionario cargado con {len(diccionario)} palabras")
            except Exception as e:
                print(f"Error al cargar el diccionario: {e}")

        # Si no hay diccionario externo o falló la carga, usamos un diccionario incorporado
        if not diccionario:
            print("Usando diccionario incorporado (limitado)")
            # Incluimos las palabras comunes que ya teníamos
            diccionario = set(self.palabras_comunes)

            # Agregamos palabras frecuentes en español
            palabras_frecuentes = ""
            # with open("tests/texto_decifrado.txt", "r", encoding="utf-8") as f:
            with open(
                "descifrado/data/diccionario_espanol.txt", "r", encoding="utf-8"
            ) as f:
                palabras_frecuentes = f.read().lower()

            # Agrega las palabras frecuentes al diccionario
            for palabra in palabras_frecuentes.split():
                palabra = palabra.strip().upper()
                if palabra:
                    diccionario.add(palabra)

            print(f"Diccionario interno creado con {len(diccionario)} palabras")

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

    def descargar_diccionario_espanol(self, ruta_guardado="diccionario_espanol.txt"):
        """Descarga un diccionario español si no existe localmente"""
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

    def descifrar(self, texto_cifrado, max_iteraciones=5000, ruta_diccionario=None):
        """Proceso completo de descifrado"""
        print("Iniciando proceso de descifrado...")

        # Intentar descargar/cargar diccionario si no se proporciona
        if ruta_diccionario is None:
            ruta_diccionario = self.descargar_diccionario_espanol()

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

        # Paso 7: Verificar resultado con diccionario completo
        verificado = self.verificar_con_diccionario(
            texto_descifrado, 0.5, ruta_diccionario
        )

        if coherencia >= 90 or verificado:
            print("¡Descifrado exitoso!")
        else:
            print("Descifrado parcial (puede requerir ajustes manuales)")

        return texto_descifrado, mejor_mapeo, coherencia


# Función para ejecutar el decodificador
def descifrar_texto(
    texto_cifrado=None, archivo_cifrado=None, max_iteraciones=10_000, diccionario=None
):
    """
    Función principal para descifrar un texto cifrado por sustitución monoalfabética

    Args:
        texto_cifrado: String con el texto cifrado
        archivo_cifrado: Ruta al archivo con el texto cifrado
        max_iteraciones: Número máximo de iteraciones para el algoritmo de optimización
        diccionario: Ruta a un archivo de diccionario español (opcional)

    Returns:
        Tupla (texto_descifrado, mapeo, coherencia)
    """
    decodificador = DecodificadorMonoalfabetico()

    if archivo_cifrado:
        texto_cifrado = decodificador.leer_texto_cifrado(archivo=archivo_cifrado)
    elif texto_cifrado is None:
        raise ValueError("Debe proporcionar texto cifrado o ruta a un archivo")

    # Descifrar el texto
    texto_descifrado, mapeo, coherencia = decodificador.descifrar(
        texto_cifrado, max_iteraciones, diccionario
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
    try:
        with open(
            "descifrado/output/resultado_descifrado.txt",
            "w",
            encoding="utf-8",
        ) as f:
            f.write("=== RESULTADO DEL DESCIFRADO ===\n")
            f.write(f"Coherencia: {coherencia:.2f}%\n\n")
            f.write("Texto descifrado:\n")
            f.write(texto_descifrado)
            f.write("\n\nMapeo utilizado:\n")
            for k, v in sorted(mapeo.items()):
                f.write(f"{k} -> {v}\n")
        print("\nResultado guardado en 'descifrado/output/resultado_descifrado.txt'")
    except Exception as e:
        print(f"No se pudo guardar el resultado: {e}")

    return texto_descifrado, mapeo, coherencia


# Ejemplo de uso
if __name__ == "__main__":
    # En el texto cifrado sabemos de antemano que la "n" es el espacio.
    caracter_espacio = "n"
    # Texto cifrado de ejemplo
    texto_cifrado = ""
    with open("descifrado/data/texto_cifrado.txt", "r", encoding="utf-8") as f:
        texto_cifrado = (
            f.read()
            .replace(
                caracter_espacio,
                " ",
            )
            .replace("\n", "")
            .lower()
        )

    # print(texto_cifrado)

    # Descifrar el texto
    res = descifrar_texto(texto_cifrado, max_iteraciones=25_000)
    print(f"{res=}")
