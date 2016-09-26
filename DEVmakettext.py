#!/usr/bin/env python
import libttext


#a useful tool to convert text to TDA MK1 machene code :)
#remember!!! no more than 729 inctrucions and 1 instruction per character,
#and remember to leave 1 instruction for the soft stop instruction ;)
CONVTEXT='''Hello :)
This is Ternary Demo Arch Mark 1.
This is a nice intro. c:

This VM is a Balanced ternary
computer.

What you see here is actual machine
code autoconverted by the DEV tool:
DEVmakettext.py :)

This is running in the VM in
real-time. Each character takes 1
CPU instruction. thats why these
characters are being displayed like
this. :)

You can see to your right, various
real-time status displays. :)

press escape to stop the VM.

do see the config file.
(BOOTUP.CFG)

you will find help in the DOCS
directory.

this is a TROM.
TROMs are the programs for TDA MK1.

now this is not a supercomputer,
but do have fun :)'''

CONVTEXT="--------------------------"

codeBat=""
#just open the output file in your code editor of choice, and copy it 
#into your TROM
#this is how the intros were made :)
outn = open('./DEVmakettext-output.txt', 'w')

for f in CONVTEXT:
	outn.write("+++0" + (libttext.charlook(f)) + "\n")



