import serial
from turtle import *
import win32api
import sys
import time

#import board
import busio

import digitalio

BTN_ADDR = 0x6f

# led = digitalio.DigitalInOut(board.LED)
# led.direction = digitalio.Direction.OUTPUT

# i2c = busio.I2C(scl = board.GP5, sda = board.GP4, frequency=100000)

pixelsPerMeter = 100
w, h = 600, 600

# def readBtnStatus():
#     data = bytearray(1)
#     while not i2c.try_lock():
#         time.sleep(0.1)
#     i2c.writeto(0x6f, bytearray([0x03]))
#     i2c.readfrom_into(0x6f, data)
#     i2c.unlock()
#     result = data[0] & 0x04
#     return result != 0

# def writeBtnLED(brightness, reg_addr):
#     while not i2c.try_lock():
#         time.sleep(0.1)
#     i2c.writeto(0x6f, bytearray([reg_addr, brightness]))
#     i2c.unlock()

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

        # if avgVx > 1.5:
        #     avgVx = 1.5
        # elif avgVx < -1.5:
        #     avgVx = -1.5
        if abs(self.vx) > 1.5:
            self.vx = self.vx/abs(self.vx) * 1.5
        avgVx = (self.vx + oldVx)/2
        # if avgVy > 1.5:
        #     avgVy = 1.5
        # elif avgVy < 1.5:
        #     avgVy = -1.5
        if abs(self.vy) > 1.5:
            self.vy = self.vy/abs(self.vy) * 1.5
        avgVy = (self.vy + oldVy)/2
        avgVz = (self.vz + oldVz)/2

        self.x = self.x + avgVx*self.dt
        if abs(self.x) >= ((w-50)/2)/pixelsPerMeter:
            self.x = self.x/abs(self.x)*((w-50)/2)/pixelsPerMeter
        self.y = self.y + avgVy*self.dt
        if abs(self.y) >= ((h-50)/2)/pixelsPerMeter:
            self.y = self.y/abs(self.y)*((h-50)/2)/pixelsPerMeter


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
    motionSensor.calibrate(ser)
    while True:
        t.screen.onkeypress(exit, "q")
        t.screen.listen()

        # if readBtnStatus():
        #     writeBtnLED(255, 0x19)
        #     t.pendown()
        # else:
        #     writeBtnLED(0, 0x19)
        #     t.penup()

        count += 1
        data = ser.readline().decode().strip()
        if data:
            motionSensor.update(data)
            print(data)

            print(f"{motionSensor.x}, '{motionSensor.y}")
            x, y = t.position()
            t.goto((motionSensor.x*pixelsPerMeter, motionSensor.y*pixelsPerMeter))
            #t.setpos((motionSensor.x*10, motionSensor.y*10))


    
if __name__ == '__main__':
    motionSensor = Motion()
    t = Turtle()
    # screen.title("Air Notes App")
    # screen.bgcolor("white")
    #w, h = getScreenResolution()
    t.screen.setup(w, h, startx=50, starty=50)
    readserial('COM8', 115200)