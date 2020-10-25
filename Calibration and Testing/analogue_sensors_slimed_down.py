import sys
import time
from ADCDevice import *
from time import sleep

adc = ADCDevice()

def DHT22_data():
    # Reading from DHT22 and storing the temperature and humidity
    humi, temp = dht.read_retry(dht.DHT22, 4)
    return humi, temp

def setup():
    global adc 
    if(adc.detectI2C(0x4b)): # Detect the ads7830
        adc = ADS7830()
    else:
        print("No correct I2C address found, \n"
        "Please use command 'i2cdetect -y 1' to check the I2C address! \n"
        "Program Exit. \n");
        exit(-1)
setup()

while True:
    try:
        if (adc is not None):
       
            
            #Read value from LDR
            lightValue = adc.analogRead(0)    # read the ADC value of channel 0
            LDRvoltage = lightValue / 255.0 * 3.3  # calculate the voltage value
            LDRvoltage = '%.2f' % LDRvoltage                       
            
            #Read value from Moisture Sensor
            moistureValue = adc.analogRead(1)    # read the ADC value of channel 1
            MSvoltage = moistureValue / 255.0 * 3.3  # calculate the voltage value
            MSvoltage = '%.2f' % MSvoltage 
            
            print("Moisture value:", moistureValue, "LDR value:",lightValue)
            
        else:
            print ('Error')
        # DHT22 requires 2 seconds to give a reading, so make sure to add delay of above 2 seconds.
        sleep(0.1)
    except:
        raise Exception()
        break


