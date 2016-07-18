

from utils import *
from piece import *
from board import *

class Move():
	def __init__(self, color, pgnMove):
		self._pgn = pgnMove
		self._color = color
		self._fromCoord = None
		self._toCoord = None

	def conformMove(self, board):
		if len(self._pgn) == 2:
			## pawn move
			self._conformPawnMove(board)
		elif len(self._pgn) == 3:
			## normal piece move
			toRank = int(self._pgn[2]) - 1
			toLetter = letterToIndex(self._pgn[1])
			self._toCoord = Coordainte(index=[toRank, toLetter])
			if self._pgn[0] == "N":
				self._conformKnightMove(board)
			elif self._pgn[0] == "B":
				self._conformBishopMove(board)
			else:
				raise Exception("Unsupported piece type in pgn: " + self._pgn)
		else:
			raise Exception("Unsupported pgn length: " + self._pgn) 

	def _conformPawnMove(self, board):
		toRank = int(self._pgn[1]) - 1
		toLetter = letterToIndex(self._pgn[0])
		if toRank == 3:
			fromRank = 1
		elif toRank == 4:
			fromRank = 6
		else:
			if self._color == Color.white:
				fromRank = toRank - 1
			else:
				fromRank = toRank + 1
		fromLetter = toLetter
		self._toCoord = Coordinate(index = [toRank, toLetter])
		self._fromCoord = Coordinate(index = [fromRank, fromLetter])
		
	def _conformKnightMove(self, board):
		knightSquares = board.getSquares(type = Type.knight, color = self._color)
		for square in knightSquares:
			if square.piece.canMove(square.coord, self._toCoord):
				self._fromCoord = square.coordinate

		if  self._fromCoord == None:
			raise Exception("Couldnt find candidate piece for move.")
	
	def _conformBishopMove(self, board):
		return
		
	def isLegal(self):
		if not self._checkPGN():
			return False
		
		if not self._checkColor():
			return False
		
		return True

	def getToCoord(self):
		if self._toCoord == None:
			raise Exception ("move not conformed yet. PGN: " + self._pgn)
		return self._toCoord

	def getFromCoord(self):
		if self._fromCoord == None:
			raise Exception ("move not conformed yet. PGN: " + self._pgn)
		return self._fromCoord

	def _checkPGN(self):
		if not isinstance(self._pgn, basestring):
			return False
		
		if len(self._pgn) < 2 or len(self._pgn) > 4:
			return False

		if len(self._pgn) == 2:
			if self._pgn[0] not in ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'):
				return False

			if self._pgn[1] not in ('1', '2', '3', '4', '5', '6', '7', '8'):
				return False
		
		return True

	def _checkColor(self):
		if not isinstance(self._color, Color):
			return False

		return True

def pgnGameToMoves(pgn):
	elements = pgn.split(' ')
	moves = []
	currentPlayer = Color.white
	for element in elements:
		if element[0] not in '1234567890':
			moves.append(Move(currentPlayer, element.strip()))
			if currentPlayer == Color.white:
				currentPlayer = Color.black
			else:
				currentPlayer = Color.white

	return moves

