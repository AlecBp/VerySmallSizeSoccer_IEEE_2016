import serial
import time

controle = 1
# Data to be sent
isGamePaused = 1
isEncoderActive = 0
pinkPlayer_rightSpeed = 5
pinkPlayer_leftSpeed = 5
pinkPlayer_rightDistance = 0
pinkPlayer_leftDistance = 0
pinkPlayer_x = 0
pinkPlayer_y = 0
pinkDataArray = [isGamePaused, isEncoderActive, 
				pinkPlayer_rightSpeed, pinkPlayer_leftSpeed, 
				pinkPlayer_rightDistance, pinkPlayer_leftDistance,
				pinkPlayer_x, pinkPlayer_y]


class Communication:
	def __init__(self, target='/dev/ttyUSB0'):
		self.target=target
		self.connecting = True
		self.numberOfAttempts = 0
		self.myRobotName = ""
		while self.connecting and self.numberOfAttempts<20:
			try:
				self.arduinoSerial = serial.Serial(self.target,9600,timeout=5)
				time.sleep(2)
				self.connecting = False
				print "Connection established on "+self.target
			except:
				self.connecting = True
				self.target = "/dev/ttyUSB"+str(self.numberOfAttempts)
				self.numberOfAttempts += 1
				print "Connection error (maybe =D), attemp number "+str(self.numberOfAttempts)
		if (self.numberOfAttempts>19):
			print "Massive connection error, too many attempts... Start autodestruction sequence \o/ "


	def getName(self, forceNew=0):
		if self.myRobotName == "" and forceNew == 0:
			self.arduinoSerial.flush()
			self.arduinoSerial.write("w")
			time.sleep(.5)
			self.myRobotName = self.arduinoSerial.read()
			if self.myRobotName == "p" or self.myRobotName == "r" or self.myRobotName == "g":
				print "This robot name is "+self.myRobotName
				return self.myRobotName
			else:
				print "Unexpected name "+str(self.myRobotName)
				self.myRobotName = ""
				return self.myRobotName
		else:
			"Robot name already known... "+self.myRobotName
			return self.myRobotName


	def sendData(self, array):
		for data in array:
			self.arduinoSerial.write(str(data))
		self.arduinoSerial.write("x")
"""
comRobot1 = Communication(target="/dev/ttyUSB0")
robot1_name = comRobot1.getName()

while controle:
	comRobot1.sendData(pinkDataArray)
	time.sleep(.03)
"""