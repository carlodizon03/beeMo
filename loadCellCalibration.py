import loadCell
import RPi.GPIO as GPIO
import json

cell1 = loadCell.Create(23,24,None)
cell2 = loadCell.Create(8,25,None)
cell3 = loadCell.Create(1,7,None)
try:
    with open('/home/pi/BeeHiveMonitoring/LoadCell_Calibration_Ratio.json') as f:
                    data = json.load(f)
    print("Current Ratios:")            
    print("Cell1:{0}".format(data["Ratio1"]))
    print("Cell2:{0}".format(data["Ratio2"]))
    print("Cell3:{0}".format(data["Ratio3"]))
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
    print("Now, I will read data in infinite loop. To exit press 'CTRL + C'")
    input('Press Enter to begin reading')

    while True:
        #print(cell3.Measure())
        print("cell1:{0}\t cell2:{1}\t cell3: {2}".format(cell1.Measure(),cell2.Measure(),cell3.Measure()))

except (KeyboardInterrupt, SystemExit):
    print('Bye :)')
finally:
    GPIO.cleanup()
