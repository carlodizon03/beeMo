import time
import serial
import json
#TODO: add/change/remove number
ser = serial.Serial(
    port='/dev/ttyS0',
    baudrate = 9600,
    timeout = 1
    )
#ser.write(str.encode("AT+CMGF=1\r")) # set to text mode
#time.sleep(1)
#print()
#ser.write(str.encode('AT+CMGDA="DEL ALL"\r\n')) # delete all SMS
#time.sleep(1)

def sendSMS(message):
    with open('/home/pi/BeeHiveMonitoring/Numbers.json','r') as n:
        numbers = json.load(n)
        
    for number in numbers["Numbers"]:
        print("Sending message to:{0}".format(number))
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
        time.sleep(5)

def injectSMS():
    reply = ser.read(ser.inWaiting())
    time.sleep(1)
    print(reply)
    flag = b''
    if reply != flag :
       
        ser.write(str.encode('AT+CMGR=1'+'\r\n'))
        time.sleep(1)
        reply = str(ser.read(ser.inWaiting()))
        
        if 'W:' in reply.upper():
            print(reply)
            index1 = reply.index('>')
            index2 = reply.index('<')
            values = ''
            for x in range(index1+1,index2):
                values+=reply[x]

            print()
            weights = values.split(',')
            print(values)
            for i in weights:
                print(i)
            with open('/home/pi/BeeHiveMonitoring/log.json') as f:
                data = json.load(f)
                data['Hive_1']['Weight'] = float(weights[0])
                data['Hive_2']['Weight'] = float(weights[1])
                data['Hive_3']['Weight'] = float(weights[2])
            print("updating values in log.json..")
            with open('/home/pi/BeeHiveMonitoring/log.json','w') as outfile:
                  json.dump(data,outfile,indent=4,sort_keys=True)
                  
        ser.write(str.encode('AT+CMGDA="DEL ALL"'+'\r\n'))
        time.sleep(.500)
        ser.read(ser.inWaiting())
        time.sleep(.500)

 

