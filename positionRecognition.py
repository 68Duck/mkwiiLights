from pyautogui import *
import pyautogui
import time
import keyboard
import random
import os

def getImagesFromDirectory(dir):
    images = []
    for root, dirs, files in os.walk(dir):
        for file in files:
            filePath = os.path.join(root, file)
            # filePath = filePath[len(path) + 1 : -4]
            images.append(filePath)
        
    return images

positionRegion = (126 - 50, 781 - 50, 364-126 + 100, 1011-781 + 100)
startRegion = (788, 467, 1105-788, 613-467 +20)
powerupRegion = (118, 75, 310-118 + 50, 238-75 + 50)
print(startRegion)

positionImages = getImagesFromDirectory("positionImages")
startingImages = getImagesFromDirectory("startingImages")
powerupImages = getImagesFromDirectory("powerupImages")
if __name__ == "__main__":
    print(positionImages)
    print(startingImages)
    starting = False
    while starting:
        for image in startingImages:
            if pyautogui.locateOnScreen(image, grayscale=True, region = startRegion, confidence=0.8):
                print(image)
                if image == "startingImages\\GO.PNG":
                    starting = False
                    break
                # print(image[len(path) + 1 : -4])
                
            # print("test")
    racing = True
    starHappened = False
    displayStar = False
    while racing:
        for image in positionImages:
            if pyautogui.locateOnScreen(image, grayscale=True, region = positionRegion, confidence=0.7):
                print(image)


        for image in powerupImages:
            currentlyStar = False
            if pyautogui.locateOnScreen(image, grayscale=True, region = powerupRegion, confidence=0.7):
                print(image)
                if image == "powerupImages\star.PNG":
                    starHappened = True
                    currentlyStar = True
            if starHappened and not currentlyStar:
                starStart = time.time()
                displayStar = True
                starHappened = False
        if displayStar:
            print(starStart, time.time())
            if time.time() > starStart + 7:
                displayStar = False

            
        print("test", displayStar)

