Si se va a usar un equipo ESP32, recuerde aplicar el dessbloqueo del puetpo 5005 en su equipo server
si usa linux ocmo yo, podria ejecutar el comando:

sudo ufw allow 5005

* * *

Desde la Terminal (mpremote o ampy):
Si quieres ejecutar un archivo desde tu PC en el ESP32 sin guardarlo permanentemente como main.py, usas:
Bash


mpremote run uclient_setlibrary.py

mpremote run uclient_teletexto.py

