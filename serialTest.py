import time
import serial
import json
#TODO: add/change/remove number
ser = serial.Serial(
    port='/dev/ttyS0',
    baudrate = 9600,
    timeout = 1
    )


while True:
    ser.write(str.encode('AT'+'\r\n'))
    time.sleep(1)
    reply = ser.read(ser.inWaiting())
    print(reply)    
