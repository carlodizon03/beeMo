import loadCell
import RPi.GPIO as GPIO
import json


with open('/home/pi/BeeHiveMonitoring/LoadCell_Calibration_Ratio.json') as f:
                ratio = json.load(f)

cell1 = loadCell.Create(23,24,float(ratio["Ratio1"]))
cell2 = loadCell.Create(8,25,float(ratio["Ratio2"]))
cell3 = loadCell.Create(1,7,float(ratio["Ratio3"]))
try:
    while True:
        weight = []
        weight.append(cell1.Measure())
        weight.append(cell2.Measure())
        weight.append(cell3.Measure())
        print("{0},\t{1},\t{2}".format(weight[0],weight[1],weight[2]))


except (KeyboardInterrupt, SystemExit):
    print('Bye :)')
finally:
    GPIO.cleanup()
