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

# pip
sudo apt-get install python-pip

# ffmpeg not used because we're using sox right now.
#sudo apt-get install ffmpeg libavcodec-extra

# install sox, mp3 for the soundplayer module.
sudo apt-get install sox libsox-fmt-mp3

# GPIO library
pip install RPi.GPIO
pip install wiringpi

# we need to sudo for the renaming of files so
# we install that stuff with sudo, too
sudo pip install RPi.GPIO
sudo pip install wiringpi

# ffmpeg bindings for python
#pip install ffmpeg-python

# using pydub for playing all sorts of sound files.
#pip install pydub

# using sounddevice for recording
