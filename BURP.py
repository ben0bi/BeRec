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

# play a blocking beep sound.
def BURP_Bebeep():
	dev = 1
	SP.playTone(420, 0.025, True, dev)
	sleep(0.05)
	SP.playTone(210, 0.1, True, dev)

# play an unblocking beep sound.
def BURP_Bebeep2():
	dev = 1
	SP.playTone(210, 0.1, True, dev)
	sleep(0.05)
	SP.playTone(420, 0.025, True, dev)

# play a normal beep sound.
def BURP_Beep():
	dev = 1
	SP.playTone(210, 0.025, True, dev)

# play BURP start sound.
BURP_Bebeep()
BURP_Bebeep()
BURP_Bebeep2()

print("Reading files..")
files = []
# get all files in the root dir and its sub dirs.
for root, subdirs, fs in os.walk(globals.BURP_rootDir):
	print('--\nroot = '+root)
	for subdir in subdirs:
		print('\t- subdir '+subdir)
		sd = subdir.replace(' ', '_')
		if(sd!=subdir):
			print "RENAMING DIRECTORY "+subdir+" TO "+sd
			od = os.path.join(root,subdir)
			nd = os.path.join(root, sd)
			print("("+od+" -> "+nd+")")
			os.rename(od, nd)

	for filename in fs:
		fpath = os.path.join(root, filename)
		# maybe rename the file
		newpath = filename.replace(' ', '_')
		newpath = newpath.replace('(','[')
		newpath = newpath.replace(')',']')
		newpath = newpath.replace('{','[')
		newpath = newpath.replace('}',']')
		newpath = os.path.join(root, newpath)
		if(newpath!=fpath):
			print "RENAMING "+filename+" TO "+newpath
			os.rename(fpath, newpath)
		#	fpath = newpath
		print('\t- file %s' % (filename))
		# check if file can be played and maybe add it to the list.
		#if(SP.canPlay(newpath)):
		files.append(newpath)

if len(files) <= 0:
	print("!! NO FILES FOUND, CHECK DIRECTORIES !!")
	print("Root directory: "+globals.BURP_rootDir)
print("ENDOF Readfiles")

# initialize gpio and stuff.
def BURP_Init():
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(globals.PBTN_1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
	GPIO.setup(globals.PBTN_2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
	GPIO.setup(globals.PBTN_3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
	GPIO.setup(globals.PBTN_4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
	GPIO.setup(globals.PBTN_5, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
#	GPIO.setup(globals.PBTN_6, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
#	GPIO.setup(globals.PBTN_7, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
#	GPIO.setup(globals.PBTN_8, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
	return

# get the next track if there is one.
def BURP_checkForNextTrack(reverse = 0):
	global files
	# increase or decrease
	if reverse==0:
		globals.BURP_fileIDX = globals.BURP_fileIDX + 1
	else:
		globals.BURP_fileIDX = globals.BURP_fileIDX - 1
	# check if idx is in array or reset to 0
	if globals.BURP_fileIDX >= len(files):
		globals.BURP_fileIDX = 0
	# and vice versa
	if(globals.BURP_fileIDX < 0):
		globals.BURP_fileIDX = len(files)-1
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
	try:
		if(globals.BURP_Song != 0):
			print("PLAY START")
			globals.BURP_Song.play()
			globals.BURP_STATE = globals.BURPSTATE_PLAY
		else:
			print("ERROR: SONG IS null")
			BURP_Stop()
	except:
		print("ERROR: COULD NOT PLAY TRACK")
		BURP_Stop()

# stop the inserted track.
def BURP_Stop():
	globals.BURP_STATE = globals.BURPSTATE_STOP
	try:
		if(globals.BURP_Song!=0):
			if(globals.BURP_Song.isPlaying()):
				globals.BURP_Song.stop()
				sleep(0.5)
	except:
		print("ERROR: COULD NOT STOP TRACK.")

def BURP_UPDATE():
	# check if song is playing or get next one if play mode is set.
	if(globals.BURP_Song != 0):
		# its stopped but state is play, so song has ended.
		# get next one and play it.
		if(not globals.BURP_Song.isPlaying() and globals.BURP_STATE == globals.BURPSTATE_PLAY):
			print("PLAY MODE, SONG ENDED, GET NEXT..")
			BURP_checkForNextTrack()
			BURP_Play()
	else:
		print("TRACK IS null, INSERTING...")
		# there is no track inserted. try to load the next one.
		# but do not play it.
		BURP_checkForNextTrack()
		if globals.BURP_STATE != globals.BURPSTATE_REC and globals.BURP_STATE != globals.BURPSTATE_RECPAUSE:
			BURP_Stop()

	# buttons are set to GND and have pull-up resistors.
	# so, 0 is pressed and 1 is released!
	pp=GPIO.input(globals.BTN_PLAYPAUSE)
	fw=GPIO.input(globals.BTN_FWD)
	rw=GPIO.input(globals.BTN_REW)
	st=GPIO.input(globals.BTN_STOP)
	rc=GPIO.input(globals.BTN_REC)
#	vu=GPIO.input(globals.BTN_VOLUP)
#	vd=GPIO.input(globals.BTN_VOLDOWN)
#	md=GPIO.input(globals.BTN_MODECHANGE)
#	an=GPIO.input(globals.BTN_ANYTHING)

# button test
#	print(pp,fw,rw,st,rc) #,vu,vd,md)

# test
	vu = globals.BUTTON_UP
	vd = globals.BUTTON_UP

	# check if volup or voldown were pressed
	# volup
	if(vu==globals.BUTTON_DOWN and globals.PRESS_VOLUP == 0 and vd != globals.BUTTON_DOWN): # vd must be != vu !!!
		# TODO: volume up
		print("VOLUP")
		globals.PRESS_VOLUP = 1

	if(vu==globals.BUTTON_UP):
		globals.PRESS_VOLUP = 0

	# voldown
	if(vd==globals.BUTTON_DOWN and globals.PRESS_VOLDOWN == 0 and vu != globals.BUTTON_DOWN): # vd must be != vu !!!
		# TODO: volume down
		print("VOLDOWN")
		globals.PRESS_VOLDOWN = 1

	if(vd==1):
		globals.PRESS_VOLDOWN = 0

	# check if record was pressed.
	if(rc==globals.BUTTON_DOWN and globals.PRESS_REC==0):
		globals.PRESS_REC = 1
		# maybe stop the actual song from playing.
		if(globals.BURP_Song.isPlaying()):
			globals.BURP_Song.stop()
		# record
		if(globals.BURP_STATE!=globals.BURPSTATE_REC and globals.BURP_STATE!=globals.BURPSTATE_RECPAUSE):
			globals.BURP_STATE = globals.BURPSTATE_REC
#			BURP_Beep()
			# TODO: record
			print "TODO: o RECORD"
		else:
			# TODO: stop and save record
			BURP_Stop()
			print "TODO: o STOP RECORD"
	if(rc==globals.BUTTON_UP):
		globals.PRESS_REC = 0

	# check if playpause was pressed.
	if(pp==globals.BUTTON_DOWN and globals.PRESS_PP==0):
		globals.PRESS_PP = 1
		# pause record
		if(globals.BURP_STATE==globals.BURPSTATE_REC):
			# TODO: pause record
			print(":> PAUSE RECORD")
			globals.BURP_STATE = globals.BURPSTATE_RECPAUSE
			BURP_Bebeep2()
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
				BURP_Bebeep2()
			else:
				# it's not playing so set mode to stop.
				# this should never happen but...it could.
				BURP_Stop()
				BURP_Bebeep()
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
	if(pp==globals.BUTTON_UP):
		globals.PRESS_PP = 0

	# check if stop was pressed
	if(st==globals.BUTTON_DOWN and globals.PRESS_STOP==0):
		globals.PRESS_STOP = 1
		if(globals.BURP_STATE == globals.BURPSTATE_PLAY or globals.BURP_STATE == globals.BURPSTATE_PAUSE):
			print("[] STOP PLAY")
			BURP_Stop()
			BURP_Bebeep2()
		elif(globals.BURP_STATE==globals.BURPSTATE_REC or globals.BURP_STATE == globals.BURPSTATE_RECPAUSE):
			# TODO: stop and save record.
			print("[] STOP RECORD")
			BURP_Stop()
			BURP_Bebeep2()
		else:
			# already stopped, beep
			BURP_Bebeep()
	if(st==globals.BUTTON_UP):
		globals.PRESS_STOP = 0

	# check if rew or fwd were pressed
	# forward button pressed
	if(fw==globals.BUTTON_DOWN and rw!=globals.BUTTON_DOWN):
		print(">> FORWARD")
		globals.PRESS_FWD = 1
		# maybe stop song from playing
		if(globals.PRESS_FWD==0 and globals.BURP_Song.isPlaying()):
			globals.BURP_Song.stop()
		# get next track
		if(globals.PRESS_FWD == 0 or globals.BURP_STATE!=globals.BURPSTATE_PLAY):
			BURP_checkForNextTrack(0)
		# if state was play: play ;)
		if(globals.PRESS_FWD == 0 and (globals.BURP_STATE==globals.BURPSTATE_PLAY or globals.BURP_STATE==globals.BURPSTATE_PAUSE)):
			print("Try to play new track..")
			BURP_Stop()
			BURP_Play()
		elif(globals.PRESS_FWD==1 and globals.BURP_STATE!=globals.BURPSTATE_PLAY and globals.BURP_STATE!=globals.BURPSTATE_PAUSE):
			if(globals.BURP_STATE!=globals.BURPSTATE_REC and globals.BURP_STATE!=globals.BURPSTATE_RECPAUSE):
				BURP_Stop()
			BURP_Beep()
		globals.PRESS_FWD = 1

	if(fw==globals.BUTTON_UP):
		globals.PRESS_FWD = 0

	# rewind button pressed
	if(rw==globals.BUTTON_DOWN and fw != globals.BUTTON_DOWN):
		print("<< REWIND")
		if(globals.PRESS_REW == 0 and globals.BURP_Song.isPlaying()):
			globals.BURP_Song.stop()
		# get previous track
		if(globals.PRESS_REW == 0 or globals.BURP_STATE!=globals.BURPSTATE_PLAY):
			BURP_checkForNextTrack(1)
		# if state was play: play ;)
		if(globals.PRESS_REW == 0 and (globals.BURP_STATE==globals.BURPSTATE_PLAY or globals.BURP_STATE==globals.BURPSTATE_PAUSE)):
			print("Try to play new track..")
			BURP_Stop()
			BURP_Play()
		elif(globals.PRESS_REW==1 and globals.BURP_STATE!=globals.BURPSTATE_PLAY and globals.BURP_STATE!=globals.BURPSTATE_PAUSE):
			if(globals.BURP_STATE!=globals.BURPSTATE_REC and globals.BURP_STATE!=globals.BURPSTATE_RECPAUSE):
				BURP_Stop()
			BURP_Beep()
		globals.PRESS_REW = 1

	if(rw==globals.BUTTON_UP):
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
