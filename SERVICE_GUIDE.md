# Watchdog Service Control 🚀

Este documento describe el funcionamiento y la gestión del script de control para el **Stream Server**, permitiendo su ejecución como un servicio de sistema en segundo plano dentro del entorno de la PoC.

## 📂 Ubicación y Estructura
El servicio está diseñado para operar estrictamente en la siguiente ruta:
`Path: /home/marcelo/poc_streaming/`

**Componentes involucrados:**
- `server.py`: El núcleo del servidor de streaming.
- `watchdog_service.sh`: Script de gestión (Start/Stop/Status).
- `server.pid`: Archivo temporal que almacena el ID del proceso activo.
- `server_service.log`: Registro histórico de eventos y errores.

---

## 🛠️ Comandos de Gestión

El script `watchdog_service.sh` actúa como un wrapper para facilitar la administración del servidor sin necesidad de gestionar manualmente los PIDs de Python.

### 1. Iniciar el Servicio
Lanza el servidor en segundo plano utilizando `nohup` para que persista tras cerrar la sesión SSH.
```bash
./watchdog_service.sh start