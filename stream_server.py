#!/usr/bin/env python3
import subprocess, sys, time, os, struct, unittest

# --- CONFIGURACIÓN DE ENTORNO ---
LOGLEVEL = os.getenv("LOGLEVEL", "INFO").upper()

def setup_environment():
    pkgs = ["numpy==1.26.4", "opencv-python==4.5.5.62"]
    changed = False
    for p in pkgs:
        name = p.split('=')[0]
        try:
            __import__(name if name != "opencv-python" else "cv2")
        except ImportError:
            print(f"[*] Instalando: {p}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--force-reinstall", p])
            changed = True
    if changed: os.execv(sys.executable, [sys.executable] + sys.argv)

setup_environment()
import cv2
import numpy as np
import socket

class TestWatchdogProtocol(unittest.TestCase):
    def test_header_integrity(self):
        header = struct.pack("!BI", 1, 100)
        t, l = struct.unpack("!BI", header)
        self.assertEqual(t, 1)
        self.assertEqual(l, 100)

def main():
    start_time = time.time()
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # --- VARIABLES DE ANÁLISIS ---
    last_v_time = 0
    jitter_list = []
    latency_list = []
    
    try:
        sock.bind(("0.0.0.0", 5005))
        print(f"--- SERVER WATCHDOG (TELEMETRÍA ACTIVA) ---")
    except Exception as e:
        print(f"Error Socket: {e}"); return

    try:
        while True:
            data, addr = sock.recvfrom(65535)
            curr_time = time.time()
            if len(data) < 5: continue
            
            tipo, longitud = struct.unpack("!BI", data[:5])
            payload = data[5:]

            if tipo == 0:  # VIDEO
                # 1. Análisis de Jitter
                if last_v_time > 0:
                    delta = curr_time - last_v_time
                    # Esperamos ~25 FPS (0.04s). El jitter es la varianza.
                    jitter = abs(delta - 0.04)
                    jitter_list.append(jitter)
                last_v_time = curr_time

                nparr = np.frombuffer(payload, np.uint8)
                frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                if frame is not None:
                    if LOGLEVEL == "DEBUG": 
                        cv2.putText(frame, f"Jitter: {jitter*1000:.2f}ms", (10, 30), 1, 1, (0,255,0), 1)
                    cv2.imshow("Watchdog Monitor", frame)
            
            elif tipo == 1:  # TELETEXTO (Análisis de Latencia)
                msg = payload.decode('utf-8', errors='ignore')
                
                # 2. Análisis de Latencia End-to-End
                # Esperamos formato del cliente: "WATCHDOG_UPTIME: Xs | TS: 123456.78"
                if "TS:" in msg:
                    try:
                        ts_str = msg.split("TS:")[1].strip()
                        sent_ts = float(ts_str)
                        latency = (curr_time - sent_ts) * 1000 # a ms
                        latency_list.append(latency)
                        if LOGLEVEL == "DEBUG": print(f"[LATENCY] {latency:.2f} ms")
                    except: pass
                
                print(f"[{time.strftime('%H:%M:%S')}] {addr[0]} >> {msg}")

            if cv2.waitKey(1) & 0xFF == ord('q'): break
    except KeyboardInterrupt:
        pass
    finally:
        sock.close()
        cv2.destroyAllWindows()
        
        # --- REPORTE DE ANÁLISIS FINAL ---
        total_time = time.time() - start_time
        print(f"\n" + "="*40)
        print(f"📊 RESUMEN TÉCNICO WATCHDOG")
        print(f"Duración: {total_time:.2f}s")
        if jitter_list:
            avg_jitter = (sum(jitter_list) / len(jitter_list)) * 1000
            print(f"Jitter Promedio: {avg_jitter:.2f} ms")
        if latency_list:
            avg_lat = sum(latency_list) / len(latency_list)
            print(f"Latencia E2E Promedio: {avg_lat:.2f} ms")
        print("="*40)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        unittest.main(argv=[sys.argv[0]], exit=False)
    else:
        main()