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

    def runGame(self, positionChangeFunction, startFunction):
        self.starting = True
        currentNumber = 3
        while self.starting:
            if currentNumber == 3:
                if pyautogui.locateOnScreen("startingImages\\3test.PNG", grayscale=True, region = (934, 498, 40, 61), confidence=0.8):
                    print("3test")
                    startFunction("3")
                    currentNumber = 2
                    continue
            if currentNumber == 2:
                if pyautogui.locateOnScreen("startingImages\\2test.PNG", grayscale=True, region = (945, 546, 25, 53), confidence=0.8):
                    print("2test")
                    startFunction("2")
                    currentNumber = 1
                    continue
            if currentNumber == 1:
                if pyautogui.locateOnScreen("startingImages\\1test.PNG", grayscale=True, region = (918, 496, 45, 39), confidence=0.8):
                    print("1test")
                    startFunction("1")
                    currentNumber = 0
                    continue
            if currentNumber == 0:
                if pyautogui.locateOnScreen("startingImages\\goTest.PNG", grayscale=True, region = (885, 506, 28, 46), confidence=0.8):
                    print("GO!")
                    startFunction("GO")
                    currentNumber = 3
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