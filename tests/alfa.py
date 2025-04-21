texto_cifrado = ""
with open("texto_cifrado.txt", "r") as f:
    texto_cifrado = f.read()

texto_decifrado = ""
with open("texto_decifrado.txt", "r") as f:
    texto_decifrado = f.read()

mapeo = {}
for decifra, cifra in zip(texto_decifrado, texto_cifrado):
    if decifra not in mapeo:
        mapeo[decifra] = cifra

print(mapeo)
