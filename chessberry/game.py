import logging

from utils import *
from piece import *
from move import *
from board import *

class Game():
	def __init__(self):
		self._logger = logging.getLogger('Game')
		self._logger.debug('Initializing Game object')
		## init board
		self._board = Board()

		## init game state
		self._sideToMove = Color.white
		self._castlingAbility = "KQkq"
		self._enPassantTargetSquare = "-"
		self._halfMoveClock = 0
		self._fullMoveCounter = 0

		self.applyfen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
		self._logger.debug('Completed initialing Game object')

	def isMoveLegal(self, move):
		return move.isLegal()
	
	def applyMove(self, move):
		self._logger.info('Applying move: %s', move)
		if not move.isLegal():
			self._logger.info('Move was illegal. Aborting')
			return False

		move.conformMove(self._board)

		capture = False

		if move.castleSide():
			self._logger.debug('Identified move as castling. Proceeding')
			## find rook
			rookSquares = self._board.getSquares(piecetype=Type.rook, color=self._sideToMove)
			castleRank = 0 if self._sideToMove == Color.white else 7
			rookLetter = 0 if move.castleSide == CastleSide.queenside else 7	
			rookCoord = Coordinate(index=[rookLetter, castleRank])
			rook = None
			for square in rookSquares:
				if square.coord.pgn == rookCoord.pgn:
					rook = square.piece
					
			if not rook:
				raise Exception("Couldn't find matching rook in coord " + str(rookCoord.pgn) + " for castles move.\n" + self._board.ascii())

			## move rook
			self._logger.debug('Moving rook')
			fromSquare = self._board.getSquare(rookCoord)
			toSquareLetter = 3 if move.castleSide == CastleSide.queenside else 5
			toSquare = self._board.getSquare(Coordinate(index=[toSquareLetter, castleRank]))
			fromSquare.piece = None
			toSquare.piece = rook

			## move king
			fromSquare = self._board.getSquare(Coordinate(index=[4, castleRank]))
			toSquareLetter = 2 if move.castleSide == CastleSide.queenside else 6
			toSquare = self._board.getSquare(Coordinate(index=[toSquareLetter, castleRank]))
			self._logger.debug('Moving king')
			pieceToMove = fromSquare.piece
			fromSquare.piece = None
			toSquare.piece = pieceToMove
			
			## update castlingAbility
			if self._sideToMove == Color.white:
				self._castlingAbility = self._castlingAbility.replace("K", "")
				self._castlingAbility = self._castlingAbility.replace("Q", "")

			else:
				self._castlingAbility = self._castlingAbility.replace("k", "")
				self._castlingAbility = self._castlingAbility.replace("q", "")
			self._logger.debug('Updated castling ability to: %s', 
								self._castlingAbility)
		else:
			## regular piece move
			fromSquare = self._board.getSquare(move.getFromCoord())
			pieceToMove = fromSquare.piece
			fromSquare.piece = None

			toSquare = self._board.getSquare(move.getToCoord())
			if toSquare.piece != None:
				capture = True
			toSquare.piece = pieceToMove

		## An passant target square is specified after a double push, 
		## regardless of whether an en passant capture is really possible
		self._enPassantTargetSquare = "-"
		if pieceToMove.type() == Type.pawn:
			if move.getFromCoord().distanceTo(move.getToCoord())[1] == 2:
				enPassantTargetRankStr = "3"
				if pieceToMove.color() == Color.black:
					enPassantTargetRankStr = "6"
				self._enPassantTargetSquare = fromSquare.coord.pgn[0] + enPassantTargetRankStr
		self._logger.debug('Updated en passant target square to: %s',
							self._enPassantTargetSquare)

		## The halfmove clock is reset after a pawn move or capture, and incremented otherwise
		if pieceToMove.type() == Type.pawn or capture == True:
			self._halfMoveClock = 0
		else:
			self._halfMoveClock += 1
		self._logger.debug('Updated half move clock to: %s',
							self._halfMoveClock)

		if pieceToMove.color() == Color.black:
			self._fullMoveCounter += 1
			self._sideToMove = Color.white
		else:
			self._sideToMove = Color.black

		self._logger.debug('Updated full move counter to: %s',
							self._fullMoveCounter)
		self._logger.debug('Updated side to move to: %s',
							self._sideToMove)	
		if self._castlingAbility == "":
			self._castlingAbility = "-"
		self._logger.debug('Updated castling ability to: %s',
							self._castlingAbility)
		self._logger.info('Finished applying move: %s', move)
	
		return True

	def applyfen(self, fenstring):
		self._logger.info('Applying fen: %s', fenstring)
		fenarray = fenstring.split(' ')
		
		# Piece placement. FEN placement starts at the 8th rank
		fenranks = fenarray[0].split('/')
		rankindex = 7
		for rank in fenranks:
			letterindex = 0
			for letter in rank:
				if isInt(letter):
					letterindex += int(letter)
				else:
					coord = Coordinate(index=[letterindex, rankindex])
					square = self._board.getSquare(coord)
					square.piece = makePiece(letter)
					letterindex += 1
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
		self._logger.info('Finished applying fen: %s', fenstring)

	def fen(self):
		# FEN is the Forsyth-Edwards Notation, which describes a chess position.
		fen = []
		## Piece Placement
		## the piece placement is determined by rank, starting at the 8th rank
		## and moving down the board. Each rank is seperated by a '/'
		## Within each rank, pieces go in order from A to H
		placement = ""
		ranks = copy.copy(self._board.getRanks())
		ranks.reverse()
		for rank in ranks:
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
	
			if rank != ranks[-1]:
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

	def sideToMove(self):
		return self._sideToMove
