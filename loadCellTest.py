import loadCell
import RPi.GPIO as GPIO
import json
from hx711 import HX711
import time

cell1_dt = 23 
cell1_sck = 24

cell2_dt = 8 
cell2_sck = 25

cell3_dt = 16
cell3_sck = 20

cell1Swap = 'cell1.swp'
cell2Swap = 'cell2.swp'
cell3Swap = 'cell3.swp'

try:
    print('Constructing Cell1')
    cell1  = loadCell.Create(cell1_dt,cell1_sck, swapFile = cell1Swap)
    time.sleep(2)
    print('Constructing Cell2')
    cell2  = loadCell.Create(cell2_dt,cell2_sck, swapFile = cell2Swap)
    time.sleep(2)
    print('Constructing Cell3')
    cell3  = loadCell.Create(cell3_dt,cell3_sck, swapFile = cell3Swap)
    time.sleep(2)
    print('Begin Measuremeant..')
    
    while True:

        val1 = cell1.Measure()
        time.sleep(2)
        val2 = cell2.Measure()
        time.sleep(2)
        val3 = cell3.Measure()
        time.sleep(2)
        print("Cell1= {0:0.2f}kg\t Cell2= {1:0.2f}kg \t Cell3= {2:0.2f}kg".format(val1,val2,val3))
        
        
except (KeyboardInterrupt, SystemExit):
    print('Bye :)')
finally:
    GPIO.cleanup()
