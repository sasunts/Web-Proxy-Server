import socket
import sys
from random import randint

def Main():
    #port generation between numbers 5000 and 30000
    port = randint(5000, 30000)

    #local host
    host = '127.0.0.1'

    #TCP Socket creation
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind((host, port))
    print("Server started on port:" + str(port) + "\n")



if __name__ == '__main__':
	Main()
