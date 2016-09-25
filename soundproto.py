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


pygame.mixer.init(frequency=22050 , size=-16)


#poor man's wave generator :p
def sqblksnd(reptimes, multit):
	ex="!"
	til="^"
	sampl=(((ex * reptimes) + (til * reptimes)) * multit)
	return sampl
#wavsp=(sqblksnd(220, 20))
	
	
def mk1buzz(code):
	timechar=code[0]
	print timechar
	if timechar=="+":
		timemag=60
	elif timechar=="-":
		timemag=20
	else:
		timemag=40
	freqcode=((code[1]) + (code[2]) + (code[3]) + (code[4]) +(code[5]))
	print freqcode
	baserep=160
	repjump=2
	magn=libTDAcommon.buzznumstruct5(freqcode)
	repadd=(repjump * magn)
	samplmag=sqblksnd((baserep + repadd), (20))
	sampltnk=samplmag[:6480]
	if timechar=="+":
		sampltnk=(sampltnk + sampltnk + sampltnk + sampltnk + sampltnk)
	elif timechar=="-":
		sampltnk=(sampltnk)
	else:
		sampltnk=(sampltnk + sampltnk + sampltnk)
	print sampltnk
	return sampltnk

wavsp=mk1buzz("0-----")

snf=pygame.mixer.Sound(wavsp)

snf.play()
time.sleep(1)
wavsp=mk1buzz("0+++++")

snf=pygame.mixer.Sound(wavsp)

snf.play()

evhappenflg2=0
while evhappenflg2==0:
		time.sleep(.1)
		for event in pygame.event.get():
			if event.type == KEYDOWN and event.key == K_RETURN:
				evhappenflg2=1
				break
