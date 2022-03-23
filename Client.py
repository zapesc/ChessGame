from socket import *
import Graphics

from Chess import *
import tkinter as tk
from tkinter import Frame, PhotoImage, Toplevel, ttk
import tkmacosx as tkm
import os


#----------------------------------------------------------------------------Network--------------------------------------------#
default_ip = 'localhost'
default_port = 4000
connected_ip = ''
connected_port = 0
server_identifier = (default_ip, default_port)
max_attempts = 10
cookie = 0
username = ''
#chatName = ''

client_sock = socket( AF_INET , SOCK_STREAM )

def setIdentifier(server_address = 'localhost', server_port = 4000):
    global server_identifier
    server_identifier = (server_address, server_port)

def connect(attempt):
    try:
        client_sock.connect(server_identifier)
    except:
        if attempt<max_attempts:
            client_sock.close()
            print('Could not connect to server at', server_identifier)
        else:
            print('Could not connect to server at', server_identifier, '\nRetrying...')
            connect(attempt+1)

def comm(user='None', cookie = 'None', command = 'Cookie', data = 'None'):
    global server_identifier
    client_socket = socket( AF_INET , SOCK_STREAM )
    client_socket.connect( server_identifier )
    message = user + ": " + str(cookie) + ': ' + command + ': ' + data
    message = message.encode()
    client_socket.send(message)
    reply = client_socket.recv( 2048 )
    reply = reply.decode()
    client_socket.close()
    return reply

def setUName():
    global cookie
    global username
    reply = comm(user=username, cookie=cookie, command='User')
    return reply





#---------------------------------------------------------------------Graphics-------------------------------------------------#

Graphics.main_window.update_idletasks()
Graphics.main_window.update()

connection = tk.Toplevel()
connection.title('Server Selection')
inputFrame = tk.Frame(connection)
inputFrame.grid(row=0, column=0, sticky="nsew")
ipBox = tk.LabelFrame(inputFrame, text="Server Address")
ipBox.grid(row=0, column = 0, padx=5, pady=5)
server_ip = tk.Text(ipBox, height = 1, width = 40)
portBox = tk.LabelFrame(inputFrame, text="Server Port")
portBox.grid(row=0, column = 1, padx=5, pady=5)
server_port = tk.Text(portBox, height = 1, width = 20)
server_ip.grid(row=0, column=0, sticky='nsew')
server_port.grid(row=0, column =0, sticky='nsew')
submit = tk.Button(inputFrame, text='Submit', command= lambda: connectServer())

submit.grid(row=0, column=2, padx=5, pady=5, sticky='snew')
connection.rowconfigure(0,weight=1)
connection.rowconfigure(1,weight=1)

usernameFrame = tk.LabelFrame(connection, text="Username")
usernameFrame.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)
usernameEntry = tk.Text(usernameFrame, height = 1, width = 76)
usernameFrame.rowconfigure(0, weight=1)
usernameEntry.grid(row=0, column=0, sticky='nsew')

statusLabel = tk.Label(connection, text="Choose Server to connect to. Leave blank for default.")
statusLabel.grid(row=2, column=0, sticky = 'nsew')

def connectServer():
    connectChoice(server_ip.get("1.0","end-1c"), server_port.get("1.0","end-1c"), usernameEntry.get("1.0","end-1c"))

def disable_event():
   pass

def enable_event():
   connection.destroy()

connection.protocol("WM_DELETE_WINDOW", disable_event)

def connectChoice(ip,port, uname):
    global username
    global cookie
    global statusLabel
    global server_identifier
    global default_port
    global default_ip
    try:
        if port != '':
            p = int(port)
        if ip == '' and port=='':
            if not connected_ip== default_ip and connected_port == default_port:
                cookie=0
            server_identifier = (default_ip, default_port)
            try:
                if cookie==0:
                    cookie = comm()
                if uname=='':
                    username = "Guest " + str(cookie)
                    uname = username
                else:
                    username = uname
                if setUName() == 'OK':
                    statusLabel.configure(text='Connected to Default Server as ' + username)
                    Graphics.chatName = username
                    connection.protocol("WM_DELETE_WINDOW", enable_event)
                else:
                    if username != uname:
                        statusLabel.configure(text='That Username is taken')
                    else: 
                        statusLabel.configure(text='Connected to Default Server as ' + username)
            except:
                statusLabel.configure(text='Unable to connect to chosen Server: ' + default_ip +':'+ default_port)
        else:
            if not connected_ip == ip and connected_port == int(port):
                cookie=0
            server_identifier = (ip, int(port))
            try:
                if cookie==0:
                    cookie = comm()
                if uname== '':
                    username = "Guest " + str(cookie)
                    uname = username
                else:
                    username = uname
                if setUName() == 'OK':
                    statusLabel.configure(text='Connected to Server as ' + username)
                    Graphics.chatName = username
                    connection.protocol("WM_DELETE_WINDOW", enable_event)
                else:
                    if username != uname:
                        statusLabel.configure(text='That Username is taken')
                    else:
                        statusLabel.configure(text='Connected to Default Server as ' + username)     
            except:
                statusLabel.configure(text='Unable to connect to chosen Server: ' + ip +':'+ port)
    except:
        statusLabel.configure(text='Port must be a number!') 





Graphics.main_window.update_idletasks()
Graphics.main_window.update()
connection.update_idletasks()
connection.update()
connection.grab_set()


Graphics.main_window.mainloop()