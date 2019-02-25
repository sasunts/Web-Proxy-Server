import Tkinter as tk
import socket
import sys
import threading
import os
import zlib

HEIGHT = 600
WIDTH = 800
MAX_CONNECTION = 50             #Number of backlog request
BUFFER = 5120                   #buffer size of data to be recieved
blocked_urls = []               #list of blocked urls
cache ={}                       #Key value pair (hashmap) for cache for O(1) access
blocked_file = "block.txt"      #Name of blocked lists file used to fetch later


def run(port):
    #declared global variables
    global blocked_urls
    #Initialise the blocked URLS
    block = open(blocked_file, "r")
    for i in block:
        blocked_urls.append(i)
    block.close()
    while True:
        try:
            #Creation of TCP Connection
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.bind(('', int(port))) #CRASHES HERE!
            server.listen(MAX_CONNECTION)
            print("Server Started on Port: " + str(port_listen))
            print("Running proxy")
            break
        except socket.error:
            print("Try again, port in use")
            return
        except ValueError:
            print("Inalid argument try again")
            return
        except Exception:
            pass


    # while True:
    #     try:
    #         conn, addr = server.accept()
    #         request = conn.recv(BUFFER)
    #         #Here we start the threads which call the function handler
    #         pyThread = threading.Thread(target = handler, args=(conn, request))
    #         pyThread.daemon = True
    #         pyThread.start()
    #     except KeyboardInterrupt:
    #         server.close()
    #         print("Exiting")
    #         sys.exit()

    server.close()
    return








###########################GUI##########################
#start
root = tk.Tk()
canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack()


left_frame = tk.Frame(root)
left_frame.place( relwidth=0.5,relheight=0.5)

right_frame = tk.Frame(root)
right_frame.place(relx=0.5, relwidth=0.5,relheight=0.5)

console_frame = tk.Frame(root, bd=5, bg="black")
console_frame.place(rely=0.5,relwidth=1, relheight=1)

label_console = tk.Label(console_frame,)
label_console.place(relx=0, rely=0, relwidth =1,relheight=1)

label = tk.Label(root, text= "Web Proxy Server")
label.place(x=330,y=0)
label_console_title = tk.Label(root, text= "Console")
label_console_title.place(x=370,y=280)

#####left!!!!
label_port = tk.Label(left_frame, text= "Enter proxy port:")
label_port.place(x=10, y=100)

port_entry = tk.Entry(left_frame)
port_entry.place(x=10, y=130)
startButton = tk.Button(left_frame, text = "Start", command=lambda:run(port_entry.get()) )
startButton.place(x=10, y=160)
idicator = tk.Label(left_frame,height=1, width =1, bg= "red")
idicator.place(x=30, y =200)
#######

###Right!!!
label_url = tk.Label(right_frame, text= "Enter url i.e www.example.com:")
label_url.place(x=10, y=100)

entry_url = tk.Entry(right_frame)
entry_url.place(x=10, y=130)
blockButton = tk.Button(right_frame, text = "Block")
blockButton.place(x=10, y=160)
unblockButton = tk.Button(right_frame, text = "Unblock")
unblockButton.place(x=80, y=160)

#end
root.mainloop()
