import sys
import Adafruit_DHT as dht
import time
from ADCDevice import *
from urllib.request import urlopen
from time import sleep
import RPi.GPIO as GPIO
import datetime

adc = ADCDevice()
valvePin = 11 #define valve pin

# Enter Your API key here
myAPI = '5KJ5TVQRF5NFSEXL'
# URL where we will send the data, Don't change it
baseURL = 'https://api.thingspeak.com/update?api_key=%s' % myAPI


def DHT22_data():

    # Reading from DHT22 and storing the temperature and humidity
    humi, temp = dht.read_retry(dht.DHT22, 4)
    return humi, temp

def setup():
    global adc
    if(adc.detectI2C(0x48)): # Detect the pcf8591.
        adc = PCF8591()
    elif(adc.detectI2C(0x4b)): # Detect the ads7830
        adc = ADS7830()
    else:
        print("No correct I2C address found, \n"
        "Please use command 'i2cdetect -y 1' to check the I2C address! \n"
        "Program Exit. \n");
        exit(-1)

#Valve Setup
GPIO.setmode(GPIO.BOARD)       # use PHYSICAL GPIO Numbering
GPIO.setup(valvePin, GPIO.OUT)   # set the ledPin to OUTPUT mode
GPIO.output(valvePin, GPIO.HIGH) # close the valve

#Set up last water
lastwater = datetime.datetime(2020, 5, 17)

def openvalve():
    global lastwater

    GPIO.output(valvePin, GPIO.LOW) # open the valve
    print('Valve is open')
    print('Watering for 5 seconds...')
    sleep(5)
    GPIO.output(valvePin, GPIO.HIGH) # close the valve
    print('Valve is closed now')

    lastwater = datetime.datetime.now() # Flag to check against.

def checkwater():

    now = datetime.datetime.now() #Get the current time
    watertimedifference = now-lastwater #Get the difference since the last water
    minutes = watertimedifference.total_seconds() / 60 #Convert the difference to minutes
    
    if int(MSpercentage) < 70 and minutes > 30: #Check if plants should be watered
        openvalve()
    else:
        print('Does not need to be watered')
       
def destroy():
    GPIO.cleanup()                      # Release all GPIO

while True:
    try:
        setup()
        # Read Humidity and temperature
        humi, temp = DHT22_data()
        # If Reading is valid
        if isinstance(humi, float) and isinstance(temp, float):
            # Formatting to two decimal places
            humi = '%.2f' % humi
            temp = '%.2f' % temp
            
            #Read value from LDR
            lightValue = adc.analogRead(0)    # read the ADC value of channel 0
            LDRvoltage = lightValue / 255.0 * 3.3  # calculate the voltage value
            print ('LDR ADC Value : %d, LDR Voltage : %.2f'%(lightValue,LDRvoltage))
            #Read value from Moisture Sensor
            moistureValue = adc.analogRead(1)    # read the ADC value of channel 1
            MSvoltage = moistureValue / 255.0 * 3.3  # calculate the voltage value
            print ('MS ADC Value : %d, MS Voltage : %.2f'%(moistureValue,MSvoltage))
            
            LDRpercentage = 100 - (lightValue / 254) * 100
            MSpercentage = ((moistureValue / 195) * 100)

            checkwater()

            LDRpercentage = '%.2f' % LDRpercentage
            MSpercentage = '%.2f' % MSpercentage 
           
            print(temp, humi, moistureValue, lightValue)
            # Sending the data to thingspeak
            conn = urlopen(baseURL + '&field1=%s&field2=%s&field3=%s&field4=%s' %
                        (temp, humi, MSpercentage, LDRpercentage))
            print(conn.read())
            # Closing the connection
            conn.close()
        else:
            print ('Error')
        # DHT22 requires 2 seconds to give a reading, so make sure to add delay of above 2 seconds.
        print('Waiting for 5 minutes...')
        sleep(300)
    

    except:      
            destroy()
            raise Exception()
            break
        
