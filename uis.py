import events

class UIController():
	def __init__(self):
		return

	def getEvents(self, eventStack):
		return

class CommandlineUI(UIController):
	def getEvents(self, eventStack):
		result = raw_input("UI Input: ")
		if result != "":
			if result == "exit":
				event = events.Event(events.EventType.exit)
			else: 
				event = events.Event(events.EventType.user, data=result)
			eventStack.append(event)
		return
	
class ExitUI(UIController):
	def getEvents(self, eventStack):
		event = events.Event(events.EventType.exit)
		eventStack.append(event)
		return

class DummyUI(UIController):
	def getEvents(self, eventStack):
		return
