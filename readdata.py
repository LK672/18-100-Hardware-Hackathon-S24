import serial
from turtle import *
import win32api
import sys
import time

pixelsPerMeter = 100
w, h = 600, 600

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
        self.xoffset = 0
        self.yoffset = 0
        self.zoffset = 0
        self.dt = 1*(10**-1)
        self.btnStatus = 0
        self.press = False
        self.release = False
        self.oldStatus = 0
        self.btnPressTime = 0

        self.btnFirstPressTime = 0
    
    def getCurrPos(self):
        return (self.x, self.y)
    
    def calibrate(self, ser):
        xList = []
        yList = []
        zList = []
        start = time.time()
        while (time.time() - start < 5):
            data = ser.readline().decode().strip()
            if data:
                aList = data.split(',')
                xList.append(float(aList[0]))
                yList.append(float(aList[1]))
                zList.append(float(aList[2]))
        xSum = 0
        ySum = 0
        zSum = 0
        for i in range(len(xList)):
            xSum += xList[i]
            ySum += yList[i]
            zSum += zList[i]
        self.xoffset = xSum/len(xList)
        self.yoffset = ySum/len(yList)
        self.zoffset = zSum/len(zList)
    
    def isDoublePressed(self):
        return self.press and time.time() - self.btnPressTime < 0.5

    def update(self, data):
        accelList = data.split(',')

        oldAx = self.ax
        oldAy = self.ay
        oldAz = self.az

        oldVx = self.vx
        oldVy = self.vy
        oldVz = self.vz

        self.ax= float(accelList[0]) - self.xoffset
        self.ay = float(accelList[1]) - self.yoffset
        self.az = float(accelList[2]) - self.zoffset

        if abs(self.ax) < 0.5:
            self.ax = 0
        if abs(self.ay) < 1:
            self.ay = 0
        if abs(self.vx) < 0.5:
            self.vx = 0
        if abs(self.vy) < 1:
            self.vy = 0

        avgAx = (self.ax + oldAx)/2
        avgAy = (self.ay + oldAy)/2
        avgAz = (self.az + oldAz)/2

        self.vx = (self.vx + avgAx*self.dt)
        self.vy = (self.vy + avgAy*self.dt)
        self.vz = (self.vz + avgAz*self.dt)

        if abs(self.vx) > 1.5:
            self.vx = self.vx/abs(self.vx) * 1.5
        avgVx = (self.vx + oldVx)/2
       
        if abs(self.vy) > 1.5:
            self.vy = self.vy/abs(self.vy) * 1.5
        avgVy = (self.vy + oldVy)/2

        self.x = self.x + avgVx*self.dt
        if abs(self.x) >= ((w-50)/2)/pixelsPerMeter:
            self.x = self.x/abs(self.x)*((w-50)/2)/pixelsPerMeter
        self.y = self.y + avgVy*self.dt
        if abs(self.y) >= ((h-50)/2)/pixelsPerMeter:
            self.y = self.y/abs(self.y)*((h-50)/2)/pixelsPerMeter

        self.btnStatus = int(accelList[-1])

        

def readserial(comport, baudrate):
    ser = serial.Serial(comport, baudrate, timeout = 0.1)

    t.penup()
    print("Calibrating...")
    motionSensor.calibrate(ser)
    print("Calibration Complete")
    while True:
        t.screen.onkeypress(exit, "q")
        t.screen.listen()

        if motionSensor.btnStatus == 1 and motionSensor.btnFirstPressTime == 0:
            motionSensor.btnFirstPressTime = time.time()
            btnPressList = [1]
        
        if time.time() - motionSensor.btnFirstPressTime <= 0.5:
            btnPressList.append(motionSensor.btnStatus)
            zeroIndex = -1
            for i in range(len(btnPressList)):
                if btnPressList[i] == 0:
                    zeroIndex = i
                    break
            print(btnPressList)
            if zeroIndex != -1 and btnPressList[zeroIndex:].count(1) > 0:
                print('undo')
                t.clear()
        elif time.time() - motionSensor.btnFirstPressTime > 0.7:
            motionSensor.btnFirstPressTime = 0
            btnPressList = []
        data = ser.readline().decode().strip()
        if data:
            motionSensor.update(data)
            t.goto((motionSensor.x*pixelsPerMeter, motionSensor.y*pixelsPerMeter))
            if motionSensor.btnStatus == 1:
                t.pendown()
            else:
                t.penup()
        motionSensor.oldStatus = motionSensor.btnStatus

    
if __name__ == '__main__':
    motionSensor = Motion()
    t = Turtle()
    t.screen.setup(w, h, startx=50, starty=50)
    readserial('COM8', 115200)