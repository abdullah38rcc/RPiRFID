from smartcard.ATR import ATR
from smartcard.util import toHexString

atr = ATR([0x3B, 0x9E, 0x95, 0x80, 0x1F, 0xC3, 0x80, 0x31, 0xA0, 0x73,
0xBE, 0x21, 0x13, 0x67, 0x29, 0x02, 0x01, 0x01, 0x81,0xCD,0xB9] )
print atr
print 'historical bytes: ', toHexString( atr.getHistoricalBytes() )
print 'checksum: ', "0x%X" % atr.getChecksum()
print 'checksum OK: ', atr.checksumOK
print 'T0 supported: ', atr.isT0Supported()
print 'T1 supported: ', atr.isT1Supported()
print 'T15 supported: ', atr.isT15Supported()