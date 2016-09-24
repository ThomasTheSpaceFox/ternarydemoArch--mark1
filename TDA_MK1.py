#!/usr/bin/env python
import libtfont0
import libtrom
import pygame.event
import pygame.key
import pygame.display
import pygame.image
import pygame.mixer
import pygame
from pygame.locals import *
import time
import os
import libTDAcommon
import libbaltcalc
import libttext
pygame.display.init()
screensurf=pygame.display.set_mode((648, 486))
pygame.display.set_caption("TDA Mark 1", "TDA Mark 1")
pygame.font.init()
simplefont = pygame.font.SysFont(None, 16)
pixcnt1=0
pixjmp=14

abt=["TDA", "Mark 1", "v1.0", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "ready", ""]

#config defaults
BOOTUPFILE="BOOTUP.TROM"
CPUWAIT=(0.1)


execfile('BOOTUP.CFG')
#print BOOTUPFILE

#4 trit instruct
#6 trit data.
#as such:
#iiiidddddd

#RAMBANK startup begin
RAMbank = {}

#calmlst = open("ORDEREDLIST6.txt")

#ramstart
for ramadr in libTDAcommon.calmlst:
	#print "foobar"
	ramadr=ramadr.replace("\n", "")
	RAMbank[ramadr] = "000000"
	#

#RAMBANK startup end

ROMFILE=BOOTUPFILE
stopflag=0
EXECCHANGE=0
#ROMFILE=open(BOOTUPFILE)
EXECADDR="------"
REG1="000000"
REG2="000000"
while stopflag==0:
	curinst=(libtrom.tromreadinst(EXECADDR,ROMFILE))
	curdata=(libtrom.tromreaddata(EXECADDR,ROMFILE))
	#ROM READ (first register)
	if curinst=="----":
		REG1=(libtrom.tromreaddata(EXECADDR,ROMFILE))
		#print("----")
	#ROM READ (second register)
	elif curinst=="---0":
		REG2=(libtrom.tromreaddata(EXECADDR,ROMFILE))
		#print("---0")
	#IO READ REG1
	elif curinst=="---+":
		REG1=RAMbank[curdata]
		#print("---+")
	#IO READ REG2
	elif curinst=="--0-":
		REG2=RAMbank[curdata]
		#print("--0-")
	#IO WRITE REG1
	elif curinst=="--00":
		RAMbank[curdata] = REG1	
	#IO WRITE REG2
	elif curinst=="--0+":
		RAMbank[curdata] = REG2
	#swap primary Registers
	elif curinst=="--+-":
		REGTEMP = REG1
		REG1 = REG2
		REG2 = REGTEMP 
	#copy Register 1 to register 2
	elif curinst=="--+0":
		REG2 = REG1
	#copy Register 2 to register 1
	elif curinst=="--++":
		REG1 = REG2
	#invert register 1
	elif curinst=="-0--":
		REG1 = (libbaltcalc.BTINVERT(REG1))
	#invert register 2
	elif curinst=="-0-0":
		REG2 = (libbaltcalc.BTINVERT(REG2))
	#add both registers, load awnser into REG1
	elif curinst=="-0-+":
		REG1 = (libTDAcommon.trunkto6(libbaltcalc.btadd(REG1, REG2)))
	#sub both registers, load awnser into REG1
	elif curinst=="-00-":
		REG1 = (libTDAcommon.trunkto6(libbaltcalc.btsub(REG1, REG2)))
	#mul both registers, load awnser into REG1
	elif curinst=="-000":
		REG1 = (libTDAcommon.trunkto6(libbaltcalc.btmul(REG1, REG2)))
	#dev both registers, load awnser into REG1
	elif curinst=="-00+":
		REG1 = (libTDAcommon.trunkto6(libbaltcalc.btdev(REG1, REG2)))
	#set REG1
	elif curinst=="-0+-":
		REG1 = curdata
	#set REG1
	elif curinst=="-0+0":
		REG2 = curdata
	#SHUTDOWN VM
	elif curinst=="000-":
		stopflag=1
	#NULL INSTRUCTION (DOES NOTHING) USE WHEN YOU WISH TO DO NOTHING :p
	elif curinst=="0000":
		print("NULLinstruction")
	#goto rom adress specified by CURRENT DATA
	elif curinst=="000+":
		EXECADDRNEXT=curdata
		EXECCHANGE=1
	#goto rom adress specified by Register 1
	elif curinst=="00+-":
		EXECADDRNEXT=REG1
		EXECCHANGE=1
	
	elif curinst=="00+0":
		if REG1==REG2:
			EXECADDRNEXT=curdata
			EXECCHANGE=1
	#dump register 1 to TTY
	elif curinst=="++0+":
		print ("REG1 DUMP:" + REG1)
		abt=libTDAcommon.abtslackline(abt, ("REG1 DUMP:" + REG1))
	#dump Register 2 to TTY
	elif curinst=="+++-":
		print ("REG2 DUMP:" + REG2)
		abt=libTDAcommon.abtslackline(abt, ("REG2 DUMP:" + REG2))
	#tty write port (direct)
	elif curinst=="+++0":
		abt=libTDAcommon.abtcharblit(abt, (libttext.charcodelook(curdata)))
	#Buzzer (direct)
	elif curinst=="++++":
		print "derp"
	#print(EXECADDR)
	
	if EXECADDR=="++++++":
		stopflag=1
	EXECADDR=libbaltcalc.btadd(EXECADDR, "+")
	if EXECCHANGE==1:
		EXECCHANGE=0
		#print("ding")
		EXECADDR=EXECADDRNEXT
	#clear buffer secion of IObus
	#this means: DONT USE THE BUFFER SECTION OF THE IObus AS RAM :|
	#chklist = open("ORDEREDLIST6REGISTER.txt")
	for ramadr in libTDAcommon.chklist:
		#print "foobar"
		ramadr=ramadr.replace("\n", "")
		RAMbank[ramadr] = "000000"
		#
	screensurf.fill((0,127,255))
	for fnx in abt:
		fnx=fnx.replace('\n', '')
		abttext=simplefont.render(fnx, True, (255, 255, 255), (0, 0, 0))
		screensurf.blit(abttext, (0, pixcnt1))
		pixcnt1 += pixjmp
	pixcnt1=0
	pygame.display.update()
	time.sleep(CPUWAIT)
	
	evhappenflg2=0


while evhappenflg2==0:
		time.sleep(.1)
		for event in pygame.event.get():
			if event.type == KEYDOWN and event.key == K_RETURN:
				evhappenflg2=1
				break
	