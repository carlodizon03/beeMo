
import RPi.GPIO as GPIO 
from hx711 import HX711

#TODO: replace GPIO.Cleanup() to the end of the main
#       

class Create:
    
    
    def __init__(self, dout_pin, sck_pin, ratio):
        self.__dout_pin = dout_pin
        self.__sck_pin = sck_pin
       
        if ratio is not None:
             self.__ratio = ratio
             GPIO.setmode(GPIO.BCM)
             self.__hx711 = HX711(self.__dout_pin, self.__sck_pin )
             __err = self.__hx711.zero()
             if __err:
                raise ValueError('Tare is unsuccessful.')
            #__ratio = 190.4
             self.__hx711.set_scale_ratio(self.__ratio) 
           
        
    def Calibrate(self):
          
        try:
            GPIO.setmode(GPIO.BCM)
            self.__hx711 = HX711(self.__dout_pin, self.__sck_pin )
            __err = self.__hx711.zero()
            __ratio = 0
            if __err:
                raise ValueError('Tare is unsuccessful.')
            __reading = self.__hx711.get_raw_data_mean()
            if __reading:
                print('Data subtracted by offset but still not converted to units:',
                  __reading)
            else:
                print('invalid data', __reading)

            # In order to calculate the conversion ratio to some units, in my case I want grams,
            # you must have known weight.
            input('Put known weight on the scale and then press Enter')
            __reading = self.__hx711.get_data_mean()
            if __reading:
                print('Mean value from HX711 subtracted by offset:', __reading)
                known_weight_grams = input('Write how many grams it was and press Enter: ')
                try:
                    value = float(known_weight_grams)
                    print(value, 'grams')
                except ValueError:
                    print('Expected integer or float and I have got:',known_weight_grams)

                __ratio = __reading / value
           
                self.__hx711.set_scale_ratio(__ratio) 
                print('Ratio is set:' , __ratio)
                print(self.__hx711.get_weight_mean(20), 'g')
                print(self.__hx711.get_weight_mean(20), 'g')
                print(self.__hx711.get_weight_mean(20), 'g')
                print(self.__hx711.get_weight_mean(20), 'g')
            else:
                raise ValueError('Cannot calculate mean value. Try debug mode. Variable reading:', __reading)
        finally:
           # GPIO.cleanup()
            return __ratio
    def Measure(self):
     
            __value = self.__hx711.get_weight_mean(20)
            #if __value < 0:
            #    __value = 0
            return __value/1000
         
       
       
