import socket
import sys
import threading
import os

MAX_CONNECTION = 50
BUFFER = 5120
HOST = '127.0.0.1'
port_listen = ""


def Main():
    global port_listen
    while True:
        userIn = raw_input("|C - Connection | S - Settings | E - Exit|\n")

        if(userIn is "c"):
            while True:
                try:
                    port_listen = int(raw_input("Enter proxy port: "))
                    run()
                except socket.error:
                    print("Try again in port in use")
                    pass
        elif(userIn is "e"):
            print("Exiting")
            sys.exit()


def run():
    global port_listen
    print(port_listen)
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(('', int(port_listen)))
        server.listen(MAX_CONNECTION)
        print("Server Started on Port: " + str(port_listen))
        print("Running proxy")
    except Exception:
        print("Unable to start server")
        sys.exit()

    while True:
        try:
            conn, addr = server.accept()
            request = conn.recv(BUFFER)
            pyThread = threading.Thread(target = handler, args=(conn, request))
            pyThread.daemon = True
            pyThread.start()
        except KeyboardInterrupt:
            server.close()
            print("Exiting")
            sys.exit()

    server.close()


def handler(conn, request):


    try:
        first_line = request.split('\n')[0]
        url = first_line.split(' ')[1]
        http_pos = url.find("://")

        if(http_pos == -1):
            temp = url
        else:
            temp = url[(http_pos+3):]


        port_pos = temp.find(":")
        webserver_pos = temp.find("/")
        if webserver_pos == -1:
            webserver_pos = len(temp)
        webserver = ""
        port = -1
        if (port_pos==-1 or webserver_pos <port_pos):
            port = 80
            webserver = temp[:webserver_pos]
        else:
            port = int((temp[(port_pos+1):])[:webserver_pos-port_pos-1])
            webserver = temp[:port_pos]

        proxy_server(webserver, port, conn,request)
    except Exception, e:
        pass



def proxy_server(webserver, port, conn, request):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((webserver, port))
        s.send(request)

        while True:
            reply = s.recv(BUFFER)

            if(len(reply)>0):
                conn.send(reply)
                print("Request Handled : " + webserver)
            else:
                break

            s.close()
            conn.close()
    except socket.error:
        s.close()
        conn.close()
        sys.exit()




if __name__ == '__main__':
	Main()
