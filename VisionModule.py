import numpy as np
import cv2
import time
from Vector2 import *
from Picanha import Picanha


class Vision:
    def __init__(self, correctPerspectiveIsActive=1, src=0):
        # HSV Parameters
        self.blue_team_min = (100, 160, 150)
        self.blue_team_max = (140, 255, 255)
        self.yellow_team_min = (15, 80, 180)
        self.yellow_team_max = (60, 255, 255)
        self.ball_min = (15, 85, 207)
        self.ball_max = (22, 255, 255)
        self.red_min = (176, 105, 235)
        self.red_max = (179, 255, 255)
        self.pink_min = (140, 99, 200)
        self.pink_max = (170, 255, 255)
        self.green_min = (75, 90, 135)
        self.green_max = (90, 255, 255)
        # Empty vars for not crashing
        self.redPoint = (0, 0)
        self.pinkPoint = (0, 0)
        self.greenPoint = (0, 0)
        self.redPrimaryColor = (0, 0)
        self.pinkPrimaryColor = (0, 0)
        self.greenPrimaryColor = (0, 0)

        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.currentTeamColor = "blue"
        self.yellowTeamCenter = []
        self.blueTeamCenter = []
        self.detectionRadius = 15
        self.tempo = time.time()
        self.fps = 0

        self.ASPECT_RATIO = (420, 480)  # h,w
        self.picanha = Picanha()
        self.updateColorParamenters(self.picanha.load())
        self.correctPerspectiveIsActive = correctPerspectiveIsActive
        self.src = src
        if self.correctPerspectiveIsActive:
            self.correctPerspectiveFirstTime()
        else:
            self.updatePointsForTransfromPerspective()

    def debugVisual(self, imgToDrawDebug):
        self.debugImage = imgToDrawDebug
        self.count = 0
        for centerY in self.yellowTeamCenter:
            cv2.circle(self.debugImage, centerY, int(15), (30, 120, 120), 1)
            self.drawDebugText(self.debugImage, "Y" + str(self.count + 1) + ":" + str(centerY), 10, 50 + self.count * 25)
            self.count += 1

        self.count = 0
        for centerB in self.blueTeamCenter:
            cv2.circle(self.debugImage, centerB, int(15), (110, 120, 120), 1)
            self.drawDebugText(self.debugImage, "B" + str(self.count + 1) + ":" + str(centerB), 10, 125 + self.count * 25)
            self.count += 1

        self.drawDebugText(self.debugImage, "RP" + str(self.count + 1) + ":" + str(self.redPoint), 10, 200)
        self.drawDebugText(self.debugImage, "PP" + str(self.count + 1) + ":" + str(self.pinkPoint), 10, 225)
        self.drawDebugText(self.debugImage, "GP" + str(self.count + 1) + ":" + str(self.greenPoint), 10, 250)
        self.drawDebugText(self.debugImage, "ball:" + str(self.ballCenter), 10, 20)
        self.drawDebugText(self.debugImage, self.fps, 420, 20)
        cv2.circle(self.debugImage, self.ballCenter, int(15), (10, 120, 120), 1)

        # Lines
        cv2.line(self.debugImage, self.redPoint, self.redPrimaryColor, (255, 255, 255), 2)
        cv2.line(self.debugImage, self.pinkPoint, self.pinkPrimaryColor, (255, 255, 255), 2)
        cv2.line(self.debugImage, self.greenPoint, self.greenPrimaryColor, (255, 255, 255), 2)

        return self.debugImage

    def updateFPS(self):
        self.tempo = time.time()

    def getFPS(self):
        self.fps = 1 / (time.time() - self.tempo)
        print "FPS: ", self.fps

    def updatePointsForTransfromPerspective(self):
        self.M = self.picanha.load("pointsM")
        print "self.M contains= "+str(self.M)

    def updateColorParamenters(self, loadedTable):
        colorTable = loadedTable
        self.blue_team_min = colorTable[0]
        self.blue_team_max = colorTable[1]
        self.yellow_team_min = colorTable[2]
        self.yellow_team_max = colorTable[3]
        self.ball_min = colorTable[4]
        self.ball_max = colorTable[5]
        self.red_min = colorTable[6]
        self.red_max = colorTable[7]
        self.pink_min = colorTable[8]
        self.pink_max = colorTable[9]
        self.green_min = colorTable[10]
        self.green_max = colorTable[11]
        print "color parements updated"

    def setTeamColor(self, teamColor):
        self.currentTeamColor = str(teamColor)

    def medianBlur(self, img):
        self.img = cv2.medianBlur(img, 5)
        return self.img

    def convertHSV(self, img):
        self.img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        return self.img

    def convertBGR(self, img):
        self.img = cv2.cvtColor(img, cv2.COLOR_HSV2BGR)
        return self.img

    def erodeDilate(self, img):
        if 0:
            bufferImg = cv2.erode(img, None, iterations=1)
            bufferImg = cv2.dilate(bufferImg, None, iterations=1)
            return bufferImg
        else:
            return img

    def findBlueTeam(self, img):
        self.img = img
        self.mask = cv2.inRange(img, self.blue_team_min, self.blue_team_max)
        #self.mask = cv2.erode(self.mask, None, iterations=1)
        #self.mask = cv2.dilate(self.mask, None, iterations=1)
        self.mask = self.erodeDilate(self.mask)
        cnts = cv2.findContours(self.mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None
        centerList = []
        arrayTeste = []
        if len(cnts) > 0:
            for cnt in cnts:
                # c=max(cnts, key=cv2.contourArea)
                ((x, y), radius) = cv2.minEnclosingCircle(cnt)
                # arrayTeste.append([[center], radius])
                M = cv2.moments(cnt)
                if M["m00"] != 0:
                    cx = int(M['m10'] / M['m00'])
                    cy = int(M['m01'] / M['m00'])
                else:
                    cx, cy = 0, 0
                center = (cx, cy)
                if radius > 5:
                    # cv2.circle(self.img, (int(x), int(y)), int(radius+5), (255, 0, 0), 2)
                    # cv2.circle(self.img, center, 5, (0, 0, 255), -1)
                    arrayTeste.append([[center], radius])
                    centerList.append(center)
            # implementar codigo para elimnar falsos jogadores
            # escolher apenas os que possuem o maior raio
            if len(arrayTeste) > 3:
                print "Mais do que 3 possiveis jogadores azuis foram encontrados"
                radiusList = []
                for counter in range(len(arrayTeste)):
                    radiusList.append(arrayTeste[counter][1])
                print "blue radiusList: "
                print radiusList
            # debug prints
            """
            print "len = " + str(len(arrayTeste))
            print arrayTeste
            print arrayTeste[0]
            print arrayTeste[0][0]
            """
        self.blueTeamCenter = centerList[:]
        # print "This is self.blueTeamCenter var value = "+str(self.blueTeamCenter)+" and this is centerList = "+str(centerList)
        return self.img, centerList

    def findYellowTeam(self, img):
        self.img = img
        self.mask = cv2.inRange(img, self.yellow_team_min, self.yellow_team_max)
        #self.mask = cv2.erode(self.mask, None, iterations=1)
        #self.mask = cv2.dilate(self.mask, None, iterations=1)
        self.mask = self.erodeDilate(self.mask)
        cnts = cv2.findContours(self.mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None
        arrayTeste = []
        centerList = []
        if len(cnts) > 0:
            for cnt in cnts:
                # c=max(cnts, key=cv2.contourArea)
                ((x, y), radius) = cv2.minEnclosingCircle(cnt)
                # arrayTeste.append([[center], radius])
                M = cv2.moments(cnt)
                if M["m00"] != 0:
                    cx = int(M['m10'] / M['m00'])
                    cy = int(M['m01'] / M['m00'])
                else:
                    cx, cy = 0, 0
                center = (cx, cy)
                if radius > 5:
                    # cv2.circle(self.img, (int(x), int(y)), int(radius+5), (255, 0, 0), 2)
                    # cv2.circle(self.img, center, 5, (0, 0, 255), -1)
                    arrayTeste.append([[center], radius])
                    centerList.append(center)
            # implementar codigo para elimnar falsos jogadores
            # escolher apenas os que possuem o maior raio
            if len(arrayTeste) > 3:
                print "Mais do que 3 possiveis jogadores amarelos foram encontrados"
                radiusList = []
                for counter in range(len(arrayTeste)):
                    radiusList.append(arrayTeste[counter][1])
                print "yellow radiusList: "
                print radiusList
            # debug prints
            """
            print "len = " + str(len(arrayTeste))
            print arrayTeste
            print arrayTeste[0]
            print arrayTeste[0][0]
            """
        self.yellowTeamCenter = centerList[:]
        return self.img, centerList

    def findBall(self, img):
        self.img = img
        self.mask = cv2.inRange(img, self.ball_min, self.ball_max)
        #self.mask = cv2.erode(self.mask, None, iterations=1)
        self.mask = cv2.dilate(self.mask, None, iterations=2)
        #self.mask = self.erodeDilate(self.mask)
        cnts = cv2.findContours(self.mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None

        if len(cnts) > 0:
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            # print "This is the ball radius: "+str(radius)
            M = cv2.moments(c)
            if M["m00"] != 0:
                cx = int(M['m10'] / M['m00'])
                cy = int(M['m01'] / M['m00'])
            else:
                cx, cy = 0, 0
            center = (cx, cy)
        # cv2.circle(self.img, (int(x), int(y)), int(radius+5), (255, 130, 0), 2)
        # cv2.circle(self.img, center, 5, (255, 130, 0), -1)
        self.ballCenter = center
        return self.img, center

    def findRedPlayer(self, img):
        self.img = img
        self.mask = cv2.inRange(img, self.red_min, self.red_max)
        #self.mask = cv2.erode(self.mask, None, iterations=1)
        #self.mask = cv2.dilate(self.mask, None, iterations=1)
        self.mask = self.erodeDilate(self.mask)
        cnts = cv2.findContours(self.mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None
        centerList = []
        if len(cnts) > 0:
            for cnt in cnts:
                ((x, y), radius) = cv2.minEnclosingCircle(cnt)
                M = cv2.moments(cnt)
                if M["m00"] != 0:
                    cx = int(M['m10'] / M['m00'])
                    cy = int(M['m01'] / M['m00'])
                else:
                    cx, cy = 0, 0
                center = (cx, cy)
                if radius > 2:
                    # cv2.circle(self.img, (int(x), int(y)), int(radius+5), (0, 100, 0), 1)
                    # cv2.circle(self.img, center, 5, (0, 0, 255), -1)
                    centerList.append(center)
            # print centerList

            if self.currentTeamColor == "blue":
                for point in centerList:
                    for player in self.blueTeamCenter:
                        playerVector = Vector2(player[0], player[1])
                        pointVector = Vector2(point[0], point[1])
                        distance = (playerVector - pointVector).tamanho()
                        # print "result: "+str(distance)
                        if distance < self.detectionRadius:
                            self.redPrimaryColor = player
                            self.redPoint = point
                            return player, point

            # else = cor do time e yellow
            else:
                for point in centerList:
                    for player in self.yellowTeamCenter:
                        playerVector = Vector2(player[0], player[1])
                        pointVector = Vector2(point[0], point[1])
                        distance = (playerVector - pointVector).tamanho()
                        # print "result: "+str(distance)
                        if distance < self.detectionRadius:
                            self.redPrimaryColor = player
                            self.redPoint = point
                            return player, point
        return None, None

    def findPinkPlayer(self, img):
        self.img = img
        self.mask = cv2.inRange(img, self.pink_min, self.pink_max)
        #self.mask = cv2.erode(self.mask, None, iterations=1)
        #self.mask = cv2.dilate(self.mask, None, iterations=1)
        self.mask = self.erodeDilate(self.mask)
        cnts = cv2.findContours(self.mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None
        centerList = []
        if len(cnts) > 0:
            for cnt in cnts:
                ((x, y), radius) = cv2.minEnclosingCircle(cnt)
                M = cv2.moments(cnt)
                if M["m00"] != 0:
                    cx = int(M['m10'] / M['m00'])
                    cy = int(M['m01'] / M['m00'])
                else:
                    cx, cy = 0, 0
                center = (cx, cy)
                if radius > 2:
                    # cv2.circle(self.img, (int(x), int(y)), int(radius+5), (0, 100, 0), 1)
                    # cv2.circle(self.img, center, 5, (0, 0, 255), -1)
                    centerList.append(center)
            # print centerList

            if self.currentTeamColor == "blue":
                for point in centerList:
                    for player in self.blueTeamCenter:
                        playerVector = Vector2(player[0], player[1])
                        pointVector = Vector2(point[0], point[1])
                        distance = (playerVector - pointVector).tamanho()
                        # print "result: "+str(distance)
                        if distance < self.detectionRadius:
                            self.pinkPrimaryColor = player
                            self.pinkPoint = point
                            return player, point

            # else = cor do time e yellow
            else:
                for point in centerList:
                    for player in self.yellowTeamCenter:
                        playerVector = Vector2(player[0], player[1])
                        pointVector = Vector2(point[0], point[1])
                        distance = (playerVector - pointVector).tamanho()
                        # print "result: "+str(distance)
                        if distance < self.detectionRadius:
                            self.pinkPrimaryColor = player
                            self.pinkPoint = point
                            return player, point
        return None, None

    def findGreenPlayer(self, img):
        self.img = img
        self.mask = cv2.inRange(img, self.green_min, self.green_max)
        #self.mask = cv2.erode(self.mask, None, iterations=1)
        #self.mask = cv2.dilate(self.mask, None, iterations=1)
        self.mask = self.erodeDilate(self.mask)
        cnts = cv2.findContours(self.mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None
        centerList = []
        if len(cnts) > 0:
            for cnt in cnts:
                ((x, y), radius) = cv2.minEnclosingCircle(cnt)
                M = cv2.moments(cnt)
                if M["m00"] != 0:
                    cx = int(M['m10'] / M['m00'])
                    cy = int(M['m01'] / M['m00'])
                else:
                    cx, cy = 0, 0
                center = (cx, cy)
                if radius > 2:
                    # cv2.circle(self.img, (int(x), int(y)), int(radius+5), (0, 100, 0), 1)
                    # cv2.circle(self.img, center, 5, (0, 0, 255), -1)
                    centerList.append(center)
            # print centerList

            if self.currentTeamColor == "blue":
                for point in centerList:
                    for player in self.blueTeamCenter:
                        playerVector = Vector2(player[0], player[1])
                        pointVector = Vector2(point[0], point[1])
                        distance = (playerVector - pointVector).tamanho()
                        # print "result: "+str(distance)
                        if distance < self.detectionRadius:
                            self.greenPrimaryColor = player
                            self.greenPoint = point
                            return player, point

            # else = cor do time e yellow
            else:
                for point in centerList:
                    for player in self.yellowTeamCenter:
                        playerVector = Vector2(player[0], player[1])
                        pointVector = Vector2(point[0], point[1])
                        distance = (playerVector - pointVector).tamanho()
                        # print "result: "+str(distance)
                        if distance < self.detectionRadius:
                            self.greenPrimaryColor = player
                            self.greenPoint = point
                            return player, point
        return None, None

    def drawDebugText(self, img, text, pos_x, pos_y):
        cv2.putText(img, str(text), (pos_x, pos_y), self.font, .5, (255, 255, 255), 1)

    def draw_circle(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDBLCLK:
            cv2.circle(self.img, (x, y), 0, (255, 0, 0), -1)
            self.pts[self.pointIndex] = (x, y)
            self.pointIndex = self.pointIndex + 1

    def selectFourPoints(self):
        print "Please select 4 points, by double clicking on each of them in the order: \n\
        top left, top right, bottom left, bottom right."

        while (self.pointIndex != 4):
            cv2.imshow('image', self.img)
            key = cv2.waitKey(20) & 0xFF
            if key == 27:
                return False
        if self.pointIndex == 4:
            self.mouseClicksFinished = 1
            return True

    def correctPerspectiveFirstTime(self):
        cap = cv2.VideoCapture(self.src)
        ret, self.img = cap.read()
        while ret != 1:
            ret, self.img = cap.read()
        self.pts = [(0, 0), (0, 0), (0, 0), (0, 0)]
        self.pointIndex = 0

        self.pts2 = np.float32([[0, 0], [self.ASPECT_RATIO[1], 0], [0, self.ASPECT_RATIO[0]],
                                [self.ASPECT_RATIO[1], self.ASPECT_RATIO[0]]])
        cv2.namedWindow('image')
        cv2.setMouseCallback('image', self.draw_circle)
        self.mouseClicksFinished = 0
        if self.correctPerspectiveIsActive:
            while (self.mouseClicksFinished == 0):
                if (self.selectFourPoints()):
                    # The four points of the A4 paper in the image
                    self.pts1 = np.float32([\
                        [self.pts[0][0], self.pts[0][1]],\
                        [self.pts[1][0], self.pts[1][1]],\
                        [self.pts[2][0], self.pts[2][1]],\
                        [self.pts[3][0], self.pts[3][1]]])

                    self.M = cv2.getPerspectiveTransform(self.pts1, self.pts2)
                    self.picanha.save(self.M, name="pointsM")
                    cap.release()
                    cv2.destroyAllWindows()
                    time.sleep(2)

    def applyPerspectiveCorrection(self, img):
        self.transformedImage = cv2.warpPerspective(img, self.M, (self.ASPECT_RATIO[1], self.ASPECT_RATIO[0]))
        return self.transformedImage
