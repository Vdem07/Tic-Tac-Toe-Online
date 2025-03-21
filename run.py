import os
import subprocess
import time

# Изменение текущей рабочей директории на папку скрипта
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Запуск сервера
server_process = subprocess.Popen(["python", "server.py"])

# Ждем некоторое время, чтобы сервер успел запуститься
time.sleep(2)

# Запуск клиента
subprocess.Popen(["python", "client.py"])
