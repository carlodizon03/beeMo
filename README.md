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
