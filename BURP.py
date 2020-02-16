# BURP
# Benobis Universal Recorder & Player
# * A music recorder behaving like an old tape recorder.
# * and an MP3 Player
# * reading data from additional SD-cards
# by Oki Wan Ben0bi in 2020
# https://github.com/ben0bi/BeRec.github

#from pydub import AudioSegment
#from pydub.playback import play

from soundplayer.soundplayer import SoundPlayer as SP

import RPi.GPIO as GPIO

import globals

from time import sleep

#test
#globals.BURP_Song = AudioSegment.from_file('MUSIC/american_high.mp3','mp3')
#play(globals.BURP_Song)
#endof test

globals.BURP_Song = SP("MUSIC/american_high.mp3",1)

# the actual position of the endless tape
BURPos = 0

def BURP_Init():
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(globals.PBTN_1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.setup(globals.PBTN_2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.setup(globals.PBTN_3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.setup(globals.PBTN_4, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.setup(globals.PBTN_5, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.setup(globals.PBTN_6, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.setup(globals.PBTN_7, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.setup(globals.PBTN_8, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	return

def BURP_UPDATE():
	# check if song is playing
	if(not globals.BURP_Song.isPlaying() and globals.BURP_STATE == globals.BURPSTATE_PLAY):
		globals.BURP_STATE = globals.BURPSTATE_STOP

	# buttons are set to GND and have pull-up resistors.
	# so, 0 is pressed and 1 is released!
	pp=GPIO.input(globals.BTN_PLAYPAUSE)
	fw=GPIO.input(globals.BTN_FWD)
	rw=GPIO.input(globals.BTN_REW)
	st=GPIO.input(globals.BTN_STOP)
	rc=GPIO.input(globals.BTN_REC)
	vu=GPIO.input(globals.BTN_VOLUP)
	vd=GPIO.input(globals.BTN_VOLDOWN)
#	an=GPIO.input(globals.BTN_ANYTHING)
	print(pp,fw,rw,st,rc,vu,vd)

	# check if volup or voldown were pressed
	# volup
	if(vu==0 and globals.PRESS_VOLUP == 0 and vd != 0): # vd must be != vu !!!
		# TODO: volume up
		print("VOLUP")
		globals.PRESS_VOLUP = 1

	if(vu==1):
		globals.PRESS_VOLUP = 0

	# voldown
	if(vd==0 and globals.PRESS_VOLDOWN == 0 and vu != 0): # vd must be != vu !!!
		# TODO: volume down
		print("VOLDOWN")
		globals.PRESS_VOLDOWN = 1

	if(vd==1):
		globals.PRESS_VOLDOWN = 0

	# check if record was pressed.
	if(rc==0 and globals.PRESS_REC==0):
		globals.PRESS_REC = 1
		# maybe stop the actual song from playing.
		if(globals.BURP_Song.isPlaying()):
			globals.BURP_Song.stop()
		# record
		if(globals.BURP_STATE!=globals.BURPSTATE_REC and globals.BURP_STATE!=globals.BURPSTATE_RECPAUSE):
			globals.BURP_STATE = globals.BURPSTATE_REC
			# TODO: record
			print "TODO: o RECORD"
		else:
			# TODO: stop and save record
			globals.BURP_STATE = globals.BURPSTATE_STOP
			print "TODO: o STOP RECORD"
	if(rc==1):
		globals.PRESS_REC = 0
	sleep(0.25)

	# check if playpause was pressed.
	if(pp==0 and globals.PRESS_PP==0):
		globals.PRESS_PP = 1
		# pause record
		if(globals.BURP_STATE==globals.BURPSTATE_REC):
			# TODO: pause record
			print(":> PAUSE RECORD")
			globals.BURP_STATE = globals.BURPSTATE_RECPAUSE
		# continue record
		elif(globals.BURP_STATE==globals.BURPSTATE_RECPAUSE):
			# TODO: continue record
			print(":> CONTINUE RECORD")
			globals.BURP_STATE=globals.BURPSTATE_REC
		# pause play
		elif(globals.BURP_STATE==globals.BURPSTATE_PLAY):
			# pause play
			if(globals.BURP_Song.isPlaying()):
				globals.BURP_Song.pause()
				globals.BURP_STATE = globals.BURPSTATE_PAUSE
#			else:
#				globals.BURP_Song.stop()
#				globals.BURP_STATE = globals.BURPSTATE_STOP
			print(":> PAUSE PLAY")
		# continue play
		elif(globals.BURP_STATE!=globals.BURPSTATE_RECPAUSE and globals.BURP_STATE!=globals.BURPSTATE_PLAY):
			# play
			if(globals.BURP_STATE==globals.BURPSTATE_STOP):
				globals.BURP_Song.play()
				print(":> START PLAY")
			elif(globals.BURP_STATE==globals.BURPSTATE_PAUSE):
				globals.BURP_Song.resume()
				print(":> RESUME PLAY")
			globals.BURP_STATE=globals.BURPSTATE_PLAY
	if(pp==1):
		globals.PRESS_PP = 0

	# check if stop was pressed
	if(st==0 and globals.PRESS_STOP==0):
		globals.PRESS_STOP = 1
		if(globals.BURP_STATE == globals.BURPSTATE_PLAY or globals.BURP_STATE == globals.BURPSTATE_PAUSE):
			if(globals.BURP_Song.isPlaying()):
				globals.BURP_Song.stop()
			globals.BURP_STATE = globals.BURPSTATE_STOP
			print("[] STOP PLAY, SET TO 0")
		elif(globals.BURP_STATE==globals.BURPSTATE_REC or globals.BURP_STATE == globals.BURPSTATE_RECPAUSE):
			# TODO: stop and save record.
			globals.BURP_STATE = globals.BURPSTATE_STOP
			print("[] STOP RECORD")
	if(st==1):
		globals.PRESS_STOP = 0

	# check if rew or fwd were pressed
	# forward button pressed
	if(fw==0):
		# TODO: fast forward
		print(">> FORWARD")
		globals.PRESS_FWD = 1

	if(fw==1):
		globals.PRESS_FWD = 0

	# rewind button pressed
	if(rw==0):
		# TODO: fast backward
		print("<< REWIND")
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
