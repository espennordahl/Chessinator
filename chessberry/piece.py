from enum import Enum

from utils import *

class Type(Enum):
	pawn = 0
	knight = 1
	bishop = 2
	rook = 3
	queen = 4
	king = 5

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


