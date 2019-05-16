import DHT
import RPi.GPIO as GPIO

import time
dht_sensors = [11,19,10,12,27,26,4]
#dht_sensors = [4,17,27,22,10,9,11]
try:
    dht = DHT.DHT_SENSOR(dht_sensors)


    temp, humid = dht.getValues()
    while True:
        for index in range(len(temp)):
            print("DHT{0}:{1:.2f}   {2:.2f}".format(index,temp[index],humid[index]))
        time.sleep(1)   

except (KeyboardInterrupt, SystemExit):
    print('Bye :)')
finally:
    GPIO.cleanup()
