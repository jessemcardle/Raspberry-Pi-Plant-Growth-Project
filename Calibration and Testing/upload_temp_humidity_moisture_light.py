import sys
import Adafruit_DHT as dht
import time
from ADCDevice import *
from urllib.request import urlopen
from time import sleep

adc = ADCDevice()

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

while True:
    try:
        setup()
        #Read value from DHT22
        humi, temp = DHT22_data()
        #test below lines
        humi = '%.2f' % humi                       
        temp = '%.2f' % temp
        print(humi, temp)

        #Read value from LDR
        LDRvalue = adc.analogRead(0)    # read the ADC value of channel 0
        LDRvoltage = LDRvalue / 255.0 * 3.3  # calculate the voltage value
        print ('LDR ADC Value : %d, LDR Voltage : %.2f'%(LDRvalue,LDRvoltage))
        #Read value from Moisture Sensor
        MSvalue = adc.analogRead(1)    # read the ADC value of channel 1
        MSvoltage = MSvalue / 255.0 * 3.3  # calculate the voltage value
        print ('ADC Value : %d, Voltage : %.2f'%(MSvalue,MSvoltage))

        # If Reading is valid
        """ if isinstance(humi, float) and isinstance(temp, float) and isinstance(temp, float) and isinstance(temp, float):
            # Formatting to two decimal places
            humi = '%.2f' % humi                       
            temp = '%.2f' % temp
            print(temp, humi)
            # Sending the data to thingspeak
            
            conn = urlopen(baseURL + '&field1=%s&field2=%s' % (temp, humi))
            print (conn.read())
            # Closing the connection
            conn.close()
        else:
            print ('Error') """
        # DHT22 requires 2 seconds to give a reading, so make sure to add delay of above 2 seconds.
        sleep(3)
    except:
        raise Exception()
        break