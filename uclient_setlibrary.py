#!/usr/bin/env micropython
import network
import time
import mip
import gc

# --- CONFIGURACIÓN ---
SSID = "TU-APP-SSID"
PASSWORD = "TU-PASSWORD"

def instalar_librerias():
    # 1. Configurar Wi-Fi
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    if not wlan.isconnected():
        print("Conectando a la red:", SSID)
        wlan.connect(SSID, PASSWORD)
        
        # Esperar hasta 10 segundos a que conecte
        timeout = 10
        while not wlan.isconnected() and timeout > 0:
            print("Esperando conexión... ({}s)".format(timeout))
            time.sleep(1)
            timeout -= 1

    if wlan.isconnected():
        print("\n¡Conectado con éxito!")
        print("Configuración de red:", wlan.ifconfig())
        
        # 2. Instalar unittest usando mip
        print("\nIniciando descarga de 'unittest' desde micropython-lib...")
        try:
            # Forzamos limpieza de RAM antes de la descarga
            gc.collect() 
            
            # Instalación
            mip.install("unittest")
            
            print("\n-------------------------------------------")
            print("INSTALACIÓN COMPLETADA")
            print("Ya puedes usar 'import unittest' en tus scripts.")
            print("-------------------------------------------")
            
        except Exception as e:
            print("\nError durante la instalación:", e)
            print("Asegúrate de que el ESP32 tenga acceso a internet real.")
    else:
        print("\nError: No se pudo establecer conexión Wi-Fi. Verifica tus credenciales.")

# Ejecutar el proceso
if __name__ == "__main__":
    instalar_librerias()