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
        self.userMap = {}       #Maps user to cookie    {username: cookie}
        self.waiting = {}       #dict of people waiting for game {cookie: desiredOpponentCookie}
        self.game = {}          #dict of ongoing games    {cookie : opCookie}
        self.waitingData = {}   #data waiting to be sent to clients next time they connect {cookie: data}
        self.waitingMoveData = {} #Move data waiting to be received by client
        self.waitingPromData = {} #promotion data waiting to be received by client
        self.chatData = {}      #chat data waiting to be sent ot clients next time they connect {cookie: data}
        self.cookieMap = {}     #Maps cookie to user    {cookie: user}
        self.endData = {}       #Maps cookie to end data {cookie: data}
        self.users = 0

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
                error = "ERR: Username already exists!"
                reply = error.encode()
                connection_socket.send(reply)
            else:
                if command == 'Start':
                    if data == 'None':
                        found = False
                        for userCookie in q.waiting:
                            if q.waiting[userCookie] == 'None' or q.waiting[userCookie] == user:
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
                            if q.userMap[data] in q.waiting and (q.waiting[q.userMap[data]] == user or q.waiting[q.userMap[data]] == 'None'):             #waiting stores cookies with status
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
                    q.cookieMap[cookie] = user
                if command == 'GetStatus':
                    reply = 'No'
                    if cookie in q.waitingData:
                        if not q.waitingData[cookie] == '':
                            reply = q.waitingData[cookie]
                            q.waitingData[cookie] = ''
                    reply = reply.encode()
                    connection_socket.send(reply)
                if command == 'GetMove':
                    reply = ''
                    if cookie in q.waitingMoveData:
                        if not q.waitingMoveData[cookie] == '':
                            reply = q.waitingMoveData[cookie]
                            q.waitingMoveData[cookie] = ''
                    reply = reply.encode()
                    connection_socket.send(reply)
                if command == 'GetProm':
                    reply = ''
                    if cookie in q.waitingPromData:
                        if not q.waitingPromData[cookie] == '':
                            reply = q.waitingPromData[cookie]
                            q.waitingPromData[cookie] = ''
                    reply = reply.encode()
                    connection_socket.send(reply)
                if command == 'GetChat':
                    reply = ''
                    if cookie in q.chatData:
                        if not q.chatData[cookie] == '':
                            reply = q.chatData[cookie]
                            q.chatData[cookie] = ''
                    reply = reply.encode()
                    connection_socket.send(reply)
                if command == 'GetName':
                    reply = ''
                    if data in q.cookieMap:
                        reply = q.cookieMap[data]
                    reply = reply.encode()
                    connection_socket.send(reply)
                if command == 'Move':                                   #Move Format: P#a1  where c is color, P is piece, P is piece num, a-f is 0-7 x, 0-7 is y -- use # = 0 for singular pieces
                    reply = 'OK'
                    reply = reply.encode()
                    connection_socket.send(reply)
                    q.waitingMoveData[q.game[cookie]] = data
                if command == 'Prom':                                   #Promote Format: P#a1V    where V is value
                    reply = 'OK'
                    reply = reply.encode()
                    connection_socket.send(reply)
                    q.waitingPromData[q.game[cookie]] = data
                if command == 'Chat':
                    chat = data
                    reply = 'OK'
                    reply = reply.encode()
                    connection_socket.send(reply)
                    q.chatData[q.game[cookie]] = chat           
                if command == 'End':
                    if cookie in q.endData:
                        reply = q.endData[cookie] 
                        reply = reply.encode()
                        print(reply)
                        connection_socket.send(reply)
                        if q.endData[cookie] != '':
                            if cookie in q.game:                            #Remove Opponent from dictionaries
                                opCookie = q.game[cookie]
                                if opCookie in q.game:
                                    del q.game[opCookie]
                                if opCookie in q.waitingData:
                                    del q.waitingData[opCookie]
                                if opCookie in q.waitingMoveData:
                                    del q.waitingMoveData[opCookie]
                                if opCookie in q.waitingPromData:
                                    del q.waitingPromData[opCookie]
                                if opCookie in q.chatData:
                                    del q.chatData[opCookie]
                                if opCookie in q.cookieMap:
                                    del q.cookieMap[opCookie]
                                if opCookie in q.endData:
                                    del q.endData[opCookie]
                            if user in q.userMap:
                                del q.userMap[user]
                            if cookie in q.game:
                                del q.game[cookie]
                            if cookie in q.waitingData:
                                del q.waitingData[cookie]
                            if cookie in q.waitingMoveData:
                                del q.waitingMoveData[cookie]
                            if cookie in q.waitingPromData:
                                del q.waitingPromData[cookie]
                            if cookie in q.chatData:
                                del q.chatData[cookie]
                            if cookie in q.cookieMap:
                                del q.cookieMap[cookie]
                            if cookie in q.endData:
                                del q.endData[cookie]
                    else:
                        if data!='None':
                            reply = "End: Closing Connection"
                            reply = reply.encode()
                            connection_socket.send(reply)
                            if cookie in q.game:
                                q.endData[q.game[cookie]] = data
                            if cookie in q.waiting:                         #Remove from Queue
                                del q.waiting[cookie]
                            if user in q.userMap:                           #Remove username association
                                del q.userMap[user]
        else:
            if command == 'Cookie':
                q.users+=1
                reply = str(q.users)
                reply = reply.encode()
                connection_socket.send(reply)
            if command == 'User':
                if user == 'None':
                    reply = "ERR: Invalid Name!"
                    reply = reply.encode()
                    connection_socket.send(reply)
                else:  
                    q.userMap[user] = cookie
                    reply = "OK"
                    reply = reply.encode()
                    connection_socket.send(reply)

        connection_socket.close()
        if command != 'GetStatus':
            print(user, cookie, command, data)
    except:
        connection_socket.close()

server_socket.close()