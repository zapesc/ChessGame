from socket import *
import tkinter as tk
import time
def current_milli_time():
    return round(time.time() * 1000)
#----------------------------------------------------------------------------Network--------------------------------------------#
class Client:
    def __init__(self):
        self.default_ip = '192.168.137.31'
        self.default_port = 4000
        self.connected_ip = ''
        self.connected_port = 0
        self.server_identifier = (self.default_ip, self.default_port)
        self.max_attempts = 10
        self.cookie = 0
        self.username = ''
        self.opName = ''
        self.opCookie = 0
        self.pollingDelay = 2000     #ms to wait before sending a new request to server
        self.lastRequest = 0
        self.endGame = False
        self.client_socket = socket( AF_INET , SOCK_STREAM )
        self.observer = None
        self.connected = False
        self.ready = False


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
                self.connected = True
            except:
                self.client_socket = socket( AF_INET , SOCK_STREAM )
                self.connected = False
                raise TimeoutError
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
            #self.client_socket.close()
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

    def gameLoop(self):
        while not self.endGame:
            if self.ready and current_milli_time() >= self.lastRequest + self.pollingDelay:
                self.lastRequest = current_milli_time()
                reply = self.comm(command='GetStatus')
                if reply.find('Start') == 0:
                    try:
                        self.observer.graphics.connection.destroy()
                    except:
                        pass
                    self.opName = self.comm(command='GetName', data=reply[reply.index("Start") + 6:])
                    self.observer.graphics.statusText.configure(text='Game against ' + self.opName)
                    if reply[reply.index("Start") + 5: reply.index("Start")+6]=='W':
                        self.observer.side = 'white'
                        self.observer.otherSide = 'black'
                    else:
                        self.observer.side = 'black'
                        self.observer.otherSide = 'white'
                    self.observer.setBoard()
                    self.observer.showMoves([4,4])
                reply = self.comm(command='GetChat')
                if reply != 'None':
                    self.observer.MsgReceive(reply)
                reply = self.comm(command='GetMove')
                if reply != 'None':
                    pieceName = reply[0:2]
                    moveTo = [int(reply[2]), int(reply[3])]
                    if self.observer.side == 'white':
                        self.observer.board.move(self.observer.board.black[pieceName], moveTo)
                        self.observer.setBoard()
                        self.observer.nextMove = 'white'
                    if self.observer.side == 'black':
                        self.observer.board.move(self.observer.board.white[pieceName], moveTo)
                        self.observer.setBoard()
                        self.observer.nextMove = 'black'
                reply = self.comm(command='GetProm')
                if reply != 'None':
                    pieceName = reply[0:2]
                    newValue = reply[2]
                    if self.observer.side == 'white':
                        self.observer.board.promote(self.observer.board.black[pieceName], newValue)
                        self.observer.setBoard()
                        self.observer.nextMove = 'white'
                    if self.observer.side == 'black':
                        self.observer.board.promote(self.observer.board.white[pieceName], newValue)
                        self.observer.setBoard()
                        self.observer.nextMove = 'black'
                reply = self.comm(command='End')
                if reply != 'None':
                    self.observer.endScreen(reply)
            self.observer.update()

            




#---------------------------------------------------------------------Graphics-------------------------------------------------#
