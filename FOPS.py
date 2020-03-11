# FOPS File OPerationS
# File Operations for BURP.
# BURP + Benobis Universal Recorder & Player
# by Benedict "Oki Wan Benobi" Jäggi @ MMXX

import os, sys
from os.path import isfile, join

import globals

files = []

SDMOUNTED = 0
# returns 0 on fail.
def mountSD():
    """ mount the sd card in slot one. """
    global SDMOUNTED
    if(SDMOUNTED==1)
        unmountSD()
    # mount here.
    return 0

def unmountSD():
    """ remove the sd card in slot one. """
    global SDMOUNTED
    SDMOUNTED = 0

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
            newpath = newpath.replace(chr(0x99),'')
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
        print("Root directory: "+directory)
    print("ENDOF ReadFiles")

def ClearFiles():
    """ clear the file list. """
    global files
    files = []
