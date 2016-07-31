import events

from chessberry.board import *
from chessberry.piece import *

class SensorController():
	def __init__(self):
		return
	
	def getEvents(self, eventStack):
		return

class ReidSwitchSensor(SensorController):
	initialBoard = 	[	[1, 1, 1, 1, 1, 1, 1, 1],
						[1, 1, 1, 1, 1, 1, 1, 1],
						[0, 0, 0, 0, 0, 0, 0, 0],
						[0, 0, 0, 0, 0, 0, 0, 0],
						[0, 0, 0, 0, 0, 0, 0, 0],
						[0, 0, 0, 0, 0, 0, 0, 0],
						[1, 1, 1, 1, 1, 1, 1, 1],
						[1, 1, 1, 1, 1, 1, 1, 1]]
	
	def __init__(self):
		self._board = Board()
		self._binaryBoard = None 

	def getEvents(self, eventStack):
		return

	def _newBinaryBoard(self, binaryBoard):
		if self._binaryBoard is None:
			if binaryBoard == ReidSwitchSensor.initialBoard:
				self._initBoard()

	def _initBoard(self):
		self._binaryBoard = ReidSwitchSensor.initialBoard
		for x in range(0,8):
			fen = "RNBQKBNR"
			coordinate = Coordinate(index=[x,0])
			square = self._board.getSquare(coordinate)
			square.piece = makePiece(fen[x])
		for x in range(0,8):	
			coordinate = Coordinate(index=[x,1])
			square = self._board.getSquare(coordinate)
			square.piece = makePiece("P")
		for x in range(0,8):	
			coordinate = Coordinate(index=[x,6])
			square = self._board.getSquare(coordinate)
			square.piece = makePiece("p")
		for x in range(0,8):	
	 		fen = "rnbqkbnr"
			coordinate = Coordinate(index=[x,7])
			square = self._board.getSquare(coordinate)
			square.piece = makePiece(fen[x])


class CommandlineSensor(SensorController):
	def getEvents(self, eventStack):
		result = raw_input("Sensor input: ")
		if result != "":
			if result == "exit":
				event = events.Event(events.EventType.exit)
			else:
				event = events.Event(events.EventType.sensor, data=result)
			eventStack.append(event)
		return

class ExitSensor(SensorController):
	def getEvents(self, eventStack):
		event = events.Event(events.EventType.exit)
		eventStack.append(event)
		return

class SingleMoveSensor(SensorController):
	def __init__(self):
		self._eventCounter = 0

	def getEvents(self, eventStack):
		if self._eventCounter == 0:
			self._eventCounter += 1
			eventData = ["move", "e4"]
			event = events.Event(events.EventType.sensor, data=eventData)
			eventStack.append(event)
		else:
			event = events.Event(events.EventType.exit)
			eventStack.append(event)

class ThreeMovesSensor(SensorController):
	def __init__(self):
		self._eventCounter = 0
		self._moves = [ ["move", "e4"], ["move", "d6"], ["move", "Nc3"] ]

	def getEvents(self, eventStack):
		if self._eventCounter < len(self._moves):
			event = events.Event(events.EventType.sensor, data=self._moves[self._eventCounter])
			eventStack.append(event)
			self._eventCounter += 1
		else:
			event = events.Event(events.EventType.exit)
			eventStack.append(event)

			
