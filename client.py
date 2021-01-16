import argparse
import base64
import datetime
import hashlib
import os
import socket
import sys
import threading

from Crypto import Random
from Crypto.Cipher import AES
from termcolor import colored


class AESCipher(object):
    def __init__(self, key):
        self.bs = AES.block_size    
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, raw):
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw.encode()))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[: AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size :])).decode("utf-8")

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[: -ord(s[len(s) - 1 :])]


class Send(threading.Thread):
    def __init__(self, sock, name):
        super().__init__()
        self.sock = sock
        self.name = name

    def run(self):
        while True:
            print("{}: ".format(self.name), end="")
            sys.stdout.flush()
            message = sys.stdin.readline()[:-1]
            if message == "QUIT":
                self.sock.sendall(
                    "Server: {} has left the chat.".format(self.name).encode("utf-8")
                )
                break
            else:
                message = enc.encrypt("{}: {}".format(self.name, message))
                self.sock.sendall(message)
        self.sock.close()
        os._exit(0)


class Receive(threading.Thread):
    def __init__(self, sock, name):
        super().__init__()
        self.sock = sock
        self.name = name
        self.messages = None

    def run(self):
        while True:
            message = self.sock.recv(1024)
            if message:
                try:
                    message = str(enc.decrypt(message))
                except:
                    message = message.decode("utf-8")
                print("\r{}\n{}: ".format(colored(message, "red"), self.name), end="")
            else:
                print("\nlost connection...")
                self.sock.close()
                os._exit(0)


class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.name = None
        self.messages = None

    def start(self):
        self.sock.connect((self.host, self.port))
        self.name = input("Your name: ")
        send = Send(self.sock, self.name)
        receive = Receive(self.sock, self.name)
        send.start()
        receive.start()
        self.sock.sendall("Server: {} has joined".format(self.name).encode("utf-8"))
        return receive


def main(host, port):
    client = Client(host, port)
    client.start()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("host")
    parser.add_argument(
        "-p", metavar="PORT", type=int, default=1060, help="TCP port (default 1060)"
    )
    args = parser.parse_args()
    secret_key = input('type your key: ')
    enc = AESCipher(secret_key)
    main(args.host, args.p)
