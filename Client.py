from socket import *
from Graphics import *
import tkinter as tk

from Chess import *
import tkinter as tk
from tkinter import Frame, PhotoImage, Toplevel, ttk
import tkmacosx as tkm
import os


#----------------------------------------------------------------------------Network--------------------------------------------#
server_address = 'localhost'
server_port = '4000'
server_identifier = (server_address, server_port)
max_attempts = 10


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

main_window.mainloop()
#---------------------------------------------------------------------Graphics-------------------------------------------------#