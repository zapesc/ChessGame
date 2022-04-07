from Chess import *
import tkinter as tk
from tkinter import SOLID, Frame, PhotoImage, Toplevel, ttk
from tkinter.scrolledtext import ScrolledText
import tkmacosx as tkm
import os
import Client

class Graphics:
    def __init__(self):
        # root window
        self.main_window = tk.Tk()
        self.main_window.iconbitmap("ChessPieces/AppIcon.ico")
        self.main_window.geometry('1200x850')
        self.main_window.title("Chess")
        self.main_window.columnconfigure(0, weight=1)
        self.main_window.columnconfigure(1, weight=1)
        self.main_window.rowconfigure(0, weight=1)

        self.wking = PhotoImage(file = r"ChessPieces/WK.png")
        self.bking = PhotoImage(file = r"ChessPieces/BK.png")
        self.wbish = PhotoImage(file = r"ChessPieces/WB.png")
        self.bbish = PhotoImage(file = r"ChessPieces/BB.png")
        self.wnight = PhotoImage(file = r"ChessPieces/WN.png")
        self.bnight = PhotoImage(file = r"ChessPieces/BN.png")
        self.wqueen = PhotoImage(file = r"ChessPieces/WQ.png")
        self.bqueen = PhotoImage(file = r"ChessPieces/BQ.png")
        self.wrook = PhotoImage(file = r"ChessPieces/WR.png")
        self.brook = PhotoImage(file = r"ChessPieces/BR.png")
        self.wpawn = PhotoImage(file = r"ChessPieces/WP.png")
        self.bpawn = PhotoImage(file = r"ChessPieces/BP.png")
        self.none = PhotoImage(file = r"ChessPieces/None.png")
        self.circle = PhotoImage(file = r"ChessPieces/Move.png")

        self.main_window.resizable(True, True)

        self.board_frame = Frame(self.main_window)
        self.board_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        for i in range(9):
            self.board_frame.columnconfigure(i, weight=1)
            self.board_frame.rowconfigure(i, weight=1)

        self.boardArr = [[0 for x in range(8)] for x in range(8)]
        
        self.chat_frame = tk.LabelFrame(self.main_window, text="Chat Room")
        self.chat_frame.grid(row=0, column=1, sticky = 'nsew', padx=10, pady=10, rowspan=2)
        self.chat = ScrolledText(self.chat_frame, height = 47, width = 40)
        self.chat_frame.columnconfigure(0, weight=4)
        self.chat_frame.columnconfigure(1, weight=1)
        self.chat_frame.rowconfigure(0, weight=1)

        self.chat.grid(row=0, column =0, sticky = 'nsew' , padx=10, pady=5)
        self.chat.insert(tk.END, 'Send a message!\n ')
        self.chat.configure(state='disabled')
        self.input_txt = tk.Text(self.chat_frame, height = 3, width = 40)
        self.input_txt.grid(row=1, column =0, sticky = 'nsew' , padx=10, pady=10)

        self.statusFrame = tk.Frame(self.main_window)
        self.statusText = tk.Label(self.statusFrame, text = 'Waiting for Opponent')
        self.statusText.pack(anchor='center')
        self.statusFrame.grid(row=1, column=0, sticky = 'nsew', padx=5, pady=5)

        self.connection = tk.Toplevel()
        self.connection.iconbitmap("ChessPieces/AppIcon.ico")
        self.connection.title('Server Selection')
        self.connection.resizable(0,0)

        self.inputFrame = tk.Frame(self.connection)
        self.inputFrame.grid(row=0, column=0, sticky="nsew")

        self.ipBox = tk.LabelFrame(self.inputFrame, text="Server Address")
        self.ipBox.grid(row=0, column = 0, padx=5, pady=5)
        self.server_ip = tk.Text(self.ipBox, height = 1, width = 40)
        self.server_ip.grid(row=0, column=0, sticky='nsew')

        self.portBox = tk.LabelFrame(self.inputFrame, text="Server Port")
        self.portBox.grid(row=0, column = 1, padx=5, pady=5)
        self.server_port = tk.Text(self.portBox, height = 1, width = 20)
        self.server_port.grid(row=0, column =0, sticky='nsew')

        self.submit = tk.Button(self.inputFrame, text='Submit')
        self.submit.grid(row=0, column=2, padx=5, pady=5, sticky='snew')

        self.usernameFrame = tk.LabelFrame(self.connection, text="Username")
        self.usernameFrame.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)
        self.usernameEntry = tk.Text(self.usernameFrame, height = 1, width=70)
        self.usernameEntry.grid(row=0, column=0, sticky='nsew')

        self.statusLabel = tk.Label(self.connection, text="Choose Server to connect to. Leave blank for default.")
        self.statusLabel.grid(row=2, column=0, sticky = 'nsew')

    


class GraphicsUpdater:
    def __init__(self, client):
        self.board = Game()
        self.client = client
        self.graphics = Graphics()
        self.selectedPiece = None
        self.side = ''
        self.otherSide = ''
        self.nextMove = 'white'
        self.chatName = ''
        self.once = 0
        self.graphics.connection.grab_set()
        self.graphics.input_txt.bind('<Return>', lambda e: self.ChatSender(e))
        self.graphics.submit.configure(command= lambda: self.connectServer())
        self.graphics.connection.protocol("WM_DELETE_WINDOW", self.disable_event)
        self.graphics.main_window.protocol("WM_DELETE_WINDOW", self.close_connection)

        for i in range(8):
            for j in range(8):
                if not (i + j)%2 == 0:
                    if os.name == 'posix':
                        self.graphics.boardArr[i][j] = tkm.Button(self.graphics.board_frame, bg='#ffffff', fg='Black')
                    else:
                        self.graphics.boardArr[i][j] = tk.Button(self.graphics.board_frame, bg='#ffffff', fg='Black', relief=SOLID, borderwidth=1)
                    self.graphics.boardArr[i][j].configure(font = ("Helvetica", 20, "normal"), height=2, width=5, command = lambda i=i, j=j:self.showMoves([i,j]))
                    
                else:
                    if os.name == 'posix':
                        boardArr[i][j] = tkm.Button(self.graphics.board_frame, bg='#E1FF99', fg='Black')
                    else: 
                        self.graphics.boardArr[i][j] = tk.Button(self.graphics.board_frame, bg='#E1FF99', fg='Black', relief=SOLID, borderwidth=1)
                    self.graphics.boardArr[i][j].configure(font = ("Helvetica", 20, "normal"), height=2, width=5, command = lambda i=i, j=j:self.showMoves([i,j]))
                self.graphics.boardArr[i][j].grid(row=8-j, column=i,  sticky="nsew")
 
    def showMoves(self, pos):
        if self.selectedPiece != None:
            if pos in self.selectedPiece.simpleMoves:
                self.board.move(self.selectedPiece, pos)
                self.setBoard()
                for piece in self.board.ownSide(self.selectedPiece):
                    if self.board.ownSide(self.selectedPiece)[piece] == self.selectedPiece:
                        selectedPieceName = piece
                if self.side == 'white':
                    pieceValue = self.board.white[selectedPieceName].piece
                else:
                    pieceValue = self.board.black[selectedPieceName].piece
                if ((self.side == 'white' and pos[1] == 7) or (self.side == 'black' and pos[1]==0)) and pieceValue=='P':
                    self.promote_ask(selectedPieceName, pos)
                else:
                    self.client.sendMove(selectedPieceName + str(pos[0]) + str(pos[1]) )
                if self.nextMove == 'white':
                    self.nextMove = 'black'
                else:
                    self.nextMove = 'white'
                self.selectedPiece = None
                selectedPieceName = ''
            
        for i in range(8):
            for j in range(8):
                if not (i + j)%2 == 0:
                        self.graphics.boardArr[i][j].configure(bg='#ffffff')
                else:
                        self.graphics.boardArr[i][j].configure(bg='#E1FF99')
                    
        if self.board.getPiece(pos) != None and self.board.getPiece(pos).color == self.nextMove and self.board.getPiece(pos).color == self.side:
            original = self.selectedPiece
            self.selectedPiece = self.board.getPiece(pos)
            if original == self.selectedPiece:
                self.selectedPiece=None
            if self.selectedPiece!=None:
                for move in self.selectedPiece.simpleMoves:
                    self.graphics.boardArr[move[0]][move[1]].configure(bg = '#7f7f7f')
            #boardArr[pos[0]][pos[1]].configure
        else:
            self.selectedPiece = None       

    def setBoard(self):
        if self.side == 'black' and self.once==0:
            self.once+=1
            for i in range(8):
                for j in range(4):
                    tempButton = (self.graphics.boardArr[i][7-j])
                    self.graphics.boardArr[i][7-j] = (self.graphics.boardArr[i][j])
                    self.graphics.boardArr[i][j] = tempButton
                    self.graphics.boardArr[i][7-j].configure(command= lambda i=i, j=7-j:self.showMoves([i,j]))
                    self.graphics.boardArr[i][j].configure(command= lambda i=i, j=j:self.showMoves([i,j]))

        for i in range(8):
            for j in range(8):
                if self.board.getPiece([i,j]) != None:
                    if self.board.getPiece([i,j]).piece[0] == 'K' and self.board.getPiece([i,j]).color == 'white':
                        self.graphics.boardArr[i][j].configure(image = self.graphics.wking, height=100, width=100)
                    if self.board.getPiece([i,j]).piece[0] == 'K' and self.board.getPiece([i,j]).color == 'black':
                        self.graphics.boardArr[i][j].configure(image = self.graphics.bking, height=100, width=100)
                    if self.board.getPiece([i,j]).piece[0] == 'R' and self.board.getPiece([i,j]).color == 'white':
                        self.graphics.boardArr[i][j].configure(image = self.graphics.wrook, height=100, width=100)
                    if self.board.getPiece([i,j]).piece[0] == 'R' and self.board.getPiece([i,j]).color == 'black':
                        self.graphics.boardArr[i][j].configure(image = self.graphics.brook, height=100, width=100)
                    if self.board.getPiece([i,j]).piece[0] == 'N' and self.board.getPiece([i,j]).color == 'white':
                        self.graphics.boardArr[i][j].configure(image = self.graphics.wnight, height=100, width=100)
                    if self.board.getPiece([i,j]).piece[0] == 'N' and self.board.getPiece([i,j]).color == 'black':
                        self.graphics.boardArr[i][j].configure(image = self.graphics.bnight, height=100, width=100)
                    if self.board.getPiece([i,j]).piece[0] == 'B' and self.board.getPiece([i,j]).color == 'white':
                        self.graphics.boardArr[i][j].configure(image = self.graphics.wbish, height=100, width=100)
                    if self.board.getPiece([i,j]).piece[0] == 'B' and self.board.getPiece([i,j]).color == 'black':
                        self.graphics.boardArr[i][j].configure(image = self.graphics.bbish, height=100, width=100)
                    if self.board.getPiece([i,j]).piece[0] == 'Q' and self.board.getPiece([i,j]).color == 'white':
                        self.graphics.boardArr[i][j].configure(image = self.graphics.wqueen, height=100, width=100)
                    if self.board.getPiece([i,j]).piece[0] == 'Q' and self.board.getPiece([i,j]).color == 'black':
                        self.graphics.boardArr[i][j].configure(image = self.graphics.bqueen, height=100, width=100)
                    if self.board.getPiece([i,j]).piece[0] == 'P' and self.board.getPiece([i,j]).color == 'white':
                        self.graphics.boardArr[i][j].configure(image = self.graphics.wpawn, height=100, width=100)
                    if self.board.getPiece([i,j]).piece[0] == 'P' and self.board.getPiece([i,j]).color == 'black':
                        self.graphics.boardArr[i][j].configure(image = self.graphics.bpawn, height=100, width=100)
                else:
                    self.graphics.boardArr[i][j].configure(image = self.graphics.none, height=100, width=100)

    def ChatSender(self, e):
        text = self.graphics.input_txt.get("0.0","end-1c")
        if text != '':
            message = self.chatName + ': ' + text
            self.client.sendChat(message)
            self.graphics.chat.configure(state='normal')
            self.graphics.chat.insert(tk.END, '\n' + message)
            self.graphics.chat.configure(state='disabled')
            self.graphics.chat.see("end")
        self.graphics.input_txt.delete('1.0','end')
        self.graphics.input_txt.mark_set("insert", "1.0")    
        return "break"

    def MsgReceive(self, msg):
        self.graphics.chat.configure(state='normal')
        self.graphics.chat.insert(tk.END, '\n' + msg )
        self.graphics.chat.configure(state='disabled')

    def promote_ask(self, piece, pos):
        prom_window = tk.Toplevel()
        prom_window.protocol("WM_DELETE_WINDOW", self.disable_event)
        prom_window.resizable(0,0)
        prom_window.title('Promote Pawn')
        prom_window.iconbitmap("ChessPieces/AppIcon.ico")
        description = tk.Label(prom_window, text='Choose a piece to promote to')
        description.grid(row=0, column=0)
        prom_window.columnconfigure(0, weight=1)
        prom_window.rowconfigure(0, weight=1)
        prom_window.rowconfigure(1, weight=1)
        choices = tk.Frame(prom_window)
        choices.grid(row=1, column=0)
        if self.side == 'white':
            value1 = tk.Button(choices, height=100, width=100, image = self.graphics.wbish, command=lambda window = prom_window, piece=piece, value='B', pos = pos: self.promote(piece, value, window, pos))
            value1.grid(row=0, column=0)
            value2 = tk.Button(choices, height=100, width=100, image = self.graphics.wnight, command=lambda window = prom_window, piece=piece, value='N', pos = pos: self.promote(piece, value, window, pos))
            value2.grid(row=0, column=1)
            value3 = tk.Button(choices, height=100, width=100, image = self.graphics.wrook, command=lambda window = prom_window, piece=piece, value='R', pos = pos: self.promote(piece, value, window, pos))
            value3.grid(row=0, column=2)
            value4 = tk.Button(choices, height=100, width=100, image = self.graphics.wqueen, command=lambda window = prom_window, piece=piece, value='Q', pos = pos: self.promote(piece, value, window, pos))
            value4.grid(row=0, column=3)
        if self.side == 'black':
            value1 = tk.Button(choices, height=100, width=100, image = self.graphics.bbish, command=lambda window = prom_window, piece=piece, value='B', pos = pos: self.promote(piece, value, window, pos))
            value1.grid(row=0, column=0)
            value2 = tk.Button(choices, height=100, width=100, image = self.graphics.bnight, command=lambda window = prom_window, piece=piece, value='N', pos = pos: self.promote(piece, value, window, pos))
            value2.grid(row=0, column=1)
            value3 = tk.Button(choices, height=100, width=100, image = self.graphics.brook, command=lambda window = prom_window, piece=piece, value='R', pos = pos: self.promote(piece, value, window, pos))
            value3.grid(row=0, column=2)
            value4 = tk.Button(choices, height=100, width=100, image = self.graphics.bqueen, command=lambda window = prom_window, piece=piece, value='Q', pos = pos: self.promote(piece, value, window, pos))
            value4.grid(row=0, column=3)

    def promote(self, piece, value, window, pos):
        if self.side=='white':
            self.board.promote(self.board.white[piece], value)
        if self.side=='black':
            self.board.promote(self.board.black[piece], value)
        self.client.sendProm(piece + value)
        self.client.sendMove( piece + str(pos[0]) + str(pos[1]) )
        self.setBoard()
        window.destroy()

    def connectServer(self):
        self.connectChoice(self.graphics.server_ip.get("1.0","end-1c"), self.graphics.server_port.get("1.0","end-1c"), self.graphics.usernameEntry.get("1.0","end-1c"))

    def connectChoice(self, ip,port, uname):
        if ip == '' and port=='':
            ip = self.client.default_ip
            port = self.client.default_port
        try:
            port =  int(port)
            if not (self.client.connected_ip == ip and self.client.connected_port == port):
                self.client.cookie = 0
                self.client.connected_ip = ip
                self.client.connected_port = port
            self.client.server_identifier = (ip, port)
            try:
                if self.client.cookie==0:
                    self.client.cookie = self.client.comm()
                if uname=='':
                    self.client.username = "Guest " + str(self.client.cookie)
                    uname = self.client.username
                else:
                    self.client.username = uname
                if self.client.setUName() == 'OK':
                    self.graphics.statusLabel.configure(text='Connected to Default Server as ' + self.client.username)
                    self.chatName = self.client.username
                    self.opponentAsk()
                else:
                    self.graphics.statusLabel.configure(text='That Username is taken')
            except:

                self.graphics.statusLabel.configure(text='Unable to connect to chosen Server: ' + ip +':'+ str(port))
        except:
            self.graphics.statusLabel.configure(text='Port must be a number!') 

    def opponentAsk(self):
        self.graphics.inputFrame.destroy()
        self.graphics.connection.title('Opponent Selection')
        self.graphics.usernameFrame.configure(text = 'Opponent: ')
        self.graphics.usernameEntry.delete('1.0','end')
        self.graphics.submit = tk.Button(self.graphics.usernameFrame, text='Submit', command= lambda: self.opponentHelper())
        self.graphics.submit.grid(row=0, column=1)
        self.graphics.statusLabel.configure(text='Connected to Default Server as ' + self.client.username + ". Enter username of opponent to face, or leave blank for random.")

    def opponentHelper(self):
        self.opponentChoice(self.graphics.usernameEntry.get("1.0","end-1c"))

    def opponentChoice(self, opponent):
        if opponent=='':
            opponent = 'None'
        self.client.comm(command='Start', data=opponent)
        self.graphics.statusLabel.configure(text="Waiting for Opponent", height=10, width=30)
        self.graphics.usernameFrame.destroy()
        self.graphics.connection.protocol("WM_DELETE_WINDOW", self.close_all)
        self.client.ready = True
        #self.client.gameLoop()
        
    def update(self):
        try:
            self.graphics.main_window.update()
            self.graphics.main_window.update_idletasks()
            self.graphics.connection.update_idletasks()
            self.graphics.connection.update()
        
            if self.board.winner != '' and not self.client.endGame:
                self.client.comm(command='End', data=self.board.winner)
                self.nextMove = 'None'
                self.endScreen(self.board.winner)
        except:
            pass
            

    def disable_event(self):
        pass

    def close_all(self):
        self.graphics.connection.destroy()
    
    def close_connection(self):
        self.client.comm(command='End', data='Quit')
        self.graphics.main_window.destroy()
        self.client.endGame = True
        self.client.running = False
        for thread in self.client.threadQueue:
            thread.join()
        
    
    def endScreen(self, winner):
        self.client.endGame = True
        screen = tk.Toplevel()
        screen.title('Game Results')
        screen.iconbitmap("ChessPieces/AppIcon.ico")
        winnerLabel = tk.Label(screen, height=10, width=30)
        winnerLabel.grid(row=0, column=0)
        if winner != 'stalemate':
            if winner == "Quit":
                winnerLabel.configure(text= self.otherSide.capitalize() + ' Resigned!')
            else:
                winnerLabel.configure(text = winner.capitalize() + ' Won!')
        else:
            winnerLabel.configure(text= 'A stalemate was reached!')
        while True:
            self.update()


class ClientGraphicsInterface:
    def __init__(self):
        self.client = Client.Client()
        self.updater = GraphicsUpdater(self.client)
        self.client.set_observer(self.updater)
        self.client.gameLoop()


c = ClientGraphicsInterface()







