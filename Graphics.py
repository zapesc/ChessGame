from Chess import *
import tkinter as tk
from tkinter import SOLID, Frame, PhotoImage, Toplevel, ttk
from tkinter.scrolledtext import ScrolledText
import tkmacosx as tkm
import os


board = Game()
board.update()
chatName = ''
chatQueue= ''
moveQueue = ''
side = ''
otherSide = ''


# root window
main_window = tk.Tk()
main_window.geometry('1200x850')
main_window.title("Chess")
main_window.columnconfigure(0, weight=4)
main_window.columnconfigure(1, weight=1)
main_window.rowconfigure(0, weight=4)
main_window.rowconfigure(1, weight=1)

wking = PhotoImage(file = r"ChessPieces/WK.png")
bking = PhotoImage(file = r"ChessPieces/BK.png")
wbish = PhotoImage(file = r"ChessPieces/WB.png")
bbish = PhotoImage(file = r"ChessPieces/BB.png")
wnight = PhotoImage(file = r"ChessPieces/WN.png")
bnight = PhotoImage(file = r"ChessPieces/BN.png")
wqueen = PhotoImage(file = r"ChessPieces/WQ.png")
bqueen = PhotoImage(file = r"ChessPieces/BQ.png")
wrook = PhotoImage(file = r"ChessPieces/WR.png")
brook = PhotoImage(file = r"ChessPieces/BR.png")
wpawn = PhotoImage(file = r"ChessPieces/WP.png")
bpawn = PhotoImage(file = r"ChessPieces/BP.png")
none = PhotoImage(file = r"ChessPieces/None.png")
circle = PhotoImage(file = r"ChessPieces/Move.png")


main_window.resizable(True, True)

# main_frame = Frame(main_window)
# main_frame.grid(row=1, column=1, sticky="nsew")
# main_frame.columnconfigure(0, weight=4)
# main_frame.columnconfigure(1, weight=1)

left_frame = Frame(main_window)
left_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
for i in range(9):
    left_frame.columnconfigure(i, weight=1)
    left_frame.rowconfigure(i, weight=1)


boardArr = []

for i in range(8):
    zeroes = []
    for j in range(8):
        zeroes.append(0)
    boardArr.append(zeroes)

selectedPiece = None
selectedPieceName = ''
nextMove = 'white'
def showMoves(pos):
    global selectedPiece
    global selectedPieceName
    global nextMove
    global moveQueue
    if selectedPiece != None:
        if pos in selectedPiece.simpleMoves:
            board.move(selectedPiece, pos)
            setBoard()
            for piece in board.ownSide(selectedPiece):
                if board.ownSide(selectedPiece)[piece] == selectedPiece:
                    selectedPieceName = piece
                moveQueue = selectedPieceName + str(pos[0]) + str(pos[1])
            if nextMove == 'white':
                nextMove = 'black'
            else:
                nextMove = 'white'
            selectedPiece = None
            selectedPieceName = ''
        

    for i in range(8):
        for j in range(8):
            if not (i + j)%2 == 0:
                boardArr[i][j].configure(bg='#E1FF99')
            else:
                boardArr[i][j].configure(bg='#ffffff')
    
    if board.getPiece(pos) != None and board.getPiece(pos).color == nextMove and board.getPiece(pos).color == side:
        original = selectedPiece
        selectedPiece = board.getPiece(pos)
        if original == selectedPiece:
            selectedPiece=None
        if selectedPiece!=None:
            for move in selectedPiece.simpleMoves:
                boardArr[move[0]][move[1]].configure(bg = '#7f7f7f')
        #boardArr[pos[0]][pos[1]].configure
    else:
        selectedPiece = None       

for i in range(8):
    for j in range(8):
        if not (i + j)%2 == 0:
            if os.name == 'posix':
                boardArr[i][j] = tkm.Button(left_frame, bg='#E1FF99', fg='Black')
            else:
                boardArr[i][j] = tk.Button(left_frame, bg='#E1FF99', fg='Black', relief=SOLID, borderwidth=1)
            boardArr[i][j].configure(font = ("Helvetica", 20, "normal"), height=2, width=5, command = lambda i=i, j=j:showMoves([i,j]))
            
        else:
            if os.name == 'posix':
                boardArr[i][j] = tkm.Button(left_frame, bg='#ffffff', fg='Black')
            else: 
                boardArr[i][j] = tk.Button(left_frame, bg='#ffffff', fg='Black', relief=SOLID, borderwidth=1)
            boardArr[i][j].configure(font = ("Helvetica", 20, "normal"), height=2, width=5, command = lambda i=i, j=j:showMoves([i,j]))
        boardArr[i][j].grid(row=8-j, column=i,  sticky="nsew")

def setBoard():
    for i in range(8):
        for j in range(8):
            if board.getPiece([i,j]) != None:
                if board.getPiece([i,j]).piece[0] == 'K' and board.getPiece([i,j]).color == 'white':
                    boardArr[i][j].configure(image = wking, height=100, width=100)
                if board.getPiece([i,j]).piece[0] == 'K' and board.getPiece([i,j]).color == 'black':
                    boardArr[i][j].configure(image = bking, height=100, width=100)
                if board.getPiece([i,j]).piece[0] == 'R' and board.getPiece([i,j]).color == 'white':
                    boardArr[i][j].configure(image = wrook, height=100, width=100)
                if board.getPiece([i,j]).piece[0] == 'R' and board.getPiece([i,j]).color == 'black':
                    boardArr[i][j].configure(image = brook, height=100, width=100)
                if board.getPiece([i,j]).piece[0] == 'N' and board.getPiece([i,j]).color == 'white':
                    boardArr[i][j].configure(image = wnight, height=100, width=100)
                if board.getPiece([i,j]).piece[0] == 'N' and board.getPiece([i,j]).color == 'black':
                    boardArr[i][j].configure(image = bnight, height=100, width=100)
                if board.getPiece([i,j]).piece[0] == 'B' and board.getPiece([i,j]).color == 'white':
                    boardArr[i][j].configure(image = wbish, height=100, width=100)
                if board.getPiece([i,j]).piece[0] == 'B' and board.getPiece([i,j]).color == 'black':
                    boardArr[i][j].configure(image = bbish, height=100, width=100)
                if board.getPiece([i,j]).piece[0] == 'Q' and board.getPiece([i,j]).color == 'white':
                    boardArr[i][j].configure(image = wqueen, height=100, width=100)
                if board.getPiece([i,j]).piece[0] == 'Q' and board.getPiece([i,j]).color == 'black':
                    boardArr[i][j].configure(image = bqueen, height=100, width=100)
                if board.getPiece([i,j]).piece[0] == 'P' and board.getPiece([i,j]).color == 'white':
                    boardArr[i][j].configure(image = wpawn, height=100, width=100)
                if board.getPiece([i,j]).piece[0] == 'P' and board.getPiece([i,j]).color == 'black':
                    boardArr[i][j].configure(image = bpawn, height=100, width=100)
            else:
                boardArr[i][j].configure(image = none, height=100, width=100)

setBoard()

chat_frame = tk.LabelFrame(main_window, text="Chat Room")
chat_frame.grid(row=0, column=1, sticky = 'nsew', padx=10, pady=10, rowspan=2)
chat = ScrolledText(chat_frame, height = 47, width = 40)
chat_frame.columnconfigure(0, weight=4)
chat_frame.columnconfigure(1, weight=1)
chat_frame.rowconfigure(0, weight=1)

chat.grid(row=0, column =0, sticky = 'nsew' , padx=10, pady=5)
chat.insert(tk.END, 'Send a message!\n ')
chat.configure(state='disabled')
input_txt = tk.Text(chat_frame, height = 3, width = 40)
input_txt.grid(row=1, column =0, sticky = 'nsew' , padx=10, pady=10)

statusFrame = tk.Frame(main_window)
statusText = tk.Label(statusFrame, text = 'Waiting for Opponent')
statusText.pack(anchor='center')
statusFrame.grid(row=1, column=0, sticky = 'nsew', padx=5, pady=5)


def MsgReceive(msg):
    chat.configure(state='normal')
    chat.insert(tk.END, '\n' + msg )
    chat.configure(state='disabled')


def ChatSender(e):
    global chatQueue
    global chatName
    text = input_txt.get("0.0","end-1c")
    if text != '':
        message = chatName + ': ' + text
        chatQueue = message
        chat.configure(state='normal')
        chat.insert(tk.END, '\n' + message)
        chat.configure(state='disabled')
        chat.see("end")
    input_txt.delete('1.0','end')
    input_txt.mark_set("insert", "1.0")    
    return "break"

input_txt.bind('<Return>', lambda e: ChatSender(e)) ###PUT THIS IN NETWORK PYTHON FILE, CALL WITH MESSAGE SENDING



