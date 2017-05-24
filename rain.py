#import  RPi.GPIO as GPIO
import threading
import time
import datetime

#GPIO.setmode(GPIO.BCM)
#GPIO.setup(12, GPIO.IN,pull_up_down=GPIO.PUD_UP)
 
rainfall = 0 

def daily_rainfall():
    '''            Total daily rainfall log

    Each midnight, log the total rainfall for the day.
    Set the current_day variable to the new day, wait another 24 hours
    Runs in a separate thread so it will work even if the mail loop is
    not active, which is true when there is no rain
    '''
    now = datetime.datetime.now()
    new_day = str(now.year) + str(now.month) + str(now.day)   #will change after midnight
    current_day, most_rain = 0, 0
    while True:
        now = datetime.datetime.now()
        #new_day = now.minute                    # for testing .. changes each minute
        new_day = str(now.year) + str(now.month) + str(now.day)   #will change after midnight
        
        if rainfall > most_rain:
            most_rain = rainfall
        print ("Rainfall is {},total accumulation {}".format(rainfall, most_rain))
        
        if current_day != new_day:              # it's a new day
            current_day = new_day
            
            print ('Total rainfall for {}-{}-{} is {}'.format (now.month, now.day,now.year, most_rain))
            try:
                log = open('dailyrain.log' , 'a')
                log.write('{} {:.2f}\n'.format(datetime.datetime.now().strftime("%Y-%m-%d"), most_rain))
                log.close()
            except:
                print ('Cannot write to daily log file')
            most_rain = 0            # reset daily
            # time.sleep(10)
        else:
            time.sleep(60)
            print ('Waking up, it is still today, going back to sleep')


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
        ####################### Measure Rainfall ######################     
        if (inputValue == False):
            x = x + 1
            rainfall = x * 0.011
            print (round(rainfall,4))
        time.sleep(600)               # remove after testing

        ####################  Reset at Midnight #####################
        now = datetime.datetime.now()
        new_day = str(now.year) + str(now.month) + str(now.day)   #will change after midnight
        # day = now.minute           # for faster testing
        if current_day != new_day:
            current_day = new_day
            x = 0
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
