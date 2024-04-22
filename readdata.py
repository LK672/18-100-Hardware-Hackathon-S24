import serial
from turtle import *
import win32api
import sys

def getScreenResolution():
    width = win32api.GetSystemMetrics(0)
    height = win32api.GetSystemMetrics(1)
    return width, height

def exit():
    sys.exit()

class Motion:
    def __init__(self):
        self.ax = 0
        self.ay = 0
        self.az = 0
        self.vx = 0
        self.vy = 0
        self.vz = 0
        self.x = 0
        self.y = 0 
        self.z = 0
        self.dt = 1*(10**-2)
    
    def getCurrPos(self):
        return (self.x, self.y)
    
    def update(self, data):
        accelList = data.split(',')
        self.ax = round(float(accelList[0]))
        self.ay = round(float(accelList[1]))
        self.az = round(float(accelList[2]))

        if abs(self.ax*self.dt) > 0.05:
            self.vx += self.ax*self.dt

        if abs(self.ay*self.dt) > 0.05:
            self.vy += self.ay*self.dt
        
        if abs(self.az*self.dt) > 0.05:
            self.vz += self.ay*self.dt

        self.x = self.x + self.vx*self.dt + 0.5*self.ax*(self.dt**2)
        self.y = self.y + self.vy*self.dt + 0.5*self.ay*(self.dt**2)

def readserial(comport, baudrate):

    ser = serial.Serial(comport, baudrate, timeout = 0.1)

    print("temp,accelX,accelY,accelZ,gyroX,gyroY,gyroZ")
    t.pendown()
    count = 0
    while True:
        t.screen.onkeypress(exit, "q")
        t.screen.listen()
        count += 1

        data = ser.readline().decode().strip()
        if data:
            motionSensor.update(data)
            print(data)

            #print(f"{motionSensor.x}")
            #print(f"{motionSensor.y}")
            t.goto(motionSensor.x, motionSensor.y)


    
if __name__ == '__main__':
    motionSensor = Motion()
    t = Turtle()
    # screen.title("Air Notes App")
    # screen.bgcolor("white")
    w, h = getScreenResolution()
    t.screen.setup(w, h, startx=50, starty=50)
    readserial('COM6', 115200)