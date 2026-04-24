#!/usr/bin/env micropython
import usocket as socket
import ustruct as struct
import utime as time
import network
import sys
import gc
import unittest

# --- CONFIGURACIÓN ---
WIFI_SSID = "TU-APP-SSID"          # <--- Cambia esto
WIFI_PASS = "TU-PASSWORD"      # <--- Cambia esto
SERVER_IP = "1.1.1.1"    # <--- IP de tu PC/Servidor streaming
SERVER_PORT = 5005
LOG_DEBUG = True

# --- UTILIDADES DE RED ---
def conectar_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Conectando a WiFi {}...".format(WIFI_SSID))
        wlan.connect(WIFI_SSID, WIFI_PASS)
        
        # Timeout de 10 segundos para la conexión
        intentos = 0
        while not wlan.isconnected() and intentos < 20:
            time.sleep_ms(500)
            intentos += 1
            
    if wlan.isconnected():
        print("Conectado! IP:", wlan.ifconfig()[0])
        return True
    else:
        print("Error: No se pudo conectar al WiFi.")
        return False

# --- PRUEBAS UNITARIAS ---
class TestWatchdogProtocol(unittest.TestCase):
    def test_text_encoding(self):
        msg = "Prueba: ñ á"
        encoded = msg.encode('utf-8')
        self.assertEqual(encoded.decode('utf-8'), msg)

    def test_header_logic(self):
        # Empaqueta: 1 (byte), 50 (unsigned int 4 bytes)
        header = struct.pack("!BI", 1, 50)
        t, l = struct.unpack("!BI", header)
        self.assertEqual(t, 1)
        self.assertEqual(l, 50)

# --- LÓGICA PRINCIPAL DEL INYECTOR ---
def ejecutar_inyector():
    # Limpieza de memoria inicial
    gc.collect()
    
    # Crear socket UDP (SOCK_DGRAM)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    dest_addr = (SERVER_IP, SERVER_PORT)
    
    inicio = time.time()
    count = 0
    
    print("\n--- INYECTOR WATCHDOG ACTIVO ---")
    print("Enviando a {}:{}".format(SERVER_IP, SERVER_PORT))

    try:
        while True:
            count += 1
            ts = time.time()
            
            # Construir mensaje
            msg = "HEARTBEAT | SEQ: {} | TS: {}".format(count, ts)
            payload = msg.encode('utf-8')
            
            # Cabecera binaria (! = Big Endian, B = 1 byte Tipo, I = 4 bytes Longitud)
            header = struct.pack("!BI", 1, len(payload))
            
            # Envío (Cabecera + Datos)
            sock.sendto(header + payload, dest_addr)
            
            if LOG_DEBUG:
                print("[{}] Enviado: {}".format(count, msg))
            
            # Esperar 2 segundos
            time.sleep(2)
            
            # Liberar RAM periódicamente
            if count % 10 == 0:
                gc.collect()

    except KeyboardInterrupt:
        print("\nDetenido por el usuario.")
    except Exception as e:
        print("\nError inesperado:", e)
    finally:
        sock.close()
        final = time.time() - inicio
        print("Sesión cerrada. Tiempo total: {}s".format(final))

# --- PUNTO DE ENTRADA ---
if __name__ == "__main__":
    # 1. Ejecutar Pruebas
    print("Iniciando validación de protocolos...")
    try:
        # En MicroPython unittest.main() corre todos los TestCases definidos
        unittest.main()
    except Exception as e:
        print("Error ejecutando tests:", e)
    
    print("-" * 30)

    # 2. Iniciar Red e Inyector
    if conectar_wifi():
        ejecutar_inyector()
    else:
        print("No se puede iniciar el inyector sin conexión.")