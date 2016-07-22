import events

class SensorController():
	def __init__(self):
		return
	
	def getEvents(self, eventStack):
		return

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

			
