import threading
from imageProcessor import ImageProcessor
from sendToPi import Raspberry_pi_manager

piManager = Raspberry_pi_manager("192.168.0.79", None)

def sendPosition(imageFile):
    global piManager
    print(imageFile)
    position = imageFile.split("\\")[1][:-4]
    print(position)
    piManager.send_command(f"position({position})")

def sendStart(number):
    global piManager 
    print(number)
    if number == "GO":
        piManager.send_command("green_flash()")
    else:
        piManager.send_command("red_flash()")
    print("sned")

def main():

    global piManager

    piManager.connect_client()

    imageProcessor = ImageProcessor()
    t = threading.Thread(target = imageProcessor.runGame, args=[sendPosition, sendStart])
    # imageProcessor.runGame(print)
    t.start()
    t.join()
    # while True:
    #     pass

if __name__ == "__main__":
    main()