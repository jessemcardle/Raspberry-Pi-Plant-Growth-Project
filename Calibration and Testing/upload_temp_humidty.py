import sys

from urllib.request import urlopen
from time import sleep

import Adafruit_DHT as dht
# Enter Your API key here
myAPI = '5KJ5TVQRF5NFSEXL'
# URL where we will send the data, Don't change it
baseURL = 'https://api.thingspeak.com/update?api_key=%s' % myAPI 

def DHT22_data():
    # Reading from DHT22 and storing the temperature and humidity
    humi, temp = dht.read_retry(dht.DHT22, 4) 
    return humi, temp
while True:
    try:
        humi, temp = DHT22_data()
        # If Reading is valid
        if isinstance(humi, float) and isinstance(temp, float):
            # Formatting to two decimal places
            humi = '%.2f' % humi                       
            temp = '%.2f' % temp
            print(temp, humi)
            # Sending the data to thingspeak
            #conn = urllib2.urlopen(baseURL + '&temperature=%s&humidity=%s' % (temp, humi))
            conn = urlopen(baseURL + '&field1=%s&field2=%s' % (temp, humi))
            print (conn.read())
            # Closing the connection
            conn.close()
        else:
            print ('Error')
        # DHT22 requires 2 seconds to give a reading, so make sure to add delay of above 2 seconds.
        sleep(60)
    except:
        raise Exception()
        break
