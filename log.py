import time

class Log:
    def __init__(self, logname):
        self.logname = logname
        self.description = 'Use: instance = Log(name)'
        

    def write(self, data):
        self.data = data
        try:
            log = open (self.logname, 'a')
            log.write(self.data + '\n')
        except:
            print('Cannot write to log file')
        log.close
        

logname = 'temperature.log'
temperature = 50
frequency = 30
t=Log(logname)
print (t.description)


while True:
    
    t.write(str(temperature))
    time.sleep(1)


