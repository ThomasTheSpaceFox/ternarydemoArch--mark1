#!/usr/bin/env python
import libTDAcommon

def tromreadinst(romaddr, ROMNAME):
	line=libTDAcommon.numstruct(romaddr)
	n = open(ROMNAME)
	linecnt=1
	for fdelta in n:
		if linecnt==line:
			dataret=((fdelta[0]) + (fdelta[1]) + (fdelta[2]) + (fdelta[3]))
			
			return dataret
		linecnt += 1
			
def tromreaddata(romaddr, ROMNAME):
	line=libTDAcommon.numstruct(romaddr)
	n = open(ROMNAME)
	linecnt=1
	for fdelta in n:
		if linecnt==line:
			dataret=((fdelta[4]) + (fdelta[5]) + (fdelta[6]) + (fdelta[7]) + (fdelta[8]) + (fdelta[9]))
			return dataret
		linecnt += 1

#print(tromreadinst("------", "BOOTUP.TROM"))
#print(tromreaddata("------", "BOOTUP.TROM"))
