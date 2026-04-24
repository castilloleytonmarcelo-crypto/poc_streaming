#!/bin/bash

# --- CONFIGURACIÓN ---
APP_NAME="Watchdog Stream Server"
DIR="~/poc_streaming"
SCRIPT="stream_server.py"
PYTHON_BIN="/usr/bin/python3"
PID_FILE="$DIR/stream_server.pid"
LOG_FILE="$DIR/stream_server_service.log"

# Exportamos el LOGLEVEL para que el script Python lo detecte
export LOGLEVEL="INFO"

start() {
    if [ -f $PID_FILE ] && kill -0 $(cat $PID_FILE) 2>/dev/null; then
        echo "[!] $APP_NAME ya está ejecutándose (PID: $(cat $PID_FILE))."
    else
        echo "[*] Iniciando $APP_NAME..."
        cd $DIR
        # Ejecutamos en segundo plano y guardamos el PID
        nohup $PYTHON_BIN $SCRIPT >> $LOG_FILE 2>&1 &
        echo $! > $PID_FILE
        echo "[+] $APP_NAME iniciado con éxito."
    fi
}

stop() {
    if [ ! -f $PID_FILE ]; then
        echo "[!] No se encontró el archivo PID. ¿Está el servidor activo?"
    else
        PID=$(cat $PID_FILE)
        echo "[*] Deteniendo $APP_NAME (PID: $PID)..."
        kill $PID
        rm -f $PID_FILE
        echo "[+] Servidor detenido."
    fi
}

status() {
    if [ -f $PID_FILE ] && kill -0 $(cat $PID_FILE) 2>/dev/null; then
        echo "[ONLINE] $APP_NAME está funcionando (PID: $(cat $PID_FILE))."
        echo "[STATS] Últimas líneas del log:"
        tail -n 5 $LOG_FILE
    else
        echo "[OFFLINE] $APP_NAME no está activo."
    fi
}

case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        stop
        sleep 2
        start
        ;;
    status)
        status
        ;;
    *)
        echo "Uso: $0 {start|stop|restart|status}"
        exit 1
esac

exit 0