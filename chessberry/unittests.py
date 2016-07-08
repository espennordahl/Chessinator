import unittest

from chess import Game, Move, Color, pgnGameToMoves

## TODO:
## - pawn takes
## - any takes
## - castle
## - move legality pawns
## - move legality queen
## - move legality king
## - move legality rook
## - move legality bishop
## - system event loop

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
	
	def testPawnMoves(self):
		legalMove = Move(Color.white, 'a4')
		self.assertTrue(self.game.isMoveLegal(legalMove))	

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

	def testFullGameAnandVsCarlsenFEN(self):
		game = Game()

		fenFile = open('game01.fen')
		pgnFile = open('game01.pgn')

		moves = pgnGameToMoves(pgnFile.read())
		fen = []
		for line in fenFile:
			fen.append(line.strip())

		fenFile.close()
		pgnFile.close()

		i = 0
		for move in moves:
			self.assertTrue(move.isLegal())
			self.assertTrue(game.isMoveLegal(move))
			self.assertTrue(game.applyMove(move))
			self.assertEquals(game.fen(), fen[i], 'Failed on Move ' + str(i+1) + ". Should be: \n" + repr(fen[i]) + ". Was: \n" + repr(game.fen()) )
			i += 1

if __name__ == '__main__':
	unittest.main()
