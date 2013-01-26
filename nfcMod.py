#!/usr/bin/python

import nfc
import nfc.ndef

def main():
    clf = nfc.ContactlessFrontend()

    while True:
        tag = clf.poll()
        if tag and tag.ndef:
            break

    message = nfc.ndef.Message(tag.ndef.message)
    for record in message:
        if record.type == "urn:nfc:wkt:T":
            text = nfc.ndef.TextRecord(record)
            print text.language + ": " + text.text

if __name__ == '__main__':
    main()
