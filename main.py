import DHT
import loadCell
import time
import RPi.GPIO as GPIO
from datetime import datetime
import json
from pprint import pprint
import sys
dht_sensors = [4,17,27,22,10,9,11]

dht = DHT.DHT_SENSOR(dht_sensors)
with open('/home/pi/BeeHiveMonitoring/LoadCell_Calibration_Ratio.json') as f:
                ratio = json.load(f)
                
cell1 = loadCell.Create(24,23,float(ratio["Ratio1"]))
cell2 = loadCell.Create(8,25,float(ratio["Ratio2"]))
cell3 = loadCell.Create(6,5,float(ratio["Ratio3"]))



	try:
    
    while True:
        
    
        temp, humid = dht.getValues()
        weight = []
        weight.append(cell1.Measure())
        weight.append(cell2.Measure())
        weight.append(cell3.Measure())
        for index in range(len(temp)):
            print("{0:.2f}   {1:.2f}".format(temp[index],humid[index]))
             
        print("{0},{1},{2}".format(weight[0],weight[1],weight[2]))
      
        
        try:
            with open('/home/pi/BeeHiveMonitoring/log.json') as f:
                data = json.load(f)

            print(data)
            print("updating values..")

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
            print("values updated..")
            print("saving..")
            
            with open('/home/pi/BeeHiveMonitoring/log.json','w') as outfile:
                  json.dump(data,outfile,indent=4,sort_keys=True)

            with open('/home/pi/BeeHiveMonitoring/history.json') as f:
                history = json.load(f)

            history['Reports'].append(data)

            with open('/home/pi/BeeHiveMonitoring/history.json','w') as out:
                json.dump(history,out,indent=4,sort_keys = True)
                
            print("Saved!")    
        except KeyboardInterrupt:
            print("Program Interrupted!")
            sys.exit(0)
        
        else:
            print("Done..")
            

       


finally:
    
   
    print("Stopping code..")
    GPIO.cleanup()
      

