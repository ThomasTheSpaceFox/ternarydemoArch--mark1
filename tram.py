#!/usr/bin/env python
import libbaltcalc
import libTDAcommon

#this is a test of the RAM system.

RAMbank = {}

calmlst = open("ORDEREDLIST6.txt")

#ramstart
for ramadr in calmlst:
	#print "foobar"
	ramadr=ramadr.replace("\n", "")
	RAMbank[ramadr] = "000000"
	#

print RAMbank
print RAMbank["+000++"]
RAMbank["+000++"] = "++++++"
print RAMbank["+000++"]