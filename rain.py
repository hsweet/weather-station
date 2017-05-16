import  RPi.GPIO as GPIO
import time


GPIO.setmode(GPIO.BCM)
GPIO.setup(12, GPIO.IN,pull_up_down=GPIO.PUD_UP)

x=0

while True:
    inputValue = GPIO.input(12)
    if (inputValue == False):
        #add if you need to count
        #print(x)
        x=x+1
        rainfall=x*0.011
        print (rainfall)
    time.sleep(0.05)
