import threading
from imageProcessor import ImageProcessor
from sendToPi import Raspberry_pi_manager

from getpass import getpass
password = getpass()
piManager = Raspberry_pi_manager("192.168.0.79", password)

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
    print("send")

def sendFinish():
    global piManager
    piManager.send_command("finish()")

def main():

    global piManager
    piManager.run_file()
    piManager.connect_client()
    imageProcessor = ImageProcessor()
    t = threading.Thread(target = imageProcessor.runGame, args=[sendPosition, sendStart, sendFinish])
    # imageProcessor.runGame(print)
    t.daemon = True
    t.start()
    t.join()
    # while True:
    #     pass

if __name__ == "__main__":
    main()