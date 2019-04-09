import time
import serial
import json
#TODO: add/change/remove number
ser = serial.Serial(
    port='/dev/ttyS0',
    baudrate = 9600,
    timeout = 1
    )

def sendSMS(message):
    with open('/home/pi/BeeHiveMonitoring/Numbers.json','r') as n:
        numbers = json.load(n)
        print("Sending message to:")
        for number in numbers["Numbers"]:
            print(number)
    for number in numbers["Numbers"]:
        ser.write(str.encode('AT'+'\r\n'))
        time.sleep(1)
        reply = ser.read(ser.inWaiting())
        #print(reply)
        ser.write(str.encode('AT+CMGF=1'+'\r\n'))
        time.sleep(1)
        reply = ser.read(ser.inWaiting())
        #print(reply)
        cmgs = "AT+CMGS=\"{0}\"\r\n".format(number)
        #print(cmgs);
        ser.write(str.encode(cmgs))
        time.sleep(1)
        reply = ser.read(ser.inWaiting())
        #print(reply)
        ser.write(str.encode(message))
        time.sleep(1)
        reply = ser.read(ser.inWaiting())
        #print(reply)
        ser.write(str.encode('\x1A'))

def receiveSMS():
    reply = ser.read(ser.inWaiting())
    time.sleep(1)
    print(reply)
    flag = b''
    if reply != flag :
       
        ser.write(str.encode('AT+CMGR=1'+'\r'))
        time.sleep(1)
        reply = str(ser.read(ser.inWaiting()))
        
        if 'STATUS' in reply.upper():
            print(reply)
        ser.write(str.encode('AT+CMGDA="DEL ALL"'+'\r'))
        time.sleep(.500)
        ser.read(ser.inWaiting())
        time.sleep(.500)
sendSMS("hello")

