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

import os, sys
from os.path import isfile, join

import RPi.GPIO as GPIO

import globals

from time import sleep

print("FILETEST")
files = []
# get all files in the root dir and its sub dirs.
for root, subdirs, fs in os.walk(globals.BURP_rootDir):
	print('--\nroot = '+root)
	for subdir in subdirs:
		print('\t- subdir '+subdir)
	for filename in fs:
		fpath = os.path.join(root, filename)
		# maybe rename the file
		newpath = filename.replace(' ', '_')
		newpath = newpath.replace('(','')
		newpath = newpath.replace(')','')
		newpath = os.path.join(root, newpath)
		if(newpath!=fpath):
			print "RENAMING "+filename+" TO "+newpath
			os.rename(fpath, newpath)
		#	fpath = newpath
		print('\t- file %s (full path %s)' % (filename, newpath))
		files.append(newpath)

if len(files) <= 0:
	print("!! NO FILES FOUND, CHECK DIRECTORIES !!")
	print("Root directory: "+globals.BURP_rootDir)
print("ENDOF FILETEST")

# initialize gpio and stuff.
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

# get the next track if there is one.
def BURP_checkForNextTrack():
	global files
	# increase idx
	globals.BURP_fileIDX = globals.BURP_fileIDX + 1
	# check if idx is in array or reset to 0
	if globals.BURP_fileIDX >= len(files):
		globals.BURP_fileIDX = 0
	# check if array has members, anyway, and stop if not.
	if len(files) <= 0:
		globals.BURP_fileIDX = -1
		globals.BURP_STATE = globals.BURPSTATE_STOP
	# get the song with the given idx and play it.
	if globals.BURP_fileIDX >= 0:
		print("Set Track to: "+files[globals.BURP_fileIDX])
		globals.BURP_Song = SP(globals.BURP_actualDir+files[globals.BURP_fileIDX],1)

# play the inserted track
def BURP_Play():
	if(globals.BURP_Song != 0):
		globals.BURP_Song.play()
		globals.BURP_STATE = globals.BURPSTATE_PLAY
	else:
		globals.BURP_STATE = globals.BURPSTATE_STOP


def BURP_UPDATE():
	# check if song is playing or get next one if play mode is set.
	if(globals.BURP_Song != 0):
		# its stopped but state is play, so song has ended.
		# get next one and play it.
		if(not globals.BURP_Song.isPlaying() and globals.BURP_STATE == globals.BURPSTATE_PLAY):
			BURP_checkForNextTrack()
			BURP_Play()
	else:
		# there is no track inserted. try to load the next one.
		# but do not play it.
		BURP_checkForNextTrack()
		if globals.BURP_STATE != globals.BURPSTATE_REC and globals.BURP_STATE != globals.BURPSTATE_RECPAUSE:
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
	md=GPIO.input(globals.BTN_MODECHANGE)
#	an=GPIO.input(globals.BTN_ANYTHING)
#	print(pp,fw,rw,st,rc,vu,vd,md)

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
			else:
				# it's not playing so set mode to stop.
				# this should never happen but...it could.
				globals.BURP_Song.stop()
				globals.BURP_STATE = globals.BURPSTATE_STOP
			print(":> PAUSE PLAY")
		# continue play
		elif(globals.BURP_STATE!=globals.BURPSTATE_RECPAUSE and globals.BURP_STATE!=globals.BURPSTATE_PLAY):
			# play
			if(globals.BURP_STATE==globals.BURPSTATE_STOP):
				BURP_Play()
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

	# wait some time to save processor time.
	sleep(0.1)

BURP_Init()

try:
        while True:
		BURP_UPDATE()

except KeyboardInterrupt:
        print("User exit.")

finally:
	GPIO.cleanup()
	print("done")
