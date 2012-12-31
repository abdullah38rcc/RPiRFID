
serials = {}

class CardSerials():
    def __init__(self):
        pass

def findSerial(fileName, textString):
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

def parseFile(inFile):
    localFile = open(inFile, "r")
    s = []
    d = {}

    for line in localFile.readlines():
        line.rstrip()
        s.append(line)
    localFile.close()
    # print s
    
    for x in s:
        d[x] = True
        
    print d
    

def getFile(filePath):
    pass


if __name__ == '__main__':
    # import urllib
    # import twisted?
    # fetch file

 
    parseFile("dlserials.txt")

    serials = {'a', 'b'}
    print serials
    

