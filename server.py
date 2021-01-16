import argparse
import os
import socket
import threading

class Server(threading.Thread):
    def __init__(self, host, port):
        super().__init__()
        self.connections = []
        self.host = host
        self.port = port

    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((self.host, self.port))
        sock.listen(1)
        print("Listening at", sock.getsockname())
        while True:
            sc, sockname = sock.accept()
            server_socket = ServerSocket(sc, sockname, self)
            server_socket.start()
            self.connections.append(server_socket)
            print("joined: ", sc.getpeername())

    def broadcast(self, message, source):
        for connection in self.connections:
            if connection.sockname != source:
                connection.send(message)

    def remove_connection(self, connection):
        self.connections.remove(connection)


class ServerSocket(threading.Thread):
    def __init__(self, sc, sockname, server):
        super().__init__()
        self.sc = sc
        self.sockname = sockname
        self.server = server

    def run(self):
        while True:
            message = self.sc.recv(1024).decode("utf-8")
            if message:
                print("{} says {!r}".format(self.sockname, message))
                self.server.broadcast(message, self.sockname)
            else:
                print("{} has closed the connection".format(self.sockname))
                self.sc.close()
                server.remove_connection(self)
                return

    def send(self, message):
        self.sc.sendall(message.encode("utf-8"))


def exit(server):
    while True:
        ipt = input("")
        if ipt == "q":
            print("Closing all connections...")
            for connection in server.connections:
                connection.sc.close()
            print("Shutting down the server...")
            os._exit(0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Chatroom Server")
    parser.add_argument("host", help="Interface the server listens at")
    parser.add_argument(
        "-p", metavar="PORT", type=int, default=1060, help="TCP port (default 1060)"
    )
    args = parser.parse_args()
    server = Server(args.host, args.p)
    server.start()
    exit = threading.Thread(target=exit, args=(server,))
    exit.start()
