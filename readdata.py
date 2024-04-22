import serial
from turtle import Turtle
import win32api

def get_screen_resolution():
    width = win32api.GetSystemMetrics(0)
    height = win32api.GetSystemMetrics(1)
    return width, height

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

        self.vx += self.ax*self.dt
        if abs(self.vx <= 0.1):
            self.vx = 0
        self.vy += self.ay*self.dt
        if abs(self.vy <= 0.1):
            self.vy = 0
        self.vz += self.az*self.dt
        if abs(self.vz <= 0.1):
            self.vz = 0

        self.x += self.vx*self.dt
        self.y += self.vy*self.dt
        self.z += self.vz*self.dt

def readserial(comport, baudrate):

    ser = serial.Serial(comport, baudrate, timeout = 0.1)

    print("temp,accelX,accelY,accelZ,gyroX,gyroY,gyroZ")
    while True:
        data = ser.readline().decode().strip()
        if data:
            motionSensor.update(data)
            print(f"{motionSensor.vx}")
    
if __name__ == '__main__':
    motionSensor = Motion()
    t = Turtle()
    t.screen.title("Air Notes App")
    t.screen.bgcolor("white")
    readserial('COM6', 115200)