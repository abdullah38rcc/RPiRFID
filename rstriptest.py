#!/usr/bin/python

import logging

logging.basicConfig()
logger = logging.getLogger('rstriptest.py')
logger.setLevel(logging.DEBUG)

def addCard(serialString):
	print serialString
	logger.debug("Attempting to add %s", serialString)
	# num = serialString.find('ACS')
	num = serialString.find('/')
	if (num > 0):
		logger.debug('Found delimiter at %s', num)
		serialStripped = serialString[:num]
	
	# serialStripped = '3B 8F 80 01 80 4F 0C A0 00 00 03 06 03 00 03 00 00 00 00 68'
	logger.debug('Post formating: %s', serialStripped)


testString = '00 00 03 06 03 00 03 00 00 00 00 68 / ACS dslfsd', 'nothing'
addCard(testString[0])



