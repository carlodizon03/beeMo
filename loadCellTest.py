import loadCell
import RPi.GPIO as GPIO
import json
from hx711 import HX711
import time

cell1_dt = 23 
cell1_sck = 24

cell2_dt = 8 
cell2_sck = 25

cell3_dt = 1 
cell3_sck = 7 

cell1Swap = 'cell1.swp'
cell2Swap = 'cell2.swp'
cell3Swap = 'cell3.swp'

try:
    print('Constructing Cell1')
    cell1  = loadCell.Create(cell1_dt,cell1_sck, swapFile = cell1Swap)
    print('Constructing Cell2')
    cell2  = loadCell.Create(cell2_dt,cell2_sck, swapFile = cell2Swap)
    print('Constructing Cell3')
    cell3  = loadCell.Create(cell3_dt,cell3_sck, swapFile = cell3Swap)
    print('Begin Measuremeant..')
    while True:

        val1 = cell1.Measure()
        time.sleep(1)
        val2 = cell2.Measure()
        time.sleep(1)
        val3 = cell3.Measure()
        time.sleep(1)
        print("Cell1= {0}kg\t Cell2= {1}kg \t Cell3= {2}kg".format(val1,val2,val3))
        
    
except (KeyboardInterrupt, SystemExit):
    print('Bye :)')
finally:
    GPIO.cleanup()
