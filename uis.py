
class UIController():
	def __init__(self):
		return

	def getEvents(self, eventStack):
		return

class CommandlineUI(UIController):
	def getEvents(self, eventStack):
		received = raw_input("UI Input: ")
		if received != "":
			eventStack.append(received)
		return
	
class ExitUI(UIController):
	def getEventsl(self, eventStack):
		eventStack.append("exit")
		return
