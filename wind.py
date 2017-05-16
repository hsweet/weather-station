import  RPi.GPIO as GPIO
import time
import datetime
import random

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN,pull_up_down=GPIO.PUD_UP)
 
def wind(cycles):
    start = time.time()
    for pulses in range(cycles):
        time.sleep(random.randrange(0,3))
        GPIO.wait_for_edge(23, GPIO.RISING)  #Rising or falling edge give different results!
        # print (pulses)           # show the count
    duration = time.time() - start      # how long it took to count n cycles
    frequency = cycles / duration       # in Hz (cycles per second)
    wind_speed = 1.492 * frequency      # multiplier is from the manual
    return wind_speed

    # print ('Duration is {} seconds for 10 pulses. Frequency is {} hz'.format(duration, frequency))

recent_speeds = []
while True:
    # calculate max and average of day's readings.  Save data to log file.
    
    wind_speed = (wind(10))
    recent_speeds.append(wind_speed)            # save readings in a list
    # print (recent_speeds)
    raw_avg = (sum(recent_speeds)/len(recent_speeds))
    avg = format (raw_avg,'.2f')
    raw_fastest = max(recent_speeds)
    fastest = format(raw_fastest,'.2f')
    
    print('Avg speed {:.2f}'.format (sum(recent_speeds)/len(recent_speeds)))    # average speed
    print ('max {:.2f}'.format (max(recent_speeds)))                      # fastest reading
    print ('-' * 12)
    # keep the list from getting too large, or covering too much time for an average to make sense
    # this code deletes the oldest reading each time so the average is the average of the last n readings
    # not the whole day.
    if len(recent_speeds) > 100:
        del recent_speeds[0]
   
    #time.sleep (60)  #once a minute should be enough
    print ("{} | {:.2f}".format (datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S"), wind_speed))
    try:
        log = open('/var/www/html/windlog.txt', 'a')
        log.write("{} {:.2f} {} {} \n".format (datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S"), wind_speed, avg, fastest))
        log.close()
    except KeyboardInterrupt:
         log.close()
         exit('Thats all, folks')

'''
how is wind speed measured
http://www.wral.com/weather/blogpost/1283652/
'''
 
