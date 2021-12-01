import unittest
import random
from Cgame import MoveAI, CEngine 


class TestScoreBoard(unittest.TestCase):

    def setUp(self):
        self.gs = CEngine.GameState()
        self.gsstandard = CEngine.GameState()
    def test_scoreboard(self):
        emptyboard = [
            ["//", "//", "//", "//", "//", "//", "//", "//"],
            ["//", "//", "//", "//", "//", "//", "//", "//"],
            ["//", "//", "//", "//", "//", "//", "//", "//"],
            ["//", "//", "//", "//", "//", "//", "//", "//"],
            ["//", "//", "//", "//", "//", "//", "//", "//"],
            ["//", "//", "//", "//", "//", "//", "//", "//"],
            ["//", "//", "//", "//", "//", "//", "//", "//"],
            ["//", "//", "//", "//", "//", "//", "//", "//"]]
        onlyWhiteboard = [
            ["//", "//", "//", "//", "//", "//", "//", "//"],
            ["//", "//", "//", "//", "//", "//", "//", "//"],
            ["//", "//", "//", "//", "//", "//", "//", "//"],
            ["//", "//", "//", "//", "//", "//", "//", "//"],
            ["//", "//", "//", "//", "//", "//", "//", "//"],
            ["//", "//", "//", "//", "//", "//", "//", "//"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
        startboard = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["//", "//", "//", "//", "//", "//", "//", "//"],
            ["//", "//", "//", "//", "//", "//", "//", "//"],
            ["//", "//", "//", "//", "//", "//", "//", "//"],
            ["//", "//", "//", "//", "//", "//", "//", "//"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
        
        #Test for Material Values
        self.assertEqual(MoveAI.scoreMaterial(startboard), 0, "should be 0")
        self.assertEqual(MoveAI.scoreMaterial(emptyboard), 0, "should be 0")
        self.assertEqual(MoveAI.scoreMaterial(onlyWhiteboard), 39, "should be 31")
    def test_getValidMoves(self):
        validMoves = self.gs.getValidMoves()
        self.assertEqual(len(validMoves), 20, "On move one there are 20 legal Moves")

    def test_makeUndoMove(self):
        validMoves = self.gs.getValidMoves()
        self.gs.makeMove(validMoves[random.randint(0, len(validMoves)-1)])
        self.gs.undoMove()
        self.assertEqual(self.gs.board, self.gsstandard.board, "Making and Undoing a move shouldnt change anything")

    def test_insertFen(self):
        twoKingBoard = [
            ["//", "//", "//", "//", "//", "//", "//", "//"],
            ["//", "//", "//", "//", "//", "//", "//", "//"],
            ["//", "//", "//", "//", "//", "//", "//", "//"],
            ["//", "//", "bK", "//", "//", "//", "//", "//"],
            ["//", "//", "//", "//", "wK", "//", "//", "//"],
            ["//", "//", "//", "//", "//", "//", "//", "//"],
            ["//", "//", "//", "//", "//", "//", "//", "//"],
            ["//", "//", "//", "//", "//", "//", "//", "//"]]
        self.gs.LoadFenString("8/8/8/2k5/4K3/8/8/8 w - - 0 1")
        self.assertEqual(self.gs.board, twoKingBoard, "FenString should load correctly")
        self.assertEqual((self.gs.currentCastlingRight.wks, self.gs.currentCastlingRight.wqs , self.gs.currentCastlingRight.bks, self.gs.currentCastlingRight.bqs),
                        (False, False, False, False), "Castle Rights")
        self.assertEqual(self.gs.whiteKingLocation, (4, 4), "WK location")


    #Find Mate
    def test_checkMate(self):
        self.gs.LoadFenString("3R2k1/5ppp/8/8/8/8/6K1/8 b - - 0 1")
        self.gs.getValidMoves()
        self.assertEqual(self.gs.chekMate, True, "Checkmate not True")

    #Find Stalemate
    def test_staleMate(self):
        self.gs.LoadFenString("4k3/4P3/4K3/8/8/8/8/8 b - - 0 1")
        self.gs.getValidMoves()
        self.assertEqual(self.gs.staleMate, True, "Stalemate not True")

if __name__ == '__main__':
    unittest.main()