 # beeMo

## LOAD CELL CALIBRATION

1) You need a laptop with VNC installed or a monitor and mouse
2) Open a folder.
3) Go to /home/pi/BeeHiveMonitoring folder
4) Open loadCellCalibration.py
5) Press F5 to Run the script.
6) A python shell will appear and just follow the steps that will be provided. 

## WIFI configuration

1) You need a laptop and a card reader
2) Remove the SD card from the raspberry pi
4) Plug it in your PC/Laptop.
5) WARNING: a format window will pop up when the PC/Laptop read the SD card. JUST IGNORE or CLOSE IT. 
6) DONT FORMAT THE SD CARD!
7) go to boot partition.
8) open the wpa_supplicant.conf file or create a new text file and plug this code:
    <pre> 
          country=ph
          update_config=1
          ctrl_interface=/var/run/wpa_supplicant

          network={
                  scan_ssid=1
                  ssid="yourWIFISSIDHere"
                  psk="yourWIFIPasswordHere"
                  }
    <code>
  9) save the file as wpa_supplicant.conf
  10) copy and paste the file in the boot partition.
  11) remove SD Card from PC and plug it back to the Raspberry Pi.
  12) Check if it is successfully connected by viewing in the monitor or by scanning the IP address within the same network using "Advanced IP Scanner" Software (download from google)


## Pin COnfiguration


* DHT Hive 1 Layer 1  -  GPIO 11
* DHT Hive 1 Layer 2  -  GPIO 19
* DHT Hive 2 Layer 1  -  GPIO 10
* DHT Hive 2 Layer 2  -  GPIO 12
* DHT Hive 3 Layer 1  -  GPIO 27
* DHT Hive 3 Layer 2  -  GPIO 26
* DHT Outsude   -  GPIO 4

* Load Cell Hive 1 - Dout:23, Sck:24
  * vcc - tblue -
  * sck - blue   - 
  * dt - orange -  
  * gnd - tOrange - 

* Load Cell Hive 2 - Dout:8, Sck:25
  * vcc - tBlue -red
  * sck - blue - green
  * dt -  brown - yellow
  * gnd - tBrown - black 
 
* Load Cell Hive 3 - Dout:16, Sck:20 
  * vcc - tgreen - red 
  * sck - tblue   - blue
  * dt - orange - yellow 
  * gnd - tOrange - gray

* GSM - RX:GPIO14, TX:GPIO15

* LCD - SCL:GPIO3, SDA:GPIO2

## To Create an Autostart

1) Open Terminal

2) Edit: 
    sudo nano /etc/xdg/lxsession/LXDE-pi/autostart
    
3) add 
    sudo python /home/pi/BeeHiveMonitoring/bootStrap.py
    
4) Reboot and observe

## Fixed: ImportError:No Module named Adafruit_DHT

* Caused: in bootStrap.py, the main.py is run using python3 which caused the error because the Adafruit_DHT module was installed only in pyhon.
* Fix: 
 1) Go to cloned package folder.
 2) Install the package using:
      sudo python3 setup.py install
 3) Test

## Switching Serial0 from ttyAMA0 to ttyS0

 1) sudo nano /boot/config.txt
 2) put "enable_uart=1" at the bottom and save
 3) reboot rpi
 4) To check, run ls -l /dev

## To enable Serial port:
 1)run sudo raspi-config
 2)at interfacing option go to serial:
 3)disable console
 4)enable serial port
 5) reboot
 
## Enabling i2c
 1)sudo apt-get install -y python-smbus
 2)sudo apt-get install -y i2c-tools
 3)sudo raspi-config
 4)enable i2c under interfacing options
 5)to check, connect an i2c device and run  "sudo i2cdetect -y 1"
