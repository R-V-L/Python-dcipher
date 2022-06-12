import os
import sys
import requests
from bs4 import BeautifulSoup as bs
from urllib.parse import urlsplit
import hashlib

#claveSinEncriptar = "unicorn"
#clave = "1abcb33beeb811dca15f0ac3e47b88d9"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
}

servicios = {
	'md5': ['https://hashtoolkit.com/decrypt-md5-hash/?hash=', 'https://md5.gromweb.com/?md5=', 'https://md5hashing.net/hash/md5/'],
	'sha1': ['https://hashtoolkit.com/decrypt-sha1-hash/?hash=', 'https://sha1.gromweb.com/?hash=', 'https://md5hashing.net/hash/sha1/'],
	'sha224': ['https://md5hashing.net/hash/sha224/'],
	'sha256': ['https://hashtoolkit.com/decrypt-sha256-hash/?hash=', 'https://md5hashing.net/hash/sha256/'],
	'sha384': ['https://hashtoolkit.com/decrypt-sha384-hash/?hash=', 'https://md5hashing.net/hash/sha384/'],
	'sha512': ['https://hashtoolkit.com/decrypt-sha512-hash/?hash=', 'https://md5hashing.net/hash/sha512/'],
	'ripemd320': ['https://md5hashing.net/hash/ripemd320/']
}


def obtenerClave(uri, cifrado="md5"):
    urlBase = urlsplit(uri).netloc
    urlHtml = requests.get(uri, headers=headers)
    urlParseado = bs(urlHtml.content, 'lxml')
    
    if not urlHtml.status_code == 200:
        return False

    match urlBase:
        case ('hashtoolkit.com'):
            try:
                return urlParseado.find(
                "span", title=f"decrypted {cifrado} hash").get_text(strip=True)
            except:
                return False
        case ('md5.gromweb.com'):
            try:
                return urlParseado.find(
                "em", class_="long-content string").get_text(strip=True)
            except:
                return False
        case _:
            return False

def descifrarHash(clave, cifrado="md5"):
    for uri in servicios[cifrado]:
        url_completa = uri + clave
        claveDescifrada = obtenerClave(url_completa, cifrado)
        if claveDescifrada:
            return f"¡Descifrado ({clave}): {claveDescifrada}"
    return "No se pudo descifrar el hash: " + clave

def cifrarHash(clave, cifrado="md5"):
    match cifrado:
        case ('md5'):
            claveEnBytes = bytes(clave, 'utf-8')
            return f"Cifrado ({clave}): {hashlib.md5(claveEnBytes).hexdigest()}"
        case _:
            return False

#sys.argv.append("1abcb33beeb811dca15f0ac3e47b88d9")
#sys.argv.append("descifrar")

if __name__ == "__main__":
    if len(sys.argv) >= 3:
        clave = sys.argv[1]
        accion = sys.argv[2]
        try:
            cifrado = sys.argv[3]
            print(f"Definido: {sys.argv[3]}")
        except:
            cifrado = "md5"
        if(accion == "descifrar"):
            print(descifrarHash(clave, cifrado))
        elif(accion == "cifrar"):
            print(cifrarHash(clave, cifrado))
    else:
        print(
            f"Error: Se necesita un argumento de entrada, uno de accion [descifrar, cifrar] y un cifrado [md5, sha1, sha224, sha256, sha384, sha512]. Ejemplo: python {os.path.basename(__file__)} unicorn descifrar md5")