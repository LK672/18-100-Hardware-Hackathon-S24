import serial

def readserial(comport, baudrate):

    ser = serial.Serial(comport, baudrate, timeout = 0.1)

    print("temp,accelX,accelY,accelZ,gyroX,gyroY,gyroZ")
    while True:
        data = ser.readline().decode().strip()
        if data:
            print(data)
    
if __name__ == '__main__':

    readserial('COM6', 115200)