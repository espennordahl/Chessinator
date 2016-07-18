

from utils import *
from piece import *
from move import *
from board import *

class Game():
	def __init__(self):
		## init board
		self._board = Board()

		## init game state
		self._sideToMove = Color.white
		self._castlingAbility = "KQkq"
		self._enPassantTargetSquare = "-"
		self._halfMoveClock = 0
		self._fullMoveCounter = 0

		self.applyfen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")

	def isMoveLegal(self, move):
		return move.isLegal()
	
	def applyMove(self, move):
		if not move.isLegal():
			return False

		move.conformMove(self._board)

		fromSquare = self._board.getSquare(move.getFromCoord())
		pieceToMove = fromSquare.piece
		fromSquare.piece = None

		toSquare = self._board.getSquare(move.getToCoord())
		toSquare.piece = pieceToMove

		## An passant target square is specified after a double push, 
		## regardless of whether an en passant capture is really possible
		if pieceToMove.type() == Type.pawn:
			if move.getFromCoord().distanceTo(move.getToCoord())[1] == 2:
				enPassantTargetRankStr = "3"
				if pieceToMove.color() == Color.black:
					enPassantTargetRankStr = "6"
				self._enPassantTargetSquare = indexToLetter(move.fromLetter()) + enPassantTargetRankStr
			else:
				self._enPassantTargetSquare = "-"
		else:
			self._enPassantTargetSquare = "-"

		## The halfmove clock is reset after a pawn move or capture, and incremented otherwise
		if pieceToMove.type() == Type.pawn:
			self._halfMoveClock = 0
		else:
			self._halfMoveClock += 1

		if pieceToMove.color() == Color.black:
			self._fullMoveCounter += 1
			self._sideToMove = Color.white
		else:
			self._sideToMove = Color.black
			

		return True

	def applyfen(self, fenstring):
		fenarray = fenstring.split(' ')
		
		# Piece placement. FEN placement starts at the 8th rank
		fenranks = fenarray[0].split('/')
		rankindex = 7
		for rank in fenranks:
			fileindex = 0
			for letter in rank:
				if isInt(letter):
					fileindex += int(letter)
				else:
					coord = Coordinate(index=[rankindex, fileindex])
					square = self._board.getSquare(coord)
					square.piece = makePiece(letter)
					fileindex += 1
			rankindex -= 1

		# Side to move
		if fenarray[1] == "w":
			self._sideToMove = Color.white
		elif fenarray[1] == "b":
			self._sideToMove = Color.black
		else:
			raise Exception("invalid fen. Could not real SideToMove", fenarray)

		# Castling ability
		self._castlingAbility = fenarray[2]

		# En passant target square
		self._enPassantTargetSquare = fenarray[3]

		# Halfmove clock
		self._halfMoveClock = int(fenarray[4])

		# Fullmove counter
		self._fullMoveCounter = int(fenarray[5])

	def fen(self):
		# FEN is the Forsyth-Edwards Notation, which describes a chess position.
		fen = []
		## Piece Placement
		## the piece placement is determined by rank, starting at the 8th rank
		## and moving down the board. Each rank is seperated by a '/'
		## Within each rank, pieces go in order from A to H
		placement = ""
		for rank in self._board.getRanks():
			noPieceCounter = 0
			for square in rank:
				if square.hasPiece():
					if noPieceCounter:
						placement = placement + str(noPieceCounter)
						noPieceCounter = 0
					placement = placement + square.piece.fen()

				else: ## no piece
					noPieceCounter += 1

			if noPieceCounter:
				placement = placement + str(noPieceCounter)
	
			if rank > 0:
				placement = placement + "/"

		fen.append(placement)

		## Side to move
		if self._sideToMove == Color.white:
			fen.append("w")
		else:
			fen.append("b")

		## Castling ability
		fen.append(self._castlingAbility)

		## En passant target square
		fen.append(self._enPassantTargetSquare)

		## Halfmove clock
		fen.append(str(self._halfMoveClock))

		## Fullmove counter
		fen.append(str(self._fullMoveCounter))

		return " ".join(fen)


