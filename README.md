# Proyecto SpiderLock

**SpiderLock** es una herramienta de cifrado híbrido que utiliza dos algoritmos de cifrado para proteger tus archivos de manera segura: **AES (Advanced Encryption Standard)** y **RSA (Rivest-Shamir-Adleman)**.

El programa utiliza AES para cifrar los archivos de manera rápida y eficiente. Luego, la clave utilizada para cifrar el archivo se cifra utilizando RSA, un algoritmo de cifrado asimétrico. Este enfoque híbrido proporciona la seguridad del cifrado asimétrico con la eficiencia del cifrado simétrico.

**SpiderLock** está diseñado para ofrecer una manera sencilla y accesible de cifrar y descifrar archivos mediante un menú interactivo en la línea de comandos.

## Requisitos

- Python 3.x
- `pycryptodome` (instalable con `pip install pycryptodome`)
- Sistema operativo: Linux, macOS o Windows (con soporte para Python)

Asegúrate de tener Python instalado correctamente antes de ejecutar el programa. Puedes verificarlo con el siguiente comando:

```bash
python --version
```

 ## Instalación de pycryptodome
Puedesar instalar pycryptodome con alguna se las siguientes instrucciones:

```bash
    pip install pycryptodome
```

o si lo prefieres:
```python
    pip install -r requirements.txt
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
