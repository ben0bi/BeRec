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

# the actual position of the endless tape
BURPos = 0

def BURP_Init():
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(globals.BTN_PLAYPAUSE, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.setup(globals.BTN_STOP, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.setup(globals.BTN_FWD, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.setup(globals.BTN_REW, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.setup(globals.BTN_REC, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.setup(globals.BTN_VOLUP, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.setup(globals.BTN_VOLDOWN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.setup(globals.BTN_ANYTHING, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	return

def BURP_UPDATE():
	# buttons are set to GND and have pull-up resistors.
	# so, 0 is pressed and 1 is released!
	pp=GPIO.input(globals.BTN_PLAYPAUSE)
	fw=GPIO.input(globals.BTN_FWD)
	rw=GPIO.input(globals.BTN_REW)
	st=GPIO.input(globals.BTN_STOP)
	rc=GPIO.input(globals.BTN_REC)
	vu=GPIO.input(globals.BTN_VOLUP)
	vd=GPIO.input(globals.BTN_VOLDOWN)
	an=GPIO.input(globals.BTN_ANYTHING)
	print(pp,fw,rw,st,rc,vu,vd,an)

	# check if record was pressed.
	if(rc==0 and globals.PRESS_REC==0):
		globals.PRESS_REC = 1
		if(globals.BURP_STATE!=globals.BURPSTATE_REC and globals.BURP_STATE!=globals.BURPSTATE_RECPAUSE):
			if(globals.BURP_STATE==globals.BURPSTATE_PLAY):
				# TODO: stop the playing
				print("play stopped")
			globals.BURP_STATE = globals.BURPSTATE_REC
			print "RECORD"
		else:
			# TODO: stop and save record
			globals.BURP_STATE = globals.BURPSTATE_PAUSE
			print "STOP RECORD"
	if(rc==1):
		globals.PRESS_REC = 0
	sleep(0.25)

	# check if playpause was pressed.
	if(pp==0 and globals.PRESS_PP==0):
		globals.PRESS_PP = 1
		# pause record
		if(globals.BURP_STATE==globals.BURPSTATE_REC):
			print("PAUSE RECORD")
			globals.BURP_STATE = globals.BURPSTATE_RECPAUSE
		# pause play
		elif(globals.BURP_STATE==globals.BURPSTATE_PLAY):
			print("PAUSE PLAY")
			globals.BURP_STATE = globals.BURPSTATE_PAUSE
		# continue record
		elif(globals.BURP_STATE==globals.BURPSTATE_RECPAUSE):
			print("CONTINUE RECORD")
			globals.BURP_STATE=globals.BURPSTATE_REC
		# continue play
		elif(globals.BURP_STATE!=globals.BURPSTATE_RECPAUSE and globals.BURP_STATE!=globals.BURPSTATE_PLAY):
			print("START/CONTINUE PLAY")
			globals.BURP_STATE=globals.BURPSTATE_PLAY
	if(pp==1):
		globals.PRESS_PP = 0

	# check if rew or fwd were pressed
	# forward button pressed
	if(fw==0):
		print("FORWARD-->")
		globals.PRESS_FWD = 1

	if(fw==1):
		globals.PRESS_FWD = 0

	# rewind button pressed
	if(rw==0):
		print("<--REWIND")
		globals.PRESS_REW = 1

	if(rw==1):
		globals.PRESS_REW = 0
BURP_Init()

try:
        while True:
		BURP_UPDATE()

except KeyboardInterrupt:
        print("User exit.")

finally:
	GPIO.cleanup()
	print("done")
