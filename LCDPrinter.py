import LCD
import os
import time
import json
from pprint import pprint
import sys
lcd = LCD.Create()

lcd.Clear()

while True:
    try:
        with open('/home/pi/BeeHiveMonitoring/history.json','r') as f:
            d = json.load(f)
    
        
        lastIndex = len(d['Reports']) -1
        data = d['Reports'][lastIndex]
        pprint(data)
        hive1_temp = data['Hive_1']['Temperatures']
        hive2_temp = data['Hive_2']['Temperatures']
        hive3_temp = data['Hive_3']['Temperatures']
        hive1_humid = data['Hive_1']['Humidities']
        hive2_humid = data['Hive_2']['Humidities']
        hive3_humid = data['Hive_3']['Humidities']
        weight1 = data['Hive_1']['Weight']
        weight2 = data['Hive_2']['Weight']
        weight3 = data['Hive_3']['Weight']
        out_temp = data['Outside']['Temperature']
        out_humid = data['Outside']['Humidity']
        lcd.DisplayData(1,hive1_temp,hive1_humid,weight1)
        time.sleep(3)
        lcd.DisplayData(2,hive2_temp,hive2_humid,weight2)
        time.sleep(3)
        lcd.DisplayData(3,hive3_temp,hive3_humid,weight3)
        time.sleep(3)
        lcd.DisplayOutside(out_temp,out_humid)
        time.sleep(3)
    except KeyboardInterrupt:
        lcd.Print(1,"Program Interrupted!")
        print("LCD: Program Interrupted!")
        lcd.Clear()
        sys.exit(0)
    else:
        lcd.Clear()
