from enum import Enum
import logging

from utils import *

class Type(Enum):
	pawn = 0
	knight = 1
	bishop = 2
	rook = 3
	queen = 4
	king = 5

def makePiece(fenstring):
	logger = logging.getLogger('Piece')
	color = Color.white
	if fenstring.islower():
		color = Color.black
	lowerFenstring = fenstring.lower()
	if lowerFenstring == "p":
		logging.debug('Creating piece: %s %s', color, 'Pawn')
		return Pawn(color)
	elif lowerFenstring == "n":
		logging.debug('Creating piece: %s %s', color, 'Pawn')
		return Knight(color)
	elif lowerFenstring == "b":
		logging.debug('Creating piece: %s %s', color, 'Pawn')
		return Bishop(color)
	elif lowerFenstring == "r":
		logging.debug('Creating piece: %s %s', color, 'Pawn')
		return Rook(color)
	elif lowerFenstring == "q":
		logging.debug('Creating piece: %s %s', color, 'Pawn')
		return Queen(color)
	elif lowerFenstring == "k":
		logging.debug('Creating piece: %s %s', color, 'Pawn')
		return King(color)

class Piece():
	def __init__(self, color):
		self._logger = logging.getLogger('Piece')
		self._color = color
	
	def type(self):
		raise Exception("Called abstract class method.")
		return None
	
	def color(self):
		return self._color

	def canMove(self, fromCoord, toCoord, obstacles, takes=False):
		raise Exception("Called abstract class method.")
		return False
	
	def __eq__(self, other):
		if self.type() != other.type():
			return False
		if self.color() != other.color():
			return False
		return True

class Pawn(Piece):
	def type(self):
		return Type.pawn

	def fen(self):
		if self.color() == Color.black:
			return "p"
		else:
			return "P"
	
	def canMove(self, fromCoord, toCoord, obstacles, takes=False):
		xDist = abs(fromCoord.index[0] - toCoord.index[0])
		yDiff = fromCoord.index[1] - toCoord.index[1]
		
		if self.color() == Color.white:
			yDiff *= -1
		
		if not takes:
			if yDiff == 1 and xDist == 0:
				return True

			if yDiff == 2 and xDist == 0:
				if self.color() == Color.white:
					if fromCoord.index[1] == 1:
						return True
				else:
					if fromCoord.index[1] == 6:
						return True
		else:
			return yDiff == 1 and xDist == 1


class Knight(Piece):
	def type(self):
		return Type.knight

	def fen(self):
		if self.color() == Color.black:
			return "n"
		else:
			return "N"

	def canMove(self, fromCoord, toCoord, obstacles, takes=False):
		xDist = abs(fromCoord.index[0] - toCoord.index[0])
		yDist = abs(fromCoord.index[1] - toCoord.index[1])

		if xDist == 1 and yDist == 2:
			return True

		if xDist == 2 and yDist == 1:
			return True

		return False

class Bishop(Piece):
	def type(self):
		return Type.bishop

	def fen(self):
		if self.color() == Color.black:
			return "b"
		else:
			return "B"
	
	def canMove(self, fromCoord, toCoord, obstacles, takes=False):
		xDist = abs(fromCoord.index[0] - toCoord.index[0])
		yDist = abs(fromCoord.index[1] - toCoord.index[1])

		return xDist == yDist

class Rook(Piece):
	def type(self):
		return Type.rook

	def fen(self):
		if self.color() == Color.black:
			return "r"
		else:
			return "R"
		
	def canMove(self, fromCoord, toCoord, obstacles, takes=False):
		xDist = abs(fromCoord.index[0] - toCoord.index[0])
		yDist = abs(fromCoord.index[1] - toCoord.index[1])
		
		if xDist == 0:
			for rank in range(	min(fromCoord.index[1], toCoord.index[1]) +1 , 
								max(toCoord.index[1], fromCoord.index[1])):
				if obstacles[rank][fromCoord.index[0]]:
					return False
			return True

		if yDist == 0:
			for letter in range(min(fromCoord.index[0], toCoord.index[0]) +1 , 
								max(toCoord.index[0], fromCoord.index[0])):
				if obstacles[fromCoord.index[1]][letter]:
					return False
			return True


class Queen(Piece):
	def type(self):
		return Type.queen

	def fen(self):
		if self.color() == Color.black:
			return "q"
		else:
			return "Q"

	def canMove(self, fromCoord, toCoord, obstacles, takes=False):
		xDist = abs(fromCoord.index[0] - toCoord.index[0])
		yDist = abs(fromCoord.index[1] - toCoord.index[1])
		
		if xDist == yDist or xDist == 0 or yDist == 0:
			return True
		else:
			return False

class King(Piece):
	def type(self):
		return Type.king

	def fen(self):
		if self.color() == Color.black:
			return "k"
		else:
			return "K"

	def canMove(self, fromCoord, toCoord, obstacles, takes=False):
		xDist = abs(fromCoord.index[0] - toCoord.index[0])
		yDist = abs(fromCoord.index[1] - toCoord.index[1])
		
		return xDist == 1 or yDist == 1	
