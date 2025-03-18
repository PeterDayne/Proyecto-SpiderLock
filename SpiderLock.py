# Autor: Pedro Chavez Ruiz
# Fecha: 14/03/2025 (Primera versiona)

# Bibliotecas
import os
import sys
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from base64 import b64encode, b64decode

# Generar claves con RSA
def generar_claves():

    clave = RSA.generate(2048)

    if not os.path.exists("clave_privada.pem") and not os.path.exists("clave_publica.pem"):
        with open("clave_privada.pem", "wb") as archivo_privado:
            archivo_privado.write(clave.export_key())

        with open("clave_publica.pem", "wb") as archivo_publico:
            archivo_publico.write(clave.publickey().export_key())

        print("Claves RSA generadas.")

    else:
    
        print("Las claves ya existen, no se generaron nuevas.")

# Se cifra el archivo con AES y luego se cifra la clave AES con RSA
def cifrar(archivo, clave_publica):

    # Leer los datos del archivo
    with open(archivo, "rb") as f:
        datos = f.read()
    
    # Generar clave AES de manera aleatoria
    clave_aes = os.urandom(16)
    
    # Cifrar los datos del archivo con la clave AES
    cifrar_aes = AES.new(clave_aes, AES.MODE_EAX)
    text_cifrado, verificador = cifrar_aes.encrypt_and_digest(datos)
    
    # Cifrar clave AES (del archivo) con RSA (ya generadas)
    with open(clave_publica, "rb") as f:

        clave_rsa = RSA.import_key(f.read())

    cifrar_rsa = PKCS1_OAEP.new(clave_rsa)
    clave_aes_cifrada = cifrar_rsa.encrypt(clave_aes)
    
    # Guardar archivo cifrado
    with open(archivo, "wb") as f:

        f.write(clave_aes_cifrada + cifrar_aes.nonce + verificador + text_cifrado)

    print("Archivo cifrado.")

# Se descifra el archivo con RSA y luego se descifra la clave AES con AES
def descifrar(archivo_cifrado, clave_privada):

    # Leer los datos del archivo cifrado
    with open(archivo_cifrado, "rb") as f:

        contenido = f.read()
    
    # Extraer el contenido por partes
    clave_aes_cifrada = contenido[:256]
    nonce = contenido[256:272]
    tag = contenido[272:288]
    texto_cifrado = contenido[288:]
    
    # Importar (extraer) la clave privada RSA del archivo clave_privada.pem
    with open(clave_privada, "rb") as f:
        clave_rsa = RSA.import_key(f.read())

    # Descifrar clave AES con RSA
    descifrar_rsa = PKCS1_OAEP.new(clave_rsa)
    clave_aes = descifrar_rsa.decrypt(clave_aes_cifrada)
    
    # Confifurar el descifrado de AES
    descifrar_aes = AES.new(clave_aes, AES.MODE_EAX, nonce=nonce)
    datos = descifrar_aes.decrypt_and_verify(texto_cifrado, tag)
    
    # Guardar archivo descifrado
    with open(archivo_cifrado, "wb") as f:

        f.write(datos)

    print("Archivo descifrado.")

# Función principal con el menú
def menu():

    while True:

        print("""
        1. Generar claves RSA
        2. Cifrar archivo
        3. Descifrar archivo
        4. Salir
        """)

        try:

            opcion = int(input("Seleccione una opción: "))

        except ValueError:

            print("Ingrese un número válido.")
            continue

        if opcion == 1:

            generar_claves()

        elif opcion == 2:

            archivo = input("Ingrese el archivo a cifrar (ejemplo.txt): ").strip()
            clave = input("Ingrese la clave pública (clave_publica.pem): ").strip()

            try:

                cifrar(archivo, clave)

            except FileNotFoundError:
                
                print("Error: Archivo o clave pública no encontrados.")

            except Exception as e:
                
                print(f"Error inesperado: {e}")            
                
        elif opcion == 3:

            archivo = input("Ingrese el archivo a descifrar (ejemplo.txt): ").strip()
            clave = input("Ingrese la clave privada (clave_privada.pem): ").strip()

            try: 
                
                descifrar(archivo, clave) 
            
            except FileNotFoundError:
                
                print("Error: Archivo o clave privada no encontrados")

            except ValueError:

                print("Error: No se pudo verificar la autenticidad del archivo")            

            except Exception as e:
                
                print(f"Error inesperado: {e}")

        elif opcion == 4:

            sys.exit()

        else:

            print("Opción inválida, intente nuevamente.")

menu()