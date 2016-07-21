
class SensorController():
	def __init__(self):
		return
	
	def getEvents(self, eventStack):
		return

class CommandlineSensor(SensorController):
	def getEvents(self, eventStack):
		result = raw_input("Sensor input: ")
		if result != "":
			eventStack.append(result)
		return

class ExitSensor(SensorController):
	def getEvents(self, eventStack):
		eventStack.append("exit")
		return
