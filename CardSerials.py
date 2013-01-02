import logging


class CardSerials():
    def __init__(self):
        logging.basicConfig()
        self.logger = logging.getLogger('CardSerials.py')
        self.logger.setLevel(logging.DEBUG)
        
        self.currentCards = []
        self.d = {}
        self.serials = {}
        
    def addCard(self, serial):
        self.currentCards.append(serial)
    
    def removeCard(self, serial):
        self.currentCards.remove(serial)
    
    def validCards(self):
        """Returns True if there are any cards present that are authorized"""
        for s in self.currentCards:
            if s in self.d:
                return True
            else:
                return False
    
    def parseFile(self, inFile):
        """Take in a file of serial numbers and return a dictionary of serials"""
        
        # Open the file for reading in
        localFile = open(inFile, "r")
    
        # transfer lines of serials to a list        
        s = []
        
        for line in localFile.readlines():
            line = line.rstrip()
            s.append(line)
        localFile.close()
        self.logger.debug('Parsed File into List:')
        self.logger.debug(self.s)
   
        # transfer serials from the list to a dictionary
        for x in s:
            self.d[x] = True
        self.logger.debug('Parsed Dictionary')
        self.logger.debug(self.d)
        
        return self.d
    

def oldFindSerial(fileName, textString):
    infile = open (fileName, "r")
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

