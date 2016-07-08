from enum import Enum

import robot

class Status(Enum):
	waiting = 0
	error = 1
	initializing = 2

class GameController:
	def __init__(self):
	
	def connectToBoard(self, port="/dev/ttyUSB0"):
		self._robot = robot.Robot(port)
		self._robot.waitForReady()

	def eventLoop(self):
		error = ""
		status = Status.initializing
		while status != Status.error:
			## check arduino for board changes
			
			## check UI for remote signals
			
			## check engine for candidate moves
