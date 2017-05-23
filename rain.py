#import  RPi.GPIO as GPIO
import threading
import time
import datetime
import random

#GPIO.setmode(GPIO.BCM)
#GPIO.setup(12, GPIO.IN,pull_up_down=GPIO.PUD_UP)
 
rainfall = 0 

def is_bigger(than):
    pass
    

def is_new_day():
    '''Keep a daily log of total rainfall

    Wait for midnight, log the total rainfall for the day.
    Set the dom variable to the new day, wait another 24 hours
    Runs in a separate thread so it will work even if the mail loop is
    not active, which is true when there is no rain
    '''
    now = datetime.datetime.now()
    day = str(now.year) + str(now.month) + str(now.day)   #will change after midnight
    dom, mostrain = 0, 0
    while True:
        now = datetime.datetime.now()
        #day = random.randint(1,2)
        day = now.minute
        #day = str(now.year) + str(now.month) + str(now.day)   #will change after midnight
        
        if rainfall > mostrain:
            mostrain = rainfall
        print ("Rainfall is {},total accumulation {}".format(rainfall, mostrain))
        
        if dom != day:              # it's a new day
            dom = day
            print (day)
            
            print ('Total rainfall for {}-{}-{} is {}'.format (now.month, now.day,now.year, mostrain))
            try:
                log = open('dailyrain.log' , 'a')
                log.write('{} {:.2f}\n'.format(datetime.datetime.now().strftime("%Y-%m-%d"), mostrain))
                log.close()
            except:
                print ('Cannot write to daily log file')
            mostrain = 0            # reset daily
            time.sleep(10)
        else:
            time.sleep(2)
            print ('Waking up, still today, back to sleep'.format (rainfall))
            #print (rainfall)


def measure_rainfall():
    x=0
    now = datetime.datetime.now()
    day = str(now.year) + str(now.month) + str(now.day)   #will change after midnight
    dom = 0 
    
    while True:
        '''Accumulate total daily rainfall.  Write to daily log file
           Needs code to reset rainfall to zero at midnight
    '''    
        #inputValue = GPIO.input(12)                        #poll  or
        #inputValue = GPIO.wait_for_edge(12, GPIO.RISING)   #interupt
        inputValue = 0              # for testing only

        now = datetime.datetime.now()
        day = now.minute
        global rainfall
        ####################### Measure Rainfall ######################     
        if (inputValue == False):
            x = x + 1
            rainfall = x*0.011
            print (rainfall)
        time.sleep(1)               # remove after testing

        ####################  Reset at Midnight #####################
        if dom != day:
            dom = day
            x = 0
            #print (day)
        ##################### write to log file ######################
        try:
            log = open('rain.log', 'a')
            log.write("{} {:.2f}  \n".format (datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S"), rainfall))
            log.close()
        except KeyboardInterrupt:
             log.close()
             exit('Thats all, folks')

threading.Thread(target = is_new_day).start()
threading.Thread(target = measure_rainfall).start()
