#!/usr/bin/env python
import cgitb
import struct
import io
import socket

cgitb.enable()
print("Content-Type: text/html;charset=utf-8\r\n\r\n")

VERSION = 2
IHL = 5

daemons = {
    "porta": [9001, 9002, 9003],
    "seq": [0, 0, 0]
}

def checksumIPV4(totalLen, identification, flag, ttl, protocol, src, dst):
    checksum = (VERSION << 12) | (IHL << 8)
    checksum += totalLen
    checksum += identification
    checksum += flag << 13
    checksum += (ttl << 8) | protocol
    #fonte da conversao de ip string para inteiro:
    #https://stackoverflow.com/questions/5619685/conversion-from-ip-string-to-integer-and-backward-in-python
    src = struct.unpack("!I", socket.inet_aton(src))[0]
    checksum += src
    dst = struct.unpack("!I", socket.inet_aton(dst))[0]
    checksum += dst
    checksum = (checksum >> 16) + (checksum & 0xFFFF)
    checksum = (checksum >> 16) + (checksum & 0xFFFF)
    checksum = (~checksum & 0xFFFF)

    return checksum

def verifyChecksumIPV4(totalLen, identification, flag, ttl, protocol, src, dst, headerChecksum):
    checksum = (VERSION << 12) | (IHL << 8)
    checksum += totalLen
    checksum += identification
    checksum += flag << 13
    checksum += (ttl << 8) | protocol
    checksum += headerChecksum #agora inclui o headerChecksum na soma
    src = struct.unpack("!I", socket.inet_aton(src))[0]
    checksum += src
    dst = struct.unpack("!I", socket.inet_aton(dst))[0]
    checksum += dst
    checksum = (checksum >> 16) + (checksum & 0xFFFF)
    checksum = (checksum >> 16) + (checksum & 0xFFFF)
    checksum = (~checksum & 0xFFFF)

    return checksum == 0x0000

def criarpacote(src, dst, maq, protocol, options, flag, ttl):
    pacote = io.BytesIO()

    '''
    1. "Version": versao do protocolo = 2
    2. "IHL": tamanho do cabecalho = tamanho total do cabecalho. Em geral, sera um valor fixo em bytes.
    3. "Type of Service" = deixar em zero.
    4. "Total Length" = tamanho total do pacote, incluindo os parametros.
    '''
    totalLen = IHL * 4 + options
    if options % 4 != 0:
        totalLen = 4 - (options % 4)
    word = (VERSION << 28 | IHL << 24 | totalLen)
    pacote.write(struct.pack("!I", word))

    '''
    5. "Identification" = colocar um numero de sequencia, a ser checado com a resposta.
    6. "Flags" = sao 3 bits = marcar como 000 se requisicao e 111 se resposta.
    7. "Fragment Offset" = deixar em zero.
    '''
    identification = daemons["seq"][maq]
    if flag == 7:
        ttl = ttl - 1
    word = ((identification << 16) | (flag << 13))
    pacote.write(struct.pack("!I", word))
    daemons["seq"][maq] += 1

    '''
    8. "Time to Live" = iniciar com X e na resposta, o numero tera que ser X-1. X pode ser inicializado com
        qualquer numero.
    9. "Protocol" = codigo do comando sendo enviado para o daemon, ou seja,"ps", "df", "finger" and "uptime" devem
        ser suportados. Desse modo, o nosso padrao sera o seguinte: numero 1 para "ps", numero 2 para "df",
        numero 3 para "finger", e numero 4 para "uptime".
    10. "HeaderChecksum"=soma de verificacao, caso aconteca de algum bit invertido, esse campo detecta erros.
        Implementar a sua propria funcao de crc16 e adicionar o resultado antes do envio das mensagens,
        e verificar do outro lado que a mensagem esta correta.
    '''
    headerChecksum = checksumIPV4(totalLen, identification, flag, ttl, protocol, src, dst)
    word = ((ttl << 24) | (protocol << 16) | headerChecksum)
    pacote.write(struct.pack("!I", word))


    '''
    11. "Source Address" = endereco da maquina de envio.
    '''
    pacote.write(src)

    '''
    12. "Destination Address" = endereco da maquina de destino.
    '''
    pacote.write(dst)

    '''
    13. "Options": campo com argumentos opcionais do comando correspondente (somente na mensagem de REQUEST),
        por exemplo, ps "-ef". Adicionalmente, o seu "daemon" deve fazer uma checagem previa destas opcoes antes de
        executa-las, garantindo que parametros maliciosos como "|", ";", e ">" nao sejam executados. Esse campo tera
        tamanho variavel, portanto, nao se preocupe se na figura acima, esse campo aparenta ter 32 bits
    '''
    pacote.write(options)
    for i in range(4 - (options % 4)):
        pacote.write(struct.pack("B", 0))

    daemons["seq"][maq] += 1

    return pacote
