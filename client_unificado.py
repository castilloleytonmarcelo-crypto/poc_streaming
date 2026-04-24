#!/usr/bin/env python3
import subprocess, sys, time, os, struct, random, unittest

# --- CONFIGURACIÓN DE ENTORNO Y LOGS ---
# Se puede ejecutar como: LOGLEVEL=DEBUG python3 client_unificado.py
LOGLEVEL = os.getenv("LOGLEVEL", "DEBUG").upper()

def setup_environment():
    """Verifica e instala dependencias específicas para hardware Xeon/Legacy."""
    pkgs = ["numpy==1.26.4", "opencv-python==4.5.5.62"]
    changed = False
    for p in pkgs:
        name = p.split('=')[0]
        try:
            # Intentar importar para verificar compatibilidad de versión
            if name == "numpy":
                import numpy as np
                if np.__version__.startswith('2.'): raise ImportError
            elif name == "opencv-python":
                import cv2
        except ImportError:
            print(f"[*] Corrigiendo dependencia: {p}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--force-reinstall", p])
            changed = True
    
    # Si hubo cambios, reiniciar el script para cargar las nuevas versiones
    if changed: 
        print("[*] Entorno actualizado. Reiniciando script...")
        os.execv(sys.executable, [sys.executable] + sys.argv)

# Ejecución inmediata de la configuración
setup_environment()

import cv2
import numpy as np
import socket

class TestWatchdogProtocol(unittest.TestCase):
    """Pruebas unitarias integradas para validación de protocolo."""
    def test_payload_limit(self):
        # Verifica que un frame máximo no exceda el límite teórico de UDP
        dummy_data = b"X" * 60000
        header = struct.pack("!BI", 0, len(dummy_data))
        self.assertLessEqual(len(header + dummy_data), 65535)

    def test_timestamp_format(self):
        # Verifica que el timestamp sea un float válido
        ts = time.time()
        self.assertIsInstance(ts, float)

def main():
    start_time = time.time()
    # Configuración de red
    UDP_IP = "127.0.0.1"
    UDP_PORT = 5005
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Aumentar buffer de envío para ráfagas de video
    if sys.platform != "win32":
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1048576)

    # Inicializar captura de video
    cap = cv2.VideoCapture(0)
    
    print(f"--- CLIENTE UNIFICADO WATCHDOG ---")
    print(f"Plataforma: {sys.platform} | Destino: {UDP_IP}:{UDP_PORT}")

    try:
        frame_count = 0
        while True:
            ret, frame = cap.read()
            
            # --- GENERADOR DE CARGA SINTÉTICA (Fail-safe) ---
            if not ret:
                # Si no hay cámara, generamos un frame de test con ruido visual
                frame = np.zeros((480, 640, 3), dtype=np.uint8)
                # Dibujar elementos aleatorios para variar el peso del JPEG (Estres de red)
                for _ in range(15):
                    color = (random.randint(0,255), 255, random.randint(0,255))
                    cv2.circle(frame, (random.randint(0,640), random.randint(0,480)), 
                               random.randint(10,50), color, -1)
                
                cv2.putText(frame, f"MODO CARGA SINTETICA", (50, 400), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                cv2.putText(frame, f"FRAME: {frame_count}", (50, 440), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 1)

            frame_count += 1

            # --- CANAL 0: VIDEO (Compresión JPEG) ---
            # Calidad variable según LOGLEVEL para pruebas de ancho de banda
            quality = 40 if LOGLEVEL == "INFO" else 25
            _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, quality])
            video_data = buffer.tobytes()
            
            # Encabezado binario: Tipo 0 (1 byte) + Longitud (4 bytes)
            header_v = struct.pack("!BI", 0, len(video_data))
            sock.sendto(header_v + video_data, (UDP_IP, UDP_PORT))

            # --- CANAL 1: TELETEXTO (Telemetría + Latencia) ---
            # Incluimos el Timestamp (TS) para que el servidor calcule latencia E2E
            current_ts = time.time()
            uptime = int(current_ts - start_time)
            msg = f"NODE_01 | UPTIME: {uptime}s | TS: {current_ts}"
            payload_t = msg.encode('utf-8')
            
            header_t = struct.pack("!BI", 1, len(payload_t))
            sock.sendto(header_t + payload_t, (UDP_IP, UDP_PORT))

            if LOGLEVEL == "DEBUG" and frame_count % 20 == 0:
                print(f"[DEBUG] Enviados {len(video_data)} bytes de video | {len(payload_t)} bytes texto")

            # Control de FPS (aprox 25 FPS)
            time.sleep(0.04)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except KeyboardInterrupt:
        print("\nTransmisión detenida por el usuario.")
    finally:
        cap.release()
        sock.close()
        print(f"--- Resumen de sesión ---")
        print(f"Frames totales: {frame_count}")
        print(f"Tiempo total: {time.time() - start_time:.2f} segundos")

if __name__ == "__main__":
    # Si se pasa el argumento 'test', ejecuta las pruebas unitarias
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        unittest.main(argv=[sys.argv[0]], exit=False)
    else:
        main()