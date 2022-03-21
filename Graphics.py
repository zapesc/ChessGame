from Chess import *
import tkinter as tk
from tkinter import Frame, PhotoImage, Toplevel, ttk
import tkmacosx as tkm
import os


board = Game()


# root window
my_window = tk.Tk()
my_window.geometry('1200x850')
my_window.title("Chess")
my_window.columnconfigure(0, weight=4)
my_window.columnconfigure(1, weight=1)
my_window.rowconfigure(0, weight=4)
my_window.rowconfigure(1, weight=1)

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


my_window.resizable(True, True)

# main_frame = Frame(my_window)
# main_frame.grid(row=1, column=1, sticky="nsew")
# main_frame.columnconfigure(0, weight=4)
# main_frame.columnconfigure(1, weight=1)

left_frame = Frame(my_window)
left_frame.grid(row=0, column=0, sticky="nsew")
for i in range(9):
    left_frame.columnconfigure(i, weight=1)
    left_frame.rowconfigure(i, weight=1)


boardArr = []

for i in range(8):
    zeroes = []
    for j in range(8):
        zeroes.append(0)
    boardArr.append(zeroes)

for i in range(8):
    for j in range(8):
        if not (i + j)%2 == 0:
            if os.name == 'posix':
                boardArr[i][j] = tkm.Button(left_frame, bg='#E1FF99', fg='Black')
            else:
                boardArr[i][j] = tk.Button(left_frame, bg='#E1FF99', fg='Black')
            boardArr[i][j].configure(font = ("Helvetica", 20, "normal"), height=2, width=5)
            boardArr[i][j].grid(row=8-j, column=i,  sticky="nsew")
        else:
            if os.name == 'posix':
                boardArr[i][j] = tkm.Button(left_frame, bg='#ffffff', fg='Black')
            else: 
                boardArr[i][j] = tk.Button(left_frame, bg='#ffffff', fg='Black')
            boardArr[i][j].configure(font = ("Helvetica", 20, "normal"), height=2, width=5)
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

chat_frame = tk.LabelFrame(my_window, text="Chat Room")
chat_frame.grid(row=0, column=1, sticky = 'nsew', padx=10, pady=10)
chat = tk.Text(chat_frame, height = 47, width = 40)
chat_frame.columnconfigure(0, weight=4)
chat_frame.columnconfigure(1, weight=1)
chat_frame.rowconfigure(0, weight=1)

chat.grid(row=0, column =0, sticky = 'nsew' , padx=10, pady=5)
chat.insert(tk.END, 'Send a message!\n ')
chat.configure(state='disabled')
input_txt = tk.Text(chat_frame, height = 3, width = 40)
input_txt.grid(row=1, column =0, sticky = 'nsew' , padx=10, pady=10)




def MsgReceive(user,msg):
    chat.configure(state='normal')
    chat.insert(tk.END, '\n' + user + ': ' + msg)
    chat.configure(state='disabled')

def ChatSender(e):
    chat.insert(tk.END, '\n' + 'juan' + ':' + 'hi')
    chat.configure(state='disabled')

input_txt.bind('<Return>', ChatSender) ###PUT THIS IN NETWORK PYTHON FILE, CALL WITH MESSAGE SENDING


my_window.mainloop()
