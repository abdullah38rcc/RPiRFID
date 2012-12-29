from smartcard.CardMonitoring import CardMonitor, CardObserver
from smartcard.util import * 

from twisted.web.server import Site
from twisted.web.resource import Resource
from twisted.internet import reactor
try:
    import RPi.GPIO as GPIO
    GPIO_available = True
except ImportError:
    GPIO_available = False
import urllib
import threading
import time

# Global
# authorized = False

# Web content handler
class ReturnWebpage(Resource):
    def __init__(self, serialNum):
        Resource.__init__(self)
        self.serialNum = serialNum

    def render_GET(self, request):
        authorized = findSerial('dlserials.txt', str(self.serialNum))
        return "<html><body><pre>%s</pre></body></html>" % (authorized,)

# Root webpage
class getSerial(Resource):
    def getChild(self, name, request):
        return ReturnWebpage(int(name))

class CardObserver(CardObserver):
    def __init__(self):
        pass

    def update(self, observable, (addedcards, removedcards)):
        print "Added:  ", addedcards
        print "Removed:", removedcards

class CardObservingThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        # Instanciate a monitor
        self.cardmonitor = CardMonitor()
        # Create a new observerable
        self.cardobserver = CardObserver()
        self.success = False

    def run(self):
        self.cardmonitor.addObserver(self.cardobserver)
        try:

            self.success = True
            print "card observer added"
        except:
            print "addObserver exception"
            if (self.cardmonitor == None):
                            print "cardmonitor does not exist"
            if (self.cardobserver == None):
                            print "cardobserver does not exist"

# Class for background flashing of LED
class FlashLED(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
	def run(self):
		print 'flashing led'
		GPIO.setup(12, GPIO.HIGH)
		time.sleep(1)
		GPIO.setup(12, GPIO.LOW)

# Pulls down file from dropbox and saves to local disk
def download(url):
    """ Download file from web and save """
    print 'Saving file ', url
    webFile = urllib.urlopen(url)
    localFile = open("dlserials.txt", "w")
    localFile.write(webFile.read())
    webFile.close()
    localFile.close()
    print 'done'

# Background process to fetch file every minute		
class FetchFile(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.kill = False
    def run(self):
        while (not self.kill):
            n = 0
            # Check for a new file every 60 (2 * 30) seconds
            while (not self.kill) and (n < 30):
                time.sleep(2)
                n += 1
            download('http://dl.dropbox.com/u/2435953/dlserials.txt')
    def stop(self):
        self.kill == True

def findSerial(fileName, textString):
    infile = open (fileName, "r")
    text = infile.read()
    infile.close()

    search = textString
    index = text.find(search)
    if index > 0:
        print search, "found at index", index
        if GPIO_available:
            background = FlashLED()
            background.start()
        return True
    else:
        print 'Serial not found'
        return False

def GPIOinit():
    # Set GPIO for RPi pin numbers
    GPIO.setmode(GPIO.BOARD)
    # set 12 as output
    GPIO.setup(12, GPIO.OUT)
    # set 12 low
    GPIO.setup(12, GPIO.LOW)
	
if __name__ == '__main__':
    import sys
    if len(sys.argv) == 2:
        try:
            download(sys.argv[1])
        except IOError:
            print 'Filename not found.'
    else:
        
        # Setup GPIO
        if GPIO_available:
            GPIOinit()

        # Start card monitor
        card = CardObservingThread()
        card.start()

        if (card.success == True):
            print "Starting Background File Service"
            # Start file grabbing process
            backgroundFile = FetchFile()
            backgroundFile.start()

            print "Starting Web Server"
            # Start web server
            root = getSerial()
            factory = Site(root)
            reactor.listenTCP(8880, factory)
            reactor.run()

        while True:
            i = raw_input ("q for exit ")
            if (i == 'q'):
                if (backgroundFile != None):
                    backgroundFile.stop()
                break
