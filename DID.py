# DID DIsplay Driver
# display driver for BURP
# BURP + Benobis Universal Recorder & Player

# import the stuff for the display
import sys
sys.path.append('./')
import rgb1602

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

# update scrolling texts.
def DI_UPDATE():
	global DI_TITLE, DI_TITLEPOSITION, DI_TITLEDIRECTION
	global DI_SYMBOL, DION
	# return at begin to save processor time.
	if(DION==0):
		return

	if(len(DI_TITLE)>15):
        	DI_TITLEPOSITION = DI_TITLEPOSITION + DI_TITLEDIRECTION
        	if(DI_TITLEPOSITION>=len(DI_TITLE)-12): # +3 waits some time at end.
			DI_TITLEDIRECTION = -1
		if(DI_TITLEPOSITION<=-3): # -3: this waits some time at start
			DI_TITLEDIRECTION = 1
	else:
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
	# should do nothing because the cursor was
	# set to position 1 for the text and 0 for
	# the symbol but....here you have it:
	# uncomment this below.
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
def symbol(which):
	global lcd, DI_SYMBOL
	DI_SYMBOL = which
	lcd.setCursor(0,0)
	lcd.write(which)

# upper text parameters.
DI_TITLE = "[Nothing]"
DI_TITLEPOSITION = 0
DI_TITLEDIRECTION = 1
# set the text on the upper line, it will scroll if it is longer.
def uppertext(text):
	global DI_TITLE, DI_TITLEPOSITION, DI_TITLEDIRECTION
	DI_TITLE = text
	DI_TITLEPOSITION = 1
	DI_TITLEDIRECTION = -1 # position 0 and direction -1 waits some time at startup.

# fade the display out after some time.
DITIME = 5 # display time until it fades out, in seconds.
DION = 1 # is the display on?
DITIME_ACTUAL = 0.0
def DI_FADE_OUT(frametime):
	global DITIME, DITIME_ACTUAL, DION
	global DIAR, DIAG, DIAB
	if(DION==1):
		DITIME_ACTUAL=DITIME_ACTUAL+frametime
		if(DITIME_ACTUAL>=DITIME):
			if(DIAR>0):
				DIAR=DIAR-3
			if(DIAG>0):
				DIAG=DIAG-3
			if(DIAB>0):
				DIAB=DIAB-3
			if(DIAR<0):
				DIAR=0
			if(DIAG<0):
				DIAG=0
			if(DIAB<0):
				DIAB=0
			color(DIAR,DIAG,DIAB)
		if(DIAR<=0 and DIAG<=0 and DIAB<=0):
			DION=0
			DITIME_ACTUAL=0.0

# turn the display on with the actual color.
def DI_ON():
    global DIR, DIG, DIB
    global DION, DITIME_ACTUAL
    color(DIR, DIG, DIB)
    DITIME_ACTUAL=0.0
    DION=1

# initialize the display.
def DI_INIT():
    global lcd
    lcd=rgb1602.RGB1602(16,2) #create LCD object,specify col and row

# show menu
def showPlayMenu():
	global DIREF_UPARROW, DIREF_DOWNARROW, DIREF_LEFTARROW, DIREF_RIGHTARROW
	global DIREF_PLAY, DIREF_PAUSE, DIREF_STOP, DIREF_REW, DIREF_FWD
	lcd.setCursor(0,1)
	lcd.write(DIREF_UPARROW)
	lcd.printout(":")
	lcd.write(DIREF_PLAY)
	lcd.write(DIREF_PAUSE)
	lcd.printout(" ")
	lcd.write(DIREF_DOWNARROW)
	lcd.printout(":")
	lcd.write(DIREF_STOP)
	lcd.printout(" ")
	lcd.write(DIREF_LEFTARROW)
	lcd.printout(":")
	lcd.write(DIREF_LEFTARROW)
	lcd.printout(" ")
	lcd.write(DIREF_RIGHTARROW)
	lcd.printout(":")
	lcd.write(DIREF_RIGHTARROW)

# Display Symbols
# make some custom characters and their reference ids
# for the display character table:
DIREF_UPARROW = 0
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
DIREF_DOWNARROW = 1
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
DIREF_RIGHTARROW = 2
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
DIREF_LEFTARROW = 3
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
DIREF_STOP = 4
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
DIREF_PAUSE = 5
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
DIREF_PLAY = 6
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
DIREF_REC = 7
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
DIREF_RECPAUSE = 8
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
