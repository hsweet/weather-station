import  RPi.GPIO as GPIO
import sys
# sys will allow for passing command line parameters
import time
#  use time.ctime() for human readable time stamp or
#  time.time for a timestamp easier to use for calculations

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN,pull_up_down=GPIO.PUD_UP)

#  read command line arguments to choose metric or imperial 
# .argv[0] is program name
# empty argument, defaults to Imperial
if len(sys.argv) <2 or sys.argv[1] == 'i':    
    units = 'i'
elif sys.argv[1] == 'm':
    units = 'm'
else:
    exit('Usage:  wind.py i or wind py m')
    
def wind(cycles, units):
    '''takes the average of several measurements of wind speed

uses interupts, so will just wait till there is wind to send result.
Default is to use Imperial units
    '''
    start = time.time()                 # start timer
    for impulse_count in range(cycles):
        GPIO.wait_for_edge(23, GPIO.RISING)  # Rising or falling edge 
    duration = time.time() - start      # how long it took
    frequency = cycles / duration       # in Hz (cycles per second)
    if units == "i":                    # imperial
        speed = 1.492 * frequency
        print ('using imperial units')
    elif units == "m":                  # metric
        speed = 2.4 * frequency
        print ('using metric units')
    return (speed)
 
while True:
    try:
        speed = (wind(10, units))
        print("{} | {:.2f}".format(time.ctime(),speed))
        log = open('/var/www/html/windlog.txt', 'a')
        #log.write (str(time.time()) +"  " + str(speed)[:5] + '\n')
        log.write (str(speed)[:5] + '\n')
        log.close()
        time.sleep (1)
    except KeyboardInterrupt:
         log.close()
         exit('Thats all, folks')
