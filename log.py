import time

class Log:
    def __init__(self, logname):
        self.logname = logname
        self.description = 'Use: instance = Log(name)'
        self.path = '/var/www/html/'
        self.fullname = self.path + self.logname

    def write(self, data):
        self.data = data
        try:
            log = open (self.fullname, 'a')
            log.write(self.data + '\n')
        except:
            print('Cannot write to log file')
        log.close
        
#******************************* sample instance ******************
logname = 'temperature.log'
temperature = time.time()
t=Log(logname)
print (t.description)


while True:
    
    t.write(str(temperature))
    time.sleep(5)
