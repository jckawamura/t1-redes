## Crição do daemon, utilizados pelas 3 máquinas
## sudo python deamon.py --port 9001
## sudo python deamon.py --port 9002
## sudo python deamon.py --port 9003

import os
import cgi
import cgitb
import socket

def main():

    ##Saída recebida do usuário:

    msg = ' '
    msg_host = ' '
    porta = 9000

    #Recebendo o Host e a Porta
    tupla = ((msg_host, porta))

    ## Estabelecendo conexao, aceitando. A ideia de ouvir as tres maquinas
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.bind(tupla)
    cliente.listen(3)

    while not 0:
        con, enderecoCliente = cliente.accept()

        ## Tamanho de 32 suficiente neste caso
        msg = con.recv(32)

        if mensagem:
            comando = decodifica(mensagem)

            mensagem = mensagem.split()
            msgRecebida = os.popen(comando).read()
            msgSaida = "RESPONSE " + mensagem[1] + " " + saidaTerminal

        else:
            break

##Decoficando Mensagem
##Recebe o comando a ser decodificado
##Retorna comando decodificado

def decodifica(comando):
    comandoList = comando.split()
    if comandoList[0] != "REQUEST":
        return "fechar"
    if comandoList[1] == "1":
        enviaComando = "ps"
    if comandoList[1] == "2":
        enviaComando = "df"
    if comandoList[1] == "3":
        enviaComando = "finger"
    if comandoList[1] == "4":
        enviaComando = "uptime"
    return enviaComando