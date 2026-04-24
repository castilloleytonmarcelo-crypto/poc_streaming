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
    

RFCs fundamentales que dan validez técnica a esta implementación:

* * *

### 1\. El Pilar del Transporte: RFC 768 (UDP)

Tu sistema utiliza **UDP (User Datagram Protocol)** para priorizar la velocidad sobre la fiabilidad.

*   **Por qué aplica:** Es el estándar base para cualquier transmisión donde el _jitter_ y la latencia son más críticos que la recuperación de paquetes perdidos (perfecto para tu streaming en el Xeon).
    
*   **Relevancia:** Valida tu elección de no usar TCP para evitar el "head-of-line blocking".
    

### 2\. Tiempo Real y Sincronización: RFC 3550 (RTP)

Aunque tu protocolo es personalizado (el header de 5 bytes), conceptualmente sigue los principios del **RTP (Real-time Transport Protocol)**.

*   **Análisis de Latencia:** El RFC 3550 define cómo usar _timestamps_ y números de secuencia para reconstruir el tiempo de los medios y calcular el **Jitter**, tal como implementamos en tu `server.py`.
    
*   **Teletexto:** Este RFC contempla la carga útil (_payload_) de datos no visuales sincronizados con el video.
    

### 3\. Multiplexación de Datos: RFC 4571

Este RFC describe cómo enmarcar múltiples flujos (como tu video y tu teletexto) para que viajen sobre un protocolo de transporte orientado a datagramas.

*   **Tu implementación:** Tu cabecera binaria `struct.pack("!BI", tipo, longitud)` es una forma simplificada de lo que este RFC estandariza para separar canales de datos dentro de un mismo flujo.
    

### 4\. Payload de Video (JPEG): RFC 2435

Como tu `client_unificado.py` utiliza `cv2.imencode('.jpg', ...)`, técnicamente te riges por el estándar de **RTP Payload Format for JPEG-compressed Video**.

*   **Detalle técnico:** Define cómo se deben fragmentar y empaquetar los cuadros JPEG para que el receptor pueda reconstruirlos eficientemente.
    

* * *

### Resumen de Respaldo Técnico para tu PoC

Concepto

RFC

Función en tu Proyecto

**Transporte**

**RFC 768**

Uso de Sockets UDP para baja latencia.

**Telemetría**

**RFC 3550**

Lógica de Timestamps para medir Latencia E2E y Jitter.

**Carga Útil**

**RFC 2435**

Transmisión de frames comprimidos en formato JPEG.

**Encapsulación**

**RFC 4571**

Segmentación de canales (Video vs. Teletexto).

* * *
Esta sección explica no solo qué librerías usas, sino el **rol crítico** que cumple cada una dentro de la arquitectura de streaming y por qué seleccionamos versiones específicas para tu hardware Xeon.

* * *

📚 Referencia de Librerías y Dependencias
-----------------------------------------

El proyecto **Watchdog Stream PoC** utiliza un conjunto de librerías seleccionadas por su estabilidad, bajo consumo de recursos y compatibilidad con arquitecturas de servidor legadas.

### 1\. Librerías Externas (Instalables vía Pip)

Librería

Versión

Propósito en el Proyecto

**OpenCV (`opencv-python`)**

`4.5.5.62`

Gestión de captura de video, codificación/decodificación JPEG y renderizado de la interfaz gráfica del monitor.

**NumPy (`numpy`)**

`1.26.4`

Manejo de estructuras de datos matriciales (frames) y manipulación de buffers binarios de alta velocidad.

Exportar a Hojas de cálculo

> **Nota del Arquitecto:** Se utiliza **NumPy 1.26.4** para evitar incompatibilidades de la ABI con la versión 2.0+, asegurando que el procesamiento de imágenes en Ubuntu 26.04 sea fluido sobre el hardware Intel Xeon.

### 2\. Librerías Nativas de Python (Standard Library)

Estas librerías no requieren instalación adicional y son fundamentales para el funcionamiento del protocolo:

*   **`socket`**: Implementa la interfaz de red de bajo nivel. Es el motor que gestiona los datagramas UDP para el transporte de video y teletexto.
    
*   **`struct`**: Crucial para la **Multiplexación Binaria**. Permite empaquetar y desempaquetar la cabecera de 5 bytes `[Tipo][Longitud]` en formato C compatible (`!BI`).
    
*   **`unittest`**: Framework integrado para la validación de la integridad del protocolo mediante las pruebas unitarias incluidas en cada script.
    
*   **`subprocess`**: Utilizada por el sistema de **Autoinstalación** para gestionar el entorno de dependencias sin intervención del usuario.
    
*   **`time`**: Responsable de la generación de _timestamps_ para el cálculo de **Latencia End-to-End** y **Jitter**.
    
*   **`os` & `sys`**: Gestión de rutas de archivos, variables de entorno (`LOGLEVEL`) y control de señales del sistema operativo.

* * *

### 📡 Relación de Librerías en el Flujo de Datos

1.  **Captura:** `opencv` toma el frame de la cámara.
    
2.  **Procesamiento:** `numpy` convierte el frame en un buffer comprimido.
    
3.  **Empaquetado:** `struct` añade la cabecera técnica de Watchdog.
    
4.  **Transporte:** `socket` envía el paquete vía UDP.
    
5.  **Análisis:** `time` y `unittest` validan que la entrega sea estable y correcta.
    

Esta estructura garantiza que tu PoC sea modular y fácil de portar a otros servidores dentro de tu red local o entornos de producción.

* * *

**Arquitecto Responsable:** Marcelo Castillo

**Proyecto:** Watchdog Streaming Monitoring System

**Repositorio Oficial:** [poc\_streaming](https://github.com/castilloleytonmarcelo-crypto/poc_streaming.git)
 (Arquitectura de streaming híbrido diseñada para la transmisión multiplexada de **Video (Canal 0)** y **Teletexto/Telemetría (Canal 1)** sobre el protocolo UDP.)

