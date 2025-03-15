# Proyecto SpiderLock
Este programa implementa un sistema de cifrado híbrido utilizando AES (Advanced Encryption Standard) para cifrar archivos y RSA (Rivest-Shamir-Adleman) para cifrar la clave AES del mismo.


 ## Instalación
Antes de ejecutar el código, asegúrate de tener Python 3 instalado y los siguientes paquetes:

```bash
    pip install pycryptodome
```

## Uso
1. Ejecutar el programa
    Para iniciar el menú interactivo, simplemente ejecuta:
    ```bash
        python SpiderLock.py
    ```

2. Opciones del menú
    1. Generar claves RSA
        Selecciona la opción 1 para generar clave_privada.pem y clave_publica.pem.

    2. Cifrar un archivo
        Selecciona 2 e ingresa Nombre del archivo a cifrar y tu clave pública

    3. Descifrar un archivo
        Selecciona 3 e ingresa el nombre del archivo a descifrar y tu clave privada

    4. Salir
        Selecciona 4 para salir del programa


3. Al usar alguna de las opciones te

## Recomendaciones
Por razaones de seguridad NO compartas tu llave pública (clave_privada.pem)
