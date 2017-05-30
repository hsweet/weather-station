#import  RPi.GPIO as GPIO
import threading
import time
import datetime

#GPIO.setmode(GPIO.BCM)
#GPIO.setup(12, GPIO.IN,pull_up_down=GPIO.PUD_UP)

starting = True   # Don't write to log at startup
rainfall = 0

def daily_rainfall():
    '''            Total daily rainfall log

    Each midnight, log the total rainfall for the day.
    Set the current_day variable to the new day, wait another 24 hours
    Runs in a separate thread so it will work even if the mail loop is
    not active, which is true when there is no rain
    '''
    now = datetime.datetime.now()
    new_day = str(now.year) + str(now.month) + str(now.day)   #changes ay midnight
    current_day, total_daily_rain = 0, 0
    
    while True:
        global rainfall, starting
        now = datetime.datetime.now()
        # new_day = now.minute                    # for testing .. changes each minute
        new_day = str(now.year) + str(now.month) + str(now.day)   # midnight
        
        if rainfall > total_daily_rain:
            total_daily_rain = rainfall
        print ("Rainfall is {},total accumulation {}".format(rainfall, total_daily_rain))
        
        if current_day != new_day and starting == False:              # Program already running @ midnight
            print ('It is a new day')
            current_day = new_day
            rainfall = 0                        # won't be reset by rain guage unless rain at midnight!
            # but could be a concurency issue if it is raining and the other thread is trying to write
            # the rainfall amount at the same time this as this thread 
            
            print ('Total rainfall for {}-{}-{} is {}'.format (now.month, now.day,now.year, total_daily_rain))
            try:
                log = open('dailyrain.log' , 'a')
                log.write('{} {:.2f}\n'.format(datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S"), total_daily_rain))
                log.close()
            except:
                print ('Cannot write to daily log file')
            total_daily_rain = 0            # reset daily
        else:
            time.sleep(60)
            print ('Waking up, it is still today, going back to sleep')
            
        starting = False                             # program is already running

def read_rain_guage():
    '''Read rain guage, write aculmulating log during a rain
       Runs with an interupt so only runs when there is rain,  
       Resets to zero when it detects a change of day

    '''
    x = 0
    now = datetime.datetime.now()
    day = str(now.year) + str(now.month) + str(now.day)   #will change after midnight
    current_day = 0 
    
    while True:
        #inputValue = GPIO.input(12)                        #poll  or
        #inputValue = GPIO.wait_for_edge(12, GPIO.RISING)   #interupt
        inputValue = 0              # for testing only
        global rainfall
        
        ####################  Reset at Midnight #####################
        # should happen before guage is read to insure reading is reset 
        # next rain day
        now = datetime.datetime.now()
        new_day = str(now.year) + str(now.month) + str(now.day)# midnight
        #new_day = now.minute           # for faster testing
        if current_day != new_day:
            current_day = new_day
            x = 0
        ####################### Measure Rainfall ######################     
        if (inputValue == False):
            x = x + 1
            rainfall = x * 0.011
            print (round(rainfall,4))
        time.sleep(1200)               # remove after testing
        ##################### write to log file ######################
        try:
            log = open('rain.log', 'a')
            log.write("{} {:.2f}  \n".format (datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S"), rainfall))
            log.close()
        except KeyboardInterrupt:
             log.close()
             exit('Thats all, folks')
             

threading.Thread(target = daily_rainfall).start()
threading.Thread(target = read_rain_guage).start()
