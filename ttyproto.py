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

def abtslackline(receveabt, linetext):
	interx=[(receveabt[1]), (receveabt[2]),(receveabt[3]), (receveabt[4]), (receveabt[5]), (receveabt[6]), (receveabt[7]), (receveabt[8]), (receveabt[9]), (receveabt[10]), (receveabt[11]), (receveabt[12]), (receveabt[13]), (receveabt[14]), (receveabt[15]), (receveabt[16]), (receveabt[17]), (receveabt[18]), (receveabt[19]), (receveabt[20]), (receveabt[21]), (receveabt[22]), (receveabt[23]), (receveabt[24]), (receveabt[25]),(receveabt[26]), (linetext)]
	return interx

def abtcharblit(receveabtb, charblit):
	if charblit=="\n":
		receveabtb=abtslackline(receveabtb, "")
	else:
		charnum=0
		curr=receveabtb[26]
		for f in curr:
			if charnum==36:
				receveabtb=abtslackline(receveabtb, "")
			charnum += 1
		receveabtb[26]=((receveabtb[26]) + charblit)
			
			

for fnx in abt:
	fnx=fnx.replace('\n', '')
	abttext=simplefont.render(fnx, True, (255, 255, 255), (0, 0, 0))
	screensurf.blit(abttext, (0, pixcnt1))
	pixcnt1 += pixjmp
pygame.display.update()
screensurf.fill((0,0,0))

abt=(abtslackline(abt, "test"))

time.sleep(1)
pixcnt1=0

for fnx in abt:
	fnx=fnx.replace('\n', '')
	abttext=simplefont.render(fnx, True, (255, 255, 255), (0, 0, 0))
	screensurf.blit(abttext, (0, pixcnt1))
	pixcnt1 += pixjmp
pygame.display.update()

evhappenflg2=0
while evhappenflg2==0:
		time.sleep(.1)
		for event in pygame.event.get():
			if event.type == KEYDOWN and event.key == K_RETURN:
				evhappenflg2=1
				break