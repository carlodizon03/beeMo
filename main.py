import DHT 
import loadCell
import time
import RPi.GPIO as GPIO
from datetime import datetime
import json
import GSM as gsm
from pprint import pprint
import sys
#gsm.sendSMS("Starting..")
time.sleep(2)
dht_sensors = [4,17,27,22,10,9,11]
print("Constructing DHT Sensors")
dht = DHT.DHT_SENSOR(dht_sensors)
with open('/home/pi/BeeHiveMonitoring/LoadCell_Calibration_Ratio.json') as f:
                ratio = json.load(f)
                

cell1_dt = 23 
cell1_sck = 24

cell2_dt = 8 
cell2_sck = 25

cell3_dt = 1 
cell3_sck = 7 

cell1Swap = 'cell1.swp'
cell2Swap = 'cell2.swp'
cell3Swap = 'cell3.swp'
print('Constructing Cell1')
cell1  = loadCell.Create(cell1_dt,cell1_sck, swapFile = cell1Swap)
print('Constructing Cell2')
cell2  = loadCell.Create(cell2_dt,cell2_sck, swapFile = cell2Swap)
print('Constructing Cell3')
cell3  = loadCell.Create(cell3_dt,cell3_sck, swapFile = cell3Swap)
print('Begin Measuremeant..')

try:
    
    while True:
        
        print("Geting DHT Values")
        temp, humid = dht.getValues()
        print("Getting Cell1")
        weight = []
        weight.append(cell1.Measure())
        time.sleep(1)
        print("Getting Cell2")
        weight.append(cell2.Measure())
        time.sleep(1)
        print("Getting Cell3")
        weight.append(cell3.Measure())
        time.sleep(1)
        
        for index in range(len(temp)):
            print("Temp   Humid")
            print("{0:.2f}C   {1:.2f}%".format(temp[index],humid[index]))
             
        print("Cell1= {0}kg \tCell2= {1}kg \tCellll3= {2}kg".format(weight[0],weight[1], weight[2],3))
      
        
        try:
            with open('/home/pi/BeeHiveMonitoring/log.json') as f:
                data = json.load(f)

            #print(data)
            

            timestamp = str(datetime.now())
            
            data['Timestamp'] = timestamp
            
            data['Hive_1']['Temperatures'][0] = temp[0]
            data['Hive_1']['Temperatures'][1] = temp[1]
            data['Hive_1']['Humidities'][0] = humid[0]
            data['Hive_1']['Humidities'][1] = humid[1]
            data['Hive_1']['Weight'] = weight[0]
            
            
            data['Hive_2']['Temperatures'][0] = temp[2]
            data['Hive_2']['Temperatures'][1] = temp[3]
            data['Hive_2']['Humidities'][0] = humid[2]
            data['Hive_2']['Humidities'][1] = humid[3]
            data['Hive_2']['Weight'] = weight[1]

            data['Hive_3']['Temperatures'][0] = temp[4]
            data['Hive_3']['Temperatures'][1] = temp[5]
            data['Hive_3']['Humidities'][0] = humid[4]
            data['Hive_3']['Humidities'][1] = humid[5]
            data['Hive_3']['Weight'] = weight[2]

            data['Outside']['Temperature'] = temp[6]
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
        except KeyboardInterrupt:
            print("Program Interrupted!")
            sys.exit(0)
        
       
            

       


finally:
    
   
    print("Stopping code..")
    GPIO.cleanup()
      

