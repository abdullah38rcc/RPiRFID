from twisted.web.server import Site
from twisted.web.resource import Resource
from twisted.internet import reactor
import RPi.GPIO as GPIO
import urllib
import threading
import time

# Web content handler
class ReturnWebpage(Resource):
    def __init__(self, serialNum):
        Resource.__init__(self)
        self.serialNum = serialNum

    def render_GET(self, request):
        return "<html><body><pre>%s</pre></body></html>" % (self.serialNum,)

# Root webpage
class getSerial(Resource):
  def getChild(self, name, request):
      return ReturnWebpage(int(name))

class FlashLED(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
	def run(self):
		print 'flashing led'
		GPIO.setup(12, GPIO.HIGH)
		time.sleep(1)
		GPIO.setup(12, GPIO.LOW)

def download(url):
    """ Download file from web and save """
    print 'Saving file ', url
    webFile = urllib.urlopen(url)
    localFile = open("dlserials.txt", "w")
    localFile.write(webFile.read())
    webFile.close()
    localFile.close()
    print 'done'

def findSerial(fileName, textString):
    infile = open (fileName, "r")
    text = infile.read()
    infile.close()

    search = textString
    index = text.find(search)
    if index > 0:
        print search, "found at index ", index
        background = FlashLED()
        background.start()
    else:
        print 'Serial not found'


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
        # Start web server
        root = getSerial()
        factory = Site(root)
        reactor.listenTCP(8880, factory)
        reactor.run()

        # Setup GPIO
        GPIOinit()

        download('http://dl.dropbox.com/u/2435953/dlserials.txt')
        findSerial('dlserials.txt', "353568")

"""
        import os
        print 'usage: %s http://server.com/file' % os.path.basename(sys.argv[0])"""
        

