#!/usr/bin/env python

import struct
from socket import *
from backend import *

daemons = {
    "endereco_ip": ["127.0.0.1", "127.0.0.1", "127.0.0.1"],
}

'''
Um procedimento que ira executar todos os comandos recebidos pela maquinas.
Atraves dos pacotes montados, digitados por usuario (mensagens)
Recebe: Lista de comandos, e seus respectivos numeros.
Retorna: Respostas ao comando

Leitura: https://docs.python.org/2/howto/sockets.html
Leitura: https://docs.python.org/3/library/io.htm
Leitura: https://docs.python.org/3/library/struct.html
'''
def exeComandos(comandoList, numComando):

    #Recebera a lista das Tuplas de comandos
    respostas = []

    for cmd in comandoList:

        #Sera usado para enviar o pacote
        #Olhar https://docs.python.org/2/howto/sockets.html
        usuarioSocket.connect((daemons["endereco_ip"][numComando], daemons["porta"][numComando]))
        usuarioSocket = socket(AF_INET, SOCK_STREAM)

        #Origem e Destino, que possuem o mesmo endereco
        origem = inet_aton(gethostbyname(gethostname()))
        destino = inet_aton(daemons["ip"][numComando])

        #Enviando....
        pkg = criarpacote(cmd[0], cmd[1], numComando, origem, destino)
        pkg.seek(0)
        usuarioSocket.send(pkg.read())

        #Recebendo...
        #Leitura: https://docs.python.org/3/library/io.html
        pkg = io.BytesIO(usuarioSocket.recv(10240))

        pkg.seek(0, 2)
        outputLen = pkg.tell() - 20

        #Interpretacao dos dados
        pkg.seek(20)
        o = struct.unpack("s" * outputLen, pkg.read())
        respostas.append("".join(o))

        usuarioSocket.close()

    return respostas
