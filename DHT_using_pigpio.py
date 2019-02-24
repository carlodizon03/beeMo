import pigpio
import DHT22
from time import sleep

pi = pigpio.pi()

class Create:

    def __init__(self, sensors):
        self.__sensors = sensors

    def Measure(self):
        __temperatures = []
        __humidities = []

        for sensor in self.__sensors:
            __container = DHT22.sensor(pi,sensor)
            __container.trigger()
            sleep(.1)
            
            if __container.temperature() is not None and __container.humidity() is not None:
                if __container.temperature() < 0 or __container.humidity() < 0:
                    __temperatures.append(0)
                    __humidities.append(0)
                else:   
                    __temperatures.append(__container.temperature())
                    __humidities.append(__container.humidity())

           
                
                

        return __temperatures,__humidities
