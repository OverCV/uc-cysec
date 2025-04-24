"""
Clase principal del decodificador monoalfabético.
"""

from utils.texto import leer_texto_cifrado, descifrar_texto
from utils.frecuencias import analizar_frecuencias, identificar_patrones
from utils.mapeo import mapear_frecuencias_iniciales, refinar_mapeo_con_patrones
from utils.verificacion import verificar_con_diccionario, descargar_diccionario_espanol
from algoritmos.hill_climbing import busqueda_hill_climbing
from algoritmos.coherencia import calcular_coherencia


class DecodificadorMonoalfabetico:
    """Clase para descifrar textos cifrados con sustitución monoalfabética."""

    def __init__(self):
        """Inicializa el decodificador."""
        pass

    def leer_texto_cifrado(self, archivo=None, texto=None):
        """Lee el texto cifrado desde un archivo o directamente como string."""
        return leer_texto_cifrado(archivo, texto)

    def analizar_frecuencias(self, texto):
        """Analiza las frecuencias de caracteres en el texto cifrado."""
        return analizar_frecuencias(texto)

    def mapear_frecuencias_iniciales(self, frecuencias_cifrado):
        """Crea un mapeo inicial basado en frecuencias."""
        return mapear_frecuencias_iniciales(frecuencias_cifrado)

    def identificar_patrones(self, texto_cifrado):
        """Identifica patrones que podrían corresponder a palabras comunes."""
        return identificar_patrones(texto_cifrado)

    def refinar_mapeo_con_patrones(self, mapeo, patrones, texto_cifrado):
        """Refina el mapeo usando patrones de palabras comunes."""
        return refinar_mapeo_con_patrones(mapeo, patrones, texto_cifrado)

    def descifrar_texto(self, texto_cifrado, mapeo):
        """Descifra el texto usando el mapeo actual."""
        return descifrar_texto(texto_cifrado, mapeo)

    def calcular_coherencia(self, texto_descifrado):
        """Calcula la coherencia del texto descifrado basado en n-gramas comunes."""
        return calcular_coherencia(texto_descifrado)

    def busqueda_hill_climbing(
        self, texto_cifrado, mapeo_inicial, max_iteraciones=500, umbral_coherencia=95
    ):
        """Implementa el algoritmo de hill climbing para buscar el mejor mapeo."""
        return busqueda_hill_climbing(
            texto_cifrado, mapeo_inicial, max_iteraciones, umbral_coherencia
        )

    def verificar_con_diccionario(
        self, texto_descifrado, umbral=0.5, ruta_diccionario=None
    ):
        """Verifica cuántas palabras descifradas existen en un diccionario español."""
        return verificar_con_diccionario(texto_descifrado, umbral, ruta_diccionario)

    def descargar_diccionario_espanol(
        self, ruta_guardado="descifrado/data/diccionario_espanol.txt"
    ):
        """Descarga un diccionario español si no existe localmente."""
        return descargar_diccionario_espanol(ruta_guardado)

    def descifrar(
        self,
        texto_cifrado,
        max_iteraciones=5000,
        ruta_diccionario="data/diccionario_espanol.txt",
    ):
        """Proceso completo de descifrado.

        Args:
            texto_cifrado: String con el texto cifrado.
            max_iteraciones: Número máximo de iteraciones para el algoritmo.
            ruta_diccionario: Ruta al archivo del diccionario español.

        Returns:
            Tupla (texto_descifrado, mapeo, coherencia).
        """
        print("Iniciando proceso de descifrado...")

        # Intentar descargar/cargar diccionario si no se proporciona
        if ruta_diccionario is None:
            ruta_diccionario = self.descargar_diccionario_espanol()

        # Verificar si el texto de entrada ya tiene alta coherencia
        # Creamos un mapeo identidad (cada carácter se mapea a sí mismo)
        chars_unicos = set(c for c in texto_cifrado if c.isalpha())
        mapeo_identidad = {c: c for c in chars_unicos}

        coherencia_inicial = self.calcular_coherencia(texto_cifrado)
        print(f"Coherencia del texto de entrada: {coherencia_inicial:.2f}%")

        # Si la coherencia ya es alta, asumimos que el texto ya está descifrado
        # o se encuentra en un estado avanzado de descifrado
        if coherencia_inicial >= 70:
            print(
                "¡El texto ya tiene alta coherencia! Saltando pasos iniciales de mapeo."
            )
            mejor_mapeo = mapeo_identidad
            # Aún así, intentamos refinar con hill climbing por si podemos mejorar
            print("Refinando con hill climbing desde el estado actual...")
            mejor_mapeo, coherencia = self.busqueda_hill_climbing(
                texto_cifrado,
                mapeo_identidad,
                max_iteraciones,
                98,  # Umbral más alto para textos ya coherentes
            )
            texto_descifrado = self.descifrar_texto(texto_cifrado, mejor_mapeo)
        else:
            # Proceso normal para texto cifrado
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

            # Verificamos la coherencia después del mapeo inicial
            texto_refinado = self.descifrar_texto(texto_cifrado, mapeo_refinado)
            coherencia_refinada = self.calcular_coherencia(texto_refinado)
            print(f"Coherencia después del mapeo inicial: {coherencia_refinada:.2f}%")

            # Si el mapeo inicial empeora significativamente la coherencia,
            # volvemos al mapeo identidad
            if coherencia_refinada < coherencia_inicial * 0.8:  # 20% peor
                print("El mapeo inicial empeora la coherencia. Usando mapeo identidad.")
                mapeo_refinado = mapeo_identidad

            # Paso 5: Buscar mejor solución mediante hill climbing
            mejor_mapeo, coherencia = self.busqueda_hill_climbing(
                texto_cifrado,
                mapeo_refinado,
                max_iteraciones,
                95,  # Umbral estándar
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
