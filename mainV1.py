import time
import board
import busio
import digitalio

BTN_ADDR = 0x6f

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

ACCEL_ADDR = 0x6A

CTRL1_XL = 0x10  #Accelerometer conrol register
CTRL2_G = 0x11
CTRL3_C = 0x12
FIFO_DATA_OUT_L = 0x3E
TIMESTAMP0 = 0x49
STEP_COUNTER_L = 0x4B
STEP_COUNTER_H = 0x4C

TAP_CFG1 = 0x58
TAP_THS_6D = 0x59
INT_DUR2 = 0x5A
WAKE_UP_THS = 0x5B
MD1_CFG = 0x5E
FREE_FALL = 0x5D 
WAKE_UP_DUR = 0x5C
CTRL8_XL = 0x17

CTRL10_C = 0x19
OUTX_L_XL = 0x28
OUTY_L_XL = 0x2A
OUTZ_L_XL = 0x2C
CTRL9_XL = 0x18
TILT_IA = 0x3A
FUNC_SRC1 = 0x53
TIMESTAMP2 = 0x40
TIMESTAMP1 = 0x41
TIMESTAMP0 = 0x42

FIFO_CTRL1 = 0x06
FIFO_CTRL2 = 0x07
FIFO_CTRL3 = 0x08
FIFO_CTRL4 = 0x09
FIFO_CTRL5 = 0x0A
FIFO_STATUS1 = 0x3A
FIFO_STATUS2 = 0x3B
OUT_TEMP_L = 0x20
OUT_X_L_G = 0x22
OUT_X_L_XL = 0x28
STEP_COUNTER_L = 0x4B
TIMESTAMP0 = 0x40
TIMESTAMP1 = 0x41
TIMESTAMP2 = 0x42
FIFO_SRC = 0x3F
FUNC_CFG_ACCESS = 0x01
WHO_AM_I = 0x07
# acceleromter scale
FSR_2G = 16384.0  # FSR for 2G mode
FSR_4G = 8192.0   # FSR for 4G mode
FSR_8G = 4096.0   # FSR for 8G mode
FSR_16G = 2048.0  # FSR for 16G mode

i2c = busio.I2C(scl=board.GP5, sda=board.GP4, frequency=100000)

def read_accelerometer_data(FSR):
    # Get accelerometer data
    while not i2c.try_lock():
        time.sleep(0.1)
    dataArr = bytearray(6)
    i2c.readfrom_into(ACCEL_ADDR, dataArr)
    #data = i2c.readfrom_mem(ADDRESS, OUTX_L_XL, 6)
    # Convert data to G units
    i2c.unlock()
    x = (dataArr[1] << 8 | dataArr[0]) / FSR
    y = (dataArr[3] << 8 | dataArr[2]) / FSR
    z = (dataArr[5] << 8 | dataArr[4]) / FSR
    # Output values
    print('X: {} G, Y: {} G, Z: {} G'.format(x, y, z))

def get_acceleration():
    while not i2c.try_lock():
        time.sleep(0.1)
    # Read X-axis acceleration from accelerometer
    xArr = bytearray(2)
    i2c.readfrom_into(ACCEL_ADDR, xArr)
    x_accel = (int(xArr[0]) * 9.81) / (256 * 4)
    
    yArr = bytearray(2)
    i2c.readfrom_into(ACCEL_ADDR, yArr)
    y_accel = (int(xArr[0]) * 9.81) / (256 * 4)
    
    zArr = bytearray(2)
    i2c.readfrom_into(ACCEL_ADDR, zArr)
    z_accel = (int(zArr[0]) * 9.81) / (256 * 4)
    
    i2c.unlock()
    
    return x_accel, y_accel, z_accel


while True:
    #read_accelerometer_data(FSR_16G)
    x, y, z = get_acceleration()
    print('X: {} m/s^2, Y: {} m/s^2, Z: {} m/s^2'.format(x, y, z))
    time.sleep(0.1)











