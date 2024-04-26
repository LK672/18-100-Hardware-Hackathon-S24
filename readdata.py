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
        self.dt = 1*(10**-1)
    
    def getCurrPos(self):
        return (self.x, self.y)
    
    def update(self, data):
        accelList = data.split(',')
        oldAx = self.ax
        oldAy = self.ay
        oldAz = self.az

        self.ax = float(accelList[0])
        self.ay = float(accelList[1])
        self.az = float(accelList[2])

        avgAx = (self.ax + oldAx)/2
        avgAy = (self.ay + oldAy)/2
        avgAz = (self.az + oldAz)/2

        oldVx = self.vx
        oldVy = self.vy
        oldVz = self.vz

        self.vx = (self.vx + avgAx*self.dt)
        self.vy = (self.vy + avgAy*self.dt)
        self.vz = (self.vz + avgAz*self.dt)

        avgVx = (self.vx + oldVx)/2
        avgVy = (self.vy + oldVy)/2
        avgVz = (self.vz + oldVz)/2

        self.x = self.x + avgVx*self.dt
        self.y = self.y + avgVy*self.dt


        # #if abs(self.ax*self.dt) > 0.05:
        # self.vx += self.ax*self.dt

        # #if abs(self.ay*self.dt) > 0.05:
        # self.vy += self.ay*self.dt
        
        # #if abs(self.az*self.dt) > 0.05:
        # self.vz += self.ay*self.dt

def readserial(comport, baudrate):

    ser = serial.Serial(comport, baudrate, timeout = 0.1)

    print("accelX,accelY,accelZ,gyroX,gyroY,gyroZ")
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

            print(f"{motionSensor.x}, '{motionSensor.y}")
            x, y = t.position()
            t.goto((x + motionSensor.x, y + motionSensor.y))
            #t.setpos((motionSensor.x*10, motionSensor.y*10))


    
if __name__ == '__main__':
    motionSensor = Motion()
    t = Turtle()
    # screen.title("Air Notes App")
    # screen.bgcolor("white")
    #w, h = getScreenResolution()
    w, h = 600, 600
    t.screen.setup(w, h, startx=50, starty=50)
    readserial('COM8', 115200)