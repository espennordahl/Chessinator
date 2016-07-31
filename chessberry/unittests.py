import unittest
import sys
import os

from test import test_support

from game import *
from piece import *
from utils import *
from move import *
from board import *

class ChessTestCase(unittest.TestCase):
	''' Simple TestCase subclass to customize the output.
	'''
	def shortDescription(self):
		return None

class TestCoordinates(ChessTestCase):
	''' Coordinates are pretty straight forward, but we test pretty
		thoroughly since they are such a key part of the library.'''
	
	def shortDescription(self):
		return None

	def testPGNassignment(self):
		'''Tests legal assignment using pgn.'''
		coord = Coordinate(pgn="b2")
		self.assertEquals(coord.index, [1,1])
		self.assertEquals(coord.pgn, "b2")
		
	def testIndexAssignment(self):
		'''Tests legal assignment using indices.'''
		coord = Coordinate(index=[2,3])
		self.assertEquals(coord.index, [2,3])
		self.assertEquals(coord.pgn, "c4")

	def testBadIndices(self):
		'''Relatively exhaustive test of illegal ways to create a
			Coordinate object.'''
		self.assertRaises(Exception, Coordinate, pgn="y31")
		self.assertRaises(Exception, Coordinate, pgn="23")
		self.assertRaises(Exception, Coordinate, pgn="a0")
		self.assertRaises(Exception, Coordinate, pgn="u2")
		self.assertRaises(Exception, Coordinate, pgn=[2,3])
		self.assertRaises(Exception, Coordinate, index="a3")
		self.assertRaises(Exception, Coordinate, index=[8,2])
		self.assertRaises(Exception, Coordinate, index=[2,9])
		self.assertRaises(Exception, Coordinate, index=[2,2,3])
		self.assertRaises(Exception, Coordinate, index=30)

class TestMoves(ChessTestCase):
	'''Whether a move is legal or not is context sensitive, but moves
		can be created outside of a specific game or board state, so 
		we only fail if the move is strictly illegal in any game of chess
		(ie outside of the board), or for a given board state.'''
	def setUp(self):
		'''Just to avoid creating a new game object for every test.'''
		self.game = Game()

	def testWhiteBasicMove(self):
		newMove = Move(Color.white, 'd4')
		self.assertTrue(newMove.isLegal())
		self.assertTrue(self.game.isMoveLegal(newMove))
		self.assertTrue(self.game.applyMove(newMove))
		self.assertEquals(newMove.getToCoord().pgn, 'd4')
		self.assertEquals(newMove.getFromCoord().pgn, 'd2')
	
	def testWhiteMoveOutsideOfBoard(self):
		newMove = Move(Color.white, 'm4')
		self.assertFalse(newMove.isLegal())
		self.assertFalse(self.game.isMoveLegal(newMove))
		self.assertFalse(self.game.applyMove(newMove))
	
class TestGameState(ChessTestCase):
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

		fenFile = open(os.path.join(os.path.dirname(__file__),'game01.fen'))
		pgnFile = open(os.path.join(os.path.dirname(__file__),'game01.pgn'))

		moves = pgnGameToMoves(pgnFile.read())
		fen = []
		for line in fenFile:
			fen.append(line.strip())

		fenFile.close()
		pgnFile.close()

		i = 0
		for move in moves:
			self.assertTrue(move.isLegal(), 'Failed on Move ' + str(i+1) )
			self.assertTrue(game.isMoveLegal(move), 'Failed on Move ' + str(i+1) )
			self.assertTrue(game.applyMove(move), 'Failed on Move ' + str(i+1) )
			self.assertEquals(game.fen(), fen[i], 'Failed on Move ' + str(i+1) + ". Should be: \n" + repr(fen[i]) + ". Was: \n" + repr(game.fen()) )
			i += 1

def test_main():
	test_support.run_unittest(	TestCoordinates,
								TestMoves,
								TestGameState
								)

if __name__ == '__main__':
	test_main()
