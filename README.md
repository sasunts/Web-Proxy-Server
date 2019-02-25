# Web-Proxy-Server
CS3031 - Project

### Task
The program should be able to:
1. Respond to HTTP & HTTPS requests, and should display each request on a management
console. It should forward the request to the Web server and relay the response to the
browser.
1. Handle websocket connections.
1. Dynamically block selected URLs via the management console.
1. Efficiently cache requests locally and thus save bandwidth. You must gather timing and
bandwidth data to prove the efficiency of your proxy.
1. Handle multiple requests simultaneously by implementing a threaded server.

The program can be written in a programming language of your choice. However, you must ensure that
you do not overuse any API or Library functionality that implements the majority of the work for you.


## Start

To start the proxy make sure you are using python 2.7.x
In terminal open the src folder and run the command `python server.py`


##### Attempt at GUI

The GUI is made using Tkinter however there are issues running the server on it
as the mainloop is mainly used by Tkinter and app crashes on bind of connection.

![alt text](https://github.com/sasunts/Web-Proxy-Server/blob/master/img/gui.png)
