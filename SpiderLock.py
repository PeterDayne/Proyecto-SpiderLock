# Autor: Pedro Chavez Ruiz
# Fecha: 14/03/2025 (Primera versiona)

# Bibliotecas
import os # Para manipulación de directorios y archivos.
import sys # Interacción con el sistema, en este caso, para salir del programa.
from Crypto.Cipher import AES, PKCS1_OAEP # Proporciona la funcionalidad para cifrar/descifrar con el algoritmo AES.
from Crypto.PublicKey import RSA # Proporciona la funcionalidad para generar y manejar claves RSA.
from base64 import b64encode, b64decode # Para codificar/decodificar datos en base64

# Genera y guarda una clave privada y una clave pública en archivos .pem
def generar_claves():

    # Genera las claves RSA de 2048 bits
    clave = RSA.generate(2048)

    # Verifica si las claves ya existen en el sistema, si no, las genera
    if not os.path.exists("clave_privada.pem") and not os.path.exists("clave_publica.pem"):

        with open("clave_privada.pem", "wb") as archivo_privado:

            archivo_privado.write(clave.export_key())  # Exporta la clave privada

        with open("clave_publica.pem", "wb") as archivo_publico:

            archivo_publico.write(clave.publickey().export_key()) # Exporta la clave pública

        print("Claves RSA generadas.")

    else:
    
        print("Las claves ya existen, no se generaron nuevas.")

# Se cifra el archivo con AES y luego se cifra la clave AES con RSA
def cifrar(archivo, clave_publica):

    # Leer los datos del archivo
    with open(archivo, "rb") as f:
        datos = f.read()
    
    # Generar clave AES de 16 bytes de manera aleatoria
    clave_aes = os.urandom(16)
    
    # Cifrar los datos del archivo con la clave AES
    cifrar_aes = AES.new(clave_aes, AES.MODE_EAX)
    text_cifrado, verificador = cifrar_aes.encrypt_and_digest(datos)
    
    # Cifrar clave AES (del archivo) con RSA (ya generadas)
    with open(clave_publica, "rb") as f:

        clave_rsa = RSA.import_key(f.read())

    cifrar_rsa = PKCS1_OAEP.new(clave_rsa)  # Se usa PKCS1_OAEP para el cifrado RSA
    clave_aes_cifrada = cifrar_rsa.encrypt(clave_aes) # Se cifra la clave AES
    
    # Guardamos el archivo cifrado (clave AES cifrada + nonce + tag + datos cifrados)
    with open(archivo, "wb") as f:

        f.write(clave_aes_cifrada + cifrar_aes.nonce + verificador + text_cifrado)

    print("Archivo cifrado.")

# Se descifra el archivo con RSA y luego se descifra la clave AES con AES
def descifrar(archivo_cifrado, clave_privada):

    # Leer los datos del archivo cifrado
    with open(archivo_cifrado, "rb") as f:

        contenido = f.read() # Leemos el archivo cifrado
    
    # Se extraen las partes del archivo cifrado (clave AES cifrada, nonce, tag, y texto cifrado)
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
    
    # Configurar el descifrado de AES
    descifrar_aes = AES.new(clave_aes, AES.MODE_EAX, nonce=nonce)
    datos = descifrar_aes.decrypt_and_verify(texto_cifrado, tag) # Descifrar y verificar los datos
    
    # Guardar archivo descifrado
    with open(archivo_cifrado, "wb") as f:

        f.write(datos)

    print("Archivo descifrado.")

# Mostrar el contenido del directorio actual
def mostrar_contenido_directorio():

    directorio = os.getcwd()

    archivos = os.listdir(directorio)  

    print(f"Contenido del directorio '{directorio}':")

    for archivo in archivos:

        print(archivo)

# Mostrar nombre del proyecto en ASCII
def mostrar_ascii_art():
    ascii_art = '''
 ____        _     _             _               _    
/ ___| _ __ (_) __| | ___ _ __  | |    ___   ___| | __
\___ \| '_ \| |/ _` |/ _ \ '__| | |   / _ \ / __| |/ /
 ___) | |_) | | (_| |  __/ |    | |__| (_) | (__|   < 
|____/| .__/|_|\__,_|\___|_|    |_____\___/ \___|_|\_\_
      |_|                                             

    '''
    print(ascii_art)

# Función principal con el menú
def menu():

    while True:

        mostrar_ascii_art()

        print("""
        1. Generar claves RSA
        2. Cifrar archivo
        3. Descifrar archivo     
        4. Mostrar contenido del directorio
        5. Salir
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

            mostrar_contenido_directorio()

        elif opcion == 5:

            sys.exit()

        else:

            print("Opción inválida, intente nuevamente.")

menu()