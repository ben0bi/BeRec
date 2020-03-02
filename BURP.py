#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

# display library.
import DID as D

# GPIO stuff.
import RPi.GPIO as GPIO

from time import sleep

import globals

# for the deltatime calculation
import numpy as np
import datetime

# get frametime
FRAMETIME_OLD = 0.0
deltatime = 0.0
def frametime_init():
	global FRAMETIME_OLD
	FRAMETIME_OLD = np.datetime64(datetime.datetime.now(), 'ms')

def frametime_tick():
	global FRAMETIME_OLD, deltatime
	fr = np.datetime64(datetime.datetime.now(), 'ms') # more precise than 'now' (?)
	deltatime = fr - FRAMETIME_OLD
	deltatime = deltatime.astype('int16')
	FRAMETIME_OLD = fr

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
		# special characters which made the player crash:
		newpath = newpath.replace(chr(0xc3), 'C') # ç
		newpath = newpath.replace('ç', 'c') # ç
		newpath = newpath.replace('Ú', 'U')
		newpath = newpath.replace('Ù', 'U')
		newpath = newpath.replace('Ó', 'O')
		newpath = newpath.replace('Ò', 'O')
		newpath = newpath.replace('É', 'E')
		newpath = newpath.replace('È', 'E')
		newpath = newpath.replace('À', 'A')
		newpath = newpath.replace('Á', 'A')
		newpath = newpath.replace('ú', 'u')
		newpath = newpath.replace('ù', 'u')
		newpath = newpath.replace('ó', 'o')
		newpath = newpath.replace('ò', 'o')
		newpath = newpath.replace('é', 'e')
		newpath = newpath.replace('è', 'e')
		newpath = newpath.replace('à', 'a')
		newpath = newpath.replace('á', 'a')
		newpath = newpath.replace('ä', "ae")
		newpath = newpath.replace('Ä', "Ae")
		newpath = newpath.replace('ö', "oe")
		newpath = newpath.replace('Ö', "Oe")
		newpath = newpath.replace('ü', "ue")
		newpath = newpath.replace('Ü', "Ue")
		newpath = newpath.replace('&', "and")
		newpath = newpath.replace(chr(0xc4), 'i')
		# some "very" special chars I don't know about.
		newpath = newpath.replace(chr(0xb1),'')
		newpath = newpath.replace(chr(0x87),'')
		newpath = newpath.replace(chr(0xe2),'_')
		newpath = newpath.replace(chr(0xa1),'_')
		newpath = newpath.replace(chr(0x99),'_')
		newfilename = newpath
		newpath = os.path.join(root, newpath)
		if(newpath!=fpath):
			print "RENAMING "+filename+" TO "+newfilename
			os.rename(fpath, newpath)
		#	fpath = newpath
		print('\t- file %s' % (newfilename))
		# check if file can be played and maybe add it to the list.
		#if(SP.canPlay(newpath)):
		files.append([newfilename,newpath])

if len(files) <= 0:
	BURP_Bebeep()
	print("!! NO FILES FOUND, CHECK DIRECTORIES !!")
	print("Root directory: "+globals.BURP_rootDir)
print("ENDOF Readfiles")
BURP_Beep()
BURP_Bebeep2()

lcd = 0
# initialize gpio and stuff.
def BURP_Init():
	D.DI_INIT()
	# colours: welcome text is turkis, play is green, stop is red and pause is orange.
	# when rec works, stop needs to have another color.

# set gpios
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(globals.PBTN_1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
	GPIO.setup(globals.PBTN_2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
	GPIO.setup(globals.PBTN_3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
	GPIO.setup(globals.PBTN_4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
	GPIO.setup(globals.PBTN_5, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    # get the first track...
	BURP_checkForNextTrack()
    # and then show the welcome message.
	D.setcolor(0,64,128)
	D.uppertext(globals.BURP_WELCOME)
	D.showPlayMenu()
	D.symbol(D.DISYM_IAMFROMWORLDTHREE)
	D.DI_ON() # turn the display on for x seconds.
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
		print("Set Track to: "+files[globals.BURP_fileIDX][0])
		D.uppertext(files[globals.BURP_fileIDX][0])
		globals.BURP_Song = SP(globals.BURP_actualDir+files[globals.BURP_fileIDX][1],1)

# play the inserted track
def BURP_Play():
	global files
	try:
		if(globals.BURP_Song != 0):
			D.symbol(D.DISYM_PLAY)
			print("PLAY START")
			globals.BURP_Song.play()
			globals.BURP_STATE = globals.BURPSTATE_PLAY
			# show track title
			if globals.BURP_fileIDX >= 0:
				D.uppertext(files[globals.BURP_fileIDX][0])
		else:
			print("ERROR: SONG IS null")
			BURP_Stop()
	except:
		print("ERROR: COULD NOT PLAY TRACK")
		BURP_Stop()

# stop the inserted track.
def BURP_Stop():
	globals.BURP_STATE = globals.BURPSTATE_STOP
	D.symbol(D.DISYM_STOP)
	globals.BURP_SecPart = 0.0
	globals.BURP_ActualTime = 0
	try:
		if(globals.BURP_Song!=0):
			if(globals.BURP_Song.isPlaying()):
				globals.BURP_Song.stop()
				sleep(0.5)
	except:
		print("ERROR: COULD NOT STOP TRACK.")


old_playmode = -291
def BURP_UPDATE():
	global old_playmode
	global deltatime

	# check if song is playing or get next one if play mode is set.
	if(globals.BURP_Song != 0):
		# its stopped but state is play, so song has ended.
		# get next one and play it.
		if(not globals.BURP_Song.isPlaying() and globals.BURP_STATE == globals.BURPSTATE_PLAY):
			print("PLAY MODE, SONG ENDED, GET NEXT..")
			BURP_Stop()
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
#	rc=GPIO.input(globals.BTN_REC)
#	vu=GPIO.input(globals.BTN_VOLUP)
#	vd=GPIO.input(globals.BTN_VOLDOWN)
	mc=GPIO.input(globals.BTN_MODECHANGE)
#	an=GPIO.input(globals.BTN_ANYTHING)

# button test
#	print(pp,fw,rw,st,rc) #,vu,vd,md)

#	# check if volup or voldown were pressed
#	# volup
#	if(vu==globals.BUTTON_DOWN and globals.PRESS_VOLUP == 0 and vd != globals.BUTTON_DOWN): # vd must be != vu !!!
#		# TODO: volume up
#		D.DI_ON()
#		print("VOLUP")
#		globals.PRESS_VOLUP = 1

#	if(vu==globals.BUTTON_UP):
#		globals.PRESS_VOLUP = 0

#	# voldown
#	if(vd==globals.BUTTON_DOWN and globals.PRESS_VOLDOWN == 0 and vu != globals.BUTTON_DOWN): # vd must be != vu !!!
#		D.DI_ON()
#		# TODO: volume down
#		print("VOLDOWN")
#		globals.PRESS_VOLDOWN = 1

#	if(vd==1):
#		globals.PRESS_VOLDOWN = 0

	# check if modechange was pressed.
	if(mc==globals.BUTTON_DOWN and globals.PRESS_MODECHANGE==0):
		globals.PRESS_MODECHANGE=1
		# maybe update the time mark.
		if(globals.BURP_STATE == globals.BURPSTATE_PLAY or globals.BURP_STATE == globals.BURPSTATE_REC):
			D.showTimeMark(globals.BURP_ActualTime)
		# turn the display on
		D.DI_ON()

	if(mc==globals.BUTTON_UP):
		globals.PRESS_MODECHANGE=0

	# check if record was pressed.
#	if(rc==globals.BUTTON_DOWN and globals.PRESS_REC==0):
#		globals.PRESS_REC = 1
#		# maybe stop the actual song from playing.
#		if(globals.BURP_Song.isPlaying()):
#			globals.BURP_Song.stop()
#		# record
#		if(globals.BURP_STATE!=globals.BURPSTATE_REC and globals.BURP_STATE!=globals.BURPSTATE_RECPAUSE):
#			globals.BURP_STATE = globals.BURPSTATE_REC
#			# TODO: record
#			D.setcolor(128,0,0)
#			D.symbol(D.DISYM_REC)
#			print "TODO: o RECORD"
#		else:
#			# TODO: stop and save record
#			D.setcolor(0,128,0)
#			BURP_Stop()
#			print "TODO: o STOP RECORD"
#	if(rc==globals.BUTTON_UP):
#		globals.PRESS_REC = 0

	# check if playpause was pressed.
	if(pp==globals.BUTTON_DOWN and globals.PRESS_PP==0):
		D.DI_ON()
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
			D.symbol(D.DISYM_REC)
			globals.BURP_STATE=globals.BURPSTATE_REC
		# pause play
		elif(globals.BURP_STATE==globals.BURPSTATE_PLAY):
			# pause play
			if(globals.BURP_Song.isPlaying()):
				globals.BURP_Song.pause()
				globals.BURP_STATE = globals.BURPSTATE_PAUSE
				D.setcolor(128,64,0)
				D.symbol(D.DISYM_PAUSE)
			else:
				# it's not playing so set mode to stop.
				# this should never happen but...it could.
				D.setcolor(0,128,0)
				BURP_Stop()
				BURP_checkForNextTrack(0)
				BURP_Bebeep()
			print(":> PAUSE PLAY")
		# continue play
		elif(globals.BURP_STATE!=globals.BURPSTATE_RECPAUSE and globals.BURP_STATE!=globals.BURPSTATE_PLAY):
			# play
			D.setcolor(0,128,0)
			if(globals.BURP_STATE==globals.BURPSTATE_STOP):
				BURP_Play()
				print(":> START PLAY")
			elif(globals.BURP_STATE==globals.BURPSTATE_PAUSE):
				globals.BURP_Song.resume()
				D.symbol(D.DISYM_PLAY)
				print(":> RESUME PLAY")
			globals.BURP_STATE=globals.BURPSTATE_PLAY

	if(pp==globals.BUTTON_UP):
		globals.PRESS_PP = 0

	# check if stop was pressed
	if(st==globals.BUTTON_DOWN and globals.PRESS_STOP==0):
		D.setcolor(128,0,0)
		D.DI_ON()
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
		D.DI_ON()
		print(">> FORWARD")
#new fwd code
		if(old_playmode==-291):
			old_playmode = globals.BURP_STATE
		# maybe stop song
		if(globals.BURP_Song!=0):
			if(globals.BURP_Song.isPlaying()):
				BURP_Stop()
				print("Song stopped..FWD")
		BURP_checkForNextTrack(0)
		BURP_Beep()
		globals.PRESS_FWD = 1

    	# fwd button up, maybe play the song.
	if(fw==globals.BUTTON_UP):
		if(globals.PRESS_FWD==1):
			if(old_playmode==globals.BURPSTATE_PLAY or old_playmode==globals.BURPSTATE_PAUSE):
				D.setcolor(0,128,0)
				BURP_Play()
			else:
				BURP_Stop()
			old_playmode=-291
		globals.PRESS_FWD = 0

	# forward button pressed
	if(rw==globals.BUTTON_DOWN and fw!=globals.BUTTON_DOWN):
		D.DI_ON()
		print("<< REWIND")
#new rew code
		if(old_playmode==-291):
			old_playmode = globals.BURP_STATE
		# maybe stop song
		if(globals.BURP_Song!=0):
			if(globals.BURP_Song.isPlaying()):
				BURP_Stop()
				print("Song stopped..REW")
		BURP_checkForNextTrack(1)
		BURP_Beep()
		globals.PRESS_REW = 1

    	# rew button up, maybe play the song.
	if(rw==globals.BUTTON_UP):
		if(globals.PRESS_REW==1):
			if(old_playmode==globals.BURPSTATE_PLAY or old_playmode==globals.BURPSTATE_PAUSE):
				D.setcolor(0,128,0)
				BURP_Play()
			else:
				BURP_Stop()
			old_playmode=-291
		globals.PRESS_REW = 0

	# wait some time to save processor time.
	D.DI_UPDATE()
	sleep(0.1)
	# show time of actual song and
	# modify the time values.
	if(globals.BURP_STATE == globals.BURPSTATE_PLAY or globals.BURP_STATE==globals.BURPSTATE_REC):
		globals.BURP_SecPart = globals.BURP_SecPart+deltatime
		if(globals.BURP_SecPart>=1000):
			globals.BURP_SecPart = globals.BURP_SecPart-1000
			globals.BURP_ActualTime = globals.BURP_ActualTime+1
			if(D.DION==1):
				D.showTimeMark(globals.BURP_ActualTime) # only update display when necessary.
		elif(globals.BURP_ActualTime<=0 and D.DION==1): # show first second, too
			D.showTimeMark(0)
	else:
		D.showPlayMenu()

	D.DI_FADE_OUT(deltatime) # maybe fade out the display.


# MAIN
BURP_Init()
frametime_init()

try:
        while True:
		BURP_UPDATE()
		frametime_tick()
#		print(deltatime, deltatime.astype('int64'))

except KeyboardInterrupt:
        print("User exit.")

finally:
	# clear display
	D.clear()
	# clear GPIO channels.
	GPIO.cleanup()
	print("done. Thanks for using BURP.")
