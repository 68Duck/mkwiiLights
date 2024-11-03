from pyautogui import *
import pyautogui
import time
import keyboard
import random
import os
from PIL import Image

class ImageProcessor(object):
    def __init__(self):
        self.positionRegion = (126 - 50, 781 - 50, 300, 250)
        self.startRegion = (788, 467, 1105-788, 613-467 +20)
        self.powerupRegion = (118, 75, 310-118 + 50, 238-75 + 50)

        self.positionImages = self.getImagesFromDirectory("positionImages")
        self.startingImages = self.getImagesFromDirectory("startingImages")
        self.powerupImages = self.getImagesFromDirectory("powerupImages")

        self.racing = True

    def getImagesFromDirectory(self,dir):
        images = []
        for root, dirs, files in os.walk(dir):
            for file in files:
                filePath = os.path.join(root, file)
                images.append(filePath)
                # im = Image.open(filePath)
                # print(im.size)

            
        return images

    def runGame(self, positionChangeFunction, startFunction, finishFunction):
        self.starting = True
        currentNumber = 3
        try:
            while True:
                while self.starting:
                    if currentNumber == 3:
                        if pyautogui.locateOnScreen("startingImages\\actual3.PNG", grayscale=True, region = (934, 504, 37, 50), confidence=0.8):
                            print("3test")
                            startFunction("3")
                            currentNumber = 2
                            continue
                    if currentNumber == 2:
                        if pyautogui.locateOnScreen("startingImages\\actual2.PNG", grayscale=True, region = (945, 496, 51, 15), confidence=0.8):
                            print("2test")
                            startFunction("2")
                            currentNumber = 1
                            continue
                    if currentNumber == 1:
                        if pyautogui.locateOnScreen("startingImages\\actual1.PNG", grayscale=True, region = (941, 498, 20, 32), confidence=0.8):
                            print("1test")
                            startFunction("1")
                            currentNumber = 0
                            continue
                    if currentNumber == 0:
                        if pyautogui.locateOnScreen("startingImages\\actualGo.PNG", grayscale=True, region = (869, 524, 24, 30), confidence=0.8):
                            print("GO!")
                            startFunction("GO")
                            currentNumber = 3
                            self.starting = False
                            self.racing = True
                            break

                    # print("testing", currentNumber)
                    # for image in self.startingImages:
                        # if pyautogui.locateOnScreen(image, grayscale=True, region = self.startRegion, confidence=0.8):
                        #     print(image)
                        #     if image == "startingImages\\GO.PNG":
                        #         starting = False
                        #         break
                    print("test")
                while self.racing:
                    for image in self.positionImages:
                        if pyautogui.locateOnScreen(image, grayscale=True, region = self.positionRegion, confidence=0.7):
                            positionChangeFunction(image)
                            break
                    print("processing...")
                    if pyautogui.locateOnScreen("startingImages\\actualFinish.PNG", grayscale=True, region = (1011, 494, 33, 39), confidence=0.8):
                        print("FINISH!")
                        finishFunction()
                        self.racing = False
                        self.starting = True
                        break
        except (KeyboardInterrupt):
            print("Keyboard interrupt")