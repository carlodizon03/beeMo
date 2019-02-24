import smbus
import time

I2C_ADDR  = 0x27
LCD_WIDTH = 20
LCD_CMD = 0
LCD_CHR = 1

LCD_LINE_1 = 0x80
LCD_LINE_2 = 0xC0
LCD_LINE_3 = 0x94
LCD_LINE_4 = 0xD4

LCD_BACKLIGHT  = 0x08
ENABLE = 0b00000100
    
E_PULSE = 0.0005
E_DELAY = 0.0005
bus = smbus.SMBus(1)
class Create:


    @classmethod
    def __init__(self):
        self.__lcd_init()
        self.__lcd_string("                    ",LCD_LINE_1)
        self.__lcd_string("                    ",LCD_LINE_2)
        self.__lcd_string("                    ",LCD_LINE_3)    
        self.__lcd_string("                    ",LCD_LINE_4)

    def Clear(self):
        self.__lcd_string("                    ",LCD_LINE_1)
        self.__lcd_string("                    ",LCD_LINE_2)
        self.__lcd_string("                    ",LCD_LINE_3)    
        self.__lcd_string("                    ",LCD_LINE_4)
        
    def Print(self,line,string):
        if line == 1:
            self.__lcd_string(string,LCD_LINE_1)
        if line == 2:
            self.__lcd_string(string,LCD_LINE_2)
        if line == 3:
            self.__lcd_string(string,LCD_LINE_3)
        if line == 4:
            self.__lcd_string(string,LCD_LINE_4)
        
    def DisplayData(self,hive,temp,humid,weight):
        self.Clear()
        __line1 = "       HIVE#{0}       ".format(hive)
        __line2 = "Temp|Humidity|Weight"
        humid0 = self.__addLeadingSpace("{0:3.0f}".format(humid[0]))
        humid1 = self.__addLeadingSpace("{0:3.0f}".format(humid[1]))
        temp0  = self.__addLeadingSpace("{0:2.0f}".format(temp[0]))
        temp1  = self.__addLeadingSpace("{0:2.0f}".format(temp[1]))
        weight0 = self.__addLeadingSpace("{0:2.1f}".format(weight))
        __line3 = "{0}C|   {1}% |{2}kg".format(temp0,humid0,weight0)
        __line4 = "{0}C|   {1}% |".format(temp1,humid1)
        self.__lcd_string(__line1,LCD_LINE_1)
        self.__lcd_string(__line2,LCD_LINE_2)
        self.__lcd_string(__line3,LCD_LINE_3)    
        self.__lcd_string(__line4,LCD_LINE_4)
    def __addLeadingSpace(self,string):
        __tempStr = ""
        for space in range(3-len(string)):
           __tempStr+=" "
        __tempStr+=string
        return __tempStr
    def DisplayOutside(self,temp,humid):
        self.Clear()
        humid = self.__addLeadingSpace("{0:3.0f}".format(humid))
        temp = self.__addLeadingSpace("{0:2.0f}".format(temp))
        __line1 = "       OUTSIDE       "
        __line2 = "  Temp   Humidity"
        __line3 = "  {0}C      {1}%".format(temp,humid)
        self.__lcd_string(__line1,LCD_LINE_1)
        self.__lcd_string(__line2,LCD_LINE_2)
        self.__lcd_string(__line3,LCD_LINE_3)
        self.__lcd_string("                    ",LCD_LINE_4)
    @classmethod
    def __lcd_init(self):
        # Initialise display
        self.__lcd_byte(0x33,LCD_CMD) # 110011 Initialise
        self.__lcd_byte(0x32,LCD_CMD) # 110010 Initialise
        self.__lcd_byte(0x06,LCD_CMD) # 000110 Cursor move direction
        self.__lcd_byte(0x0C,LCD_CMD) # 001100 Display On,Cursor Off, Blink Off 
        self.__lcd_byte(0x28,LCD_CMD) # 101000 Data length, number of lines, font size
        self.__lcd_byte(0x01,LCD_CMD) # 000001 Clear display
        time.sleep(E_DELAY)
    def End(self):
        self.lcd_byte(0x01, LCD_CMD)
    @classmethod
    def __lcd_byte(self,bits, mode):
    
        # Send byte to data pins
        # bits = the data
        # mode = 1 for data
        #        0 for command

        bits_high = mode | (bits & 0xF0) | LCD_BACKLIGHT
        bits_low = mode | ((bits<<4) & 0xF0) | LCD_BACKLIGHT

        # High bits
        bus.write_byte(I2C_ADDR, bits_high)
        self.__lcd_toggle_enable(bits_high)

        # Low bits
        bus.write_byte(I2C_ADDR, bits_low)
        self.__lcd_toggle_enable(bits_low)
    @classmethod
    def __lcd_toggle_enable(self,bits):
        # Toggle enable
        time.sleep(E_DELAY)
        bus.write_byte(I2C_ADDR, (bits | ENABLE))
        time.sleep(E_PULSE)
        bus.write_byte(I2C_ADDR,(bits & ~ENABLE))
        time.sleep(E_DELAY)
    @classmethod
    def __lcd_string(self,message,line):
        # Send string to display

        message = message.ljust(LCD_WIDTH," ")
  
        self.__lcd_byte(line, LCD_CMD)

        for i in range(LCD_WIDTH):
            self.__lcd_byte(ord(message[i]),LCD_CHR)

