#!/usr/bin/env python

import socket

#Dados da conexao, ip, porta
IP = '127.0.0.1'
PORTA = 9001
BUFFER_TAM = 1024 

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((IP, PORTA))
s.listen(1)

conn, addr = s.accept()
print( 'Connection address:', addr)
while 1:
    data = conn.recv(BUFFER_TAM)
    if not data: break
    print( "received data:", data)
    conn.send(data)  # echo
conn.close()
