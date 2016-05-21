import unittest

from chess import Game, Move, Color

class TestMoveLogic(unittest.TestCase):
	def setUp(self):
		self.game = Game()

	def testWhiteBasicMove(self):
		newMove = Move(Color.white, 'd4')
		self.assertTrue(newMove.isLegal())
		self.assertTrue(self.game.isMoveLegal(newMove))
		self.assertTrue(self.game.applyMove(newMove))
	
	def testWhiteMoveOutsideOfBoard(self):
		newMove = Move(Color.white, 'm4')
		self.assertFalse(newMove.isLegal())
		self.assertFalse(self.game.isMoveLegal(newMove))
		self.assertFalse(self.game.applyMove(newMove))

class TestGameState(unittest.TestCase):
	def testDefaultFEN(self):
		game = Game()
		self.assertEquals(game.fen(), 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR')
## 

if __name__ == '__main__':
	unittest.main()
