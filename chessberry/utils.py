from enum import Enum

from utils import *

class Color(Enum):
	black = 0
	white = 1

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



