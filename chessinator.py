import argparse
import sys

from chessberry.game import Game
from chessberry.move import Move

import sensors
import uis
import events


def getSubclassInModule(parent, subclass, module):
	for attribute in dir(module):
		if subclass.lower() == attribute.lower():
			return module.__dict__[attribute]

def makeSensorController(sensorArg):
	sensor = None
	## Try to create object
	subclass = getSubclassInModule(sensors.SensorController, sensorArg + "Sensor", sensors)
	if subclass:
		sensor = subclass()
	if isinstance(sensor, sensors.SensorController):
		return sensor
	else:
		raise Exception("Failed to create sensor controller of type: " + sensorArg)

def makeUIController(uiArg):
	ui = None
	## Try to create object
	subclass = getSubclassInModule(uis.UIController, uiArg + "UI", uis)
	if subclass:
		ui = subclass()
	if isinstance(ui, uis.UIController):
		return ui
	else:
		raise Exception("Failed to create sensor controller of type: " + uiArg)



class Chessinator():
	def __init__(self, sensor, ui):
		## init game
		self._game = Game()
		self._exit = False
		self._sensor = sensor
		self._ui = ui

	def runEvents(self):
		print "running event stack"
		for event in self._eventStack:
			assert(isinstance(event, events.Event))
			print "  event: " + str(event)
			if event.type == events.EventType.exit:
				self._exit = True
				return
			elif event.type == events.EventType.sensor:
				if event.data[0] == "move":
					move = Move(self._game.sideToMove(), event.data[1])
					self._game.applyMove(move)
				else:
					raise Exception("Unknown sensor event: " + str(event))

	def runEventLoop(self):
		while(not self._exit):
			## clear event stack
			self._eventStack = []
			## wait for sensor or user input
			while(len(self._eventStack) == 0):
				self._ui.getEvents(self._eventStack)
				self._sensor.getEvents(self._eventStack)
			## execute events
			self.runEvents()


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Chessinator game controller program.')
	parser.add_argument('-s', '--sensorController',
						metavar = 'sensor',
						default = 'commandline')
	parser.add_argument('-ui', '--uiController',
						metavar = 'ui',
						default = 'commandline')
	args = parser.parse_args()
	print "Well hello there!"
	
	## set up controllers
	sensor = makeSensorController(args.sensorController)
	ui = makeUIController(args.uiController)

	## init program
	program = Chessinator(sensor, ui)

	## run event loop
	program.runEventLoop()

	## shut down
	print "Good night!"
