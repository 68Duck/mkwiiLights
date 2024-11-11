import socket
import serial
import time
import threading
import numpy as np 

class DMX_controller(object):
    def __init__(self,port="/dev/ttyUSB0", Cnumber=512,Brate=250000,Bsize=8,StopB=2):
        self.channel_num = Cnumber
        self.ser = serial.Serial(port,baudrate=Brate,bytesize=Bsize,stopbits=StopB)
        self.data = np.zeros([self.channel_num+1],dtype='uint8')
        self.data[0] = 0 # StartCode
        self.sleepms = 50.0
        self.breakus = 176.0
        self.MABus = 16.0


    def set_data(self,id,data):
        self.data[id] = data

    def send(self):
        self.ser.break_condition = True
        time.sleep(self.breakus/1000000.0)
        
        # Send MAB : 8us - 1s
        self.ser.break_condition = False
        time.sleep(self.MABus/1000000.0)
        
        # Send Data
        self.ser.write(bytearray(self.data))
        
        # Sleep
        time.sleep(self.sleepms/1000.0) # between 0 - 1 sec

    def send_zero(self):
        self.data = np.zeros([self.channel_num+1],dtype='uint8')

    def send_full(self):
        self.data = np.array([255] * (self.chanel_num + 1))
        self.data[0] = 0

    def setColour(self, start_channel, r, g, b):
        self.set_data(start_channel, 255)
        self.set_data(start_channel + 1, r)
        self.set_data(start_channel + 2, g)
        self.set_data(start_channel + 3, b)

        
def flash(start_channels, r, g, b, duration = 0.2):
    global dmx 
    dmx.send_zero()
    for start_channel in start_channels:
        dmx.set_data(start_channel, 255)
        dmx.set_data(start_channel + 1, r)
        dmx.set_data(start_channel + 2, g)
        dmx.set_data(start_channel + 3, b)
        dmx.send()
    time.sleep(duration)
    dmx.send_zero()

def red_flash():
    flash([1], 255, 0, 0, 0.3)

def green_flash():
    flash([1], 0, 255, 0, 1) 


def send_dmx():
    global dmx
    while True:
        dmx.send()

if __name__ == "__main__":
    dmx = DMX_controller()
    dmx.set_data(1, 255)
    dmx.set_data(2, 255)
    dmx.set_data(3, 255)
    dmx.set_data(4, 255)

    t = threading.Thread(target=send_dmx)
    t.start()


    server = socket.socket()
    server.bind(("192.168.0.79", 12345))
    server.listen(4)
    client_socket, client_address = server.accept()
    print(client_address, "has connected")
    while True:
        # dmx.send_zero()

        recieved_data = client_socket.recv(256)
        client_socket.send("test")
        if recieved_data == "send_full":
            print("sending_full")
            dmx.send_full()
        elif recieved_data == "send_zero":
            print("sending zero")

            dmx.send_zero()
        elif recieved_data == "finish()":
            print("Finished!")
            dmx.send_zero()
        elif recieved_data == "green_flash()":
            t2 = threading.Thread(target=green_flash)
            t2.start()
            t2.join()
        elif recieved_data == "red_flash()":
            t2 = threading.Thread(target=red_flash)
            t2.start()
            t2.join()
        elif recieved_data[0:len("position(")] == "position(":
            position = recieved_data[len("position(") : -3] #gets rid of the ) and th etc.
            position = int(position)
            colours = [(255, 0, 0),
                       (255, 128, 0),
                       (255, 255, 0),
                       (128, 255, 0),
                       (0, 255, 0),
                       (0, 255, 128),
                       (0, 255, 255),
                       (0, 128, 255),
                       (0, 0, 255),
                       (128, 0, 255),
                       (255, 0, 255),
                       (255, 0, 128)]
            colour = colours[position - 1]
            dmx.setColour(1, colour[0], colour[1], colour[2])
            # if position == "1":
            #     dmx.setColour(1, )
        else:
            dmx.set_data(1, 255)
            dmx.set_data(2, 255)
            dmx.set_data(3, 255)
            dmx.set_data(4, 255)
        print(recieved_data)