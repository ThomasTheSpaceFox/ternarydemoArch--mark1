#!/usr/bin/env python
import libTDAcommon
import libbaltcalc
import libttext

#tasmfile="assmtst1.tasm"

#tasminput=open(tasmfile)
import fileinput

print("TDA-asm v1.0.0 starting")

assmoverrun=729
instcnt=0
txtblk=0

outfile="assmout.trom"


firstloop=1
for linen in fileinput.input():
	if firstloop==1:
		assmflename=fileinput.filename()
		assmnamelst=assmflename.rsplit('.', 1)
		outfile=(assmnamelst[0] + (".trom"))
		outn = open(outfile, 'w')
	lined=linen
	linen=linen.replace("\n", "")
	linen=linen.replace("	", "")
	linelist=linen.split("|")
	if (len(linelist))==2:
		instword=(linelist[0])
		instdat=(linelist[1])
	else:
		instword=(linelist[0])
		instdat="000000"
	if instword=="textstop":
		txtblk=0
	
	if txtblk==1:
		for f in lined:
			outn.write("+++0" + (libttext.charlook(f)) + "\n")
			instcnt += 1
	elif instword=="textstart":
		txtblk=1
	#raw class
	elif instword=="romread1":
		outn.write("----" + instdat + "\n")
		instcnt += 1
	elif instword=="romread2":
		outn.write("---0" + instdat + "\n")
		instcnt += 1
	elif instword=="IOread1":
		outn.write("---+" + instdat + "\n")
		instcnt += 1
	elif instword=="IOread2":
		outn.write("--0-" + instdat + "\n")
		instcnt += 1
	elif instword=="IOwrite1":
		outn.write("--00" + instdat + "\n")
		instcnt += 1
	elif instword=="IOwrite2":
		outn.write("--0+" + instdat + "\n")
		instcnt += 1
	elif instword=="regswap":
		outn.write("--+-" + instdat + "\n")
		instcnt += 1
	elif instword=="copy1to2":
		outn.write("--+0" + instdat + "\n")
		instcnt += 1
	elif instword=="copy2to1":
		outn.write("--++" + instdat + "\n")
		instcnt += 1
	elif instword=="invert1":
		outn.write("-0--" + instdat + "\n")
		instcnt += 1
	elif instword=="invert2":
		outn.write("-0-0" + instdat + "\n")
		instcnt += 1
	elif instword=="add":
		outn.write("-0-+" + instdat + "\n")
		instcnt += 1
	elif instword=="subtract":
		outn.write("-00-" + instdat + "\n")
		instcnt += 1
	elif instword=="multiply":
		outn.write("-000" + instdat + "\n")
		instcnt += 1
	elif instword=="divide":
		outn.write("-00+" + instdat + "\n")
		instcnt += 1
	elif instword=="setreg1":
		outn.write("-0+-" + instdat + "\n")
		instcnt += 1
	elif instword=="setreg2":
		outn.write("-0+0" + instdat + "\n")
		instcnt += 1
	#----jump in used opcodes----
	#color drawing
	elif instword=="colorpixel":
		outn.write("0---" + instdat + "\n")
		instcnt += 1
	elif instword=="setcolorreg":
		outn.write("0--0" + instdat + "\n")
		instcnt += 1
	elif instword=="colorfill":
		outn.write("0--+" + instdat + "\n")
		instcnt += 1
	elif instword=="setcolorvect":
		outn.write("0-0-" + instdat + "\n")
		instcnt += 1
	elif instword=="colorline":
		outn.write("0-00" + instdat + "\n")
		instcnt += 1
	elif instword=="colorrect":
		outn.write("0-0+" + instdat + "\n")
		instcnt += 1
	#mono drawing
	elif instword=="monopixel":
		outn.write("0-+-" + instdat + "\n")
		instcnt += 1
	elif instword=="monofill":
		outn.write("0-+0" + instdat + "\n")
		instcnt += 1
	elif instword=="setmonovect":
		outn.write("0-++" + instdat + "\n")
		instcnt += 1
	elif instword=="monoline":
		outn.write("00--" + instdat + "\n")
		instcnt += 1
	elif instword=="monorect":
		outn.write("00-0" + instdat + "\n")
		instcnt += 1
	#----opcode 00-+ unused----
	elif instword=="stop":
		outn.write("000-" + instdat + "\n")
		instcnt += 1
	elif instword=="null":
		outn.write("0000" + instdat + "\n")
		instcnt += 1
	elif instword=="gotodata":
		outn.write("000+" + instdat + "\n")
		instcnt += 1
	elif instword=="gotoreg1":
		outn.write("00+-" + instdat + "\n")
		instcnt += 1
	elif instword=="gotodataif":
		outn.write("00+0" + instdat + "\n")
		instcnt += 1
	elif instword=="wait":
		outn.write("00++" + instdat + "\n")
		instcnt += 1
	elif instword=="YNgoto":
		outn.write("0+--" + instdat + "\n")
		instcnt += 1
	elif instword=="userwait":
		outn.write("0+-0" + instdat + "\n")
		instcnt += 1
	elif instword=="TTYclear":
		outn.write("0+-+" + instdat + "\n")
		instcnt += 1
	#----gap in used opcodes----
	elif instword=="gotoA":
		outn.write("+---" + instdat + "\n")
		instcnt += 1
	elif instword=="gotoAif":
		outn.write("+--0" + instdat + "\n")
		instcnt += 1
	elif instword=="gotoB":
		outn.write("+--+" + instdat + "\n")
		instcnt += 1
	elif instword=="gotoBif":
		outn.write("+-0-" + instdat + "\n")
		instcnt += 1
	elif instword=="gotoC":
		outn.write("+-00" + instdat + "\n")
		instcnt += 1
	elif instword=="gotoCif":
		outn.write("+-0+" + instdat + "\n")
		instcnt += 1
	elif instword=="gotoD":
		outn.write("+-+-" + instdat + "\n")
		instcnt += 1
	elif instword=="gotoDif":
		outn.write("+-+0" + instdat + "\n")
		instcnt += 1
	elif instword=="gotoE":
		outn.write("+-++" + instdat + "\n")
		instcnt += 1
	elif instword=="gotoEif":
		outn.write("+0--" + instdat + "\n")
		instcnt += 1
	elif instword=="gotoF":
		outn.write("+0-0" + instdat + "\n")
		instcnt += 1
	elif instword=="gotoFif":
		outn.write("+0-+" + instdat + "\n")
		instcnt += 1
	#----gap in used opcodes----
	elif instword=="dumpreg1":
		outn.write("++0+" + instdat + "\n")
		instcnt += 1
	elif instword=="dumpreg2":
		outn.write("+++-" + instdat + "\n")
		instcnt += 1
	elif instword=="TTYwrite":
		outn.write("+++0" + instdat + "\n")
		instcnt += 1
	elif instword=="buzzer":
		outn.write("++++" + instdat + "\n")
		instcnt += 1
	if instcnt>assmoverrun:
		print("ERROR!: assembler has exceded rom size limit of 729!")


print ("TDA Mk1 assembly file \"" + assmflename + "\" has been compiled into: \"" + outfile + "\"")