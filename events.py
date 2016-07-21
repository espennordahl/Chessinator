import enum

class EventType(enum.Enum):
	exit = 0
	user = 1
	sensor = 2
	robot = 3

class Event:
	def __init__(self, eventType, data = []):
		self.type = eventType
		self.data = data
	
	def __repr__(self):
		return "Event Type: " + str(self.type) + ". Data: " + str(self.data)
