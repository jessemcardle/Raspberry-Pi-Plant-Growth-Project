import sys
import time
from time import sleep
import random
import datetime

a = 0
lastwater = datetime.datetime(2020, 5, 17)

def openvalve():
    
    global lastwater
    
    print('Valve is open')
    print('Watering for 5 seconds...')
    sleep(5)
    print('Valve is closed now')

    lastwater = datetime.datetime.now() # Flag to check against.

        
def checkwater():
    now = datetime.datetime.now() #Get the current time
    watertimedifference = now-lastwater #Get the difference since the last water
    minutes = watertimedifference.total_seconds() / 60 #Convert the difference to minutes
    
    if int(MSPercentage) < 70 and minutes > 30: #Check if plants should be watered
        openvalve()
    else:
        print('Does not need to be watered')
        

while True:
    try:
     
        if True:

           
            MSPercentage = random.randint(1,50)
            print(MSPercentage)
                       
            checkwater()
           
        else:
            print ('Error')
        # DHT22 requires 2 seconds to give a reading, so make sure to add delay of above 2 seconds.
        print('waiting 2 seconds before checking again...')
        sleep(2)
    

    except:      
            
            raise Exception()
            break
        
