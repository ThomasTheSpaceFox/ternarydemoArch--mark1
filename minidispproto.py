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
vmbg=pygame.image.load(os.path.join('GFX', 'VMBG.png'))
screensurf.blit(vmbg, (0, 0))
pygame.display.update()

COLORDISP=pygame.image.load(os.path.join('GFX', 'COLORDISP-DEF.png'))
MONODISP=pygame.image.load(os.path.join('GFX', 'MONODISP-DEF.png'))

pygame.display.update()
def dollytell(lookupcode):
	if lookupcode=="--":
		return("0")
	if lookupcode=="-0":
		return("32")
	if lookupcode=="-+":
		return("64")
	if lookupcode=="0-":
		return("96")
	if lookupcode=="00":
		return("127")
	if lookupcode=="0+":
		return("159")
	if lookupcode=="+-":
		return("191")
	if lookupcode=="+0":
		return("223")
	if lookupcode=="++":
		return("255")


def colorfind(CODE):
	REDBT = (CODE[0] + CODE[1])
	GRNBT = (CODE[2] + CODE[3])
	BLUBT = (CODE[4] + CODE[5])
	REDBIN = (dollytell(REDBT))
	GRNBIN = (dollytell(GRNBT))
	BLUBIN = (dollytell(BLUBT))
	#NAME = datalist
	return((int(REDBIN), int(GRNBIN), int(BLUBIN)))




pygame.draw.line(screensurf, (colorfind("++0000")), [300, 300], [300,300], 1)
pygame.display.update()

def drawpixcolor(CDISP, COL, jXY):

	jx=libTDAcommon.drawnumstruct3((jXY[0] + jXY[1] + jXY[2]))
	pygame.draw.line(DISP, colorfind(COL), [jx, jy], [jx, jy], 1)

#def drawpixmono(MDISP, COLXY)

	
def makerectbipoint(Jx1, Jy1, Jx2, Jy2):
	if Jx1>Jx2:
		sizeX=(Jx1-Jx2)
		xval=Jx2
	else:
		sizeX=(Jx2-Jx1)
		xval=Jx1
	if Jy1>Jy2:
		yval=Jy2
		sizeY=(Jy1-Jy2)
	else:
		sizeY=(Jy2-Jy1)
		yval=Jy1
	return(pygame.Rect((xval, yval), (sizeX, sizeY)))
		

screensurf.fill((255, 255, 255), (makerectbipoint(40, 40, 0, 0)))
pygame.display.update()
evhappenflg2=0
while evhappenflg2==0:
		time.sleep(.1)
		for event in pygame.event.get():
			if event.type == KEYDOWN and event.key == K_RETURN:
				evhappenflg2=1
				break



