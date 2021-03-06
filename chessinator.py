import argparse
import sys
import logging
import random

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
		self._logger = logging.getLogger('Chessinator')
		## init game
		self._game = Game()
		self._exit = False
		self._sensor = sensor
		self._ui = ui

	def runEvents(self):
		self._logger.debug('running event stack')
		for event in self._eventStack:
			assert(isinstance(event, events.Event))
			self._logger.debug('Event: %s', event)
			if event.type == events.EventType.exit:
				self._runExitEvent(event)
				return
			elif event.type == events.EventType.sensor:
				self._runSensorEvent(event)
			elif event.type == events.EventType.user:
				self._runUserEvent(event)
			elif event.type == events.EventType.robot:
				self._runRobotEvent(event)

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

	def _runExitEvent(self, event):
		self._exit = True

	def _runSensorEvent(self, event):
		if event.data[0] == "move":
			move = Move(self._game.sideToMove(), event.data[1])
			self._game.applyMove(move)
		else:
			raise Exception("Unknown sensor event: " + str(event))
	
	def _runUserEvent(self, event):
		return
	
	def _runRobotEvent(self, event):
		return

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Chessinator game controller program.')
	parser.add_argument('-s', '--sensorController',
						metavar = 'sensor',
						default = 'commandline')
	parser.add_argument('-ui', '--uiController',
						metavar = 'ui',
						default = 'commandline')
	args = parser.parse_args()

	# set up logger
	logfilename = '/tmp/chessinator.' + str(random.randrange(9999999)) + '.log'
	logformat = '[%(asctime)s] [%(levelname)s] %(name)s : %(message)s'
	logging.basicConfig(filename=logfilename, filemode='w', format = logformat, level=logging.DEBUG)
	logging.info('Starting application')
	
	## set up controllers
	logging.debug('initializing sensor controller')
	sensor = makeSensorController(args.sensorController)
	logging.debug('initializing ui controller')
	ui = makeUIController(args.uiController)

	## init program
	logging.debug('initializing program')
	program = Chessinator(sensor, ui)

	## run event loop
	program.runEventLoop()

	## shut down
	logging.info('Exiting application')
