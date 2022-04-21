from socket import *
import threading


class Queue():
    def __init__(self):
        self.userMap = {}  # Maps user to cookie    {username: cookie}
        self.waiting = {}  # dict of people waiting for game {cookie: desiredOpponentCookie}
        self.game = {}  # dict of ongoing games    {cookie : opCookie}
        self.cookieMap = {}  # Maps cookie to user    {cookie: user}
        self.users = 0
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
                                    if self.q.userMap[data] in self.q.waiting and (self.q.waiting[self.q.userMap[data]] == user or self.q.waiting[self.q.userMap[data]] == 'None'):
                                        # self.q.userMap[data] is opponent cookie
                                        self.q.game[cookie] = self.q.userMap[data]
                                        self.q.game[self.q.userMap[data]] = cookie
                                        
                                        try:
                                            self.reply(self.q.cookieReceiver[cookie], str("StartB" + self.q.userMap[data]))
                                            self.reply(self.q.cookieReceiver[self.q.userMap[data]],(str("StartW" + cookie)))
                                        except Exception as e:
                                            print(e)

                                        del self.q.waiting[self.q.userMap[data]]
                                    else:
                                        self.q.waiting[cookie] = data
                                else:
                                    self.q.waiting[cookie] = data
                            self.q.cookieMap[cookie] = user
                            self.reply(connection_socket, "No")
                        if command == 'GetName':
                            reply = 'None'
                            if data in self.q.cookieMap:
                                reply = self.q.cookieMap[data]
                            self.reply(connection_socket, reply)
                        if command == 'Move':  # Move Format: P#a1  where c is color, P is piece, P is piece num, a-f is 0-7 x, 0-7 is y -- use # = 0 for singular pieces
                            reply = 'OK'
                            self.reply(connection_socket, reply)
                            self.reply(self.q.cookieReceiver[self.q.game[cookie]],(str("Move" + data)))
                        if command == 'Prom':  # Promote Format: P#a1V    where V is value
                            reply = 'OK'
                            self.reply(connection_socket, reply)
                            self.reply(self.q.cookieReceiver[self.q.game[cookie]],(str("Prom" + data)))
                        if command == 'Chat':
                            reply = 'OK'
                            self.reply(connection_socket, reply)
                            self.reply(self.q.cookieReceiver[self.q.game[cookie]],(str("Chat" + data)))
                        if command == 'End':   
                            if data != 'None':
                                reply = "End: Closing Connection"
                                self.reply(connection_socket, reply)
                                if cookie in self.q.game:
                                    self.reply(self.q.cookieReceiver[self.q.game[cookie]],(str("End" + data)))
                                    if self.q.cookieMap[self.q.game[cookie]] in self.q.userMap:
                                        del self.q.userMap[self.q.cookieMap[self.q.game[cookie]]]       #Free up oponents username
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
                    if command == 'User':
                        if user == 'None':
                            reply = "ERR: Invalid Name!"
                            self.reply(connection_socket, reply)
                        else:
                            self.q.userMap[user] = cookie
                            reply = "OK"
                            self.reply(connection_socket, reply)

                print(user, cookie, command, data)
            except:
                pass

s = Server()