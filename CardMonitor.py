from sys import stdin, exc_info
from time import sleep

from smartcard.CardMonitoring import CardMonitor, CardObserver
from smartcard.util import *


# a simple card observer that prints inserted/removed cards
class printobserver(CardObserver):
    """A simple card observer that is notified
    when cards are inserted/removed from the system and
    prints the list of cards
    """

    def update(self, observable, (addedcards, removedcards)):
        for card in addedcards:
            print "+Inserted: ", toHexString(card.atr), card.atr
        for card in removedcards:
            print "-Removed: ", toHexString(card.atr)

try:
    cardmonitor = CardMonitor()
    cardobserver = printobserver()
    cardmonitor.addObserver(cardobserver)
    print "Insert or remove a smartcard in the system."
    print "This program will exit in 10 seconds"
    print ""

    sleep(10)

    # don't forget to remove observer, or the
    # monitor will poll forever...
    cardmonitor.deleteObserver(cardobserver)

    import sys
    if 'win32' == sys.platform:
        print 'press Enter to continue'
        sys.stdin.read(1)

except:
    print exc_info()[0], ':', exc_info()[1]
