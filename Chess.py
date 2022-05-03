import copy

class Piece():
    """Represents a Chess Piece"""
    def __init__(self, color, piece, pos):
        """Chess piece contains color, type of piece(pawn, king, etc.), Position on board, 
            moves done with this piece, and all possible moves.
        """
        self.color = color
        self.piece =  piece
        self.position = pos
        self.movesDone = 0
        self.possibleMoves = []         #2D array, containing a direction and all moves in that direction
        self.simpleMoves = []           #1D array, containing all moves possible
        self.pawnAttackMoves = []       #1D array, containing places where pawn can attack
        
    def simpleMoveMaker(self):
        """Takes all possible moves and turns them into a 1D array called simpleMoves"""
        moves = []
        for arr in self.possibleMoves:
            for direction in arr:
                if direction != []:
                    moves.append(direction)
        self.simpleMoves = moves
        return self

class Game:
    """Chess Game object. Contains two sides, and a winner. Instead of a Board with pieces on it,
        has all pieces from both sides and their positions"""
    def __init__(self):
        """Create both sides and all the Piece objects for each side"""
        self.black = {'R1':0, 'N1':0, 'B1':0, 'Q0':0, 'K0':0, 'B2':0, 'N2':0, 'R2':0,
             'P1':0, 'P2':0, 'P3':0, 'P4':0, 'P5':0, 'P6':0, 'P7':0, 'P8':0}

        self.white = {'R1':0, 'N1':0, 'B1':0, 'Q0':0, 'K0':0, 'B2':0, 'N2':0, 'R2':0,
             'P1':0, 'P2':0, 'P3':0, 'P4':0, 'P5':0, 'P6':0, 'P7':0, 'P8':0}
        
        self.winner = ''

        self.black['R1'] = Piece('black', 'R', [0,7])
        self.black['N1'] = Piece('black', 'N', [1,7])
        self.black['B1'] = Piece('black', 'B', [2,7])
        self.black['Q0']  = Piece('black', 'Q', [3,7])
        self.black['K0']  = Piece('black', 'K', [4,7])
        self.black['B2'] = Piece('black', 'B', [5,7])
        self.black['N2'] = Piece('black', 'N', [6,7])
        self.black['R2'] = Piece('black', 'R', [7,7])
        for i in range(1,9):
            self.black['P' + str(i)] = Piece('black', 'P', [i-1, 6])

        self.white['R1'] = Piece('white', 'R', [0,0])
        self.white['N1'] = Piece('white', 'N', [1,0])
        self.white['B1'] = Piece('white', 'B', [2,0])
        self.white['Q0']  = Piece('white', 'Q', [3,0])
        self.white['K0']  = Piece('white', 'K', [4,0])
        self.white['B2'] = Piece('white', 'B', [5,0])
        self.white['N2'] = Piece('white', 'N', [6,0])
        self.white['R2'] = Piece('white', 'R', [7,0])
        for i in range(1,9):
            self.white['P' + str(i)] = Piece('white', 'P', [i-1, 1])
        
        self.possibleMoves()
        
    def otherSide(self, piece: Piece):           
        """Returns dictionary of other team as passed piece
        :param piece: Piece object
        :return: dict[str, Piece] of the opposite side
        """
        if piece.color == 'black':
            return self.white
        if piece.color == 'white':
            return self.black
    
    def ownSide(self, piece: Piece):
        """Returns dictionary of same team as passed piece
        :param piece: Piece object
        :return: dict[str, Piece] of the opposite side
        """
        if piece.color == 'black':
            return self.black
        if piece.color == 'white':
            return self.white
            
    def allMoves(self, piece: Piece):             #Returns all standard moves for a piece, in a series of arrays
        """Places moves in all directions possible based on given piece
        :param piece: Piece object
        :return: Piece object"""

        if piece.piece[0]=='K':     #King moves in 8D, only 1 square
            x = piece.position[0]
            y = piece.position[1]
            piece.possibleMoves = [[[x + 1, y]], [[x-1,y]], [[x, y+1]], [[x, y-1]], [[x+1,y+1]], [[x+1, y-1]], [[x-1, y+1]], [[x-1, y-1]]]

        if piece.piece[0] == 'N':   #Knight moves in 8D, 2 sqaures along an axis and 1 along another
            x = piece.position[0]
            y = piece.position[1]
            piece.possibleMoves = [[[x + 2, y + 1]], [[x + 2, y - 1]], [[x - 2, y + 1]], [[x - 2, y - 1]], [[x + 1, y + 2]], [[x + 1, y - 2]], [[x - 1, y + 2]], [[x - 1, y - 2]]]

        if piece.piece[0]=='Q':     #Queen moves in 8D, Diagonal, Horizontal, or Vertical
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

        if piece.piece[0] == 'P':       #Pawns can move up to 2 squares on first move, and can move diagonally 1 square if enemy piece is there
            x = piece.position[0]
            y = piece.position[1]

            moves = []
            captures = []
            if piece.color == 'white':
                if self.getPiece([x, y+1]) == None:
                    moves.append([x, y +1])
                if piece.movesDone == 0 and self.getPiece([x, y+2]) == None and self.getPiece([x, y+1]) == None:
                    moves.append([x, y+2])
                for take in self.black.values():
                    if take.position == [x+1, y+1] or take.position == [x-1, y+1]:
                        captures.append(take.position)
                piece.pawnAttackMoves = [[x+1, y+1], [x-1, y+1]]
            if piece.color == 'black':
                if self.getPiece([x, y-1]) == None:
                    moves.append([x, y-1])
                if piece.movesDone == 0 and self.getPiece([x, y-2]) == None and self.getPiece([x, y-1]) == None:
                    moves.append([x, y-2])
                for take in self.white.values():
                    if take.position == [x+1, y-1] or take.position == [x-1, y-1]:
                        captures.append(take.position)
                piece.pawnAttackMoves = [[x+1, y-1], [x-1, y-1]]
            piece.possibleMoves = []
            for move in moves:      #Append normal moves and captures
                piece.possibleMoves.append([move])
            for move in captures:
                piece.possibleMoves.append([move])

        if piece.piece[0] == 'B':       #Bishops move in 4D, diagonally
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
        
        if piece.piece[0]=='R':         #Rooks move in 4D, Horizontal or Vertical
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

    def clean(self, piece: Piece):
        """Removes points outside of board from all directions of movement:
        :param piece: Piece object
        :return: Piece object"""
        for i in range(len(piece.possibleMoves)):
            direction = []
            for point in piece.possibleMoves[i]:
                if not (point[0]<0 or point[0]>7 or point[1]<0 or point[1]>7):
                    direction.append(point)
            piece.possibleMoves[i] = direction
        return piece

    def ownPiece(self, piece: Piece):             
        """Removes moves where own pieces are standing
        :param piece: Piece object
        :return: Piece object"""
        for direction in range(len(piece.possibleMoves)):
            moves = piece.possibleMoves[direction][:]
            if piece.color == 'black':
                for point in self.black.values():
                    if point.position in moves:
                        moves =  moves[0:moves.index(point.position)]       #If own piece in path, remove moves past the own piece, inclusive
            if piece.color == 'white':
                for point in self.white.values():
                    if point.position in moves:
                        moves =  moves[0:moves.index(point.position)]
            piece.possibleMoves[direction] = moves
        return piece
        
    def otherPiece(self, piece: Piece):
        """Removes moves past opponent pieces
        :param piece: Piece object
        :return: Piece object"""
        for direction in range(len(piece.possibleMoves)):
            moves = piece.possibleMoves[direction][:]
            if piece.color == 'black':
                for point in self.white.values():
                    if point.position in moves:
                        moves =  moves[0:moves.index(point.position)+1]     #If enemy piece in path, remove moves past the enemy piece
            if piece.color == 'white':
                for point in self.black.values():
                    if point.position in moves:
                        moves =  moves[0:moves.index(point.position)+1]
            piece.possibleMoves[direction] = moves
        return piece

    def isCheck(self, king: Piece, pos=False):
        """Returns whether king passed as param is in check. True if in check. Can also pass in a position to compare against, instead of king's position
        :param king: Piece
        :param pos: list
        :return: bool"""
        if pos != False:
            square = pos
        else:
            square = king.position
        for piece in self.otherSide(king).values():
            for move in piece.simpleMoves:
                if move == square:
                    return True
        return False                            

    def possibleMoves(self):               
        """Sets all valid moves to each piece"""
        for piece in self.white:
            self.otherPiece(self.ownPiece(self.clean(self.allMoves(self.white[piece]))))
            self.white[piece].simpleMoveMaker()         #Turns array of moves in each direction into array of moves
        for piece in self.black:
            self.otherPiece(self.ownPiece(self.clean(self.allMoves(self.black[piece]))))
            self.black[piece].simpleMoveMaker()

        #Setup Castling

        piece = 'R1'
        if self.white[piece].movesDone == 0 and self.white['K0'].movesDone == 0 and not self.isCheck(self.white['K0']): #If neither rook nor king have moved, and king would not pass through check, and king not in check
            if [3,0] in self.white[piece].simpleMoves and not self.isCheck(self.white['K0'], pos = [3,0]):
                self.white['K0'].simpleMoves.append([2,0])
        if self.black[piece].movesDone == 0 and self.black['K0'].movesDone == 0 and not self.isCheck(self.black['K0']): 
                    if [3,7] in self.black[piece].simpleMoves and not self.isCheck(self.black['K0'], pos = [3,7]):
                        self.black['K0'].simpleMoves.append([2,7])
                
        piece = "R2"
        if self.white[piece].movesDone == 0 and self.white['K0'].movesDone == 0 and not self.isCheck(self.white['K0']): 
            if [5,0] in self.white[piece].simpleMoves and not self.isCheck(self.white['K0'], pos = [5,0]):
                self.white['K0'].simpleMoves.append([6,0])
        if self.black[piece].movesDone == 0 and self.black['K0'].movesDone == 0 and not self.isCheck(self.black['K0']): 
                    if [5,7] in self.black[piece].simpleMoves and not self.isCheck(self.black['K0'], pos = [5,7]):
                        self.black['K0'].simpleMoves.append([6,7])
    
    def getPiece(self, position):          
        """Gets piece at a board position
        :param position: list
        :return: Piece or None"""
        for piece in self.black.values():
            if piece.position == position:
                return piece
        for piece in self.white.values():
            if piece.position == position:
                return piece
        return None
        
    def moveChecker(self, color):          
        """Removes moves that lead to own check of from options. Returns False if there are no possible moves for provided side
        :param color: str
        :return: bool""" 
        original = copy.deepcopy(self)
        possible = False
        if color == 'white':
            for piece in original.white:
                moves = []
                for move in original.white[piece].simpleMoves:
                    new = copy.deepcopy(original)
                    new.capture(new.white[piece],move)
                    new.possibleMoves()
                    if not new.isCheck(new.white['K0']):
                        moves.append(move)
                if moves!=[]:
                    possible = True
                self.white[piece].simpleMoves = moves
        else:
            for piece in original.black:
                moves = []
                for move in original.black[piece].simpleMoves:
                    new = copy.deepcopy(original)
                    new.capture(new.black[piece],move)
                    new.possibleMoves()
                    if not new.isCheck(new.black['K0']):
                        moves.append(move)
                    if moves!=[]:
                        possible = True
                self.black[piece].simpleMoves = moves
        return possible

    def capture(self, piece: Piece, move):
        """Moves Pieces and Captures if necessary
        :param piece: Piece
        :param move: list"""
        banish = [20,20]
        if self.getPiece(move) != None:
            self.getPiece(move).position = banish
        #En Passant
        elif piece.piece[0]=='P' :
            if move in piece.pawnAttackMoves and move in piece.simpleMoves:
                if piece.color == 'white':
                    self.getPiece([move[0],move[1]-1]).position = banish
                else:
                    self.getPiece([move[0],move[1]+1]).position = banish
        #Castling
        elif piece.piece[0] == 'K' and piece.movesDone == 0:
            if move == [2,0]:
                self.ownSide(piece)['R1'].position = [3,0]
                self.ownSide(piece)['R1'].movesDone +=1
            if move == [6,0]:
                self.ownSide(piece)['R2'].position = [5,0]
                self.ownSide(piece)['R2'].movesDone +=1
            if move == [2,7]:
                self.ownSide(piece)['R1'].position = [3,7]
                self.ownSide(piece)['R1'].movesDone +=1
            if move == [6,7]:
                self.ownSide(piece)['R2'].position = [5,7]
                self.ownSide(piece)['R2'].movesDone +=1
        piece.position = move       
        piece.movesDone += 1

    def move(self, piece: Piece, move):           
        """Moves a piece and updates board for next move. checks for checkmate or stalemate.
        :param piece: Piece
        :param move: list"""
        previousPos = piece.position
        self.capture(piece,move)
        self.possibleMoves()
        #add en passant moves
        if piece.piece[0] == 'P' and piece.movesDone == 1:
            if piece.color == 'black':
                for i in range(1,9):
                    #For every pawn on enemy side, if moving 1 square would place moved pawn in capture position, add that position to the enemy pawn
                    if [previousPos[0], previousPos[1] - 1] in self.otherSide(piece)['P' + str(i)].pawnAttackMoves and [previousPos[0], previousPos[1] - 1]:
                        self.otherSide(piece)['P' + str(i)].simpleMoves.append([previousPos[0], previousPos[1] - 1])
            if piece.color == 'white':
                for i in range(1,9):
                    if [previousPos[0], previousPos[1] + 1] in self.otherSide(piece)['P' + str(i)].pawnAttackMoves and [previousPos[0], previousPos[1] + 1]:
                        self.otherSide(piece)['P' + str(i)].simpleMoves.append([previousPos[0], previousPos[1] + 1])
                        
        if self.moveChecker(self.otherSide(piece)['K0'].color) == False:                  #Checks for end
            if self.isCheck(self.otherSide(piece)['K0']):
                self.winner = piece.color
            else:
                self.winner = 'stalemate'

    def promote(self, piece: Piece, value):
        """Promote a piece based on passed value
        :param piece: Piece
        :param value: str"""
        piece.piece = value



# -------------------------Testing------------------------------


# board = Game()

# #board.update()

# board.move(board.white['K'], [1,0])
# board.move(board.white['P2'], [9,9])
# board.move(board.white['P1'], [9,9])
# board.move(board.white['N1'], [9,9])
# board.move(board.white['B1'], [9,9])
# board.move(board.white['Q'], [9,9])
# board.move(board.white['R1'], [9,9])
# print(board.white['K'].simpleMoves)

# board.move(board.black['R1'], [0,0])
# board.move(board.black['R2'], [0,1])
# print(board.winner)
# print(board.white['K'].simpleMoves)
# print(board.black['R1'].simpleMoves)
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
