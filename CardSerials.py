import logging


class CardSerials():
    def __init__(self):
        logging.basicConfig()
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        self.currentCards = []  # List
        self.d = {}  # Dictionary
        self.serials = {}

    # return true if a card serial is in the list
    def cardPresent(self):
        if self.currentCards.__len__() > 0:
            self.logger.debug("self.currentCards.len=%s", str(self.currentCards.__len__()))
            self.logger.debug("")
            return True
        else:
            self.logger.debug('No cards present in currentCards[]')
            return False

    def snipSerial(self, serialSnip, delim):
        num = serialSnip.find(delim)
        self.logger.debug('Found delimiter at %s', num)
        if (num > 0):
            return serialSnip[:num].strip()
        else:
            return serialSnip

    def addCard(self, serialAdd):
        print type(serialAdd)
        self.logger.debug("Attempting to add %s", serialAdd)
        # Some serials come with a manufacture suffix so we need to remove it
        self.serialSnipped = self.snipSerial(serialAdd, '/')
        self.logger.debug('Post formating: %s', self.serialSnipped)

        try:
            self.currentCards.append(self.serialSnipped)
            self.logger.info("Added a card to the list:")
            self.logger.debug("Added serial: %s", self.serialSnipped)
        except:
            self.logger.debug("Could not add to list: %s", self.serialSnipped)

    def removeCard(self, serialRemove):
        self.logger.debug("Attempting to remove %s", serialRemove)
        self.serialSnipped = self.snipSerial(serialRemove, '/')
        self.logger.debug("Post formatting: %s", self.serialSnipped)
        try:
            self.currentCards.remove(self.serialSnipped)
            self.logger.info("Removed a card from the list")
            self.logger.debug("Removed: %s", self.serialSnipped)
        except:
            self.logger.debug("Could not remove %s", self.serialSnipped)

    def validCards(self):
        """Returns True if there are any cards present that are authorized"""
        for s in self.currentCards:
            self.logger.debug('Testing for \'%s\' in self.d', s)
            # self.logger.debug('Looking for: %s', s)
            #if (self.d[s]):
            if s in self.d:
                self.logger.info("Card found in dictionary")
                return True
            else:
                self.logger.info("Card not found in dictionary")
                return False

    def parseFile(self, inFile):
        """Take in a file of serial numbers and return a dictionary of serials"""

        # Open the file for reading in
        localFile = open(inFile, "r")

        # transfer lines of serials to a list
        s = []

        count = 0
        for line in localFile.readlines():
            count = count + 1
            line = line.rstrip()
            s.append(line)
        localFile.close()
        tempText = "Parsed " + str(count) + " lines into list:"
        self.logger.debug(tempText)
        self.logger.debug(s)

        # transfer serials from the list to a dictionary
        for x in s:
            self.d[x] = True
        self.logger.debug('Parsed Dictionary:')
        self.logger.debug(self.d)

        return self.d


def oldFindSerial(fileName, textString):
    infile = open(fileName, "r")
    text = infile.read()
    infile.close()

    search = textString
    index = text.find(search)
    if index > 0:
        print search, "found at index", index
        # if GPIO_available:
        #    background = FlashLED()
        #    background.start()
        return True
    else:
        print 'Serial not found'
        return False

if __name__ == '__main__':
    # import urllib
    # import twisted?
    # fetch file

    #d = parseFile("dlserials.txt")
    #if "3B 06 01 00 38 05 50 07" in d:
    #    print "Found"

    #print findSerial(d, "3B 06 01 00 38 05 50 07")
    pass
