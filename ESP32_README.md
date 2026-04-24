🚀 Guía de Uso: Cliente Teletexto (ESP32)
-----------------------------------------


Este repositorio contiene las herramientas necesarias para la configuración y ejecución del inyector de datos de Teletexto en dispositivos ESP32.


### ⚙️ Configuración de Variables

Antes de transferir los archivos a tu dispositivo, es **indispensable** editar los archivos `.py` y actualizar las credenciales de red y la dirección del servidor:

Python

    # Ubica estas líneas en el código y ajusta los valores:
    WIFI_SSID = "TU-APP-SSID"      # <--- Nombre de tu red Wi-Fi
    WIFI_PASS = "TU-PASSWORD"      # <--- Contraseña de tu red
    SERVER_IP = "1.1.1.1"          # <--- IP de tu PC o Servidor de streaming

### 🛠️ Configuración de Red y Seguridad

Si utilizas un servidor externo para procesar los datos, asegúrate de habilitar el tráfico a través del puerto **5005**. En sistemas **Linux**, puedes abrirlo ejecutando:

Bash

    sudo ufw allow 5005

* * *

### 💻 Ejecución desde la Terminal

Para probar los scripts sin necesidad de guardarlos permanentemente como `main.py` en la memoria del ESP32, puedes utilizar herramientas como `mpremote` o `ampy`.

**Comandos de ejecución rápida:**

*   **Instalación de dependencias:**
    
    Bash
    
        mremote run uclient_setlibrary.py
    
*   **Ejecución del cliente:**
    
    Bash
    
        mpremote run uclient_teletexto.py
    

* * *

### 📄 Descripción de los Archivos

Archivo

Función

`uclient_setlibrary.py`

Configura el entorno descargando e instalando la librería `unittest` desde **micropython-lib**.

`uclient_teletexto.py`

Script principal del **Cliente de Teletexto**. Actúa como el inyector de datos hacia el servidor.

Exportar a Hojas de cálculo

* * *

### 📌 Notas adicionales

*   Asegúrate de tener el ESP32 conectado y correctamente reconocido por tu sistema antes de ejecutar los comandos de `mpremote`.
    
*   Para una ejecución autónoma, recuerda renombrar el script principal a `main.py` y subirlo al dispositivo.