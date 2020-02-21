#!/bin/bash

# Setup for BURP
# Install all dependencies.

# this is tested on a system where I just installed
# all the stuff until I found a proper solution.
# so, if you do it on a clean system, it might not work at first time.
# just fiddle it out with uncommenting stuff.

# pip, ffmpeg
#sudo apt-get install python-pip
#sudo apt-get install ffmpeg libavcodec-extra

# install sox, mp3 for the soundplayer module.
sudo apt-get install sox libsox-fmt-mp3

# GPIO library
pip install RPi.GPIO
pip install wiringpi

# ffmpeg bindings for python
#pip install ffmpeg-python

# using pydub for playing all sorts of sound files.
#pip install pydub

# using sounddevice for recording
