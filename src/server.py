import socket
import sys
import threading
import os

MAX_CONNECTION = 50             #Number of backlog request
BUFFER = 5120                   #buffer size of data to be recieved
port_listen = ""                #global variable of port to listen on
blocked_urls = []               #list of blocked urls
blocked_file = "block.txt"      #Name of blocked lists file used to fetch later

def Main():
    #declared global variables
    global blocked_urls
    global port_listen

    #Initialise the blocked URLS
    block = open(blocked_file, "r")
    for i in block:
        blocked_urls.append(i)
    block.close()
    try:
        while True:
            #Menu system used to navigate the management console
            userIn = raw_input("|C - Connection | S - Settings | E - Exit|\n").lower()
            if(userIn == "c"):
                while True:
                    try:
                        port_listen = int(raw_input("Enter proxy port: "))
                        run()
                    except socket.error:
                        print("Try again, port in use")
                        pass
                    except ValueError:
                        print("Inalid argument try again")
                        pass

            elif(userIn == "e"):
                print("Exiting")
                sys.exit()

            elif(userIn == "s"):
                print("URLS BLOCKED:")
                for i in blocked_urls:
                    print(i.strip())

                while True:
                    #Menu system in place to add or remove URLS from the url file and blocked
                    #blocked list of urls
                    options = raw_input("|B - Block URL | U - Un-block URL | R - Return to menu| \n").lower()
                    if(options == 'b'):
                        url_to_block = raw_input("Enter Url to block i.e www.example.com\n")
                        block = True
                        #function is called to do the blocking
                        blockUrl(url_to_block, block)
                        break
                    elif(options == 'u'):
                        url_to_unblock = raw_input("Enter Url to un-block i.e www.example.com\n")
                        block = False
                        #function called to do the unblocking
                        blockUrl(url_to_unblock, block)
                        break
                    elif(options == 'r'):
                        break
                    else:
                        print("Inalid argument try again")
        else:
            print("Wrong input try again\n")

    except KeyboardInterrupt:
        print("\nExiting")
        sys.exit()

#This function creates our server and manages the threads involved in our proxy
#server
def run():
    global port_listen
    print(port_listen)
    try:
        #Creation of TCP Connection
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(('', int(port_listen)))
        server.listen(MAX_CONNECTION)
        print("Server Started on Port: " + str(port_listen))
        print("Running proxy")
    except Exception:
        pass

    while True:
        try:
            conn, addr = server.accept()
            request = conn.recv(BUFFER)
            #Here we start the threads which call the function handler
            pyThread = threading.Thread(target = handler, args=(conn, request))
            pyThread.daemon = True
            pyThread.start()
        except KeyboardInterrupt:
            server.close()
            print("Exiting")
            sys.exit()

    server.close()


#This function is gets the request data and organises it to passable argumentts which
#can then be used to either see if the url requested is blocked or if it is cached locally
def handler(conn, request):
    try:
        #Spliting http/https requests into URL
        first_line = request.split('\n')[0]
        url = first_line.split(' ')[1]
        http_pos = url.find("://")

        if(http_pos == -1):
            temp = url
        else:
            temp = url[(http_pos+3):]

        #Finding port to send to
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
        #calling proxy_server function to check if request is banned or in cache
        proxy_server(webserver, port, conn,request)
    except Exception, e:
        pass


#Function which checks if ur is banned otherwise sends the request and relays the
#data to the web browser.
def proxy_server(webserver, port, conn, request):
    try:
        #Checking to see if the url is banned
        for i in blocked_urls:
            if(i.lower().strip() == webserver.lower().strip()):
                print("You are trying to enter a forbidden URL")
                conn.close()
                return

        #sends request to a server
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((webserver, port))
        s.send(request)

        while True:
            #recieves the data which is then used to send to the browser.
            reply = s.recv(BUFFER)
            if(len(reply)>0):
                conn.send(reply)
                print("Request handled : " + webserver)
            else:
                break

            s.close()
            conn.close()
    except socket.error:
        s.close()
        conn.close()
        sys.exit()

#Function to block and unblock urls
def blockUrl(url, block):
    #Here we append the url to the block.txt file and the blocked_urls list
    if(block):
        blocked_urls.append(url)
        f = open(blocked_file, "a+")
        f.write(url +"\n")
        f.close()
        return

    elif not block:
        try:
            #first we remove the url from the blocked_urls list then
            #we read all the lines of the block.txt to store temporarily
            #and lastly we overwrite our block.txt file with all the lines that
            #are not the url to be removed.
            blocked_urls.remove(url+"\n")
            f = open(blocked_file,"r")
            temp = f.readlines()
            f.close()
            f = open(blocked_file,"w")
            for line in temp:
                if line!=url+"\n":
                    f.write(line)
            f.close()
        except ValueError:
            print("Url not in list")
            return
        return

if __name__ == '__main__':
	Main()
