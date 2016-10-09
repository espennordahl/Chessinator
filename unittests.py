import unittest
from test import test_support
import subprocess

from chessberry import unittests as chessberrytests
from chessberry.game import *
from sensors import ReidSwitchSensor

class ChessTestCase(unittest.TestCase):
	''' Simple TestCase subclass to customize the output.
	'''
	def shortDescription(self):
		return None

class TestBasic(ChessTestCase):
	def testOpenAndClose(self):
		'''Start chessberry and close it immediately.
		'''
		self.assertEquals(subprocess.call(['python', 'chessinator.py', '-s', 'exit', '-ui','exit']), 0)
	
class TestTwoPlayerGame(ChessTestCase):
	def testSingleMove(self):
		'''Do one legal move, then close the program.
		'''		
		self.assertEquals(subprocess.call(['python', 'chessinator.py', '-s', 'singleMove', '-ui','dummy']), 0)

	def testIllegalMove(self):
		'''Do one illegal move, then close the program.
		'''
		return

	def testFirstThreeMoves(self):
		'''Do Three legal moves, then close the program.
		'''
		self.assertEquals(subprocess.call(['python', 'chessinator.py', '-s', 'threeMoves', '-ui','dummy']), 0)

	def testFullGame(self):
		'''Run through complete Carlsen vs Anand game
		'''
		return

class TestReidSwitchSensor(ChessTestCase):
	'''The reid switch sensor queries the reid switch mux in a loop,
		so we don't really have a public API to run clean unit tests
		with. For that reason, we're testing using private API directly.
		'''
	def testStartBoard(self):
		sensor = ReidSwitchSensor()
		binaryBoard = [	[1, 1, 1, 1, 1, 1, 1, 1],
						[1, 1, 1, 1, 1, 1, 1, 1],
						[0, 0, 0, 0, 0, 0, 0, 0],
						[0, 0, 0, 0, 0, 0, 0, 0],
						[0, 0, 0, 0, 0, 0, 0, 0],
						[0, 0, 0, 0, 0, 0, 0, 0],
						[1, 1, 1, 1, 1, 1, 1, 1],
						[1, 1, 1, 1, 1, 1, 1, 1]]

		sensor._newBinaryBoard(copy.copy(binaryBoard))

		self.assertEquals(sensor._binaryBoard, binaryBoard)
		
		game = Game()
		self.assertEquals(sensor._board, game._board)
		return

	def testSingleMove(self):
		sensor = ReidSwitchSensor()
		binaryBoard = [	[1, 1, 1, 1, 1, 1, 1, 1],
						[1, 1, 1, 1, 1, 1, 1, 1],
						[0, 0, 0, 0, 0, 0, 0, 0],
						[0, 0, 0, 0, 0, 0, 0, 0],
						[0, 0, 0, 0, 0, 0, 0, 0],
						[0, 0, 0, 0, 0, 0, 0, 0],
						[1, 1, 1, 1, 1, 1, 1, 1],
						[1, 1, 1, 1, 1, 1, 1, 1]]

		sensor._newBinaryBoard(copy.copy(binaryBoard))

		binaryBoard = [	[1, 1, 1, 1, 1, 1, 1, 1],
						[1, 1, 1, 1, 0, 1, 1, 1],
						[0, 0, 0, 0, 0, 0, 0, 0],
						[0, 0, 0, 0, 1, 0, 0, 0],
						[0, 0, 0, 0, 0, 0, 0, 0],
						[0, 0, 0, 0, 0, 0, 0, 0],
						[1, 1, 1, 1, 1, 1, 1, 1],
						[1, 1, 1, 1, 1, 1, 1, 1]]

		
		sensor._newBinaryBoard(copy.copy(binaryBoard))
		self.assertEquals(sensor._binaryBoard, copy.copy(binaryBoard))
		
		game = Game()
		game.applyMove(Move(Color.white, "e4"))
		self.assertEquals(sensor._board, game._board)
		return
		
	def testFirstThreeMoves(self):
		return

def test_main():
	test_support.run_unittest(	TestBasic,
								TestTwoPlayerGame,
								TestReidSwitchSensor,
								)
	return

if __name__ == "__main__":
	'''Since this is the root module, we test all submodules successively
		in addition to the chessinator executable.'''
	chessberrytests.test_main()
	test_main()
