import socket
import select
import sys
from termcolor import colored
from Crypto.Cipher import AES
import base64
import datetime
secret_key = raw_input('type your key(16 or 24 or 32 character):')
if len(secret_key) not in [16,24,32]:
    print colored('Your key must be 16 or 24 characters long','red')
    secret_key = raw_input('type your key(16 or 24 or 32 or 32 character):')
def en_text(y):
    rj = len(y)
    while rj%16!=0:
            rj += 1
    msg_text = y.rjust(rj)
    cipher = AES.new(secret_key,AES.MODE_ECB) 
    encoded = base64.b64encode(cipher.encrypt(msg_text))
    decoded = cipher.decrypt(base64.b64decode(encoded))
    return encoded
def de_text(y):
    rj = len(y)
    while rj%16!=0:
            rj += 1
    msg_text = y.rjust(rj) 
    cipher = AES.new(secret_key,AES.MODE_ECB)
    decoded = cipher.decrypt(base64.b64decode(y))
    return decoded

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if len(sys.argv) != 3:
    print "Correct usage: script, IP address, port number"
    exit()
IP_address = str(sys.argv[1])
Port = int(sys.argv[2])
server.connect((IP_address, Port))
while True:
    sockets_list = [sys.stdin, server]
    read_sockets,write_socket, error_socket = select.select(sockets_list,[],[])
 
    for socks in read_sockets:
        if socks == server:
            message = socks.recv(2048)
            message_s = message.split('^')
            message = message_s[1]
            message = message_s[0] + de_text(message).replace('\n','').replace(' ','').replace('&',' ')
            print colored(message,'white')
        else:
            message = sys.stdin.readline()
            time = datetime.datetime.now()
            message = message +' ['+str(time.hour)+':'+str(time.minute)+']' 
            message = message.replace(' ','&')
            message = en_text(message)
            server.send(message)
            # sys.stdout.write("<You>")
            # sys.stdout.write(de_text(message).replace(' ',''))
            sys.stdout.flush()
server.close()
