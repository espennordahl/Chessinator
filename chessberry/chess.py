from enum import Enum

class Color(Enum):
	black = 0
	white = 1

class Type(Enum):
	pawn = 0
	knight = 1
	bishop = 2
	rook = 3
	queen = 4
	king = 5

def isInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False


class Move():
	def __init__(self, color, uciMove):
		self._uci = uciMove
		self._color = color
	
	def isLegal(self):
		if not self._checkUCI():
			return False
		
		if not self._checkColor():
			return False
		
		return True

	def _checkUCI(self):
		if not isinstance(self._uci, basestring):
			return False
		
		if len(self._uci) < 2 or len(self._uci) > 4:
			return False

		if len(self._uci) == 2:
			if self._uci[0] not in ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'):
				return False

			if self._uci[1] not in ('1', '2', '3', '4', '5', '6', '7', '8'):
				return False
		
		return True

	def _checkColor(self):
		if not isinstance(self._color, Color):
			return False

		return True

class Piece():
	def __init__(self, fenstring = ""):
		if fenstring:
			if fenstring.islower():
				self._color = Color.black
			else:
				self._color = Color.white
			lowerFenstring = fenstring.lower()
			if lowerFenstring == "p":
				self._type = Type.pawn
			elif lowerFenstring == "n":
				self._type = Type.knight
			elif lowerFenstring == "b":
				self._type = Type.bishop
			elif lowerFenstring == "r":
				self._type = Type.rook
			elif lowerFenstring == "q":
				self._type = Type.queen
			elif lowerFenstring == "k":
				self._type = Type.king

	def fen(self):
		fenstring = ""
		if self._type == Type.pawn:
			fenstring = "p"
		elif self._type == Type.knight:
			fenstring = "n"
		elif self._type == Type.bishop:
			fenstring = "b"
		elif self._type == Type.rook:
			fenstring = "r"
		elif self._type == Type.queen:
			fenstring = "q"
		elif self._type == Type.king:
			fenstring = "k"

		if self._color == Color.black:
			return fenstring
		else:
			return fenstring.upper()


class Game():
	def __init__(self):
		## init board
		self._board = []
		for i in range(0,8):
			self._board.append([])
			for j in range(0,8):
				self._board[i].append(None)

		## init game state
		self._sideToMove = Color.white
		self._castlingAbility = "KQkq"
		self._enPassantTargetSquare = "-"
		self._halfMoveClock = 0
		self._fullMoveCounter = 0

		## apply fen
		self.applyfen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")

	def isMoveLegal(self, move):
		return move.isLegal()
	
	def applyMove(self, move):
		return move.isLegal()
	
	def applyfen(self, fenstring):
		fenarray = fenstring.split(' ')
		
		# Piece placement
		fenranks = fenarray[0].split('/')
		rankindex = 7
		for rank in fenranks:
			file = 0
			for letter in rank:
				if isInt(letter):
					file += int(letter)
				else:
					self._board[rankindex][file] = Piece(fenstring=letter)
					file += 1
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
		for rank in range(7,-1,-1):
			noPieceCounter = 0
			for square in self._board[rank]:
				if square != None:
					if noPieceCounter:
						placement = placement + str(noPieceCounter)
						noPieceCounter = 0
					placement = placement + square.fen()

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
