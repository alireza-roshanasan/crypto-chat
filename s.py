import socket
import select
import sys
from thread import *
clients_co = input('how many people can enter this conversation?(enter 2 for two-person conversation):') 
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
if len(sys.argv) != 3:
    print "Correct usage: script, IP address, port number"
    exit()
IP_address = str(sys.argv[1])
Port = int(sys.argv[2])
server.bind((IP_address, Port))
server.listen(clients_co)
list_of_clients = []
def clientthread(conn, addr):
    while True:
            try:
                message = conn.recv(2048)
                if message:
                    print "<" + addr[0] + ">#" + message
                    message_to_send = "<" + addr[0] + ">#" + message
                    broadcast(message_to_send, conn)
                else:
                    remove(conn)
            except:
                continue
def broadcast(message, connection):
    for clients in list_of_clients:
        if clients!=connection:
            try:
                clients.send(message)
            except:
                clients.close()
                remove(clients)
def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)
while True:
    conn, addr = server.accept()
    if len(list_of_clients) < 2:
        list_of_clients.append(conn)
        print addr[0] + " connected"
        start_new_thread(clientthread,(conn,addr))    
conn.close()
server.close()
