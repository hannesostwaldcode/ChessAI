import unittest
from Cgame import MoveAI, CEngine

class TestScoreBoard(unittest.TestCase):

    def setUp(self):
        self.gs = CEngine.GameState()
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

    #Find Mate

    #Find Stalemate

if __name__ == '__main__':
    unittest.main()