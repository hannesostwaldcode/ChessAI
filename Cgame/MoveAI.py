
import random
from typing import Counter

#Chess Piece Values
pieceValue = {"K": 0, "Q": 9, "R": 5, "B": 3, "N": 3, "P": 1}
#Positional Values to help the AI score Moves based on positional attributes
knightScores = [[1, 1, 1, 1, 1, 1, 1, 1],
                [1, 2, 2, 2, 2, 2, 2, 1],
                [1, 2, 3, 3, 3, 3, 2, 1],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [1, 2, 3, 3, 3, 3, 2, 1],
                [1, 2, 2, 2, 2, 2, 2, 1],
                [1, 1, 1, 1, 1, 1, 1, 1]]

bishopScores = [[4,3, 2, 1, 1, 2, 3, 4],
                [3, 4, 3, 2, 2, 3, 4, 3],
                [2, 3, 4, 3, 3, 4, 3, 2],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [2, 3, 4, 3, 3, 4, 3, 2],
                [3, 4, 3, 2, 2, 3, 4, 3],
                [4, 3, 2, 1, 1, 2, 3, 4]]

queenScores = [[1, 1, 1, 3, 1, 1, 1, 1],
                [1, 2, 2, 3, 3, 2, 2, 1],
                [1, 4, 3, 3, 3, 4, 2, 1],
                [1, 2, 3, 3, 3, 2, 2, 1],
                [1, 2, 3, 3, 3, 2, 2, 1],
                [1, 4, 3, 3, 3, 4, 2, 1],
                [1, 2, 2, 3, 3, 2, 2, 1],
                [1, 1, 1, 3, 1, 1, 1, 1]]

rookScores = [[4, 3, 4, 4, 4, 4, 3, 4],
                [4, 4, 4, 4, 4, 4, 4, 4],
                [1, 1, 2, 3, 3, 2, 1, 1],
                [1, 2, 3, 4, 4, 2, 2, 1],
                [1, 2, 3, 4, 4, 2, 2, 1],
                [1, 1, 2, 3, 3, 2, 1, 1],
                [4, 4, 4, 4, 4, 4, 4, 4],
                [4, 3, 4, 4, 4, 4, 3, 4]]

whitePawnScores = [[8, 8, 8, 8, 8, 8, 8, 8],
                [8, 8, 8, 8, 8, 8, 8 ,8],
                [5, 6, 6, 7, 7, 6, 6, 5],
                [3, 3, 3, 5, 5, 3, 3, 2],
                [2, 3, 3, 4, 4, 3, 2, 1],
                [2, 2, 2, 3, 3, 1, 1, 1],
                [1, 1, 1, 0, 0, 1, 1, 1],
                [0, 0, 0, 0, 0, 0, 0, 0]]
                
blackPawnScores = [[0, 0, 0, 0, 0, 0, 0, 0],
                [1, 1, 1, 0, 0, 1, 1, 1],
                [2, 2, 2, 3, 3, 1, 1, 1],
                [2, 3, 3, 4, 4, 3, 2, 1],
                [3, 3, 3, 5, 5, 3, 3, 2],
                [5, 6, 6, 7, 7, 6, 6, 5],
                [8, 8, 8, 8, 8, 8, 8, 8],
                [8, 8, 8, 8, 8, 8, 8 ,8]]


piecePositionScores = {"N": knightScores, "R" : rookScores, "Q": queenScores, "B": bishopScores, "wP": whitePawnScores, 
                        "bP": blackPawnScores}

CHECKMATE = 1000
STALEMATE = 0
DEPTH = 3
def findRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves)-1)]


#Helper That starts the recoursion of the currently used Algorithm
def findBestMove(gs, validMoves, retrunQueue=None):
    global nextMove, runs
    nextMove = None
    random.shuffle(validMoves)
    runs = 0
    findMoveNegMax(gs, validMoves, DEPTH, -CHECKMATE, CHECKMATE, 1 if gs.whiteToMove else -1)
    #findMoveMinMax(gs, validMoves, DEPTH,  gs.whiteToMove)
    #pvs(gs, validMoves, DEPTH, -CHECKMATE,  CHECKMATE, 1 if gs.whiteToMove else -1)
    print(runs)
    if retrunQueue != None:
        retrunQueue.put(nextMove)
    else:
        return nextMove

#NegMax with Alpha/Beta Prunning - Active
def findMoveNegMax(gs, validMoves, depth, alpha, beta, turnMultiplier):
    global nextMove, runs
    runs += 1
    if depth == 0:
        return turnMultiplier * scoreBoard(gs)

    maxScore = -CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegMax(gs, nextMoves, depth-1, -beta, -alpha, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
                print(move, score)
        gs.undoMove()
        if maxScore > alpha:
            alpha = maxScore
        if alpha >= beta:
            break
    return maxScore

def pvs(gs, validMoves, depth, α, β, turnMultiplier):
    global nextMove, runs
    runs += 1
    if depth == 0:
        return turnMultiplier * scoreBoard(gs)
    maxScore = -CHECKMATE
    for index, move in enumerate(validMoves):
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        if index == 0:
            score = -pvs(gs, nextMoves, depth - 1, -β, -α, -turnMultiplier)
        else:
            score = -pvs(gs, nextMoves, depth - 1, -α - 1, -α, -turnMultiplier) 
            if α < score < β:
                score = -pvs(gs, nextMoves, depth - 1, -β, -score, -turnMultiplier)
        α = max(α, score)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
                print(move, score)
        gs.undoMove()
        if α >= β:
            break
    return α
#Scores The Position based on Material and Position(Basic)
def scoreBoard(gs):
    if gs.chekMate:
        if gs.whiteToMove:
            return CHECKMATE
        else:
            return -CHECKMATE
    elif gs.staleMate:
        return STALEMATE

    score = 0
    for row in range(len(gs.board)):
        for col in range(len(gs.board[row])):
            square = gs.board[row][col]
            if square != "//":

                piecePositionScore = 0
                if square[1] != "K":
                    if square[1] == "P":
                        piecePositionScore = piecePositionScores[square][row][col]
                    else:    
                        piecePositionScore = piecePositionScores[square[1]][row][col]

                if square[0] == 'w':
                    score += pieceValue[square[1]] + piecePositionScore * .1
                elif square[0] == 'b':
                    score -= pieceValue[square[1]] - piecePositionScore * .1

    return score






#Simple Scoring / inactive
def scoreMaterial(board):
    score = 0
    for row in board:
        for sqaure in row:
            if sqaure[0] == 'w':
                score += pieceValue[sqaure[1]]
            elif sqaure[0] == 'b':
                score -= pieceValue[sqaure[1]]

    return score

#Old Function/Algorithm / inactive
def findBestMoves(gs, validMoves):
    turnMultiplier = 1 if gs.whiteToMove else -1
    opponentMinMaxScore = CHECKMATE
    bestPlayerMove = None
    random.shuffle(validMoves)
    for playerMove in validMoves:
        gs.makeMove(playerMove)
        opponentsMoves = gs.getValidMoves()
        if gs.staleMate:
            opponentsMaxScore = STALEMATE
        elif gs.chekMate:
               opponentsMaxScore = -CHECKMATE
        else:
            opponentsMaxScore = -CHECKMATE
            for opponentsMove in opponentsMoves:
                gs.makeMove(opponentsMove)
                gs.getValidMoves()
                if gs.chekMate:
                    score = CHECKMATE
                elif gs.staleMate:
                    score = STALEMATE
                else:
                    score = -turnMultiplier * scoreMaterial(gs.board)
                if score > opponentsMaxScore:
                    opponentsMaxScore = score
                gs.undoMove()
            
        if opponentsMaxScore < opponentMinMaxScore:
            opponentMinMaxScore = opponentsMaxScore
            bestPlayerMove = playerMove
        gs.undoMove()
    return bestPlayerMove

#MinMaxAlgorithm / inactive
def findMoveMinMax(gs, validMoves, depth,  whiteToMove):
    global nextMove, runs
    runs += 1
    if depth == 0:
        return scoreBoard(gs)
    if whiteToMove:
        maxScore = -CHECKMATE
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = findMoveMinMax(gs, nextMoves, depth -1, False)
            if score > maxScore:
                maxScore = score
                if depth == DEPTH:
                    nextMoves = move
            gs.undoMove()
        return maxScore
    else:
        minScore = CHECKMATE
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = findMoveMinMax(gs, nextMoves, depth -1, True)
            if score < minScore:
                 minScore = score
                 if depth == DEPTH:
                    nextMoves = move
            gs.undoMove()
        return minScore
