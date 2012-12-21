from smartcard.CardMonitoring import CardMonitor, CardObserver
from smartcard.util import *

# a simple card observer that prints inserted/removed cards
# http://pyscard.sourceforge.net/pyscard-usersguide.html#monitoringsmartcards

class printobserver( CardObserver ):
    """A simple card observer that is notified
    when cards are inserted/removed from the system and
    prints the list of cards
    """
    def update( self, observable, (addedcards, removedcards) ):
        for card in addedcards:
            print "+Inserted: ", toHexString( card.atr )
        for card in removedcards:
            print "-Removed: ", toHexString( card.atr )


