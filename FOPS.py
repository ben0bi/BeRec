#!/usr/bin/env python
# -*- coding: utf-8 -*-

# FOPS File OPerationS
# File Operations for BURP.
# BURP + Benobis Universal Recorder & Player
# by Benedict "Oki Wan Benobi" Jaeggi @ MMXX

import os, sys
import subprocess
from os.path import isfile, join

import globals

files = []

def mountSD():
	""" try to mount all the sd cards in the list. """
	# first, clear the files list.
	ClearFiles()
	# try to mount all the sd cards.
	for sd in range(len(globals.BURP_SDdirs)):
		# mount sd here.
		sdx = globals.BURP_SDdirs[sd][0]
		mntpnt = globals.BURP_SDdirs[sd][1]
		if(globals.BURP_SDdirs[sd][2]<=0):
			globals.BURP_SDdirs[sd][2] = tryMounting(sdx, mntpnt)
		else:
			print("Device "+sdx+" already mounted at "+mntpnt)

		# and read the files here.
		if(globals.BURP_SDdirs[sd][2]>0):
			ReadFiles(globals.BURP_SDdirs[sd][1])
		else:
			print("Mounting did not work for device "+sdx)

def unmountSD():
	""" try to unmount all the mounted sd cards in the list safely. """
	# clear all files for safety purposes.
	ClearFiles()
	for sd in range(len(globals.BURP_SDdirs)):
		# unmount sd here.
		sdx = globals.BURP_SDdirs[sd][0]
		mntpnt = globals.BURP_SDdirs[sd][1]
		if(globals.BURP_SDdirs[sd][2]>0):
			globals.BURP_SDdirs[sd][2] = tryUnmounting(sdx, mntpnt)

def tryMounting(dev, mntpnt, retest=False):
    """ try to mount a specific sd card """
    try:
        sda = subprocess.check_output(['mount | grep '+dev], shell=True)

    except subprocess.CalledProcessError:
        if retest == True:
            # You may not want this error?
            print (' ')
            print ('#############################')
            print ('!!!  No flash drive found !!!')
            print (dev, mntpnt)
            print ('#############################')
            return 0
        else:
            print ('No drive found, trying to mount '+dev+'...')
            os.system('sudo mount /dev/'+dev+' '+mntpnt+' -o umask=000')
            return tryMounting(dev, mntpnt, True)

    print ('Drive '+dev+' mounted at '+mntpnt)
    return 1

def tryUnmounting(dev, mntpnt, retest=False):
    """ try to unmount a specific sd card """
    try:
        sda = subprocess.check_output(['mount | grep '+dev], shell=True)
        if(retest==False):
            print ('Drive found, trying to unmount '+dev+'...')
            os.system('sudo umount '+mntpnt)
            return tryUnmounting(dev, mntpnt, True)
        else:
            print("Unmount for "+dev+" did not work, be aware!")
            return 1

    except subprocess.CalledProcessError:
        print ('Drive '+dev+' not mounted anymore!')
        return 0

def ReadFiles(directory):
	""" get all files and fill the list with their names. """
	global files
	print("Reading files..")
	# get all files in the root dir and its sub dirs.
	for root, subdirs, fs in os.walk(directory):
		print('--\nroot = '+root)
		# check if all dirs have the right naming convention.
		for subdir in subdirs:
			print('\t- subdir '+subdir)
			sd = subdir.replace(' ', '_')
			if(sd!=subdir):
				print "RENAMING DIRECTORY "+subdir+" TO "+sd
				od = os.path.join(root,subdir)
				nd = os.path.join(root, sd)
				print("("+od+" -> "+nd+")")
				os.rename(od, nd)

        # also check if all files have the right naming convention.
        # else rename the stuff. Player could crash elsewhere.
        for filename in fs:
		# eliminate non sound files.
		if not filename.lower().endswith(('.mp3','.wav','.wave','.ogg','.flac')):
			continue

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
		newpath = newpath.replace(chr(0xe2),'')
		newpath = newpath.replace(chr(0xa1),'')
		# 0xa4 with a C before = ä
		newpath = newpath.replace(chr(0xa4),'')
		newpath = newpath.replace(chr(0x99),'')

		newfilename = newpath
		newpath = os.path.join(root, newpath)
		if(newpath!=fpath):
			print "RENAMING "+filename+" TO "+newfilename
			os.rename(fpath, newpath)
		# fpath = newpath
		print('\t- file %s' % (newfilename))
		# add the file to the list.
		files.append([newfilename,newpath])

	if len(files) <= 0:
		BURP_Bebeep()
		print("!! NO FILES FOUND, CHECK DIRECTORIES !!")
		print("Root directory: "+directory)
	print("ENDOF ReadFiles")

def ClearFiles():
    """ clear the file list. """
    global files
    files = []
