import sys
import Adafruit_DHT as DHT


class DHT_SENSOR:


    def __init__(self, sensors):
        self.__sensors = sensors

    def getValues(self):
        __temperatures = []
        __humidities = []
        
        for sensor in self.__sensors:
             __humidity, __temperature = DHT.read_retry(DHT.DHT22, sensor, 15, 3)

             if __humidity is not None and __temperature is not None:
                 __temperatures.append(__temperature)
                 __humidities.append(__humidity)
             else:
                 __temperatures.append(0)
                 __humidities.append(0)

        return __temperatures,__humidities    
                

      

