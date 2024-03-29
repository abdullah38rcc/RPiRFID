#!/usr/bin/python

from smartcard.CardMonitoring import CardMonitor, CardObserver
from smartcard.util import *

import logging
logging.basicConfig()
log = logging.getlog(__name__)
# logging levels for lowest to highest: 
# debug, info, warning (default), error, critical
log.setLevel(logging.INFO)

from CardSerials import CardSerials

from twisted.web.server import Site
from twisted.web.resource import Resource
from twisted.internet import reactor
import urllib
import threading
import time

"""
try:
    import RPi.GPIO as GPIO
    GPIO_available = True
except ImportError:
    GPIO_available = False
"""
try:
    import Lamps
    GPIO_available = True
except ImportError:
    GPIO_available = False



# TODO: Added file logging (http://docs.python.org/2/howto/logging.html)

if (GPIO_available):
    log.debug("GPIO Available")
else:
    log.debug("GPIO Not Available")

# Setup Serial Processing Object
cs = CardSerials()


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
        if (addedcards):
            #print "addedcards: ", type(addedcards)
            # have to avoid creating another pointer
            # by converting the list element to string
            # [:] would have converted the full list
            cs.addCard(str(addedcards[0]))
            log.info('Added: %s', addedcards)
        if (removedcards):
            cs.removeCard(str(removedcards[0]))
            log.info('Removed: %s', removedcards)
"""
class CardObservingThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        # Instanciate a monitor
        self.cardmonitor = CardMonitor()
        # Create a new observerable
        self.cardobserver = CardObserver()
        self.success = False
        time.sleep(2)

    def run(self):
        try:
            self.cardmonitor.addObserver(self.cardobserver)
            self.success = True
            log.info('Card Observer Added')

        except:
            log.warning('addObserver exception')
            if (self.cardmonitor == None):
                log.warning('cardmonitor does not exist')
            if (self.cardobserver == None):
                log.warning('cardobserver does not exist')
"""

"""
# Class for background flashing of LED
class FlashLED(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        def run(self):
            print 'flashing led'
            GPIO.setup(12, GPIO.HIGH)
            time.sleep(1)
            GPIO.setup(12, GPIO.LOW)
"""


# Pulls down file from dropbox and saves to local disk
def download(url):
    """ Download file from web and save """
    log.debug('Saving File %s', url)
    webFile = urllib.urlopen(url)
    localFile = open("dlserials.txt", "w")
    localFile.write(webFile.read())
    webFile.close()
    localFile.close()
    log.debug('Done saving file')


# Background process to fetch file every minute
class FetchFile(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.kill = False
        self.newFile = False

    def run(self):
        # while (not self.kill):
        while (True):
            # Check for a new file every 60 (2 * 30) seconds
            try:
                download('http://dl.dropbox.com/u/2435953/dlserials.txt')
                logging.info('downloaded file')
                self.newFile = True
            except:
                logging.warning('could not download serial file')
            time.sleep(60)

            """
            # old thread code
            n = 0
            while (not self.kill) and (n < 30):
                time.sleep(2)
                n += 1
    def stop(self):
        self.kill = True
    """


"""
def GPIOinit():
    # Set GPIO for RPi pin numbers
    GPIO.setmode(GPIO.BOARD)
    # set 12 as output
    GPIO.setup(12, GPIO.OUT)
    # set 12 low
    GPIO.setup(12, GPIO.LOW)
"""


def main():
    import sys

    # TODO Add input for URI to serial numbers file
    if len(sys.argv) == 2:
        try:
            download(sys.argv[1])
        except IOError:
            print 'Filename not found.'
    else:
        # Setup GPIO
        if GPIO_available:
            log.info("Enabling GPIO")
            initGPIO()
            """
            # Start card monitor
            card = CardObservingThread()
            card.setDaemon(True)
            card.start()
            """
    # Instanciate a monitor
    cardmonitor = CardMonitor()
    # Create a new observerable
    cardobserver = CardObserver()

    try:
        cardmonitor.addObserver(cardobserver)
        success = True
        log.info('Card Observer Added')
    except:
        log.warning('addObserver exception')
    if (cardmonitor == None):
        log.warning('cardmonitor does not exist')
    if (cardobserver == None):
        log.warning('cardobserver does not exist')

    # if (card.is_alive()):
    if (True):
        log.info("Starting Background File Service")
        # Start file grabbing process
        backgroundFile = FetchFile()
        backgroundFile.setDaemon(True)
        backgroundFile.start()

        # Start web server
        #log.info("Starting Web Server")
        #root = getSerial()
        #factory = Site(root)
        #reactor.listenTCP(8880, factory)
        #reactor.run()
    else:
        log.warning("Did not start background file service")

    Loop = True
    while (Loop):
        # i = raw_input ("q for exit\n")
        #if (i == 'q'):
        #    log.info('Quitting')
        #    if (backgroundFile.isAlive()):
        #        backgroundFile.stop()
        #    Loop = False
            # break # breaks out of the while loop
        # New file downloaded. Parse to dict
        if (backgroundFile.newFile == True):
            backgroundFile.newFile = False
            cs.parseFile("dlserials.txt")

        if (cs.cardPresent()):
            if (cs.validCards()):
                log.info("Valid card found")
            else:
                log.info("Card Present but Not Valid")
        else:
            log.info("No Cards Present")
        time.sleep(.5)

if (__name__ == "__main__"):
    main()
