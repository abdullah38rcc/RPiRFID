#!/usr/bin/python

import nfc
import nfc.ndef
import time

def main():
    clf = nfc.ContactlessFrontend()
    print "vCLF: ", clf
    print "clf type: ", type(clf)
    print "clv.dev type: ", type(clf.dev)


    """
    while True:
        tag = clf.poll()
        if tag and tag.ndef:
            break
            """
    tag = clf.poll()

    # while tag.is_present:
    #    tag = clf.poll()
    #    if tag.ndef:
    #        break
    if not tag is None:
        print "vTag.uid: '%s'", tag.getUID()

    """
    message = nfc.ndef.Message(tag.ndef.message)
    for record in message:
        if record.type == "urn:nfc:wkt:T":
            text = nfc.ndef.TextRecord(record)
            print text.language + ": " + text.text """


def loop():
    clf = nfc.ContactlessFrontend()

    while (True):        
        tag = clf.poll()
        if not tag is None:
            print "UID:", tag.getUID()
        else:
            print "No Tag"
        clf.poll()
        time.sleep(1)

if __name__ == '__main__':
    loop()
