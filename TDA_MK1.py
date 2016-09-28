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
import libtbuzz
pygame.display.init()
screensurf=pygame.display.set_mode((648, 486))
pygame.display.set_caption("TDA Mark 1", "TDA Mark 1")
pygame.font.init()
#used for TTY
simplefont = pygame.font.SysFont(None, 16)
#used for smaller data displays (inst. data etc.)
smldispfont = pygame.font.SysFont(None, 16)
#used in larger data displays (register displays, etc.)
lgdispfont = pygame.font.SysFont(None, 20)
pixcnt1=40
pixjmp=14
#graphics:
#background pixmap
vmbg=pygame.image.load(os.path.join('GFX', 'VMBG.png'))
#indicator lamps
#GREEN
LEDGREENON=pygame.image.load(os.path.join('GFX', 'LAMP-GREEN.png'))
LEDGREENOFF=pygame.image.load(os.path.join('GFX', 'LAMP-GREEN-OFF.png'))
#CPU
CPULEDACT=pygame.image.load(os.path.join('GFX', 'LAMP-BLUE.png'))
CPULEDSTANDBY=pygame.image.load(os.path.join('GFX', 'LAMP-ORANGE.png'))

COLORDISP=pygame.image.load(os.path.join('GFX', 'COLORDISP-DEF.png'))
MONODISP=pygame.image.load(os.path.join('GFX', 'MONODISP-DEF.png'))
#this list is what is displayed on the TTY on VM boot.

abt=["TDA", "Mark 1", "v2.0.1", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "ready", ""]

pygame.mixer.init(frequency=22050 , size=-16)



wavsp=libtbuzz.mk1buzz("0-----")
snf=pygame.mixer.Sound(wavsp)
snf.play()

#config defaults
TROMA="BOOTUP.TROM"
#these are dud roms full of soft stops
TROMB=("DEFAULTdud.TROM")
TROMC=("DEFAULTdud.TROM")
TROMD=("DEFAULTdud.TROM")
TROME=("DEFAULTdud.TROM")
TROMF=("DEFAULTdud.TROM")
CPUWAIT=(0.1)
stepbystep=0

execfile('BOOTUP.CFG')
#print BOOTUPFILE

#4 trit instruct
#6 trit data.
#as such:
#iiiidddddd

if stepbystep==1:
	STEPLED=LEDGREENON
else:
	STEPLED=LEDGREENOFF


#RAMBANK startup begin
RAMbank = {}

#calmlst = open("ORDEREDLIST6.txt")
screensurf.fill((0,127,255))
screensurf.blit(vmbg, (0, 0))
pygame.display.update()

#ramstart
for ramadr in libTDAcommon.calmlst:
	#print "foobar"
	ramadr=ramadr.replace("\n", "")
	RAMbank[ramadr] = "000000"
	#

MONODISPBIG=pygame.transform.scale(MONODISP, (144, 144))
COLORDISPBIG=pygame.transform.scale(COLORDISP, (148, 148))
#RAMBANK startup end
colorreg="++++++"
ROMFILE=TROMA
ROMLAMPFLG="A"
stopflag=0
EXECCHANGE=0
#ROMFILE=open(BOOTUPFILE)
EXECADDR="------"
REG1="000000"
REG2="000000"
while stopflag==0:
	curinst=(libtrom.tromreadinst(EXECADDR,ROMFILE))
	curdata=(libtrom.tromreaddata(EXECADDR,ROMFILE))
	#some screen display stuff & general blitting
	#screensurf.fill((0,127,255))
	#draw Background
	screensurf.blit(vmbg, (0, 0))
	#these show the instruction and data in the instruction/data box :)
	insttext=smldispfont.render(curinst, True, (0, 255, 255), (0, 0, 0))
	datatext=smldispfont.render(curdata, True, (0, 255, 127), (0, 0, 0))
	screensurf.blit(insttext, (552, 40))
	screensurf.blit(datatext, (590, 40))
	#these draw the register displays :)
	reg1text=lgdispfont.render(REG1, True, (255, 0, 127), (0, 0, 0))
	reg2text=lgdispfont.render(REG2, True, (255, 127, 0), (0, 0, 0))
	screensurf.blit(reg1text, (558, 78))
	screensurf.blit(reg2text, (558, 118))
	#and here is what draws the ROM address display :)
	reg2text=lgdispfont.render(EXECADDR, True, (0, 127, 255), (0, 0, 0))
	screensurf.blit(reg2text, (558, 158))
	#and the current rom display :)
	CURROMTEXT=("ROM " + ROMLAMPFLG)
	reg2text=lgdispfont.render(CURROMTEXT, True, (255, 0, 255), (0, 0, 0))
	screensurf.blit(reg2text, (558, 198))
	#LED LAMPS
	#CPU
	screensurf.blit(CPULEDACT, (605, 433))
	#STEP
	screensurf.blit(STEPLED, (605, 440))
	screensurf.blit(COLORDISPBIG, (358, 48))
	screensurf.blit(MONODISPBIG, (358, 198))
	#TTY drawer :)
	for fnx in abt:
		fnx=fnx.replace('\n', '')
		abttext=simplefont.render(fnx, True, (0, 127, 255), (0, 0, 0))
		screensurf.blit(abttext, (45, pixcnt1))
		pixcnt1 += pixjmp
	pixcnt1=40
	
	#aaaaannnnddd update display! :D
	pygame.display.update()
	
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
	#color draw
	elif curinst=="0---":
		jx=libTDAcommon.drawnumstruct3((curdata[0] + curdata[1] + curdata[2]))
		jy=libTDAcommon.drawnumstruct3((curdata[3] + curdata[4] + curdata[5]))
		RGBcol=libTDAcommon.colorfind(colorreg)
		#print monocol
		pygame.draw.line(COLORDISP, RGBcol, [jx, jy], [jx, jy], 1)
		COLORDISPBIG=pygame.transform.scale(COLORDISP, (148, 148))
	#set PPU color Register
	elif curinst=="0--0":
		colorreg=curdata
	elif curinst=="0--+":
		RGBcol=libTDAcommon.colorfind(curdata)
		#print monocol
		COLORDISP.fill(RGBcol)
		COLORDISPBIG=pygame.transform.scale(COLORDISP, (148, 148))
	#mono draw
	#mono draw pixel
	elif curinst=="0-+-":
		jx=libTDAcommon.drawnumstruct2((curdata[0] + curdata[1]))
		jy=libTDAcommon.drawnumstruct2((curdata[2] + curdata[3]))
		monocol=(int(libTDAcommon.dollytell((curdata[4] + curdata[5]))))
		#print monocol
		pygame.draw.line(MONODISP, (monocol, monocol, monocol), [jx, jy], [jx, jy], 1)
		MONODISPBIG=pygame.transform.scale(MONODISP, (144, 144))
	#mono fill
	elif curinst=="0-+0":
		monocol=(int(libTDAcommon.dollytell((curdata[4] + curdata[5]))))
		#print monocol
		MONODISP.fill((monocol, monocol, monocol))
		MONODISPBIG=pygame.transform.scale(MONODISP, (144, 144))
	#SHUTDOWN VM
	elif curinst=="000-":
		stopflag=1
		abt=libTDAcommon.abtslackline(abt, "VM SYSHALT:")
		abt=libTDAcommon.abtslackline(abt, "soft stop.")
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
	elif curinst=="00++":
		waitchop=curdata[5]
		if waitchop=="+":
			waitmagn=3
		elif waitchop=="-":
			waitmagn=2
		else:
			waitmagn=1
		time.sleep((CPUWAIT * waitmagn))
	#note these swap TROMS
	#TROMA: goto rom adress on TROMA specified by CURRENT DATA
	elif curinst=="+---":
		EXECADDRNEXT=curdata
		EXECCHANGE=1
		ROMFILE=TROMA
		ROMLAMPFLG="A"
	#conditional GOTO
	elif curinst=="+--0":
		if REG1==REG2:
			EXECADDRNEXT=curdata
			EXECCHANGE=1
			ROMFILE=TROMA
			ROMLAMPFLG="A"
	#TROMB: goto rom adress on TROMB specified by CURRENT DATA
	elif curinst=="+--+":
		EXECADDRNEXT=curdata
		EXECCHANGE=1
		ROMFILE=TROMB
		ROMLAMPFLG="B"
	elif curinst=="+-0-":
		if REG1==REG2:
			EXECADDRNEXT=curdata
			EXECCHANGE=1
			ROMFILE=TROMB
			ROMLAMPFLG="B"
	#TROMC: goto rom adress on TROMC specified by CURRENT DATA
	elif curinst=="+-00":
		EXECADDRNEXT=curdata
		EXECCHANGE=1
		ROMFILE=TROMC
		ROMLAMPFLG="C"
	#conditional GOTO
	elif curinst=="+-0+":
		if REG1==REG2:
			EXECADDRNEXT=curdata
			EXECCHANGE=1
			ROMFILE=TROMC
			ROMLAMPFLG="C"
	#TROMD: goto rom adress on TROMD specified by CURRENT DATA
	elif curinst=="+-+-":
		EXECADDRNEXT=curdata
		EXECCHANGE=1
		ROMFILE=TROMD
		ROMLAMPFLG="D"
	#conditional GOTO
	elif curinst=="+-+0":
		if REG1==REG2:
			EXECADDRNEXT=curdata
			EXECCHANGE=1
			ROMFILE=TROMD
			ROMLAMPFLG="D"
	#TROME: goto rom adress on TROME specified by CURRENT DATA
	elif curinst=="+-++":
		EXECADDRNEXT=curdata
		EXECCHANGE=1
		ROMFILE=TROME
		ROMLAMPFLG="E"
	#conditional GOTO
	elif curinst=="+0--":
		if REG1==REG2:
			EXECADDRNEXT=curdata
			EXECCHANGE=1
			ROMFILE=TROME
			ROMLAMPFLG="E"
	#TROMF: goto rom adress on TROMF specified by CURRENT DATA
	elif curinst=="+0-0":
		EXECADDRNEXT=curdata
		EXECCHANGE=1
		ROMFILE=TROMF
		ROMLAMPFLG="F"
	#conditional GOTO
	elif curinst=="+0-+":
		if REG1==REG2:
			EXECADDRNEXT=curdata
			EXECCHANGE=1
			ROMFILE=TROMF
			ROMLAMPFLG="F"
	
	
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
		snf.stop()
		#print "derp"
		wavsp=libtbuzz.mk1buzz(curdata)
		snf=pygame.mixer.Sound(wavsp)
		snf.play()
		timechop=curdata[0]
		if timechop=="+":
			time.sleep(0.3)
		elif timechop=="-":
			time.sleep(0.1)
		else:
			time.sleep(0.2)
		
	
	
	#print(EXECADDR)
	if stepbystep==1:
		#this is used when step-by-step mode is enabled
		evhappenflg2=0
		while evhappenflg2==0:
			time.sleep(.1)
			for event in pygame.event.get():
				if event.type == KEYDOWN and event.key == K_RETURN:
					evhappenflg2=1
					break
				if event.type == KEYDOWN and event.key == K_ESCAPE:
					stopflag=1
					abt=libTDAcommon.abtslackline(abt, "VM SYSHALT:")
					abt=libTDAcommon.abtslackline(abt, "User stop.")
					evhappenflg2=1
					break
		
	else:
		#...otherwise this is used to passivly check for imput
		for event in pygame.event.get():
			if event.type == KEYDOWN and event.key == K_ESCAPE:
				stopflag=1
				abt=libTDAcommon.abtslackline(abt, "VM SYSHALT:")
				abt=libTDAcommon.abtslackline(abt, "User stop.")
				break
	pygame.event.clear()
	
	if curinst=="":
		stopflag=1
		abt=libTDAcommon.abtslackline(abt, "VM SYSHALT:")
		abt=libTDAcommon.abtslackline(abt, "End Of Rom.")
	if EXECADDR=="+------":
		stopflag=1
		abt=libTDAcommon.abtslackline(abt, "VM SYSHALT:")
		abt=libTDAcommon.abtslackline(abt, "End Of RomBus.")
	EXECADDR=libbaltcalc.btadd(EXECADDR, "+")
	if EXECCHANGE==1:
		EXECCHANGE=0
		#print("ding")
		EXECADDR=EXECADDRNEXT
	if stopflag==1:
		abt=libTDAcommon.abtslackline(abt, "Press enter to exit.")
		screensurf.fill((0,127,255))
		screensurf.blit(vmbg, (0, 0))
	
		#these show the instruction and data in the instruction/data box :)
		insttext=smldispfont.render(curinst, True, (0, 255, 255), (0, 0, 0))
		datatext=smldispfont.render(curdata, True, (0, 255, 127), (0, 0, 0))
		screensurf.blit(insttext, (552, 40))
		screensurf.blit(datatext, (590, 40))
		#these draw the register displays :)
		reg1text=lgdispfont.render(REG1, True, (255, 0, 127), (0, 0, 0))
		reg2text=lgdispfont.render(REG2, True, (255, 127, 0), (0, 0, 0))
		screensurf.blit(reg1text, (558, 78))
		screensurf.blit(reg2text, (558, 118))
		#and here is what draws the ROM address display :)
		reg2text=lgdispfont.render(EXECADDR, True, (0, 127, 255), (0, 0, 0))
		screensurf.blit(reg2text, (558, 158))
		#LED LAMPS
		screensurf.blit(COLORDISPBIG, (358, 48))
		screensurf.blit(MONODISPBIG, (358, 198))
		
		CURROMTEXT=("ROM " + ROMLAMPFLG)
		reg2text=lgdispfont.render(CURROMTEXT, True, (255, 0, 255), (0, 0, 0))
		screensurf.blit(reg2text, (558, 198))
		
		screensurf.blit(CPULEDSTANDBY, (605, 433))
		screensurf.blit(STEPLED, (605, 440))
		for fnx in abt:
			fnx=fnx.replace('\n', '')
			abttext=simplefont.render(fnx, True, (0, 127, 255), (0, 0, 0))
			screensurf.blit(abttext, (45, pixcnt1))
			pixcnt1 += pixjmp
		pixcnt1=38
	
	
	pygame.display.update()
	#clear buffer secion of IObus
	#this means: DONT USE THE BUFFER SECTION OF THE IObus AS RAM :|
	#chklist = open("ORDEREDLIST6REGISTER.txt")
	for ramadr in libTDAcommon.chklist:
		#print "foobar"
		ramadr=ramadr.replace("\n", "")
		RAMbank[ramadr] = "000000"
		#
	
	
	time.sleep(CPUWAIT)
	
	evhappenflg2=0


while evhappenflg2==0:
		time.sleep(.1)
		for event in pygame.event.get():
			if event.type == KEYDOWN and event.key == K_RETURN:
				evhappenflg2=1
				break
	