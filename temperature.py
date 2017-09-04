import os
import glob
import time
import datetime
 
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
 
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'
 
def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines
 
def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1: 
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        #return temp_c, temp_f    # returns a tuple, if you want both
        return temp_f       # just farenheight
  

while True:
    temperature = read_temp()
    #print (temperature)
     ##################### write to log file ######################
    try:
        log = open('/var/www/html/temperature.log', 'a')
        log.write("{} {:.2f}  \n".format (datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S"), temperature))
        log.close()
    except KeyboardInterrupt:
         log.close()
         exit('Thats all, folks')
    ############################################
    time.sleep(1)
