import numpy as np
import cv2
from Picanha import Picanha 


class Debugger:
    def __init__(self, colorTable, shouldLoadTable=1):
        self.dblue_team_min = (100, 160, 150)
        self.dblue_team_max = (140, 255, 255)
        self.dyellow_team_min = (15, 80, 180)
        self.dyellow_team_max = (60, 255, 255)
        self.dball_min = (15, 85, 207)
        self.dball_max = (22, 255, 255)
        self.dred_min = (176,105,235)
        self.dred_max = (179,255,255)
        self.dpink_min = (140,99,200)
        self.dpink_max = (170,255,255)
        self.dgreen_min = (75,90,135)
        self.dgreen_max = (90,255,255)
        print "__Going to load table"
        if shouldLoadTable:
            self.updateColorParameters(colorTable)
        print "__Color table loaded"
        #mask control
        self.blueMaskOn = 1
        self.yellowMaskOn = 1
        self.ballMaskOn = 1
        self.redMaskOn = 1
        self.pinkMaskOn = 1
        self.greenMaskOn = 1
        #filter control
        self.blueMaskFilterOn = 1
        self.yellowMaskFilterOn = 1
        self.ballMaskFilterOn = 1
        self.redMaskFilterOn = 1
        self.pinkMaskFilterOn = 1
        self.greenMaskFilterOn = 1
        #aim
        self.aimOn = 1
        #trackbar
        print "__Going to create trackbars"

        cv2.namedWindow("Blue_trackbars")
        cv2.createTrackbar('Hmax','Blue_trackbars',self.dblue_team_max[0],255,self.nothing)
        cv2.createTrackbar('Hmin','Blue_trackbars',self.dblue_team_min[0],255,self.nothing)
        cv2.createTrackbar('Smax','Blue_trackbars',self.dblue_team_max[1],255,self.nothing)
        cv2.createTrackbar('Smin','Blue_trackbars',self.dblue_team_min[1],255,self.nothing)
        cv2.createTrackbar('Vmax','Blue_trackbars',self.dblue_team_max[2],255,self.nothing)
        cv2.createTrackbar('Vmin','Blue_trackbars',self.dblue_team_min[2],255,self.nothing)
        cv2.createTrackbar("debugger.dilateErode","Blue_trackbars",1,1,self.nothing)


        cv2.namedWindow("Yellow_trackbars")
        cv2.createTrackbar('Hmax','Yellow_trackbars',self.dyellow_team_max[0],255,self.nothing)
        cv2.createTrackbar('Hmin','Yellow_trackbars',self.dyellow_team_min[0],255,self.nothing)
        cv2.createTrackbar('Smax','Yellow_trackbars',self.dyellow_team_max[1],255,self.nothing)
        cv2.createTrackbar('Smin','Yellow_trackbars',self.dyellow_team_min[1],255,self.nothing)
        cv2.createTrackbar('Vmax','Yellow_trackbars',self.dyellow_team_max[2],255,self.nothing)
        cv2.createTrackbar('Vmin','Yellow_trackbars',self.dyellow_team_min[2],255,self.nothing)
        cv2.createTrackbar("debugger.dilateErode","Yellow_trackbars",1,1,self.nothing)

        cv2.namedWindow("Ball_trackbars")
        cv2.createTrackbar('Hmax','Ball_trackbars',self.dball_max[0],255,self.nothing)
        cv2.createTrackbar('Hmin','Ball_trackbars',self.dball_min[0],255,self.nothing)
        cv2.createTrackbar('Smax','Ball_trackbars',self.dball_max[1],255,self.nothing)
        cv2.createTrackbar('Smin','Ball_trackbars',self.dball_min[1],255,self.nothing)
        cv2.createTrackbar('Vmax','Ball_trackbars',self.dball_max[2],255,self.nothing)
        cv2.createTrackbar('Vmin','Ball_trackbars',self.dball_min[2],255,self.nothing)
        cv2.createTrackbar("debugger.dilateErode","Ball_trackbars",1,1,self.nothing)

        cv2.namedWindow("Red_trackbars")
        cv2.createTrackbar('Hmax','Red_trackbars',self.dred_max[0],255,self.nothing)
        cv2.createTrackbar('Hmin','Red_trackbars',self.dred_min[0],255,self.nothing)
        cv2.createTrackbar('Smax','Red_trackbars',self.dred_max[1],255,self.nothing)
        cv2.createTrackbar('Smin','Red_trackbars',self.dred_min[1],255,self.nothing)
        cv2.createTrackbar('Vmax','Red_trackbars',self.dred_max[2],255,self.nothing)
        cv2.createTrackbar('Vmin','Red_trackbars',self.dred_min[2],255,self.nothing)
        cv2.createTrackbar("debugger.dilateErode","Red_trackbars",1,1,self.nothing)

        cv2.namedWindow("Pink_trackbars")
        cv2.createTrackbar('Hmax','Pink_trackbars',self.dpink_max[0],255,self.nothing)
        cv2.createTrackbar('Hmin','Pink_trackbars',self.dpink_min[0],255,self.nothing)
        cv2.createTrackbar('Smax','Pink_trackbars',self.dpink_max[1],255,self.nothing)
        cv2.createTrackbar('Smin','Pink_trackbars',self.dpink_min[1],255,self.nothing)
        cv2.createTrackbar('Vmax','Pink_trackbars',self.dpink_max[2],255,self.nothing)
        cv2.createTrackbar('Vmin','Pink_trackbars',self.dpink_min[2],255,self.nothing)
        cv2.createTrackbar("debugger.dilateErode","Pink_trackbars",1,1,self.nothing)
        print "Going to create green trackbars"
        cv2.namedWindow("Green_trackbars")
        cv2.createTrackbar('Hmax','Green_trackbars',self.dgreen_max[0],255,self.nothing)
        cv2.createTrackbar('Hmin','Green_trackbars',self.dgreen_min[0],255,self.nothing)
        cv2.createTrackbar('Smax','Green_trackbars',self.dgreen_max[1],255,self.nothing)
        cv2.createTrackbar('Smin','Green_trackbars',self.dgreen_min[1],255,self.nothing)
        cv2.createTrackbar('Vmax','Green_trackbars',self.dgreen_max[2],255,self.nothing)
        cv2.createTrackbar('Vmin','Green_trackbars',self.dgreen_min[2],255,self.nothing)
        cv2.createTrackbar("debugger.dilateErode","Green_trackbars",1,1,self.nothing)
        print "__All trackbars created"


    def updateColorParameters(self, loadedTable):
        colorTable = loadedTable
        self.dblue_team_min = colorTable[0]
        self.dblue_team_max = colorTable[1]
        self.dyellow_team_min = colorTable[2]
        self.dyellow_team_max = colorTable[3]
        self.dball_min = colorTable[4]
        self.dball_max = colorTable[5]
        self.dred_min = colorTable[6]
        self.dred_max = colorTable[7]
        self.dpink_min = colorTable[8]
        self.dpink_max = colorTable[9]
        self.dgreen_min = colorTable[10]
        self.dgreen_max = colorTable[11]
        print "dgreen_max = "+str(self.dgreen_max)+", dgreen_min = "+str(self.dgreen_min)
        print "__Color parements updated"

    def dilateErode(self, img):
        _img = cv2.erode(img, None, iterations=1)
        _img = cv2.dilate(img, None, iterations=1)
        return _img

    def dilateErodeBall(self, img):
        _img = cv2.erode(img, None, iterations=1)
        _img = cv2.dilate(img, None, iterations=2)
        return _img

    def nothing(self, x):
        pass


cap = cv2.VideoCapture(1)
print "__Cap created"
picanha = Picanha()
print "__Picanha created"
debugger = Debugger(picanha.load(), shouldLoadTable=1)
print "__Debugger created"
shouldSave = 1


while(True):
    ret, frame = cap.read(0)
    if frame!=None:
        y = frame.shape[0]
        x = frame.shape[1]
        frame_debug = frame.copy()
        hsvFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        cv2.imshow("frame_debug", frame_debug)
        debugger.dblue_team_max = cv2.getTrackbarPos("Hmax", "Blue_trackbars"), cv2.getTrackbarPos("Smax", "Blue_trackbars"), cv2.getTrackbarPos("Vmax", "Blue_trackbars")
        debugger.dblue_team_min = cv2.getTrackbarPos("Hmin", "Blue_trackbars"), cv2.getTrackbarPos("Smin", "Blue_trackbars"), cv2.getTrackbarPos("Vmin", "Blue_trackbars")
        debugger.dblueMaskFilterOn = cv2.getTrackbarPos("debugger.dilateErode", "Blue_trackbars")
        debugger.dyellow_team_max = cv2.getTrackbarPos("Hmax", "Yellow_trackbars"), cv2.getTrackbarPos("Smax", "Yellow_trackbars"), cv2.getTrackbarPos("Vmax", "Yellow_trackbars")
        debugger.dyellow_team_min = cv2.getTrackbarPos("Hmin", "Yellow_trackbars"), cv2.getTrackbarPos("Smin", "Yellow_trackbars"), cv2.getTrackbarPos("Vmin", "Yellow_trackbars")
        debugger.dyellowMaskFilterOn = cv2.getTrackbarPos("debugger.dilateErode", "Yellow_trackbars")
        debugger.dball_max = cv2.getTrackbarPos("Hmax", "Ball_trackbars"), cv2.getTrackbarPos("Smax", "Ball_trackbars"), cv2.getTrackbarPos("Vmax", "Ball_trackbars")
        debugger.dball_min = cv2.getTrackbarPos("Hmin", "Ball_trackbars"), cv2.getTrackbarPos("Smin", "Ball_trackbars"), cv2.getTrackbarPos("Vmin", "Ball_trackbars")
        debugger.dballMaskFilterOn = cv2.getTrackbarPos("debugger.dilateErode", "Ball_trackbars")
        debugger.dgreen_max = cv2.getTrackbarPos("Hmax", "Green_trackbars"), cv2.getTrackbarPos("Smax", "Green_trackbars"), cv2.getTrackbarPos("Vmax", "Green_trackbars")
        debugger.dgreen_min =	cv2.getTrackbarPos("Hmin", "Green_trackbars"), cv2.getTrackbarPos("Smin", "Green_trackbars"), cv2.getTrackbarPos("Vmin", "Green_trackbars")
        debugger.dgreenMaskFilterOn = cv2.getTrackbarPos("debugger.dilateErode", "Green_trackbars")
        debugger.dpink_max = cv2.getTrackbarPos("Hmax", "Pink_trackbars"), cv2.getTrackbarPos("Smax", "Pink_trackbars"), cv2.getTrackbarPos("Vmax", "Pink_trackbars")
        debugger.dpink_min =	cv2.getTrackbarPos("Hmin", "Pink_trackbars"), cv2.getTrackbarPos("Smin", "Pink_trackbars"), cv2.getTrackbarPos("Vmin", "Pink_trackbars")
        debugger.dpinkMaskFilterOn = cv2.getTrackbarPos("debugger.dilateErode", "Pink_trackbars")
        debugger.dred_max = cv2.getTrackbarPos("Hmax", "Red_trackbars"), cv2.getTrackbarPos("Smax", "Red_trackbars"), cv2.getTrackbarPos("Vmax", "Red_trackbars")
        debugger.dred_min = cv2.getTrackbarPos("Hmin", "Red_trackbars"), cv2.getTrackbarPos("Smin", "Red_trackbars"), cv2.getTrackbarPos("Vmin", "Red_trackbars")
        debugger.dredMaskFilterOn = cv2.getTrackbarPos("debugger.dilateErode", "Red_trackbars")

        colorTable = (debugger.dblue_team_min,debugger.dblue_team_max,
            debugger.dyellow_team_min,debugger.dyellow_team_max,
            debugger.dball_min,debugger.dball_max,
            debugger.dred_min,debugger.dred_max,
            debugger.dpink_min,debugger.dpink_max,
            debugger.dgreen_min,debugger.dgreen_max)

        if debugger.aimOn:
            cv2.circle(frame_debug, (int(x/2), int(y/2)), int(10), (255, 0, 0), 2)
        #dilate erode
        if debugger.blueMaskOn:
            blueMask = cv2.inRange(hsvFrame, debugger.dblue_team_min, debugger.dblue_team_max)
            if debugger.blueMaskFilterOn:
                blueMask = debugger.dilateErode(blueMask)

        if debugger.yellowMaskOn:
            yellowMask = cv2.inRange(hsvFrame, debugger.dyellow_team_min, debugger.dyellow_team_max)
            if debugger.yellowMaskFilterOn:
                yellowMask = debugger.dilateErode(yellowMask)

        if debugger.ballMaskOn:
            ballMask = cv2.inRange(hsvFrame, debugger.dball_min, debugger.dball_max)
            if debugger.ballMaskFilterOn:
                ballMask = debugger.dilateErodeBall(ballMask)

        if debugger.redMaskOn:
            redMask = cv2.inRange(hsvFrame, debugger.dred_min, debugger.dred_max)
            if debugger.redMaskFilterOn:
                redMask = debugger.dilateErode(redMask)

        if debugger.pinkMaskOn:
            pinkMask = cv2.inRange(hsvFrame, debugger.dpink_min, debugger.dpink_max)
            if debugger.pinkMaskFilterOn:
                pinkMask = debugger.dilateErode(pinkMask)

        if debugger.greenMaskOn:
            greenMask = cv2.inRange(hsvFrame, debugger.dgreen_min, debugger.dgreen_max)
            if debugger.greenMaskFilterOn:
                greenMask = debugger.dilateErode(greenMask)


        cv2.imshow("ballMask", ballMask)
        cv2.imshow("yellowMask", yellowMask)
        cv2.imshow("blueMask", blueMask)
        cv2.imshow("redMask", redMask)
        cv2.imshow("pinkMask", pinkMask)
        cv2.imshow("greenMask", greenMask)
        cv2.imshow("frame", frame)

        #output = [frame_RGB, hsvFrame, blueMask, yellowMask, ballMask]
        #for i in range(len(output)):
        #	cv2.imshow(str(output[i]), output[i])
        """
        #images output array

        titles = ["InputImage", "HSV Image", "Blue mask result", "Yellow mask result", "Ball mask result"]
        #Display in matplotlib
        for i in xrange(len(titles)):
            plt.subplot(2, 3, i+1)  # Try changing 1 by 2 and to 2 by 1
            plt.imshow(output[i])
            plt.title(titles[i])
            plt.xticks([])  # Comment this line
            plt.yticks([])  # Comment this line
        plt.show(block=False)
        print " END "
        """




    if cv2.waitKey(1) & 0xFF == ord('q'):
        #codigo pra salvar
        if shouldSave:
            picanha.save(colorTable)
        break


# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()