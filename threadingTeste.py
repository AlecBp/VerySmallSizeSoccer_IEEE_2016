# Teste threading para captura de imagem da camera e processamento de imagem

import cv2
from WebcamVideoStream import WebcamVideoStream
from VisionModule import Vision

# ALWAYS RUN CODE WITH CORRECT PERSPECTIVE ACTIVE,
# SO THE FIRST TIME WILL CREATE A FILE WITH THE CONFIG RUNNING WITHOUT THIS FILE MAY CAUSE PROBLEMS
# TO CREATE THIS FILE JUST RUN CODE WITH CORRECT PERSPECTIVE IS ACTIVE

# INTIAL SETUP OPTIONS
controle = 1
cameraSrc = 1
# src = 0 ---> primeira camera, src = 1 ---> segunda camera.......
vision = Vision(correctPerspectiveIsActive=False, src=cameraSrc)
videoStream = WebcamVideoStream(src=cameraSrc).start()
vision.setTeamColor("yellow")


print "Entering primary loop"
while controle:
    while controle:
        vision.updateFPS()
        lastFrame = videoStream.read()
        if lastFrame != None:
            # cv2.imshow('rawInput', lastFrame)
            lastFrame = vision.applyPerspectiveCorrection(lastFrame)
            BGRframe = lastFrame.copy()
            # lastFrame = vision.medianBlur(lastFrame)
            HSVframe = vision.convertHSV(lastFrame)

            blueFrame, blueCenterList = vision.findBlueTeam(HSVframe)
            yellowFrame, yellowCenterList = vision.findYellowTeam(HSVframe)
            ballFrame, ballCenter = vision.findBall(HSVframe)
            redPrimaryColor, redPoint = vision.findRedPlayer(HSVframe)
            pinkPrimaryColor, pinkPoint = vision.findPinkPlayer(HSVframe)
            greenPrimaryColor, greenPoint = vision.findGreenPlayer(HSVframe)

            debugFrame = vision.debugVisual(BGRframe)
            cv2.imshow('debugFrame', debugFrame)

        else:
            print "ERROR EMPTY FRAME"
        if cv2.waitKey(1) & 0xFF == ord('q'):
            videoStream.stop()
            controle = 0
            break

        vision.getFPS()


cv2.destroyAllWindows()