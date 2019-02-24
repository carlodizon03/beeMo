import loadCell
import RPi.GPIO as GPIO


cell1 = loadCell.Create(24,23,None)
cell2 = loadCell.Create(8,25,None)
cell3 = loadCell.Create(6,5,None)

file = open("LoadCell_Calibration_Ratio.txt","w")
ratio = []
print("Starting Calibration for Cell 1...")
ratio.append(cell1.Calibrate())

print("Starting Calibration for Cell 2...")
ratio.append(cell2.Calibrate())

print("Starting Calibration for Cell 3...")
ratio.append(cell3.Calibrate())

for value in ratio:
    file.write(str(value))
    file.write(",")
file.close()

print("Calibration values are successfuly saved to LoadCell_Calibration_Ratio.txt .")

