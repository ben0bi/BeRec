#!/bin/bash

# Setup for BURP
# Install all dependencies.

# this is tested on a system where I just installed
# all the stuff until I found a proper solution.
# So, if you do it on a clean system, it might not
# work at first time. just fiddle it out with uncommenting
# stuff here.

# the system works on python 2 but it may also work on python 3
# I am a lazy guy so I won't write an extra 3 behind each command.
# if python without 3 is using python-3 then I will switch, too. :)

# create the mount device paths
sudo mkdir /media/sdcard1
sudo mkdir /media/sdcard2
# new: for usb sticks (not used yet)
sudo mkdir /media/usb1
sudo mkdir /media/usb2

ls /media

# python is the language.
 sudo apt-get install python -y

# but ubuntu 20 seems only to support python3
sudo apt-get install python3 -y

# pip is used for loading modules for python.
sudo apt-get install python-pip -y
sudo apt-get install python3-pip -y

# ffmpeg not used because we're using sox right now.
#sudo apt-get install ffmpeg libavcodec-extra

# install sox, mp3 for the soundplayer module.
sudo apt-get install sox
# old one...
#sudo apt-get install libsox-fmt-mp3 -y
# new one
sudo apt-get install libsox-fmt-all

# install screen for the autoboot option,
# see installation instructions in the README.
sudo apt-get install screen -y

# GPIO library
# Now here we have both because something uses wiringpi
# and I myself used RPi.GPIO before.
# there may be a clean update later only using wiringpi.
pip install RPi.GPIO
pip install wiringpi
pip3 install RPi.GPIO
pip3 install wiringpi

# we need to sudo for the renaming of files so
# we install that stuff with sudo, too
sudo pip install RPi.GPIO
sudo pip install wiringpi
sudo pip3 install RPi.GPIO
sudo pip3 install wiringpi

# for proper time calcualtions we need numpy.
# also, numpy can be used for recording, later.
pip install numpy
sudo pip install numpy
pip3 install numpy
sudo pip3 install numpy

# ffmpeg bindings for python
#pip install ffmpeg-python

# using pydub for playing all sorts of sound files.
#pip install pydub
