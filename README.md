# Watchdog Stream: Arquitectura de Multiplexación Híbrida

Este ecosistema de software implementa un protocolo de transporte ligero sobre **UDP** diseñado para la transmisión simultánea de flujos de video de alta carga y metadatos (teletexto) de baja latencia. El sistema está optimizado para entornos con hardware legado (como el procesador **Intel Xeon E5506**) y sistemas operativos **Ubuntu**.

## 🏗️ Arquitectura de Sistemas

El diseño se basa en un modelo **Productor-Consumidor** desacoplado, utilizando una cabecera binaria propietaria de 5 bytes que permite la demultiplexación de canales en el destino sin necesidad de contenedores pesados (como MP4 o MKV).

### Estructura del Paquete (Header Analysis)
Cada datagrama UDP enviado sigue el siguiente esquema de empaquetado binario:
`[1 byte: Canal/Tipo] [4 bytes: Longitud (Big-endian)] [N bytes: Payload]`

* **Canal 0 (Video):** Payload compuesto por bytes de imagen codificados en JPEG con bitrate variable.
* **Canal 1 (Teletexto):** Payload de texto codificado en UTF-8 para telemetría, estados de sensores o marcas de tiempo.

---

## 🛠️ Instalación

El proyecto cuenta con un mecanismo de **Auto-Instalación Silenciosa**. Al ejecutar cualquiera de los scripts, el sistema verificará la integridad de las librerías y forzará las versiones compatibles con la arquitectura de hardware (evitando errores de ABI en Numpy 2.0 y fallos de instrucciones AVX en el Xeon).

Para realizar una instalación manual de las dependencias base:

```bash
pip install -r requirements.txt
pip install --force-reinstall -r requirements.txt

# Watchdog Stream PoC

Arquitectura de streaming híbrido (Video + Teletexto) sobre UDP multiplexado. Diseñado para hardware Intel Xeon y entornos de alta eficiencia.

## 📥 Git Operaciones

**Clonar el repositorio:**
```bash
git clone [https://github.com/castilloleytonmarcelo-crypto/poc_streaming.git](https://github.com/castilloleytonmarcelo-crypto/poc_streaming.git)
cd poc_streaming

### Actualizar cambios localmente (Pull)

Sincronice su entorno local con las últimas mejoras del repositorio central:

Bash

    git pull origin main

### Subir cambios al repositorio (Push)

Asegure sus avances y actualizaciones en la nube siguiendo este flujo:

Bash

    git add .
    git commit -m "Descripción clara de la mejora (e.g., Optimización de buffer para Ubuntu 26.04)"
    git push origin main

* * *

🛠️ Instalación y Dependencias
------------------------------

Este ecosistema es **Self-Healing (Auto-reparable)**. Los scripts detectan y gestionan su propio entorno de ejecución para evitar errores de compatibilidad comunes.

Al iniciar cualquier componente, el sistema realiza automáticamente:

1.  **Verificación de Librerías:** Comprueba la presencia de `numpy` y `opencv-python`.
    
2.  **Corrección de ABI (Application Binary Interface):** Si detecta **Numpy 2.x**, fuerza un downgrade a la versión `1.26.4` para evitar fallos de importación en OpenCV.
    
3.  **Compatibilidad de Hardware:** Asegura la instalación de `opencv-python==4.5.5.62`, versión validada para procesadores Intel Xeon sin soporte de instrucciones AVX modernas.
    
4.  **Auto-Reinicio:** Si se requiere una instalación, el proceso se reinicia solo para cargar el nuevo entorno.
    

* * *

💻 Ejecución de Componentes
---------------------------

### 1\. Iniciar el Servidor (Consumidor)

Debe estar activo para recibir, separar y visualizar los flujos entrantes de múltiples clientes.

Bash

    python3 server.py

### 2\. Iniciar el Cliente Unificado (Productor Video + Datos)

Envía flujo de cámara y telemetría simultáneamente. Si no detecta una cámara física, activa un **generador de carga sintética** para pruebas de estrés.

Bash

    python3 client_unificado.py

### 3\. Iniciar el Cliente de Teletexto (Inyector de Datos)

Utilizado para inyectar comandos, logs de sistema o datos de sensores al stream sin carga de video.

Bash

    python3 client_teletexto.py

* * *

📊 Configuración de Diagnóstico
-------------------------------

### Para afinar el nivel de LOG

Utilice la variable de entorno `LOGLEVEL` para monitorear el tráfico de red y la integridad de los paquetes en tiempo real:

*   **En Linux / Ubuntu:** `LOGLEVEL=DEBUG python3 server.py`
    
*   **En Windows:** `set LOGLEVEL=DEBUG && python3 server.py`
    

### Pruebas Unitarias e Integración

Cada script integra la clase `TestWatchdogProtocol` para asegurar que el empaquetado binario sea consistente. Puede validar el sistema ejecutando:

Bash

    # Validación rápida mediante argumento interno
    python3 server.py test
    python3 client_unificado.py test
    
    # Reporte formal detallado vía unittest
    python3 -W ignore:ResourceWarning -m unittest -v server.py

* * *

⚙️ Funciones Principales
------------------------

*   **Multiplexación Binaria Nativa:** Implementación de cabecera de 5 bytes `[Tipo:1b][Longitud:4b]` que permite la coexistencia de video y texto en un único socket UDP.
    
*   **Resiliencia de Hardware:** Lógica de codificación adaptada para evitar errores de "Illegal Instruction" en arquitecturas de servidor legadas.
    
*   **Detección de Plataforma:** Adaptación automática de parámetros de socket y rutas según el sistema operativo (Windows/Linux).
    
*   **Análisis de Streaming:** Herramientas de telemetría integradas para reportar duración de sesión, FPS y estabilidad del flujo al finalizar la ejecución.
    

* * *

**Arquitecto Responsable:** Marcelo Castillo

**Proyecto:** Watchdog Streaming Monitoring System

**Repositorio Oficial:** [poc\_streaming](https://github.com/castilloleytonmarcelo-crypto/poc_streaming.git)
 (Arquitectura de streaming híbrido diseñada para la transmisión multiplexada de **Video (Canal 0)** y **Teletexto/Telemetría (Canal 1)** sobre el protocolo UDP.)

