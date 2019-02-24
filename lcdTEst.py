import LCD 
import time
lcd = LCD.Create()

hive = 1
temp = [12,1]
humid = [10,95]
weight = 3.06

lcd.DisplayData(hive,temp,humid,weight)
