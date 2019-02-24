import loadCell
import RPi.GPIO as GPIO
import json

cell1 = loadCell.Create(24,23,None)
cell2 = loadCell.Create(8,25,None)
cell3 = loadCell.Create(6,5,None)

with open('/home/pi/BeeHiveMonitoring/LoadCell_Calibration_Ratio.json') as f:
                data = json.load(f)
                
print(data["Ratio1"])
print(data["Ratio2"])
print(data["Ratio3"])
print()
print("Starting Calibration for Cell 1...")
data["Ratio1"] = cell1.Calibrate()

print("Starting Calibration for Cell 2...")
data["Ratio2"] = cell2.Calibrate()

print("Starting Calibration for Cell 3...")
data["Ratio3"] = cell3.Calibrate()

with open('/home/pi/BeeHiveMonitoring/LoadCell_Calibration_Ratio.json','w') as outfile:
                json.dump(data,outfile,indent=4,sort_keys=True)


print("Calibration values are successfuly saved to LoadCell_Calibration_Ratio.txt .")

