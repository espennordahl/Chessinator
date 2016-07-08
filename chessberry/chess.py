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



def letterToIndex(letter):
	if letter == "a":
		return 0
	if letter == "b":
		return 1
	if letter == "c":
		return 2
	if letter == "d":
		return 3
	if letter == "e":
		return 4
	if letter == "f":
		return 5
	if letter == "g":
		return 6
	if letter == "h":
		return 7

def indexToLetter(index):
	l = "abcdefgh"
	return l[index]

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

	def type(self):
		return self._type
	
	def color(self):
		return self._color


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
		if not move.isLegal():
			return False

		move.conformMove(self._board)

		pieceToMove = self._board[move.fromRank()][move.fromLetter()] 
		self._board[move.fromRank()][move.fromLetter()] = None

		self._board[move.toRank()][move.toLetter()] = pieceToMove

		## An passant target square is specified after a double push, 
		## regardless of whether an en passant capture is really possible
		if pieceToMove.type() == Type.pawn:
			if abs(move.fromRank() - move.toRank()) == 2:
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

