import pickle
import os
import RPi.GPIO as GPIO 
from hx711 import HX711

#TODO: replace GPIO.Cleanup() to the end of the main
#       

class Create:
    
    
    def __init__(self, dout_pin, sck_pin, swapFile):
        GPIO.setmode(GPIO.BCM)
        self.__dout_pin = dout_pin
        self.__sck_pin = sck_pin
        self.__file = swapFile
        self.__hx711 = HX711(self.__dout_pin, self.__sck_pin)
      
            
        if os.path.isfile(self.__file):
            with open(self.__file,'rb') as sf:
                self.__hx711 = pickle.load(sf)
        else:
            print("No File")
    
    
            
    def Measure(self):
        self.__hx711.power_up() 
        self.__hx711.reset()     
        __value = self.__hx711.get_weight_mean(readings = 50)

        if __value < 0:
            __value = 0
        self.__hx711.power_down()    
        return  (__value/1000)
         
       

