import serial


DEFAULT_MOTOR_SPEED = 10000

class Robot:
	def __init__(self, port = '/dev/cu.wchusbserial1420'):
		self._serial = serial.Serial(port, 115200)
		self._isReady = False
		self._position = None


	def isReady(self):
		return self._isReady

	def waitForReady(self):
		if self._isReady:
			return self._isReady
		print("Initializing motors. Waiting for 'start' signal from driver.")
		while True:
			line = self._serial.readline()
			print line
			if "start" in line:
				self._isReady = True
				self._position = [0.,0.]
				print "bot ready. Sending config instructions."
				self._sendSerial("$1 X11 Y9 ZA6") #xy step pin
				self._sendSerial("$2 X10 Y3 ZA1") #xy dir pin
				self._sendSerial("$3 XA0 Y12 Z12") # xy min pin
				self._sendSerial("$4 XA1 Y13 Z13") # xy max pin
				self._sendSerial("$6 X500 Y500.0 Z500") # xy steps pmm
				self._sendSerial("G90")
				self._sendSerial("G21")
				return self._isReady
	
	def _sendSerial(self, message):
		print "sending: " + message
		self._serial.write(message)
		line = self._serial.readline()
		print "received: " + line
		return line
	
	def moveTo(self, targetX, targetY, speed=DEFAULT_MOTOR_SPEED):
		return self.moveToX(targetX, speed) and self.moveToY(targetY, speed)

	def moveToX(self, target, speed=DEFAULT_MOTOR_SPEED):
		result = self._moveSingleAxis("X", target, speed)
		return result
	
	def moveToY(self, target, speed=DEFAULT_MOTOR_SPEED):
		result = self._moveSingleAxis("Y", target, speed)
		return result

	def move(self, targetX, targetY, speed=DEFAULT_MOTOR_SPEED):
		return self.moveX(targetX, speed) and self.moveY(targetY, speed)

	def moveX(self, target, speed=DEFAULT_MOTOR_SPEED):
		if not self.isReady():
			print "Motors not initialized."
			self.waitForReady()
		return self.moveToX(target + self._position[0], speed)

	def moveY(self, target, speed=DEFAULT_MOTOR_SPEED):
		if not self.isReady():
			print "Motors not initialized."
			self.waitForReady()
		return self.moveToY(target + self._position[1], speed)

	def _moveSingleAxis(self, axis, target, speed):
		if not self.isReady():
			print "Motors not initialized."
			self.waitForReady()	
		print "Moving to: ", target if axis == "X" else self._position[0], target if axis == "Y" else self._position[1]
		if target > 3000 or target < 0:
			print "Target outside of range: ", target
			return False
		if speed > 30000 or speed <= 0:
			print "speed outside of range: ", speed
			return False
		if type(target) is not int and type(target) is not float:
			print "target location invalid: ", target
			return False
		if type(speed) is not int and type(target) is not float:
			print "target speed invalid: ", speed
			return False
		line = self._sendSerial("G1 " + axis + str(target) + " F" + str(speed))
		if "ok" in line:
			if axis == "X":
				self._position[0] = target
			elif axis == "Y":
				self._position[1] = target
			print "Move successful. New position: ", self._position
			return True
		return False
