from enum import Enum

from utils import *
from piece import *
from board import *

class CastleSide(Enum):
	kingside = 1
	queenside = 2

class Move():
	def __init__(self, color, pgnMove):
		self._pgn = pgnMove
		self._color = color
		self._fromCoord = None
		self._toCoord = None
		self._castleSide = None
		self._candidatePGN = None

	def conformMove(self, board):
		if self._pgn[0].islower():
			## pawn move
			if len(self._pgn) == 2:
				toRank = int(self._pgn[1]) - 1
				toLetter = letterToIndex(self._pgn[0])
			else:
				toRank = int(self._pgn[2]) - 1
				toLetter = letterToIndex(self._pgn[1])
				self._candidatePGN = self._pgn[0]
			self._toCoord = Coordinate(index=[toLetter, toRank])
			self._conformPawnMove(board)
		else:
			if self._pgn == 'O-O':
				self._conformCastlesMove(board)
			else:
				## normal piece move
				if isInt(self._pgn[2]):
					## only one move candidate
					toRank = int(self._pgn[2]) - 1
					toLetter = letterToIndex(self._pgn[1])
				else:
					## multiple move candidates
					toRank = int(self._pgn[3]) - 1
					toLetter = letterToIndex(self._pgn[2])
					self._candidatePGN = self._pgn[1]
				self._toCoord = Coordinate(index=[toLetter, toRank])
				if self._pgn[0] == "N":
					self._conformKnightMove(board)
				elif self._pgn[0] == "B":
					self._conformBishopMove(board)
				elif self._pgn[0] == "R":
					self._conformRookMove(board)
				elif self._pgn[0] == "K":
					self._conformKingMove(board)
				elif self._pgn[0] == "Q":
					self._conformQueenMove(board)
				else:
					raise Exception("Unsupported piece type in pgn: " + self._pgn)

	def _conformPawnMove(self, board):
		pawnSquares = board.getSquares(piecetype = Type.pawn, color = self._color, candidatePGN = self._candidatePGN)
		takes = board.getSquare(self._toCoord).piece != None
		for square in pawnSquares:
			if square.piece.canMove(square.coord, self._toCoord, board.obstacles(), takes=takes):
				self._fromCoord = square.coord

		if  self._fromCoord == None:
			raise Exception("Couldnt find candidate piece for move " + self._pgn + ". Board:\n" + board.ascii())
		
	def _conformKnightMove(self, board):
		knightSquares = board.getSquares(piecetype = Type.knight, color = self._color, candidatePGN = self._candidatePGN)
		for square in knightSquares:
			if square.piece.canMove(square.coord, self._toCoord, board.obstacles()):
				self._fromCoord = square.coord

		if  self._fromCoord == None:
			raise Exception("Couldnt find candidate piece for move " + self._pgn + ". Board:\n" + board.ascii())
	
	def _conformBishopMove(self, board):
		bishopSquares = board.getSquares(piecetype = Type.bishop, color = self._color, candidatePGN = self._candidatePGN)
		for square in bishopSquares:
			if square.piece.canMove(square.coord, self._toCoord, board.obstacles()):
				self._fromCoord = square.coord
				
		if self._fromCoord == None:
			raise Exception("Couldnt find candidate piece for move " + self._pgn + ". Board:\n" + board.ascii())

	def _conformQueenMove(self, board):
		queenSquares = board.getSquares(piecetype = Type.queen, color = self._color, candidatePGN = self._candidatePGN)
		for square in queenSquares:
			if square.piece.canMove(square.coord, self._toCoord, board.obstacles()):
				self._fromCoord = square.coord
				
		if self._fromCoord == None:
			raise Exception("Couldnt find candidate piece for move " + self._pgn + ". Board:\n" + board.ascii())

	def _conformKingMove(self, board):
		kingSquares = board.getSquares(piecetype = Type.king, color = self._color, candidatePGN = self._candidatePGN)
		for square in kingSquares:
			if square.piece.canMove(square.coord, self._toCoord, board.obstacles()):
				self._fromCoord = square.coord
				
		if self._fromCoord == None:
			raise Exception("Couldnt find candidate piece for move " + self._pgn + ". Board:\n" + board.ascii())



	def _conformRookMove(self, board):
		rookSquares = board.getSquares(piecetype = Type.rook, color = self._color, candidatePGN = self._candidatePGN)
		for square in rookSquares:
			if square.piece.canMove(square.coord, self._toCoord, board.obstacles()):
				self._fromCoord = square.coord
				
		if self._fromCoord == None:
			raise Exception("Couldnt find candidate piece for move " + self._pgn + ". Board:\n" + board.ascii())

	def _conformCastlesMove(self, board):
		if self._pgn[0] == "o":
			self._castleSide = CastleSide.queenside
		else:
			self._castleSide = CastleSide.kingside
	
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
	
	def castleSide(self):
		return self._castleSide

	def _checkPGN(self):
		if not isinstance(self._pgn, basestring):
			return False
		
		if len(self._pgn) < 2 or len(self._pgn) > 4:
			return False

		if len(self._pgn) == 2:
			if self._pgn[0] not in ('abcdefgh'):
				return False

			if self._pgn[1] not in ('12345678'):
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

