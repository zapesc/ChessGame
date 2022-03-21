# Need to add en passant and castling

import copy

class Piece():
    def __init__(self, color, piece, pos):
        self.color = color
        self. piece =  piece
        self.position = pos
        self.movesDone = 0
        self.value = 0
        self.possibleMoves = []
        self.simpleMoves = []
        self.pawnAttackMoves = []
        
    def simpleMoveMaker(self):
        moves = []
        for arr in self.possibleMoves:
            for direction in arr:
                if direction != []:
                    moves.append(direction)
        self.simpleMoves = moves
        return self

class Game:
    def __init__(self):
        self.black = {'R1':0, 'N1':0, 'B1':0, 'Q':0, 'K':0, 'B2':0, 'N2':0, 'R2':0,
             'P1':0, 'P2':0, 'P3':0, 'P4':0, 'P5':0, 'P6':0, 'P7':0, 'P8':0}

        self.white = {'R1':0, 'N1':0, 'B1':0, 'Q':0, 'K':0, 'B2':0, 'N2':0, 'R2':0,
             'P1':0, 'P2':0, 'P3':0, 'P4':0, 'P5':0, 'P6':0, 'P7':0, 'P8':0}

        self.black['R1'] = Piece('black', 'R1', [0,7])
        self.black['N1'] = Piece('black', 'N1', [1,7])
        self.black['B1'] = Piece('black', 'B1', [2,7])
        self.black['Q']  = Piece('black', 'Q', [3,7])
        self.black['K']  = Piece('black', 'K', [4,7])
        self.black['B2'] = Piece('black', 'B2', [5,7])
        self.black['N2'] = Piece('black', 'N2', [6,7])
        self.black['R2'] = Piece('black', 'R2', [7,7])
        for i in range(1,9):
            self.black['P' + str(i)] = Piece('black', 'P' + str(i), [i-1, 6])

        self.white['R1'] = Piece('white', 'R1', [0,0])
        self.white['N1'] = Piece('white', 'N1', [1,0])
        self.white['B1'] = Piece('white', 'B1', [2,0])
        self.white['Q']  = Piece('white', 'Q', [3,0])
        self.white['K']  = Piece('white', 'K', [4,0])
        self.white['B2'] = Piece('white', 'B2', [5,0])
        self.white['N2'] = Piece('white', 'N2', [6,0])
        self.white['R2'] = Piece('white', 'R2', [7,0])
        for i in range(1,9):
            self.white['P' + str(i)] = Piece('white', 'P' + str(i), [i-1, 1])
        # self.white['N2'].position = [8,8]
        # self.white['B2'].position = [8,8]
        # self.white['P7'].position = [8,8]
        # self.black['R1'].position = [6,5]
        

    def otherSide(self, piece):            #Returns dictionary of same team as passed piece
        if piece.color == 'black':
            return self.white
        if piece.color == 'white':
            return self.black
    
    def ownSide(self, piece):              ##Returns dictionary of other team of passed piece
        if piece.color == 'black':
            return self.black
        if piece.color == 'white':
            return self.white
            
    def allMoves(self, piece):             #Returns all standard moves for a piece, in a series of arrays
        if piece.piece[0]=='K':
            x = piece.position[0]
            y = piece.position[1]
            piece.possibleMoves = [[[x + 1, y]], [[x-1,y]], [[x, y+1]], [[x, y-1]], [[x+1,y+1]], [[x+1, y-1]], [[x-1, y+1]], [[x-1, y-1]]]

        if piece.piece[0] == 'N':
            x = piece.position[0]
            y = piece.position[1]
            piece.possibleMoves = [[[x + 2, y + 1]], [[x + 2, y - 1]], [[x - 2, y + 1]], [[x - 2, y - 1]], [[x + 1, y + 2]], [[x + 1, y - 2]], [[x - 1, y + 2]], [[x - 1, y - 2]]]
            return piece

        if piece.piece[0]=='Q':
            tr = []
            tl = []
            br = []
            bl = []
            up = []
            down = []
            left = []
            right = []
            for i in range(1,8):
                tr.append([piece.position[0] + i, piece.position[1] + i])
                br.append([piece.position[0] + i, piece.position[1] - i])
                tl.append([piece.position[0] - i, piece.position[1] + i])
                bl.append([piece.position[0] - i, piece.position[1] - i])
                up.append([piece.position[0],i+piece.position[1]])
                down.append([piece.position[0],piece.position[1]-i])            
                left.append([piece.position[0]-i,piece.position[1]])
                right.append([piece.position[0]+i,piece.position[1]])
            piece.possibleMoves = [up, down, left, right, tr, tl, br, bl]
            return piece

        if piece.piece[0] == 'P':
            x = piece.position[0]
            y = piece.position[1]

            moves = []
            captures = []
            if piece.color == 'white':
                moves.append([x, y +1])
                if piece.movesDone == 0 and self.getPiece(piece.position) != None:
                    moves.append([x, y+2])
                for take in self.black.values():
                    if take.position == [x+1, y+1] or take.position == [x-1, y+1]:
                        captures.append(take.position)
                piece.pawnAttackMoves = [[x+1, y+1], [x-1, y+1]]
            if piece.color == 'black':
                moves.append([x, y-1])
                if piece.movesDone == 0 and self.getPiece(piece.position) != None:
                    moves.append([x, y-2])
                for take in self.black.values():
                    if take.position == [x+1, y-1] or take.position == [x-1, y-1]:
                        captures.append(take.position)
                piece.pawnAttackMoves = [[x+1, y-1], [x-1, y-1]]
            piece.possibleMoves = [moves, captures]

        if piece.piece[0] == 'B':
            tr = []
            tl = []
            br = []
            bl = []
            for i in range(1,8):
                tr.append([piece.position[0] + i, piece.position[1] + i])
                br.append([piece.position[0] + i, piece.position[1] - i])
                tl.append([piece.position[0] - i, piece.position[1] + i])
                bl.append([piece.position[0] - i, piece.position[1] - i])
            piece.possibleMoves = [tr, tl, br, bl]
            return piece
        
        if piece.piece[0]=='R':
            up = []
            down = []
            right = []
            left = []
            for i in range(1,8):
                up.append([piece.position[0],i+piece.position[1]])
                down.append([piece.position[0],piece.position[1]-i])            
                left.append([piece.position[0]-i,piece.position[1]])
                right.append([piece.position[0]+i,piece.position[1]])
            piece.possibleMoves = [up, down, left, right]
            return piece
        return piece

    def clean(self, piece):                #Removes invalid points (outside of board) from array of Moves
        moves = []
        for i in range(len(piece.possibleMoves)):
            direction = []
            for point in piece.possibleMoves[i]:
                if not (point[0]<0 or point[0]>7 or point[1]<0 or point[1]>7):
                    direction.append(point)
            piece.possibleMoves[i] = direction
        return piece

    def ownPiece(self, piece):             #Removes places where own pieces are from Moves
        for direction in range(len(piece.possibleMoves)):
            moves = piece.possibleMoves[direction][:]
            if piece.color == 'black':
                for point in self.black.values():
                    if point.position in moves:
                        moves =  moves[0:moves.index(point.position)]
            if piece.color == 'white':
                for point in self.white.values():
                    if point.position in moves:
                        moves =  moves[0:moves.index(point.position)]
            piece.possibleMoves[direction] = moves
        return piece
        
    def otherPiece(self, piece):           #Removes places past where other pieces are from Moves
        for direction in range(len(piece.possibleMoves)):
            moves = piece.possibleMoves[direction][:]
            if piece.color == 'black':
                for point in self.white.values():
                    if point.position in moves:
                        moves =  moves[0:moves.index(point.position)+1]
            if piece.color == 'white':
                for point in self.black.values():
                    if point.position in moves:
                        moves =  moves[0:moves.index(point.position)+1]
            piece.possibleMoves[direction] = moves
        return piece

    def isCheck(self, king):               #Boolean: Whether passed king is in check
        for piece in self.otherSide(king).values():
            for move in piece.simpleMoves:
                if move == king.position:
                    return True
        return False                            

    def possibleMoves(self):               #Sets all valid moves to each piece
        for piece in self.white:
            self.otherPiece(self.ownPiece(self.clean(self.allMoves(self.white[piece]))))
            self.white[piece].simpleMoveMaker()         #Removes outside array from Moves array, makes simpler to implement possible moves.
            if piece == 'R1':
                if self.white[piece].movesDone == 0 and self.white['K'].movesDone == 0: 
                    if [3,0] in self.white[piece].simpleMoves:
                        self.white['K'].simpleMoves.append([2,0])
            if piece == 'R2':
                if self.white[piece].movesDone == 0 and self.white['K'].movesDone == 0: 
                    if [5,0] in self.white[piece].simpleMoves:
                        self.white['K'].simpleMoves.append([6,0])
    
        for piece in self.black:
            self.otherPiece(self.ownPiece(self.clean(self.allMoves(self.black[piece]))))
            self.black[piece].simpleMoveMaker()
            if piece == 'R1':
                if self.black[piece].movesDone == 0 and self.white['K'].movesDone == 0: 
                    if [3,7] in self.black[piece].simpleMoves:
                        self.white['K'].simpleMoves.append([2,7])
            if piece == 'R2':
                if self.black[piece].movesDone == 0 and self.white['K'].movesDone == 0: 
                    if [5,7] in self.black[piece].simpleMoves:
                        self.white['K'].simpleMoves.append([6,7])
    
    def getPiece(self, position):          #Gets piece at a board position
        for piece in self.black.values():
            if piece.position == position:
                return piece
        for piece in self.white.values():
            if piece.position == position:
                return piece
        return None
        
    def moveChecker(self):                 #Removes moves that lead to own check from options 
        original = copy.deepcopy(self)

        for piece in original.white:
            new = copy.deepcopy(original)
            moves = []
            for move in original.white[piece].simpleMoves:
                new.white[piece].position = move
                new.possibleMoves()
                if not new.isCheck(new.white['K']):
                    moves.append(move)
            self.white[piece].simpleMoves = moves
        for piece in original.black:
            new = copy.deepcopy(original)
            moves = []
            for move in original.black[piece].simpleMoves:
                new.black[piece].position = move
                new.possibleMoves()
                if not new.isCheck(new.black['K']):
                     moves.append(move)
            self.black[piece].simpleMoves = moves

    def move(self, piece, move):           #Moves a piece and updates board
        previousPos = piece.position
        piece.position = move       
        piece.movesDone +=1
        self.possibleMoves()
        #en passant check
        if piece.piece[0] == 'P' and piece.movesDone == 1:
            if piece.color == 'black':
                for i in range(1,9):
                    if [previousPos[0], previousPos[1] - 1] in self.otherSide(piece)['P' + str(i)].pawnAttackMoves and [previousPos[0], previousPos[1] - 1] not in self.otherSide(piece)['P' + str(i)].simpleMoves:
                        self.otherSide(piece)['P' + str(i)].simpleMoves.append([previousPos[0], previousPos[1] - 1])
            if piece.color == 'white':
                for i in range(1,9):
                    if [previousPos[0], previousPos[1] + 1] in self.otherSide(piece)['P' + str(i)].pawnAttackMoves and [previousPos[0], previousPos[1] + 1] not in self.otherSide(piece)['P' + str(i)].simpleMoves:
                        self.otherSide(piece)['P' + str(i)].simpleMoves.append([previousPos[0], previousPos[1] + 1])
        self.moveChecker()

    def update(self):                      #Updates the board object
        self.possibleMoves()
        self.moveChecker()

board = Game()

board.update()

# board.move(board.white['P1'], [2,4])
# print(board.white['P1'].pawnAttackMoves)
# board.move(board.black['P4'], [3,4])

# print(board.white['P1'].simpleMoves)
# print(board.black['P4'].position)
# print(board.black['P4'].movesDone)
# print(board.white['K'].simpleMoves)
# board.move(board.white['K'], [3,6])
# board.update()
# print(board.white['K'].position)
# print(board.white['K'].movesDone)
# print(board.white['K'].simpleMoves)

# print(board.white['P1'].simpleMoves)
# #board.move(board.white[board.getPiece([0,1]).piece], [0,2])
# board.move(board.black['R1'], [1,3])
# board.update()
# print(board.white['P1'].position)
# print(board.white['P1'].simpleMoves)
