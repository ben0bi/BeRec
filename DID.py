#!/usr/bin/env python
# -*- coding: utf-8 -*-

# DID DIsplay Driver
# display driver for BURP
# BURP + Benobis Universal Recorder & Player
# by Benedict "Oki Wan Benobi" Jäggi @ MMXX

# import the stuff for the display
import sys
sys.path.append('./')
import rgb1602

# only used for the menu status.
import globals

# the display driver itself.
lcd = 0

# display color for resetting.
DIR = 0
DIG = 63
DIB = 0
# actual display color.
DIAR = 0
DIAG = 63
DIAB = 0

# show menu
# previous menu consisted of arrows showing what which button does.
# now it shows if sd cards are mounted and if random play is active.
# symbols are in brackets, all other chars are WYSIWIG including spaces!
# Using Internal drive:
# [sd1_status][sd2_status][etc..] [random_status]
# where card (sdx) has 2 symbols: "no card" and "card"
# and random has 2 symbols: random and straight
# previous menu, just for your consideration, which was only visible in stop mode:
# [uparrow]:[play][pause] [downarrow]:[stop] [leftarrow]:[leftarrow] [rightarrow]:[rightarrow]
def showPlayMenu():
	""" show a menu on the lower line """
	global lcd
#	global DISYM_UPARROW, DISYM_DOWNARROW, DISYM_LEFTARROW, DISYM_RIGHTARROW
#	global DISYM_PLAY, DISYM_PAUSE, DISYM_STOP, DISYM_REW, DISYM_FWD
	global DISYM_CARD, DISYM_NOCARD, DISYM_INTERNAL_DRIVE
	global DISYM_RND_STRAIGHT, DISYM_RND_RANDOM
# draw menu
# we can use 6 custom symbols at once:
# 0 is reserved for the symbol function
# 7 is reserved for the watch symbol in play mode.
# all symbols need to be set before an lcd operation is done.
	lcd.customSymbol(1, DISYM_INTERNAL_DRIVE)
	lcd.customSymbol(2, DISYM_NOCARD)
	lcd.customSymbol(3, DISYM_CARD)
	lcd.customSymbol(4, DISYM_RND_STRAIGHT)
	lcd.customSymbol(5, DISYM_RND_RANDOM)
	lcd.setCursor(0,1)
	if(globals.BURP_USE_INTERNAL_DRIVE>0):
		# show symbol for internal drive
		lcd.write(1)
	else:
		for d in globals.BURP_SDdirs:
			if(d[2]==0):
				# it is not mounted.
				lcd.write(2)
			else:
				# it is mounted.
				lcd.write(3)
# show status of random play flag.
	lcd.printout(" ")
	if globals.BURP_ISRANDOM<=0:
		lcd.write(4)
	else:
		lcd.write(5)

# update scrolling texts.
DI_SCROLLWAITTIME = 200 # wait 200 ms until next processing.
DI_SCROLLACTUALTIME = 0
def DI_UPDATE(deltatime):
	global DI_TITLE, DI_TITLEPOSITION, DI_TITLEDIRECTION
	global DI_SYMBOL, DION
	global DI_SCROLLWAITTIME
	global DI_SCROLLACTUALTIME
	# return at begin to save processor time.
	if(DION==0):
		return

	# maybe scroll the title
	if(len(DI_TITLE)>15):
		DI_SCROLLACTUALTIME = DI_SCROLLACTUALTIME + deltatime
		if(DI_SCROLLACTUALTIME>DI_SCROLLWAITTIME):
			DI_SCROLLACTUALTIME=DI_SCROLLACTUALTIME % DI_SCROLLWAITTIME
			DI_TITLEPOSITION = DI_TITLEPOSITION + DI_TITLEDIRECTION
			if(DI_TITLEPOSITION>=len(DI_TITLE)-12): # +3 waits some time at end.
				DI_TITLEDIRECTION = -1
			if(DI_TITLEPOSITION<=-3): # -3: this waits some time at start
				DI_TITLEDIRECTION = 1
	else:
		# do not scroll
        	DI_TITLEPOSITION = 0
        	DI_TITLEDIRECTION = 1

	# constrain the waiting at the end.
	dp=DI_TITLEPOSITION
	if(dp>len(DI_TITLE)-15):
		dp=len(DI_TITLE)-15

	# set the text
	t = DI_TITLE[dp:dp+15]
	lcd.setCursor(1,0)
	lcd.printout(t)
	# show the actual symbol over the text.
	# text is shown on xpos 1 and symbol on xpos 0 either,
	# but safe is safe.
	symbol(DI_SYMBOL)

# set a specific color for the display
# but leave the saved value as it is.
def color(red, green, blue):
	global lcd
	global DIAR, DIAG, DIAB
	DIAR=red
	DIAG=green
	DIAB=blue
	lcd.setPWM(0x04, red)
	lcd.setPWM(0x03, green)
	lcd.setPWM(0x02, blue)

# set a specific color for the display and save it.
def setcolor(red, green, blue):
	global DIR, DIG, DIB
	DIR=red
	DIG=green
	DIB=blue
	color(red,green,blue)

# completely clear the display
def clear():
	global lcd
	lcd.setCursor(0,0)
	lcd.printout("                ")
	lcd.setCursor(0,1)
	lcd.printout("                ")
	lcd.setPWM(0x02,0)
	lcd.setPWM(0x03,0)
	lcd.setPWM(0x04,0)

# show a specific symbol at the symbol position.
DI_SYMBOL = 0
DI_SYMBOL_X = 0
DI_SYMBOL_Y = 0
def symbol(which):
	global lcd, DI_SYMBOL, DI_SYMBOL_X, DI_SYMBOL_Y
	DI_SYMBOL = which
	if(DI_SYMBOL==0):
		return
	lcd.customSymbol(0, which)
	lcd.setCursor(DI_SYMBOL_X,DI_SYMBOL_Y)
	lcd.write(0)

# upper text parameters.
DI_TITLE = "[Nothing]"
DI_TITLEPOSITION = 0
DI_TITLEDIRECTION = 1
# set the text on the upper line, it will scroll if it is longer.
def uppertext(text):
	""" set a new text in the upper line. """
	global DI_TITLE, DI_TITLEPOSITION, DI_TITLEDIRECTION
	DI_TITLE = text
	DI_TITLEPOSITION = 1
	DI_TITLEDIRECTION = -1 # position 0 and direction -1 waits some time at startup.

# fade the display out after some time.
DITIME = 5000 # display time until it fades out, in milliseconds.
DION = 1 # is the display on?
DITIME_ACTUAL = 0
def DI_FADE_OUT(frametime):
	""" fade out the display after some time. """
	global DITIME, DITIME_ACTUAL, DION
	global DIAR, DIAG, DIAB
	if(DION==1):
		DITIME_ACTUAL=DITIME_ACTUAL+frametime
		if(DITIME_ACTUAL>=DITIME):
			# decrease all colours
			if(DIAR>0):
				DIAR=DIAR-3
			if(DIAG>0):
				DIAG=DIAG-3
			if(DIAB>0):
				DIAB=DIAB-3
			# maybe set them to 0
			if(DIAR<0):
				DIAR=0
			if(DIAG<0):
				DIAG=0
			if(DIAB<0):
				DIAB=0
			# set the color but not the values.
			color(DIAR,DIAG,DIAB)
		if(DIAR<=0 and DIAG<=0 and DIAB<=0):
			# finally turn off the display.
			DION=0
			DITIME_ACTUAL=0.0

# turn the display on with the actual color.
PLAYMENUSHOWED=0
def DI_ON():
	""" turn on the display. """
	global DIR, DIG, DIB
	global DION, DITIME_ACTUAL
	global PLAYMENUSHOWED
	color(DIR, DIG, DIB)
	DITIME_ACTUAL=0.0
	PLAYMENUSHOWED = 0
	DION=1

# initialize the display.
def DI_INIT():
	""" initialize the display. """
	global lcd
	lcd=rgb1602.RGB1602(16,2) #create LCD object,specify col and row

# clear the bottom line
def DI_CLEARBOTTOM():
	lcd.setCursor(0,1)
	lcd.printout("                ")

# show a time mark in the lower right.
def showTimeMark(seconds):
	""" show time in hours:minutes:seconds in the lower right.
	if there are no hours, it only shows minutes:seconds """
	global lcd
	global DISYM_WATCH
	lcd.customSymbol(7,DISYM_WATCH)
	minutes = 0
	hours = 0
	if(seconds>0):
		minutes = int(seconds/60)
		seconds = seconds%60
	if(minutes>0):
		hours=int(minutes/60)
		minutes=minutes%60
	t = str(seconds)
	if(len(t)==1):
		t='0'+t
	#if(minutes>0 or hours>0):
	m=str(minutes)
	if(len(m)==1):
		m='0'+m
		minutes=m
	t = str(minutes)+":"+t
	if(hours>0):
		t=str(hours)+":"+t
	lcd.setCursor(15-len(t),1)
	lcd.write(7)
	lcd.printout(t)

# for the deltatime calculation
import numpy as np
import datetime

# get frametime
FRAMETIME_OLD = 0.0
deltatime = 0.0
def frametime_init():
	""" Initialize the frametime counter so there will be no ruckeling. """
	global FRAMETIME_OLD
	FRAMETIME_OLD = np.datetime64(datetime.datetime.now(), 'ms')

def frametime_tick():
	""" call this every loop rotation. it gets the deltatime since the last rotation. """
	global FRAMETIME_OLD, deltatime
	fr = np.datetime64(datetime.datetime.now(), 'ms') # more precise than 'now' (?)
	deltatime = fr - FRAMETIME_OLD
	deltatime = deltatime.astype('int16')
	FRAMETIME_OLD = fr

# Display Symbols

# make some custom characters  for the display character table:
# symbol number 0 is reserved for the symbol function, leaves 7 to use directly.
DISYM_UPARROW = [
  0b00000,
  0b00100,
  0b01110,
  0b10101,
  0b00100,
  0b00100,
  0b00000,
  0b00000
]
DISYM_DOWNARROW = [
  0b00000,
  0b00100,
  0b00100,
  0b10101,
  0b01110,
  0b00100,
  0b00000,
  0b00000
]
DISYM_RIGHTARROW = [
  0b00000,
  0b00100,
  0b00010,
  0b11111,
  0b00010,
  0b00100,
  0b00000,
  0b00000
]

DISYM_LEFTARROW = [
  0b00000,
  0b00100,
  0b01000,
  0b11111,
  0b01000,
  0b00100,
  0b00000,
  0b00000
]

DISYM_STOP = [
  0b00000,
  0b00000,
  0b11110,
  0b11110,
  0b11110,
  0b11110,
  0b00000,
  0b00000
]

DISYM_PAUSE = [
  0b00000,
  0b01010,
  0b01010,
  0b01010,
  0b01010,
  0b01010,
  0b00000,
  0b00000
]

DISYM_PLAY = [
  0b00000,
  0b01000,
  0b01100,
  0b01110,
  0b01100,
  0b01000,
  0b00000,
  0b00000
]

# special symbols not used yet.
DISYM_REC = [
  0b00000,
  0b01110,
  0b11111,
  0b11111,
  0b11111,
  0b01110,
  0b00000,
  0b00000
]
# warning: the display seems to support only 8 symbols at once.
DISYM_RECPAUSE = [
  0b00000,
  0b01110,
  0b10001,
  0b10001,
  0b10001,
  0b01110,
  0b00000,
  0b00000
]

# a little watch
DISYM_WATCH = [
  0b00000,
  0b01110,
  0b10101,
  0b10111,
  0b10001,
  0b01110,
  0b00000,
  0b00000
]

# the welcome screen symbol.
DISYM_SMILEY = [
  0b01110,
  0b11111,
  0b10101,
  0b11111,
  0b10001,
  0b11011,
  0b01110,
  0b00000
]

# No Card Inserted.
DISYM_NOCARD = [
  0b11100,
  0b01110,
  0b00111,
  0b10011,
  0b11001,
  0b11100,
  0b11110,
  0b00000
]

# Card Inserted.
DISYM_CARD = [
  0b11100,
  0b10010,
  0b10001,
  0b10001,
  0b10001,
  0b10001,
  0b11111,
  0b00000
]

# Internal Drive
DISYM_INTERNAL_DRIVE = [
  0b00000,
  0b10110,
  0b10101,
  0b10101,
  0b10101,
  0b10110,
  0b00000,
  0b00000
]

# Random: not symbol
DISYM_RND_STRAIGHT = [
  0b00000,
  0b00100,
  0b00010,
  0b00100,
  0b00000,
  0b11111,
  0b00000,
  0b00000
]

# Random: yes symbol
DISYM_RND_RANDOM = [
  0b00000,
  0b00100,
  0b00010,
  0b00100,
  0b00010,
  0b10101,
  0b01000,
  0b00000
]
