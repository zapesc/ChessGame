from socket import *
import tkinter as tk
import time
import threading

def current_milli_time():
    return round(time.time() * 1000)
#----------------------------------------------------------------------------Network--------------------------------------------#
class Client:
    def __init__(self):
        self.default_ip = '192.168.137.1'
        self.default_port = 4000
        self.connected_ip = '' #
        self.connected_port = 0 #
        self.server_identifier = (self.default_ip, self.default_port)
        self.max_attempts = 10 #
        self.cookie = 0
        self.username = ''
        self.opName = '' #
        self.opCookie = 0 #
        self.pollingDelay = 2000     #ms to wait before sending a new request to server
        self.lastRequest = 0
        self.endGame = False
        self.client_socket = socket( AF_INET , SOCK_STREAM )
        self.recv_socket = socket(AF_INET, SOCK_STREAM)
        self.observer = None
        self.connected = False
        self.ready = False
        self.setReceiver = False
        self.threadQueue = []
        self.running = True

        self.queue = {'Start': '', 'Chat': '', 'Move': '', 'Prom': '', 'End': ''}


    def setIdentifier(self, server_address = '', server_port = 0):
        if server_address == '':
            server_address = self.default_ip
        if server_port == 0:
            server_port = self.default_port
        self.server_identifier = (server_address, server_port)

    def comm(self, user='', cook = 'None', command = 'Cookie', data = 'None'):
        if not self.connected:
            self.client_socket.settimeout(1)
            try:
                self.client_socket.connect(self.server_identifier)
                self.recv_socket.connect(self.server_identifier)
                self.connected = True
            except:
                self.client_socket = socket( AF_INET , SOCK_STREAM )
                self.recv_socket = socket( AF_INET , SOCK_STREAM )
                self.connected = False
                raise TimeoutError
        if self.cookie != 0 and not self.setReceiver:
            self.recv_socket.send((self.username + ": " + str(self.cookie) + ': ' + 'SetRecv' + ': ' + "None").encode())
            self.setReceiver = True
        if self.connected and not self.endGame:
            if user == '':
                user=self.username
            if cook=='None':
                cook = self.cookie
            message = user + ": " + str(cook) + ': ' + command + ': ' + data
            message = message.encode()
            self.client_socket.send(message)
            reply = self.client_socket.recv( 2048 )
            reply = reply.decode()
            return reply
        return ''

    def setUName(self):
        reply = self.comm(user=self.username, cook=self.cookie, command='User')
        return reply
    
    def set_observer(self, observer):
        self.observer = observer

    def sendChat(self, msg):
        self.comm(command='Chat', data= str(msg))

    def sendMove(self, move):
        self.comm(command='Move', data= move)
    
    def sendProm(self, prom):
        self.comm(command='Prom', data= prom)

    def loop(self):
        while self.running:
            while self.ready and not self.endGame:
                print("1")
                reply = self.recv_socket.recv(2048)
                reply = reply.decode()
                print(reply)
                if reply.find('Start') == 0:
                    self.queue['Start'] = reply[reply.index("Start") + 5:]
                elif reply.find('Chat') == 0:
                    self.queue['Chat'] = reply[reply.index("Chat") + 4:]
                elif reply.find('Move') == 0:
                    self.queue['Move'] = reply[reply.index("Move") + 4:]
                elif reply.find('Prom') == 0:
                    self.queue['Prom'] = reply[reply.index("Prom") + 4:]
                elif reply.find('End') == 0:
                    self.queue['End'] = reply[reply.index("End") + 3:]

    def checkQueue(self):
        if self.queue['Start'] != '':
            info = self.queue['Start']      #info contains opponent cookie and side user is playing on
            try:
                self.observer.graphics.connection.destroy()
            except:
                pass
            
            self.observer.graphics.statusText.configure(text='Game against ' + self.comm(command='GetName', data=info[1:]))
            if info[0]=='W':
                self.observer.side = 'white'
                self.observer.otherSide = 'black'
            else:
                self.observer.side = 'black'
                self.observer.otherSide = 'white'
            self.observer.setBoard()
            self.observer.showMoves([4,4])
            self.queue['Start'] = ''

        if self.queue['Chat'] != '':
            info = self.queue['Chat']
            self.observer.MsgReceive(info)
            self.queue['Chat'] = ''

        if self.queue['Move'] != '':
            info = self.queue['Move']
            pieceName = info[0:2]
            moveTo = [int(info[2]), int(info[3])]
            if self.observer.side == 'white':
                self.observer.board.move(self.observer.board.black[pieceName], moveTo)
                self.observer.setBoard()
                self.observer.nextMove = 'white'
            if self.observer.side == 'black':
                self.observer.board.move(self.observer.board.white[pieceName], moveTo)
                self.observer.setBoard()
                self.observer.nextMove = 'black'
            self.queue['Move'] = ''

        if self.queue['Prom'] != '':
            info = self.queue['Prom']
            pieceName = info[0:2]
            newValue = info[2]
            if self.observer.side == 'white':
                self.observer.board.promote(self.observer.board.black[pieceName], newValue)
                self.observer.setBoard()
                self.observer.nextMove = 'white'
            if self.observer.side == 'black':
                self.observer.board.promote(self.observer.board.white[pieceName], newValue)
                self.observer.setBoard()
                self.observer.nextMove = 'black'
            self.queue['Prom'] = ''

        if self.queue['End'] != '':
            info = self.queue['End']
            self.observer.endScreen(info)
            self.queue['End'] = ''

    def gameLoop(self):
        thread = threading.Thread(target= self.loop)
        thread.start()
        while not self.endGame: 
            self.checkQueue()
            self.observer.update()
        self.threadQueue.append(thread)

            




#---------------------------------------------------------------------Graphics-------------------------------------------------#
