#!/usr/bin/env python
import cgi
import cgitb
import socket

cgitb.enable()
print("Content-Type: text/html;charset=utf-8\r\n\r\n")
print("<head><title>Trabalho Redes</title></head>")

#Instanciando o FieldStorage
form = cgi.FieldStorage()
vetorComandos =[]

#Pegando os valores dos campos para cada maquina
for i in range(1, 4):
    if form.getvalue('maq' + str(i) + '_ps'):
        comando = "ps"
        if form.getvalue('maq' + str(i) + '-ps'):
            parametro = form.getvalue('maq' + str(i) + '-ps')
            comando = comando + " " + parametro
        vetorComandos.append(comando)

    if form.getvalue('maq' + str(i) + '_df'):
        comando = "df"
        if form.getvalue('maq' + str(i) + '-df'):
            parametro = form.getvalue('maq' + str(i) + '-df')
            comando = comando + " " + parametro
        vetorComandos.append(comando)

    if form.getvalue('maq' + str(i) + '_finger'):
        comando = "finger"
        if form.getvalue('maq' + str(i) + '-finger'):
            parametro = form.getvalue('maq' + str(i) + '-finger')
            comando = comando + " " + parametro
        vetorComandos.append(comando)

    if form.getvalue('maq' + str(i) + '_uptime'):
        comando = "uptime"
        if form.getvalue('maq' + str(i) + '-uptime'):
            parametro = form.getvalue('maq' + str(i) + '-uptime')
            comando = comando + " " + parametro
        vetorComandos.append(comando)

for i in range(len(vetorComandos)):
    print(vetorComandos[i] + "<br><br>")
