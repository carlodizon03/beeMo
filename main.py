import DHT 
import loadCell
import time
import RPi.GPIO as GPIO
from datetime import datetime
import json
#import GSM as gsm
from pprint import pprint
import sys

##LCD
import LCD
import os
import time
import json
from pprint import pprint
import sys
lcd = LCD.Create()

lcd.Clear()
###

#gsm.sendSMS("Starting..")
#time.sleep(2)
dht_sensors = [11,19,13,12,27,26,4]
#dht_sensors = [4,26,27,22,10,19,11]
print("Constructing DHT Sensors")
dht = DHT.DHT_SENSOR(dht_sensors)

cell1_dt = 23 
cell1_sck = 24

cell2_dt = 8 
cell2_sck = 25

cell3_dt = 16 
cell3_sck = 20 

cell1Swap = 'cell1.swp'
cell2Swap = 'cell2.swp'
cell3Swap = 'cell3.swp'
print('Constructing Cell1')
cell1  = loadCell.Create(cell1_dt,cell1_sck, swapFile = cell1Swap)
time.sleep(5)
print('Constructing Cell2')
cell2  = loadCell.Create(cell2_dt,cell2_sck, swapFile = cell2Swap)
time.sleep(5)
print('Constructing Cell3')
cell3  = loadCell.Create(cell3_dt,cell3_sck, swapFile = cell3Swap)
print('Begin Measuremeant..')
time.sleep(5)

try:
    
    while True:
        
        print("Geting DHT Values")
        temp, humid = dht.getValues()
        print("Getting Cell1")
        weight = []
        weight.append(cell1.Measure())
        time.sleep(2)
        print("Getting Cell2")
        weight.append(cell2.Measure())
        time.sleep(2)
        print("Getting Cell3")
        weight.append(cell3.Measure())
        time.sleep(2)
        
        for index in range(len(temp)):
            print("Temp   Humid")
            print("{0:.2f}C   {1:.2f}%".format(temp[index],humid[index]))
             
        print("Cell1= {0:.2f}kg \tCell2= {1:0.2f}kg \tCellll3= {2:0.2f}kg".format(weight[0],weight[1], weight[2],3))
      
        
        try:
            with open('/home/pi/BeeHiveMonitoring/log.json') as f:
                data = json.load(f)

            #print(data)
            

            timestamp = str(datetime.now())
            
            data['Timestamp'] = timestamp

            if( temp[0] != 0):
                data['Hive_1']['Temperatures'][0] = temp[0]
            
            if( temp[1] != 0):
                    
                data['Hive_1']['Temperatures'][1] = temp[1]
            
            if( humid[0] != 0 and humid[0] < 110):
                
                data['Hive_1']['Humidities'][0] = humid[0]

            if( humid[1] != 0 and humid[1] < 110):
                
                data['Hive_1']['Humidities'][1] = humid[1]
             

            data['Hive_1']['Weight'] = round(weight[0],2)
            

            if( temp[2] != 0):

                data['Hive_2']['Temperatures'][0] = temp[2]

            if( temp[3] !=0):

                data['Hive_2']['Temperatures'][1] = temp[3]

            if( humid[2] !=0 and humid[2] < 110):

                data['Hive_2']['Humidities'][0] = humid[2]

            if( humid[3] != 0 and humid[3] < 110):
                
                data['Hive_2']['Humidities'][1] = humid[3]

            
            data['Hive_2']['Weight'] = round(weight[1],2)

            if( temp[4] != 0):
                
                data['Hive_3']['Temperatures'][0] = temp[4]

            if( temp[5] != 0):
                
                data['Hive_3']['Temperatures'][1] = temp[5]

            if( humid[4] != 0 and humid[4] < 110):
                
                data['Hive_3']['Humidities'][0] = humid[4]

            if( humid[5] != 0 and humid[5] < 110):
                
                data['Hive_3']['Humidities'][1] = humid[5]

            data['Hive_3']['Weight'] = round(weight[2],2)

            if( temp[6] != 0):

                data['Outside']['Temperature'] = temp[6]

            if( humid[6] !=0 and  humid[6] < 110):

                data['Outside']['Humidity'] = humid[6]

            print("------------------------------")
            pprint(data)
            
            print("updating values in log.json..")
            with open('/home/pi/BeeHiveMonitoring/log.json','w') as outfile:
                  json.dump(data,outfile,indent=4,sort_keys=True)
            
            with open('/home/pi/BeeHiveMonitoring/history.json') as f:
                history = json.load(f)

            history['Reports'].append(data)
            print("updating values in .json..")
            with open('/home/pi/BeeHiveMonitoring/history.json','w') as out:
                json.dump(history,out,indent=4,sort_keys = True)
                
            print("Saved!")


            ####LCD###
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
                lcd.Clear()
                print("LCD Printing Hive 1")
                lcd.DisplayData(1,hive1_temp,hive1_humid,weight1)
                time.sleep(3)
                print("LCD Printing Hive 2")
                lcd.DisplayData(2,hive2_temp,hive2_humid,weight2)
                time.sleep(3)
                print("LCD Printing Hive 3")
                lcd.DisplayData(3,hive3_temp,hive3_humid,weight3)
                time.sleep(3)
                print("LCD Printing Hive Outside")
                lcd.DisplayOutside(out_temp,out_humid)
                time.sleep(3)
                print("LCD Clear")
                lcd.Clear()
                print("Print Gathering Data")
                lcd.Print(2,"Gathering Data")
                print("Done Printing")
        
        except KeyboardInterrupt:
            print("Program Interrupted!")
            lcd.Print(1,"Program Interrupted!")
            lcd.Clear()
            sys.exit(0)
        
       
            

       


finally:
    
   
    print("Stopping code..")
    lcd.Clear()
    GPIO.cleanup()
      

