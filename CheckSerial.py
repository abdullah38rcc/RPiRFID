
import urllib

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
    print search, "found at index ", index


if __name__ == '__main__':
    import sys
    if len(sys.argv) == 2:
        try:
            download(sys.argv[1])
        except IOError:
            print 'Filename not found.'
    else:
        download('http://dl.dropbox.com/u/2435953/dlserials.txt')
        findSerial('dlserials.txt', "353568")

"""
        import os
        print 'usage: %s http://server.com/file' % os.path.basename(sys.argv[0])"""
        

