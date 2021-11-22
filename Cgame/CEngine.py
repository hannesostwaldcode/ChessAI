

class GameState():
    def __init__(self):
        #Standard Starting Board 
        # Todo: Add load Fen string/Or Position Builder; Fisher Random Chess?
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["//", "//", "//", "//", "//", "//", "//", "//"],
            ["//", "//", "//", "//", "//", "//", "//", "//"],
            ["//", "//", "//", "//", "//", "//", "//", "//"],
            ["//", "//", "//", "//", "//", "//", "//", "//"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
        # self.board = [
        #       ["//", "//", "bK", "//", "//", "//", "//", "//"],
        #      ["//", "//", "//", "//", "//", "//", "//", "//"],
        #     ["wK", "//", "//", "//", "//", "//", "//", "//"],
        #     ["//", "//", "//", "wR", "//", "//", "//", "//"],
        #     ["//", "//", "//", "//", "//", "//", "//", "//"],
        #     ["//", "//", "//", "//", "//", "//", "//", "//"],
        #      ["//", "//", "//", "//", "//", "//", "//", "//"],
        #     ["//", "//", "bQ", "//", "//", "//", "//", "//"]]
        self.moveFunctions = {'P': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves,
                                'B': self.getBishopMoves,  'Q': self.getQueenMoves,  'K': self.getKingMoves,}

        self.whiteToMove = True
        self.moveLog = []
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        self.chekMate = False
        self.staleMate = False
        self.enpassantPossible = ()
        self.enpassantPossibleLog = [self.enpassantPossible]
        self.currentCastlingRight = CastleRights(True, True, True, True)
        self.castleRightLog = [CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks, self.currentCastlingRight.wqs, self.currentCastlingRight.bqs)]


    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "//"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        if move.pieceMoved == 'wK':
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == 'bK':
            self.blackKingLocation = (move.endRow, move.endCol)
        self.whiteToMove = not self.whiteToMove

        if move.isPawnPromotion:
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + 'Q'

        if move.isEnpassantMove:
            self.board[move.startRow][move.endCol] = '//'

        if move.pieceMoved[1] == 'P' and abs(move.startRow -move.endRow) == 2:
            self.enpassantPossible = ((move.startRow + move.endRow)//2, move.endCol)
        else:
            self.enpassantPossible = ()

        if move.isCastleMove:
            if move.endCol - move.startCol == 2:
                self.board[move.endRow][move.endCol-1] = self.board[move.endRow][move.endCol+1]
                self.board[move.endRow][move.endCol+1] = '//'
            else:
                self.board[move.endRow][move.endCol+1] = self.board[move.endRow][move.endCol-2]
                self.board[move.endRow][move.endCol-2] = '//'
        
        self.enpassantPossibleLog.append(self.enpassantPossible)

        self.updateCastleRights(move)
        self.castleRightLog.append(CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks,
                                self.currentCastlingRight.wqs,self.currentCastlingRight.bqs))

    def undoMove(self):
        if len(self.moveLog) >= 1:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            if move.pieceMoved == 'wK':
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == 'bK':
                self.blackKingLocation = (move.startRow, move.startCol)
            self.whiteToMove = not self.whiteToMove

            if move.isEnpassantMove:
                self.board[move.endRow][move.endCol] = '//'
                self.board[move.startRow][move.endCol] = move.pieceCaptured
              
            self.enpassantPossibleLog.pop()
            self.enpassantPossible = self.enpassantPossibleLog[-1]

            self.castleRightLog.pop()
            self.currentCastlingRight.wks = self.castleRightLog[-1].wks
            self.currentCastlingRight.wqs = self.castleRightLog[-1].wqs
            self.currentCastlingRight.bks = self.castleRightLog[-1].bks
            self.currentCastlingRight.bqs = self.castleRightLog[-1].bqs
            if move.isCastleMove:
                if move.endCol - move.startCol == 2:
                    self.board[move.endRow][move.endCol+1] = self.board[move.endRow][move.endCol-1]
                    self.board[move.endRow][move.endCol-1] = '//'
                else:
                    self.board[move.endRow][move.endCol-2] = self.board[move.endRow][move.endCol+1]
                    self.board[move.endRow][move.endCol+1] = '//'

            self.chekMate = False
            self.staleMate = False

            
    #Checks weather the given Move changes the Castle Rights for Both sides
    def updateCastleRights(self, move):
       
        if move.pieceMoved == 'wK':
            self.currentCastlingRight.wks = False
            self.currentCastlingRight.wqs = False
        elif move.pieceMoved == 'bK':
            self.currentCastlingRight.bks = False
            self.currentCastlingRight.bqs = False    
        elif move.pieceMoved == 'wR':
            if move.startRow == 7:
                if move.startCol == 0:
                    self.currentCastlingRight.wqs = False
                elif move.startCol == 7:
                    self.currentCastlingRight.wks = False
        elif move.pieceMoved == 'bR':
            if move.startRow == 0:
                if move.startCol == 0:
                    self.currentCastlingRight.bqs = False
                elif move.startCol == 7:
                    self.currentCastlingRight.bks = False
        if move.pieceCaptured == 'wR':
            if move.endRow == 7:
                if move.endCol == 0:
                    self.currentCastlingRight.wqs == False
                elif move.endCol == 7:
                    self.currentCastlingRight.wks = False
        elif move.pieceCaptured == 'bR':
            if move.endRow == 0:
                if move.endCol == 0:
                    self.currentCastlingRight.bqs = False
                elif move.endCol == 7:
                    self.currentCastlingRight.bks = False
       
    #Checks a list of all Theoratical Moves for their legality
    def getValidMoves(self):
        tempEnpassantPossible = self.enpassantPossible
        tempCastleRights = CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks, 
                                        self.currentCastlingRight.wqs, self.currentCastlingRight.bqs)
        moves = self.getAllPossibleMoves()
        if self.whiteToMove:
            self.getCastleMoves(self.whiteKingLocation[0], self.whiteKingLocation[1], moves) 
        else:
            self.getCastleMoves(self.blackKingLocation[0], self.blackKingLocation[1], moves) 
        for i in range(len(moves)-1, -1, -1):
            self.makeMove(moves[i])
            self.whiteToMove = not self.whiteToMove
            if self.inCheck():
                moves.remove(moves[i])
            self.whiteToMove = not self.whiteToMove
            self.undoMove()
        
        if len(moves) == 0:
            if self.inCheck():
                self.chekMate = True
            else:
                self.staleMate = True
        else:
            self.chekMate = False
            self.staleMate = False

        self.enpassantPossible = tempEnpassantPossible
        self.currentCastlingRight = tempCastleRights
        return moves

    #Legal Move Checker Helpers
    def inCheck(self):
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])

    #Checks if an opponents piece can reach the Square in Question
    def squareUnderAttack(self, r, c):
        self.whiteToMove = not self.whiteToMove
        oppMoves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove
        for move in oppMoves:
            if move.endRow == r and move.endCol == c:
                 return True

        return False
        
    #Gets all Moves possible only by Piece Move patterns
    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):
         for c in range(len(self.board[r])):
             turn = self.board[r][c][0]
             if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                 piece = self.board[r][c][1]
                 self.moveFunctions[piece](r, c, moves)
        return moves
    #Piece Movement Methods
    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove:
            if self.board[r-1][c] == "//":
                moves.append(Move((r,c), (r-1,c), self.board))
                if r == 6 and self.board[r-2][c] == "//":
                    moves.append(Move((r,c), (r-2,c), self.board))
            if c-1 >= 0:
                if self.board[r-1][c-1][0] == 'b':
                    moves.append(Move((r,c), (r-1,c-1), self.board))
                elif (r-1, c-1) == self.enpassantPossible:
                    moves.append(Move((r,c), (r-1,c-1), self.board, isEnpassantMove = True))

            if c+1 <= 7:
                if self.board[r-1][c+1][0] == 'b':
                    moves.append(Move((r,c), (r-1,c+1), self.board))
                elif (r-1, c+1) == self.enpassantPossible:
                    moves.append(Move((r,c), (r-1,c+1), self.board, isEnpassantMove = True))
        else:
            if self.board[r+1][c] == "//":
                moves.append(Move((r,c), (r+1,c), self.board))
                if r == 1 and self.board[r+2][c] == "//":
                    moves.append(Move((r,c), (r+2,c), self.board))
            if c-1 >= 0:
                if self.board[r+1][c-1][0] == 'w':
                    moves.append(Move((r,c), (r+1,c-1), self.board))
                elif (r+1, c-1) == self.enpassantPossible:
                    moves.append(Move((r,c), (r+1,c-1), self.board, isEnpassantMove = True))
            if c+1 <= 7:
                if self.board[r+1][c+1][0] == 'w':
                    moves.append(Move((r,c), (r+1,c+1), self.board))
                elif (r+-1, c+1) == self.enpassantPossible:
                    moves.append(Move((r,c), (r+1,c+1), self.board, isEnpassantMove = True))

    def getRookMoves(self, r, c, moves):
        #Move Straight +/- on one of the values / check for pieces hit or border hit
        directions = ((1, 0), (-1, 0), (0, -1), (0, 1))
        enemyColor = 'b' if self.whiteToMove else 'w'

        for d in directions:
            for x in range(1,8):
                endRow = r + d[0]*x
                endCol = c + d[1]*x
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "//":
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else:
                    break

    def getKnightMoves(self, r, c, moves):
        #validate for the squares themselves, knight doesnt care about pieces in its way
        directions = ((2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, -2), (-1, 2))
        enemyColor = 'b' if self.whiteToMove else 'w'

        for d in directions:
                endRow = r + d[0]
                endCol = c + d[1]
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "//":
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        
    def getBishopMoves(self, r, c, moves):
        #Move Diagonal + and - on each combination detemins the direction -- = left upper corner ++ right lower corner +- left lower -+ right upper / check for pieces hit or border hit
        directions = ((1, 1), (-1, -1), (1, -1), (-1, 1))
        enemyColor = 'b' if self.whiteToMove else 'w'

        for d in directions:
            for x in range(1,8):
                endRow = r + d[0]*x
                endCol = c + d[1]*x
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "//":
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else:
                    break
 
    def getQueenMoves(self, r, c, moves):
        #Rook + Bishop
        self.getBishopMoves(r, c, moves)
        self.getRookMoves(r, c, moves)

    def getKingMoves(self, r, c, moves):
        enemyColor = 'b' if self.whiteToMove else 'w'
        #8 Squares surounding it 
        #(1 0, -1 0, 1 0, -1 0, 0 1, 1- 1, 1 -1, 1 1, -1 -1)
        for x in range(-1,2):
            for y in range(-1,2):
                
                endRow = r + x
                endCol = c + y
                if 0 <= endRow < 8 and 0 <= endCol < 8 and not(r == 0 and c == 0):
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "//":
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                     
    #Casteling Generator and Helpers
    def getCastleMoves(self, r, c, moves):
        if self.squareUnderAttack(r, c):
            return
        if (self.whiteToMove and self.currentCastlingRight.wks) or (not self.whiteToMove and self.currentCastlingRight.bks):
            self.getKingsideCastleMoves(r, c, moves)
        if (self.whiteToMove and self.currentCastlingRight.wqs) or (not self.whiteToMove and self.currentCastlingRight.bqs):
            self.getQueensideCastleMoves(r, c, moves)
   
   
    #Helper for Castlinhg Moves
    def getKingsideCastleMoves(self, r, c, moves):
        if self.board[r][c+1] == '//' and self.board[r][c+2] == '//':
            if not self.squareUnderAttack(r, c+1) and not self.squareUnderAttack(r, c+2):
                moves.append(Move((r, c), (r, c+2), self.board, isCastleMove=True))

    def getQueensideCastleMoves(self, r, c, moves):
         if self.board[r][c-1] == '//' and self.board[r][c-2] == '//' and self.board[r][c-3] == '//':
            if not self.squareUnderAttack(r, c-1) and not self.squareUnderAttack(r, c-2):
                moves.append(Move((r, c), (r, c-2), self.board, isCastleMove=True))



class CastleRights():
    def __init__(self, wks, bks, wqs, bqs):
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs 
        

class Move():
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, 
                    "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a" : 0, "b": 1, "c" : 2, "d" : 3, 
                    "e" : 4, "f" : 5, "g" : 6, "h" : 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board, isEnpassantMove=False, isCastleMove=False):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.isPawnPromotion = (self.pieceMoved == 'wP' and self.endRow == 0) or (self.pieceMoved == 'bP' and self.endRow == 7)
        self.isEnpassantMove = isEnpassantMove
        if self.isEnpassantMove:
            self.pieceCaptured = 'wP' if self.pieceMoved == 'bP' else 'bP'
        self.isCapture = self.pieceCaptured != "//"
        self.isCastleMove = isCastleMove    
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False
        # Chess Notation Piece + x if it captures + Destination. Pawns dont get a letter but their File Name 
    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]

    #Generate Chess Notation String from self
    def __str__(self):
        if self.isCastleMove:
            return "O-O" if self.endCol == 6 else "O-O-O"
        
        endSquare = self.getRankFile(self.endRow, self.endCol)
        if self.pieceMoved[1] == 'P':
            if self.isCapture:
                return self.colsToFiles[self.startCol] + "x" + endSquare
            else:
                return endSquare
        
            # Pawn Promotions

        movestring = self.pieceMoved[1]
        if self.isCapture:
            movestring += 'x'
        return movestring + endSquare