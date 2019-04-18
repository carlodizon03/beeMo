import pickle 
import os 
import RPi.GPIO as GPIO 
from hx711 import HX711 

 #pins
dt = 16
sck = 20

 
try: 
    GPIO.setmode(GPIO.BCM) 
    hx = HX711(dout_pin=dt, pd_sck_pin=sck) 
 

    #assuming there is no swapFile proceed to calibration 
    #file name

    swap_file_name = 'cell3.swp'
    err = hx.zero() 
    if err: 
        raise ValueError('Tare is unsuccessful.') 
    reading = hx.get_raw_data_mean() 


    if reading:
        print('Data subtracted by offset but still not converted to units:',reading) 
    else: 
        print('invalid data', reading) 


    input('Put known weight on the scale and then press Enter') 
    reading = hx.get_data_mean(readings = 50) 

    if reading: 
        print('Mean value from HX711 subtracted by offset:', reading) 
        known_weight_grams = input('Write how many grams it was and press Enter: ') 
        try: 
            value = float(known_weight_grams) 
            print(value, 'grams') 
        except ValueError: 
            print('Expected integer or float and I have got:', 
                      known_weight_grams) 
        ratio = reading / value 
        hx.set_scale_ratio(ratio) 
        print('Ratio is set.') 

    else: 
        raise ValueError( 
                'Cannot calculate mean value. Try debug mode. Variable reading:', 
                reading) 


    print('Saving the HX711 state to swap file on persistant memory')
    with open(swap_file_name, 'wb') as swap_file: 
            pickle.dump(hx, swap_file) 
            swap_file.flush() 
            os.fsync(swap_file.fileno())

            
    print("Now, I will read data in infinite loop. To exit press 'CTRL + C'") 
    input('Press Enter to begin reading') 
    while True: 
        print(hx.get_weight_mean(50), 'g') 
 
except (KeyboardInterrupt, SystemExit): 
    print('Bye :)') 
 
finally: 
    GPIO.cleanup()
