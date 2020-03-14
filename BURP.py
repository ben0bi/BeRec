#!/usr/bin/env python
# -*- coding: utf-8 -*-

# BURP
# Benobis Universal Recorder & Player
# * A music recorder behaving like an old tape recorder.
# * and an MP3 Player
# * reading data from additional SD-cards
# https://github.com/ben0bi/BeRec.github
# by Benedict "Oki Wan Benobi" Jäggi @ MMXX

#from pydub import AudioSegment
#from pydub.playback import play

from soundplayer.soundplayer import SoundPlayer as SP

# file operations.
import FOPS as F

# display library.
import DID as D

# GPIO stuff.
import RPi.GPIO as GPIO

from time import sleep

import globals

# play a blocking beep sound.
def BURP_Bebeep():
	""" Play a double beep sound. """
	dev = 1
	SP.playTone(420, 0.025, True, dev)
	sleep(0.05)
	SP.playTone(210, 0.1, True, dev)

# play an unblocking beep sound.
def BURP_Bebeep2():
	""" play the same double beep sound the other way round. """
	dev = 1
	SP.playTone(210, 0.1, True, dev)
	sleep(0.05)
	SP.playTone(420, 0.025, True, dev)

# play a normal beep sound.
def BURP_Beep():
	""" Play a normal beep sound. """
	dev = 1
	SP.playTone(210, 0.025, True, dev)

# Card lid closed, try to mount the sd cards.
def BURP_CardLidClosed():
    """ check if the card lid is closed, try to mount or unmount devices. """
    F.mountSD()
    print "closed"

lcd = 0
# initialize gpio and stuff.
def BURP_Init():
	sym = D.DISYM_SMILEY
	# tell the user that the playerr has started.
	BURP_Bebeep2()

	# try to read all files.
# from internal directory.
	if(globals.BURP_USE_INTERNAL_DRIVE>0):
		F.ReadFiles(globals.BURP_rootDir)
	else:
# from sd cards.
		BURP_CardLidClosed()

	# tell the user that all files are loaded.
	BURP_Beep()
	BURP_Bebeep2()

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
	D.symbol(sym)
	D.DI_ON() # turn the display on for x seconds.
	return

# get the next track if there is one.
def BURP_checkForNextTrack(reverse = 0):
	# increase or decrease
	if reverse==0:
		globals.BURP_fileIDX = globals.BURP_fileIDX + 1
	else:
		globals.BURP_fileIDX = globals.BURP_fileIDX - 1
	# check if idx is in array or reset to 0
	if globals.BURP_fileIDX >= len(F.files):
		globals.BURP_fileIDX = 0
	# and vice versa
	if(globals.BURP_fileIDX < 0):
		globals.BURP_fileIDX = len(F.files)-1
	# check if array has members, anyway, and stop if not.
	if len(F.files) <= 0:
		globals.BURP_fileIDX = -1
		globals.BURP_STATE = globals.BURPSTATE_STOP
	# get the song with the given idx and play it.
	if globals.BURP_fileIDX >= 0:
		print("Set Track to: "+F.files[globals.BURP_fileIDX][0])
		D.uppertext(F.files[globals.BURP_fileIDX][0])
		globals.BURP_Song = SP(globals.BURP_actualDir+F.files[globals.BURP_fileIDX][1],1)

# play the inserted track
def BURP_Play():
	try:
		if(globals.BURP_Song != 0):
			D.symbol(D.DISYM_PLAY)
			print("PLAY START")
			globals.BURP_Song.play()
			globals.BURP_STATE = globals.BURPSTATE_PLAY
			# show track title
			if globals.BURP_fileIDX >= 0:
				D.uppertext(F.files[globals.BURP_fileIDX][0])
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
#sdmount_flag = 0
def BURP_UPDATE():
	global old_playmode
#	global sdmount_flag

	# check if song is playing or get next one if play mode is set.
	if(globals.BURP_Song != 0):
#		sdmount_flag = 0
		# its stopped but state is play, so song has ended.
		# get next one and play it.
		if(not globals.BURP_Song.isPlaying() and globals.BURP_STATE == globals.BURPSTATE_PLAY):
			print("PLAY MODE, SONG ENDED, GET NEXT..")
			BURP_Stop()
			BURP_checkForNextTrack()
			BURP_Play()
	else:
		print("TRACK IS null, INSERTING...")
#		sdmount_flag=0
		# there is no track inserted. try to load the next one.
		# but do not play it.
		BURP_checkForNextTrack()
		if globals.BURP_STATE != globals.BURPSTATE_REC and globals.BURP_STATE != globals.BURPSTATE_RECPAUSE:
			BURP_Stop()
#	elif(sdmount_flag==0):
#		sdmount_flag=1
#		print("*** NO CARD INSERTED ***")
#		D.setcolor(128,0,0)
#		D.uppertext(" *! NO CARD !* ")
#		D.symbol(D.DISYM_NOCARD)
#		D.DI_ON()
#		return
#	else:
		# no card inserted and sd mount flag is 1
#		return

	# get all buttons.
	pp=GPIO.input(globals.BTN_PLAYPAUSE)
	fw=GPIO.input(globals.BTN_FWD)
	rw=GPIO.input(globals.BTN_REW)
	st=GPIO.input(globals.BTN_STOP)
	mc=GPIO.input(globals.BTN_MODECHANGE)

# button test
#	print(pp,fw,rw,st,rc) #,vu,vd,md)

	# check if modechange was pressed.
	if(mc==globals.BUTTON_DOWN and globals.PRESS_MODECHANGE==0):
		globals.PRESS_MODECHANGE=1
		# maybe update the time mark.
		if(globals.BURP_STATE == globals.BURPSTATE_PLAY or globals.BURP_STATE == globals.BURPSTATE_REC):
			D.showPlayMenu()
			D.showTimeMark(globals.BURP_ActualTime)
		# turn the display on
		D.DI_ON()

	if(mc==globals.BUTTON_UP):
		globals.PRESS_MODECHANGE=0

	# TODO: something other: break if no card.
#	if(F.SDMOUNTED==0):
#		return

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
			# already stopped, reverse random flag
			globals.BURP_ISRANDOMPLAY = 1-BURP_ISRANDOMPLAY
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

	# show time of actual song and
	# modify the time values.
	if(globals.BURP_STATE == globals.BURPSTATE_PLAY or globals.BURP_STATE==globals.BURPSTATE_REC):
		globals.BURP_SecPart = globals.BURP_SecPart+D.deltatime
		if(globals.BURP_SecPart>=1000):
			globals.BURP_SecPart = globals.BURP_SecPart-1000
			globals.BURP_ActualTime = globals.BURP_ActualTime+1
			if(D.DION==1):
				D.DI_CLEARBOTTOM()
				D.showPlayMenu()
				D.showTimeMark(globals.BURP_ActualTime) # only update display when necessary.
		elif(globals.BURP_ActualTime<=0 and D.DION==1): # show first second, too
			D.DI_CLEARBOTTOM()
			D.showPlayMenu()
			D.showTimeMark(0)
	elif(globals.BURP_STATE!=globals.BURPSTATE_PAUSE and globals.BURP_STATE!=globals.BURPSTATE_RECPAUSE):
		if(D.DION==1 and D.PLAYMENUSHOWED==0): #spt
			D.DI_CLEARBOTTOM()
			D.showPlayMenu()
			D.PLAYMENUSHOWED=1

# MAIN
BURP_Init()
D.frametime_init()

try:
        while True:
		BURP_UPDATE()
		sleep(0.1)
		D.DI_UPDATE(D.deltatime)
		D.DI_FADE_OUT(D.deltatime) # maybe fade out the display.
		# wait some time to save processor time.
		D.frametime_tick()
#		print(D.deltatime, D.deltatime.astype('int64'))

except KeyboardInterrupt:
        print("User exit.")

finally:
	# clear display
	D.clear()
	# clear GPIO channels.
	GPIO.cleanup()
	print("done. Thanks for using BURP.")
