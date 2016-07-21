import argparse
import sys

from chessberry.game import Game
from chessberry.move import Move

import sensors
import uis

def runEvents(eventStack):
	print "running event stack"
	for event in eventStack:
		print "  event: " + str(event)
		if event == "exit":
			return False
	eventStack = []
	return True

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
	
	## init loggers

	## init game
	game = Game()

	## init robot

	## init sensors
	sensor = makeSensorController(args.sensorController)

	## init UI
	ui = makeUIController(args.uiController)

	## event loop
	keepRunning = True
	while(keepRunning):
		## clear event stack
		eventStack = []
		## wait for sensor or user input
		while(len(eventStack) == 0):
			ui.getEvents(eventStack)
			sensor.getEvents(eventStack)
		## execute events
		keepRunning = runEvents(eventStack)

	## shut down
	print "Good night!"
