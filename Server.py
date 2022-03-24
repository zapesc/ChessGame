from multiprocessing import connection
from socket import *

# Initialise important variables.
address = 'localhost'
port_number = 4000
identifier = ( address , port_number )

# Create and bind server socket.
server_socket = socket( AF_INET , SOCK_STREAM )
server_socket.bind( identifier )


server_socket.listen( 10 )

class Queue():
    def __init__(self):
        self.userMap = {}       #Maps user to cookie
        self.waiting = {}       #dict of people waiting for game {cookie: desiredOpponentCookie}
        self.game = {}          #dict of ongoing games    {cookie : opCookie}
        self.waitingData = {}   #data waiting to be sent ot clients next time they connect {cookie: data}
        self.users = 0
        self.chatData = {}      #chat data waiting to be sent ot clients next time they connect {cookie: data}
        self.cookieMap = {}     #Maps cookie to user

q = Queue()

while True:


    # Accept a new connection.
    connection_socket , client_address = server_socket.accept()             #No need to worry ab this blocking code, as clients will be connecting very often
    connection_socket.settimeout(1)                                         #Ensure one client does not take too long and block others

    try:                                                                
        message_from_client = connection_socket.recv( 2048 )                    #Messages will be received in the form:      User: Cookie: Command: Data
        msg = message_from_client.decode()                                      #Messages will be sent from client in form:    (Get/Move/Chat/Start/End): Data
        user = msg[0:msg.index(':')]
        msg = msg[msg.index(':')+2:]
        cookie = msg[0:msg.index(':')]
        msg = msg[msg.index(':')+2:]
        command =  msg[0:msg.index(':')]
        msg = msg[msg.index(':')+2:]
        data = msg
    


        if user in q.userMap:
            if q.userMap[user] != cookie:
                error = "ERR: Username does not match Cookie!"
                reply = error.encode()
                connection_socket.send(reply)
            else:
                if command == 'Start':
                    if data == 'None':
                        found = False
                        for userCookie in q.waiting:
                            if q.waiting[userCookie] == 'None':
                                q.game[cookie] = userCookie
                                q.game[userCookie] = cookie
                                q.chatData[cookie] = ''
                                q.chatData[userCookie] = ''
                                q.waitingData[cookie] = "StartB" + userCookie
                                q.waitingData[userCookie] = "StartW" + cookie
                                found = True
                                del q.waiting[userCookie] 
                                break
                        if not found:
                            q.waiting[cookie] = 'None'
                    else: 
                        if data in q.userMap:                                                                   #username to cookie
                            if q.userMap[data] in q.waiting and q.waiting[q.userMap[data]] == user:             #waiting stores cookies with status
                                q.game[cookie] = q.userMap [data]                                               #q.userMap[data] is opponent cookie
                                q.game[q.userMap[data]] = cookie
                                q.chatData[cookie] = ''
                                q.chatData[q.userMap[data]] = ''
                                q.waitingData[cookie] = "StartB" + q.userMap[data]
                                q.waitingData[q.userMap[data]] = "StartW" + cookie
                                del q.waiting[q.userMap[data]]
                            else:
                                q.waiting[cookie] = data
                        else:
                            q.waiting[cookie] = data
                if command == 'Get':
                    reply = 'No'
                    if cookie in q.waitingData:
                        if not q.waitingData[cookie] == '':
                            reply = q.waitingData[cookie]
                            q.waitingData[cookie] = ''
                    reply = reply.encode()
                    connection_socket.send(reply)
                if command == 'Move':                                   #Move Format: MovecP#a1  where c is color, P is piece, P is piece num, a-f is 0-7 x, 0-7 is y -- use # = 0 for singular pieces
                    reply = 'OK'
                    reply = reply.encode()
                    connection_socket.send(reply)
                    if q.waitingData[q.game[cookie]] != '':
                        q.waitingData[q.game[cookie]] += ('/' + command + data)
                    else:
                        q.waitingData[q.game[cookie]] += (command + data)
                if command == 'Prom':                                   #Promote Format: PromcP#a1
                    reply = 'OK'
                    reply = reply.encode()
                    connection_socket.send(reply)
                    if q.waitingData[q.game[cookie]] != '':
                        q.waitingData[q.game[cookie]].append('/' + command + data)
                    else:
                        q.waitingData[q.game[cookie]].append(command + data)
                if command == 'Chat':
                    chat = 'Chat:' + user + ": " + data
                    reply = 'OK'
                    reply = reply.encode()
                    connection_socket.send(reply)
                    q.chatData[q.game[cookie]] = chat
                if command == 'GetChat':
                    reply = 'No'
                    if cookie in q.chatData:
                        if not q.chatData[cookie] == '':
                            reply = q.chatData[cookie]
                            q.chatData[cookie] = ''
                    reply = reply.encode()
                    connection_socket.send(reply)
                if command == 'End':
                    reply = "End: Closing Connection"
                    reply = reply.encode()
                    connection_socket.send(reply)
                    del q.game[q.game[cookie]]
                    del q.game[cookie]
        else:
            if command == 'Cookie':
                q.users+=1
                reply = str(q.users)
                #reply = "OK: " + reply
                reply = reply.encode()
                connection_socket.send(reply)
            if command == 'User':
                if user == 'None':
                    reply = "ERR: Invalid Name!"
                    reply = reply.encode()
                    connection_socket.send(reply)
                else:  
                    if user in q.userMap:
                        if q.userMap[user] != cookie:
                            error = "ERR: Username already exists!"
                            reply = error.encode()
                            connection_socket.send(reply)
                    else:
                        q.userMap[user] = cookie
                        reply = "OK"
                        reply = reply.encode()
                        connection_socket.send(reply)

        connection_socket.close()
        print(user, cookie, command, data)
    except:
        connection_socket.close()

server_socket.close()