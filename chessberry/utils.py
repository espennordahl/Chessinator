prom enum import Enum

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

