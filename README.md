 # beeMo

## LOAD CELL CALIBRATION

1) You need a laptop with VNC installed or a monitor and mouse
3) Open a folder.
4) Go to /home/pi/BeeHiveMonitoring folder
5) Open loadCellCalibration.py
6) Press F5 to Run the script.
7) A python shell will appear and just follow the steps that will be provided. 

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

* DHT Hive 1 Layer 1  -  GPIO 4
* DHT Hive 1 Layer 2  -  GPIO 17
* DHT Hive 2 Layer 1  -  GPIO 27
* DHT Hive 2 Layer 2  -  GPIO 22
* DHT Hive 3 Layer 1  -  GPIO 10
* DHT Hive 3 Layer 2  -  GPIO 9
* DHT Outsude   -  GPIO 11

* Load Cell Hive 1 - Dout:24, Sck:23
* Load Cell Hive 2 - Dout:8, Sck:25
* Load Cell Hive 3 - Dout:6, Sck:5 

* GSM - RX:GPIO14, TX:GPIO15

* LCD - SCL:GPIO3, SDA:GPIO2

## To Create an Autostart

1)Open Terminal
2)Edit: 
 sudo nano /etc/xdg/lxsession/LXDE-pi/autostart
3) add 
 sudo python /home/pi/BeeHiveMonitoring/bootStrap.py
4) Reboot and observe
