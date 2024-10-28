from pyautogui import *
import pyautogui
import time
import keyboard
import random
import os


class ImageProcessor(object):
    def __init__(self):
        self.positionRegion = (126 - 50, 781 - 50, 364-126 + 100, 1011-781 + 100)
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
                # filePath = filePath[len(path) + 1 : -4]
                images.append(filePath)
            
        return images

    def runGame(self, positionChangeFunction):
        while self.racing:
            for image in self.positionImages:
                if pyautogui.locateOnScreen(image, grayscale=True, region = self.positionRegion, confidence=0.7):
                    positionChangeFunction(image)
            print("processing...")