import sys
import Adafruit_DHT as dht
import time
from ADCDevice import *
from urllib.request import urlopen
from time import sleep



def DHT22_data():
    # Reading from DHT22 and storing the temperature and humidity
    humi, temp = dht.read_retry(dht.DHT22, 4) 
    return humi, temp


while True:
    try:
        
        #Read value from DHT22
        humi, temp = DHT22_data()
        #test below lines
        humi = '%.2f' % humi                       
        temp = '%.2f' % temp
        print(humi, temp)
        
        # DHT22 requires 2 seconds to give a reading, so make sure to add delay of above 2 seconds.
        sleep(3)
    except:
        raise Exception()
        break
