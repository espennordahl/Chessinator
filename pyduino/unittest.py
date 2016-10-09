import unittests

class ChessTestCase(unittest.TestCase):
	''' Simple TestCase subclass to customize the output.
	'''
	def shortDescription(self):
		return None

class TestRobot(ChessTestCase):
	def testRobotInitialization(self):
		
