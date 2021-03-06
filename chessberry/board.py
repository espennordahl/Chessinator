import copy

from piece import *
from utils import *

class Coordinate:
	def __init__(self, pgn="", index=[-1, -1]):
		self.index = [-1,-1]
		if pgn != "":
			self._conformPGN(pgn)
		else:
			self._conformIndex(index)
	
	def distanceTo(self, otherCoord):
		return (abs(self.index[0] - otherCoord.index[0]), abs(self.index[1] - otherCoord.index[1]))

	def _conformPGN(self, pgn):
		self._checkPGN(pgn)
		self.index[0] = letterToIndex(pgn[0])
		self.index[1] = int(pgn[1])-1
		self.pgn = pgn

	def _conformIndex(self, index):
		self._checkIndex(index)
		self.index = copy.deepcopy(index)
		self.pgn = str(indexToLetter(index[0])) + str(index[1]+1)
		
	def _checkPGN(self, pgn):
		if type(pgn) is not str:
			raise Exception("Incorrect pgn format for square. Expected string, got: " + str(pgn))

		if len(pgn) != 2:
			raise Exception("Incorrect pgn format for square. Expected [letter, rank], got: " + pgn)
		
		letter = pgn[0]
		if letter not in "abcdefgh":
			raise Exception("Invalid pgn letter: " + pgn + ". Should be in range a-h.")

		if not isInt(pgn[1]):
			raise Exception("Recieved not int pgn rank: " + pgn)

		rank = int(pgn[1])
		if rank > 8 or rank < 1:
			raise Exception("Invalid pgn rank: " + pgn + ". Should be in range 1-8.")
	
	def _checkIndex(self, index):
		if len(index) != 2:
			raise Exception("Incorrect index format for square. Expceted [letter, rank], got: " + str(index))

		letter = index[0]
		rank = index[1]

		if not isInt(letter) or not isInt(rank):
			raise Exception("Invalid coordinate index. Should be [int, int]. Got: " + str([type(letter), type(rank)]))


		if letter > 7 or letter < 0:
			raise Exception("Invalid index for letter: " + str(letter) + ". Should be in 0-7 range.")

		if rank > 7 or rank < 0:
			raise Exception("Invalid index for rank: " + str(rank) + ". Should be in 0-7 range.")
	
	def __eq__(self, other):
		return self.index == other.index

class Square():
	def __init__(self, coordinate, piece=None):
		self.coord = coordinate
		self.piece = piece
	
	def hasPiece(self):
		return not self.empty()
	
	def empty(self):
		return self.piece is None
	
	def __eq__(self, other):
		if self.coord != other.coord:
			return False
		if self.piece != other.piece:
			return False
		return True

class Board:
	def __init__(self):
		self._ranks = []
		for y in range(0,8):
			self._ranks.append([])
			for x in range(0,8):
				coord = Coordinate(index=[x,y])
				self._ranks[y].append(Square(coord))
	
	def getSquare(self, coordinate):
		return self._ranks[coordinate.index[1]][coordinate.index[0]]
	
	def getRanks(self):
		return self._ranks
	
	def getSquares(self, piecetype = None, color = None, candidatePGN = None):
		matchingSquares = []
		for rank in self._ranks:
			for square in rank:
				if square.piece is None:
					continue
				if piecetype:
					if square.piece.type() != piecetype:
						continue
				if color:
					if square.piece.color() != color:
						continue
				if candidatePGN:
					if candidatePGN not in square.coord.pgn:
						continue
				matchingSquares.append(square)
		return matchingSquares

	def obstacles(self):
		ranks = []
		for y in range(0,8):
			ranks.append([])
			for x in range(0,8):
				coord = Coordinate(index=[x,y])
				ranks[y].append(self.getSquare(coord).piece != None)
		return ranks
	
	def ascii(self):
		string = '   a b c d e f g h\n'
		rankindex = 8
		rankscopy = copy.copy(self._ranks)
		rankscopy.reverse()
		for rank in rankscopy:
			string = string + str(rankindex) + ' '
			rankindex -= 1
			for square in rank:
				string = string + ' '
				if square.piece:
					string = string + square.piece.fen()
				else:
					string = string + ' '
			string = string + '\n'
		return string
	
	def __eq__(self, other):
		return self.ascii() == other.ascii()
		## TODO: why does this fail..?
	#	for x in range(0,8):
	#		for y in range(0,8):
	#			if self._ranks[y][x] != other._ranks[y][x]:
	#				return False
	#	return True

	def __repr__(self):
		return self.ascii()
