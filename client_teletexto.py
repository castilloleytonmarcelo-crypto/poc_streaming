#!/usr/bin/env python3
import socket
import struct
import time
import sys
import os
import unittest

# --- CONFIGURACIÓN DE ENTORNO ---
# El inyector es ligero y no requiere dependencias externas pesadas, 
# por lo que no necesita la lógica de autoinstalación de OpenCV/Numpy.
LOGLEVEL = os.getenv("LOGLEVEL", "DEBUG").upper()

class TestWatchdogProtocol(unittest.TestCase):
    """Pruebas unitarias para validación de inyección de datos."""
    def test_text_encoding(self):
        # Valida que el encoding UTF-8 no corrompa caracteres especiales
        msg = "Prueba de caracteres: áéíóú ñ"
        encoded = msg.encode('utf-8')
        self.assertEqual(encoded.decode('utf-8'), msg)

    def test_header_logic(self):
        # Valida que la cabecera de Canal 1 (Teletexto) sea correcta
        header = struct.pack("!BI", 1, 50)
        t, l = struct.unpack("!BI", header)
        self.assertEqual(t, 1)
        self.assertEqual(l, 50)

def main():
    # Configuración de red
    UDP_IP = "127.0.0.1"
    UDP_PORT = 5005
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    start_time = time.time()
    
    print(f"--- INYECTOR DE TELETEXTO WATCHDOG ---")
    print(f"Destino: {UDP_IP}:{UDP_PORT} | OS: {sys.platform}")

    try:
        count = 0
        while True:
            count += 1
            current_ts = time.time()
            
            # --- ESTRUCTURA DEL MENSAJE ---
            # Incluimos el TS para que el servidor pueda calcular la latencia de red pura
            # aunque no haya video.
            msg = f"HEARTBEAT | SEQ: {count} | STATUS: ALIVE | TS: {current_ts}"
            payload = msg.encode('utf-8')
            
            # Encabezado binario: Tipo 1 (1 byte) + Longitud (4 bytes)
            header = struct.pack("!BI", 1, len(payload))
            
            # Envío del paquete multiplexado
            sock.sendto(header + payload, (UDP_IP, UDP_PORT))
            
            if LOGLEVEL == "DEBUG":
                print(f"[DEBUG] Enviado ({len(payload)} bytes): {msg}")
            else:
                # En modo INFO solo mostramos una línea simple
                print(f"[*] Paquete {count} enviado correctamente.")

            # El inyector suele operar a frecuencias más bajas (e.g., cada 2 segundos)
            time.sleep(2)

    except KeyboardInterrupt:
        print("\nInyector detenido.")
    finally:
        sock.close()
        print(f"Sesión finalizada. Tiempo activo: {time.time() - start_time:.2f}s")

if __name__ == "__main__":
    # Soporte para ejecución de pruebas unitarias
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        unittest.main(argv=[sys.argv[0]], exit=False)
    else:
        main()