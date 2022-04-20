from socket import *
import threading


class Queue():
    def __init__(self):
        self.userMap = {}  # Maps user to cookie    {username: cookie}
        self.waiting = {}  # dict of people waiting for game {cookie: desiredOpponentCookie}
        self.game = {}  # dict of ongoing games    {cookie : opCookie}
        # data waiting to be sent to clients next time they connect {cookie: data}
        self.waitingData = {}
        self.waitingMoveData = {}  # Move data waiting to be received by client
        self.waitingPromData = {}  # promotion data waiting to be received by client
        # chat data waiting to be sent ot clients next time they connect {cookie: data}
        self.chatData = {}
        self.cookieMap = {}  # Maps cookie to user    {cookie: user}
        self.endData = {}  # Maps cookie to end data {cookie: data}
        self.users = 0
        self.cookieConnection = {} #maps cookie to connection
        self.cookieReceiver = {}   #maps cookie to socket designated for recieving data

class Server:
    def __init__(self):
        # Initialise important variables.
        address = '0.0.0.0'
        port_number = 4000
        identifier = (address, port_number)

        # Create and bind server socket.
        self.server_socket = socket(AF_INET, SOCK_STREAM)
        self.server_socket.bind(identifier)

        self.server_socket.listen(10)

        self.q = Queue()

        while True:
            connection_socket, client_address = self.server_socket.accept()
            #connection_socket.settimeout(1)
            thread = threading.Thread(target=self.handle_client, args=(connection_socket,))
            thread.start()

    def reply(self, socket,  msg=''):
        reply = msg.encode()
        socket.send(reply)

    def handle_client(self, connection_socket):
        print('Handling Client!')
        running = True
        while running:
            try:
                # Messages will be received in the form:      User: Cookie: Command: Data
                message_from_client = connection_socket.recv(2048)
                # Messages will be sent from client in form:    (Get/Move/Chat/Start/End): Data
                msg = message_from_client.decode()
                user = msg[0:msg.index(':')]
                msg = msg[msg.index(':')+2:]
                cookie = msg[0:msg.index(':')]
                msg = msg[msg.index(':')+2:]
                command = msg[0:msg.index(':')]
                msg = msg[msg.index(':')+2:]
                data = msg



                if command == "SetRecv":
                    self.q.cookieReceiver[cookie] = connection_socket
                    print('set receiver at cookie', cookie)

                if user in self.q.userMap:
                    if self.q.userMap[user] != cookie:
                        error = "ERR: Username already exists!"
                        reply = error.encode()
                        connection_socket.send(reply)
                    else:
                        if command == 'Start':
                            self.reply(connection_socket, 'None')
                            if data == 'None':
                                found = False
                                for userCookie in self.q.waiting:
                                    if self.q.waiting[userCookie] == 'None' or self.q.waiting[userCookie] == user:
                                        self.q.game[cookie] = userCookie
                                        self.q.game[userCookie] = cookie
                                        self.q.chatData[cookie] = ''
                                        self.q.chatData[userCookie] = ''
                                        try:
                                            self.reply(self.q.cookieReceiver[cookie], str("StartB" + userCookie))
                                            self.reply(self.q.cookieReceiver[userCookie],(str("StartW" + cookie)))
                                        except Exception as e:
                                            print(e)
                                        found = True
                                        del self.q.waiting[userCookie]
                                        break
                                if not found:
                                    self.q.waiting[cookie] = 'None'
                                    
                            else:
                                if data in self.q.userMap:  # username to cookie
                                    # waiting stores cookies with status
                                    if self.q.userMap[data] in self.q.waiting and (self.q.waiting[self.q.userMap[data]] == user or self.q.waiting[self.q.userMap[data]] == 'None'):
                                        # self.q.userMap[data] is opponent cookie
                                        self.q.game[cookie] = self.q.userMap[data]
                                        self.q.game[self.q.userMap[data]] = cookie
                                        self.q.chatData[cookie] = ''
                                        self.q.chatData[self.q.userMap[data]] = ''
                                        self.q.waitingData[cookie] = "StartB" + \
                                            self.q.userMap[data]
                                        self.q.waitingData[self.q.userMap[data]
                                                    ] = "StartW" + cookie
                                        del self.q.waiting[self.q.userMap[data]]
                                    else:
                                        self.q.waiting[cookie] = data
                                else:
                                    self.q.waiting[cookie] = data
                            self.q.cookieMap[cookie] = user
                            self.reply(connection_socket, "No")
                        if command == 'GetStatus':
                            reply = 'None'
                            if cookie in self.q.waitingData:
                                if not self.q.waitingData[cookie] == '':
                                    reply = self.q.waitingData[cookie]
                                    self.q.waitingData[cookie] = ''
                            self.reply(connection_socket, reply)
                        if command == 'GetMove':
                            reply = 'None'
                            if cookie in self.q.waitingMoveData:
                                if not self.q.waitingMoveData[cookie] == '':
                                    reply = self.q.waitingMoveData[cookie]
                                    self.q.waitingMoveData[cookie] = ''
                            self.reply(connection_socket, reply)
                        if command == 'GetProm':
                            reply = 'None'
                            if cookie in self.q.waitingPromData:
                                if not self.q.waitingPromData[cookie] == '':
                                    reply = self.q.waitingPromData[cookie]
                                    self.q.waitingPromData[cookie] = ''
                            self.reply(connection_socket, reply)
                        if command == 'GetChat':
                            reply = 'None'
                            if cookie in self.q.chatData:
                                if not self.q.chatData[cookie] == '':
                                    reply = self.q.chatData[cookie]
                                    self.q.chatData[cookie] = ''
                            self.reply(connection_socket, reply)
                        if command == 'GetName':
                            reply = 'None'
                            if data in self.q.cookieMap:
                                reply = self.q.cookieMap[data]
                            self.reply(connection_socket, reply)
                        if command == 'Move':  # Move Format: P#a1  where c is color, P is piece, P is piece num, a-f is 0-7 x, 0-7 is y -- use # = 0 for singular pieces
                            reply = 'OK'
                            self.reply(connection_socket, reply)
                            self.reply(self.q.cookieReceiver[self.q.game[cookie]],(str("Move" + data)))
                            #self.q.waitingMoveData[self.q.game[cookie]] = data
                        if command == 'Prom':  # Promote Format: P#a1V    where V is value
                            reply = 'OK'
                            self.reply(connection_socket, reply)
                            self.reply(self.q.cookieReceiver[self.q.game[cookie]],(str("Prom" + data)))
                            #self.q.waitingPromData[self.q.game[cookie]] = data
                        if command == 'Chat':
                            chat = data
                            reply = 'OK'
                            self.reply(connection_socket, reply)
                            self.reply(self.q.cookieReceiver[self.q.game[cookie]],(str("Chat" + data)))
                            #self.q.chatData[self.q.game[cookie]] = chat
                        if command == 'End':
                            if cookie in self.q.endData:
                                reply = self.q.endData[cookie]
                                self.reply(connection_socket, reply)
                                running = False
                                connection_socket.close()
                                if self.q.endData[cookie] != '':
                                    if cookie in self.q.game:  # Remove Opponent from dictionaries
                                        opCookie = self.q.game[cookie]
                                        if opCookie in self.q.game:
                                            del self.q.game[opCookie]
                                        if opCookie in self.q.waitingData:
                                            del self.q.waitingData[opCookie]
                                        if opCookie in self.q.waitingMoveData:
                                            del self.q.waitingMoveData[opCookie]
                                        if opCookie in self.q.waitingPromData:
                                            del self.q.waitingPromData[opCookie]
                                        if opCookie in self.q.chatData:
                                            del self.q.chatData[opCookie]
                                        if opCookie in self.q.cookieMap:
                                            del self.q.cookieMap[opCookie]
                                        if opCookie in self.q.endData:
                                            del self.q.endData[opCookie]
                                    if user in self.q.userMap:
                                        del self.q.userMap[user]
                                    if cookie in self.q.game:
                                        del self.q.game[cookie]
                                    if cookie in self.q.waitingData:
                                        del self.q.waitingData[cookie]
                                    if cookie in self.q.waitingMoveData:
                                        del self.q.waitingMoveData[cookie]
                                    if cookie in self.q.waitingPromData:
                                        del self.q.waitingPromData[cookie]
                                    if cookie in self.q.chatData:
                                        del self.q.chatData[cookie]
                                    if cookie in self.q.cookieMap:
                                        del self.q.cookieMap[cookie]
                                    if cookie in self.q.endData:
                                        del self.q.endData[cookie]
                            else:
                                if data != 'None':
                                    reply = "End: Closing Connection"
                                    self.reply(connection_socket, reply)
                                    if cookie in self.q.game:
                                        self.reply(self.q.cookieReceiver[self.q.game[cookie]],(str("End" + data)))
                                    if cookie in self.q.waiting:  # Remove from Queue
                                        del self.q.waiting[cookie]
                                    if user in self.q.userMap:  # Remove username association
                                        del self.q.userMap[user]
                                    running = False
                                    connection_socket.close()
                            try:
                                reply = 'None'
                                self.reply(connection_socket, reply)
                            except:
                                pass
                else:
                    if command == 'Cookie':
                        self.q.users += 1
                        reply = str(self.q.users)
                        self.reply(connection_socket, reply)
                        self.q.cookieConnection[self.q.users] = connection_socket
                    if command == 'User':
                        if user == 'None':
                            reply = "ERR: Invalid Name!"
                            self.reply(connection_socket, reply)
                        else:
                            self.q.userMap[user] = cookie
                            reply = "OK"
                            self.reply(connection_socket, reply)

                if command != 'GetStatus':
                    print(user, cookie, command, data)
            except:
                pass
                #connection_socket.close()

s = Server()