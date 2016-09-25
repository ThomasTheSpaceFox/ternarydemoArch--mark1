#!/usr/bin/env python
import libTDAcommon



#poor man's wave generator :p
def sqblksnd(reptimes, multit):
	ex="!"
	til="^"
	sampl=(((ex * reptimes) + (til * reptimes)) * multit)
	return sampl
#wavsp=(sqblksnd(220, 20))
	
	
def mk1buzz(code):
	timechar=code[0]
	#print timechar
	if timechar=="+":
		timemag=60
	elif timechar=="-":
		timemag=20
	else:
		timemag=40
	freqcode=((code[1]) + (code[2]) + (code[3]) + (code[4]) +(code[5]))
	#print freqcode
	baserep=160
	repjump=2
	magn=libTDAcommon.buzznumstruct5(freqcode)
	magn=(243 - magn)
	repadd=(repjump * magn)
	samplmag=sqblksnd((baserep + repadd), (20))
	sampltnk=samplmag[:6480]
	if timechar=="+":
		sampltnk=(sampltnk + sampltnk + sampltnk + sampltnk + sampltnk)
	elif timechar=="-":
		sampltnk=(sampltnk)
	else:
		sampltnk=(sampltnk + sampltnk + sampltnk)
	#print sampltnk
	return sampltnk
