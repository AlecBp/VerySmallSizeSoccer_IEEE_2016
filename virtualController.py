import pygame
from CommunicationPython2Arduino import Communication

pygame.init()

display_width = 800
display_height = 600

gameDisplay = pygame.display.set_mode((display_width,display_height))
controle = True

isGamePaused = 1
isEncoderActive = 0
pinkPlayer_rightSpeed = 0
pinkPlayer_leftSpeed = 0
pinkPlayer_rightDistance = 0
pinkPlayer_leftDistance = 0
pinkPlayer_x = 0
pinkPlayer_y = 0
pinkDataArray = [isGamePaused, isEncoderActive, 
				pinkPlayer_rightSpeed, pinkPlayer_leftSpeed, 
				pinkPlayer_rightDistance, pinkPlayer_leftDistance,
				pinkPlayer_x, pinkPlayer_y]

comRobot1 = Communication(target="/dev/ttyUSB0")
robot1_name = comRobot1.getName()
x=0
while controle:
	for event in pygame.event.get():

		if event.type == pygame.QUIT:
			controle = 0
			#0 - 4 ---->
			#5 - 9 <----
		if event.type == pygame.KEYDOWN:

			if event.key == pygame.K_0:
				print "0"
				x=0
			elif event.key == pygame.K_1:
				print "1"
				x=1
			elif event.key == pygame.K_2:
				print "2"
				x=2
			elif event.key == pygame.K_3:
				print "3"
				x=3
			elif event.key == pygame.K_4:
				print "4"
				x=4

			elif event.key == pygame.K_DOWN:
				print "down"
				pinkDataArray[2]=x
				pinkDataArray[3]=x

			elif event.key == pygame.K_UP:
				print "up"
				pinkDataArray[2]=5+x
				pinkDataArray[3]=5+x

			elif event.key == pygame.K_RIGHT:
				print "right"
				pinkDataArray[2]-=1
				pinkDataArray[3]+=1

			elif event.key == pygame.K_LEFT: 
				print "left"
				pinkDataArray[2]+=1
				pinkDataArray[3]-=1

			elif event.key == pygame.K_SPACE: 
				print "space"
				pinkDataArray[2]=5
				pinkDataArray[3]=0

			elif event.key == pygame.K_p:
				print "paused"
				if pinkDataArray[0] == 1:
					pinkDataArray[0] = 0
				else:
					pinkDataArray[0] = 1

		comRobot1.sendData(pinkDataArray)



pygame.quit()
quit()