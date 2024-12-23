import socket
import serial
import time
import threading

class DMX_controller(object):
    def __init__(self,port="/dev/ttyUSB0"):
        self.universe_data = [0]*513  #the first item is the start bit so should not change. Therefore there are 513 values as 0 and then 1-512
        try:
            self.ser = serial.Serial(port,baudrate=250000,bytesize=8,stopbits=2) #Creates the serial connection
            self.working = True #self.working is used for light_display to tell if dmx is being send
        except Exception as e:
            self.working = False
            raise Exception("The serial is not working. Please make sure the lights are plugged in and that you don't have any other dmx scripts running and make sure the port is correct")


    def set_data(self,id,data):
        if isinstance(id,float): #checks if the id is a float
            raise Exception("The id needs to be an integer.")
            return
        try:
            id = int(id) #converts the id to an integer as this is required to send the dmx
        except:
            raise Exception("The id is not an integer. Please try again")
            return
        if id>512 or id<1: #checks if the id is in range
            raise Exception("The id value needs to be between 1 and 512 inclusive.")
            return
        # print(id)
        self.universe_data[id] = data #sets the value at address of id to data. It is not id-1 as the first bit is a start bit so remains as 0

    def send(self,universeData = None):
        if universeData is None: #checks if universe_data is passed as a paramater
            pass
        else:
            self.universe_data = universeData #allows the data to be send as a paramater into the function for example for send_full or send_zero
        self.ser.send_break(duration=92/1000000)
        time.sleep(12/1000000.0)
        try:
            self.ser.write(bytearray(self.universe_data)) #semds the data to the universe
        except:
            self.ser.close() #Closes the serial connection if it cannot write to the universe
            raise Exception("The serial cannot write. Check the cable is plugged in.")
        time.sleep(10/1000)

    def send_zero(self):
        universe_data = [0]*513 #sets all channels to off
        self.send(universe_data)

    def send_full(self):
        universe_data = [255]*512 #sets all channels to full intensity
        universe_data.insert(0,0)
        self.send(universe_data)

    def setColour(self, start_channel, r, g, b):
        self.set_data(start_channel, 255)
        self.set_data(start_channel + 1, r)
        self.set_data(start_channel + 2, g)
        self.set_data(start_channel + 3, b)

        
def flash(start_channels, r, g, b, duration = 0.5):
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
    flash([1], 255, 0, 0)

def green_flash():
    flash([1], 0, 255, 0) 


def send_dmx():
    global dmx
    while True:
        dmx.send()

if __name__ == "__main__":
    dmx = DMX_controller()
    t = threading.Thread(target=send_dmx)
    t.start()

    server = socket.socket()
    server.bind(("192.168.0.79", 12345))
    server.listen(4)
    client_socket, client_address = server.accept()
    print(client_address, "has connected")
    while True:
        recieved_data = client_socket.recv(256)
        client_socket.send("test")
        if recieved_data == "send_full":
            print("sending_full")
            dmx.send_full()
        elif recieved_data == "send_zero":
            print("sending zero")

            dmx.send_zero()
        elif recieved_data == "green_flash()":
            t2 = threading.Thread(target=green_flash)
            t2.start()
        elif recieved_data == "red_flash()":
            t2 = threading.Thread(target=red_flash)
            t2.start()
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
        print(recieved_data)