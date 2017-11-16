import  RPi.GPIO as GPIO
import time
import datetime

GPIO.setmode(GPIO.BCM)
GPIO.setup(12, GPIO.IN,pull_up_down=GPIO.PUD_UP)

# globals, dom is set to a date that is not in any month
x, rainfall,dom = 0,0,0

def is_new_day(day):
    global dom
    if dom != day:      # new day
        dom = day
        return True
    else:
        return False    # same day

while True:
    #           Check for rain
    
    #inputValue = GPIO.input(12)                        #poll  or
    inputValue = GPIO.wait_for_edge(12, GPIO.RISING)   #interupt
    #inputValue = 0                                      #for testing
    if (inputValue == False):
        x=x+1
        rainfall=x*0.011
        # print (rainfall)
    time.sleep(1)

    #           Check for new day, save daily rainfall total
    today = datetime.datetime.now()
    next_day = is_new_day(str(today.month) + str(today.day))
    if next_day == True:
        
        #       add daily total to daily rain log
        # print ('Total rainfall for {}-{}-{} is {}'.format (today.month, today.day,today.year, rainfall))
        try:
            log = open('dailyrain.log' , 'a')
            log.write('{} {:.2f}\n'.format(datetime.datetime.now().strftime("%Y-%m-%d"), rainfall))
            log.close()
        except:
            print ('Cannot write to daily log file')
    
    #       write to log file
    try:
        log = open('rain.log', 'a')
        log.write("{} {:.2f}  \n".format (datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S"), rainfall))
        log.close()
    except KeyboardInterrupt:
         log.close()
         exit('Thats all, folks')
