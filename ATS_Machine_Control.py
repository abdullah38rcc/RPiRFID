#!/usr/bin/python

import logging
logging.basicConfig()
log = logging.getlog(__name__)
# logging levels for lowest to highest: 
# debug, info, warning (default), error, critical
log.setLevel(logging.INFO)

from CardSerials import CardSerials

# from twisted.web.resource import Resource

import urllib
import threading
import time


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


def main():
    # Instanciate Serial Processor
    cs = CardSerials()

    # TODO Add command line input for URI to serial numbers file
    GPIO_available = False

    # TODO: Added file logging (http://docs.python.org/2/howto/logging.html)

    try:
        import Lamps
        GPIO_available = True
        log.info("GPIO Available")
        log.info("Enabling GPIO")
        Lamps.initGPIO()
    except ImportError:
        log.debug("GPIO Not Available")

    try:
        import nfc
    except ImportError:
        log.warning("Could not import nfc lib")
        exit()

    import nfc.nded

    nfcreader = nfc.ContactlessFrontend()
    if nfcreader is None:
        time.sleep(.5)
        # sometimes it takes more than once
        nfcreader = nfc.ContactlessFrontend()
    if nfcreader is None:
        log.warning("Could not connect to an NFC reader")
        exit()

    while(True):
        tag = nfcreader.poll()
        if tag is None:
            if (GPIO_available):
                Lamps.noBadge()
        else:
            tagNumber = tag.getUID()

        if tagNumber is not None:
            log.info("Found badge: %s", tag.getUID())
            if cs.findCard(tagNumber):
                log.info("Found an authorized badge")
                if (GPIO_available):
                    log.info("Turning on Green Lamp")
                    Lamps.badgeMatch()
            else:
                log.infi("Present badge is not authorized")
                if (GPIO_available):
                    log.info("Turning on Red Lamp")
                    Lamps.badgeNotFound()
        time.sleep(1)

if (__name__ == "__main__"):
    main()
