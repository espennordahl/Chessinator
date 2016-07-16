

from utils import *
from piece import *

class Move():
	def __init__(self, color, pgnMove):
		self._pgn = pgnMove
		self._color = color
		self._toRank = None
		self._fromRank = None
		self._toLetter = None
		self._fromLetter = None

	def conformMove(self, board):
		if len(self._pgn) == 2:
			self._conformPawnMove(board)
		elif len(self._pgn) == 3:
			## normal piece move
			self._toRank = int(self._pgn[2]) - 1
			self._toLetter = letterToIndex(self._pgn[1])
			if self._pgn[0] == "N":
				self._conformKnightMove(board)
			elif self._pgn[0] == "B":
				self._conformBishopMove(board)
		else:
			raise Exception("Unsupported pgn length: " + self._pgn) 


	def _conformPawnMove(self, board):
		self._toRank = int(self._pgn[1]) - 1
		self._toLetter = letterToIndex(self._pgn[0])
		if self._toRank == 3:
			self._fromRank = 1
		elif self._toRank == 4:
			self._fromRank = 6
		else:
			if self._color == Color.white:
				self._fromRank = self._toRank - 1
			else:
				self._fromRank = self._toRank + 1
		self._fromLetter = self._toLetter
		
	def _conformKnightMove(self, board):
		shortestDistance = 99
		candidateIndices = None
		rankIndex = 0
		for rank in board:
			letterIndex = 0
			for square in rank:
				if square != None and square.color() == self._color and square.type() == Type.knight:
					##TODO: naive distance metric. Should be improved
					distance = abs(rankIndex - self._toRank) + abs(letterIndex - self._toLetter)
					if distance < shortestDistance:
						candidateIndices = (rankIndex, letterIndex)
				letterIndex += 1
			rankIndex += 1

		if candidateIndices == None:
			raise Exception("Couldnt find candidate piece for move.")
		else:
			self._fromRank = candidateIndices[0]
			self._fromLetter = candidateIndices[1]
	
	def _conformBishopMove(self, board):
		## search along diagonal
		return
		
	def isLegal(self):
		if not self._checkPGN():
			return False
		
		if not self._checkColor():
			return False
		
		return True

	def toRank(self):
		if self._toRank == None:
			raise Exception ("move not conformed yet. PGN: " + self._pgn)
		return self._toRank

	def fromRank(self):
		if self._fromRank == None:
			raise Exception ("move not conformed yet. PGN: " + self._pgn)
		return self._fromRank

	def toLetter(self):
		if self._toLetter == None:
			raise Exception ("move not conformed yet. PGN: " + self._pgn)
		return self._toLetter

	def fromLetter(self):
		if self._toLetter == None:
			raise Exception ("move not conformed yet. PGN: " + self._pgn)
		return self._fromLetter

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

