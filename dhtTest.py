import DHT
import RPi.GPIO as GPIO


dht_sensors = [4,17,27,22,10,9,11]

dht = DHT.DHT_SENSOR(dht_sensors)


temp, humid = dht.getValues()

for index in range(len(temp)):
    print("{0:.2f}   {1:.2f}".format(temp[index],humid[index]))
        
#except KeyboardInterrupt:
  #  print ("ending program..")
#except:
  #  print ("Error occured..")
#finally:
#   print ("Done!")
    #GPIO.cleanup()
    
