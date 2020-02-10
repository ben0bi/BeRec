# BURP
# Benobis Universal Recorder & Player
# * A music recorder behaving like an old tape recorder.
# * and an MP3 Player
# * reading data from additional SD-cards
# by Oki Wan Ben0bi in 2020
# https://github.com/ben0bi/BeRec.github

import RPi.GPIO as GPIO

import globals

from time import sleep

BTN_PLAYPAUSE = 14
BTN_STOP = 15
BTN_FWD = 18
BTN_REW = 17

BTN_VOLUP = 21
BTN_VOLDOWN = 20
BTN_REC = 16
BTN_ANYTHING = 26

# the actual position of the endless tape
BURPos = 0

# state of this player
BURP_STATE = globals.BURPSTATE_PAUSE

def BURP_Init():
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(BTN_PLAYPAUSE, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.setup(BTN_STOP, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.setup(BTN_FWD, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.setup(BTN_REW, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.setup(BTN_REC, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.setup(BTN_VOLUP, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.setup(BTN_VOLDOWN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.setup(BTN_ANYTHING, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	return

recpressed = 0
playpausepressed = 0
def BURP_UPDATE():
	global recpressed
	global playpausepressed
	global BURP_STATE

	pp=GPIO.input(BTN_PLAYPAUSE)
	fw=GPIO.input(BTN_FWD)
	rw=GPIO.input(BTN_REW)
	st=GPIO.input(BTN_STOP)
	rc=GPIO.input(BTN_REC)
	vu=GPIO.input(BTN_VOLUP)
	vd=GPIO.input(BTN_VOLDOWN)
	an=GPIO.input(BTN_ANYTHING)
	print(pp,fw,rw,st,rc,vu,vd,an)

# check if record was pressed.
	if(rc==0 and recpressed==0):
		recpressed = 1
		if(BURP_STATE!=globals.BURPSTATE_REC and BURP_STATE!=globals.BURPSTATE_RECPAUSE):
			if(BURP_STATE==globals.BURPSTATE_PLAY):
				# TODO: stop the playing
				print("play stopped")
			BURP_STATE = globals.BURPSTATE_REC
			print "RECORD"
		else:
			# TODO: stop and save record
			BURP_STATE = globals.BURPSTATE_PAUSE
			print "STOP RECORD"
	if(rc==1):
		recpressed = 0
	sleep(0.25)

# check if playpause was pressed.
	if(pp==0 and playpausepressed==0):
		playpausepressed = 1
		# pause record
		if(BURP_STATE==globals.BURPSTATE_REC):
			print("PAUSE RECORD")
			BURP_STATE = globals.BURPSTATE_RECPAUSE
		# pause play
		elif(BURP_STATE==globals.BURPSTATE_PLAY):
			print("PAUSE PLAY")
			BURP_STATE = globals.BURPSTATE_PAUSE
		# continue record
		elif(BURP_STATE==globals.BURPSTATE_RECPAUSE):
			print("CONTINUE RECORD")
			BURP_STATE=globals.BURPSTATE_REC
		# continue play
		elif(BURP_STATE!=globals.BURPSTATE_RECPAUSE and BURP_STATE!=globals.BURPSTATE_PLAY):
			print("START/CONTINUE PLAY")
			BURP_STATE=globals.BURPSTATE_PLAY
	if(pp==1):
		playpausepressed = 0

BURP_Init()

try:
        while True:
		BURP_UPDATE()

except KeyboardInterrupt:
        print("User exit.")

finally:
	GPIO.cleanup()
	print("done")


