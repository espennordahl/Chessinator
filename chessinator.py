from chessberry.game import Game
from chessberry.move import Move

def queryUserInput(eventStack):
	eventStack.append(raw_input(">>>>>  "))
	return 

def querySensorInput(eventStack):
	return

def runEvents(eventStack):
	print "running event stack"
	for event in eventStack:
		print "  event: " + str(event)
		if event == "exit":
			return False
	eventStack = []
	return True

if __name__ == "__main__":
	print "Well hello there!"
	
	## init loggers

	## init game

	## init robot

	## init sensors

	## init UI

	## event loop
	keepRunning = True
	while(keepRunning):
		## wait for sensor or user input
		sensorInput = None
		userInput = None
		eventStack = []
		while(len(eventStack) == 0):
			queryUserInput(eventStack)
			querySensorInput(eventStack)

		## parse input

		## execute events if any
		keepRunning = runEvents(eventStack)

		## notify user of results

	## shut down
	print "Good night!"
