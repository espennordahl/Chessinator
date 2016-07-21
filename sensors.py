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
		event = events.Event(eventType.exit)
		eventStack.append(event)
		return
