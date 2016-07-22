import unittest
from test import test_support
import subprocess

from chessberry import unittests as chessberrytests

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
		return

	def testFullGame(self):
		'''Run through complete Carlsen vs Anand game
		'''
		return

def test_main():
	test_support.run_unittest(	TestBasic,
								TestTwoPlayerGame
								)
	return

if __name__ == "__main__":
	'''Since this is the root module, we test all submodules successively
		in addition to the chessinator executable.'''
	chessberrytests.test_main()
	test_main()
