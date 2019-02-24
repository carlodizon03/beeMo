import time
import threading
import os

def startProgram(i):
    print("Running thread %d"%i)
    if(i==0):
        time.sleep(1)
        print("Running LCDPrinter")
        os.system("sudo python3 /home/pi/BeeHiveMonitoring/LCDPrinter.py")

    elif(i==1):
        time.sleep(1)
        print("Running main")
        os.system("sudo python3 /home/pi/BeeHiveMonitoring/main.py")
    elif(i==2):
        time.sleep(1)
        print("Running reportingModule")
        os.system("sudo python3 /home/pi/BeeHiveMonitoring/reportingModule.py")
    else:
        pass

for i in range (3):
    t = threading.Thread(target=startProgram, args=(i,))
    t.start()

 
    
