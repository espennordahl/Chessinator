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
		self.assertEquals(game.fen(), 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')

	def testFirstThreeMovesFEN(self):
		game = Game()
		
		game.applyMove(Move(Color.white, "e4"))
		self.assertEquals(game.fen(), 'rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1')
		
		game.applyMove(Move(Color.black, "c5"))
		self.assertEquals(game.fen(), 'rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq c6 0 2')
		
		game.applyMove(Move(Color.white, "Nf3"))
		self.assertEquals(game.fen(), 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2')


if __name__ == '__main__':
	unittest.main()
