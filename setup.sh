#!/bin/bash

# Setup for BURP
# Install all dependencies.

# pip, ffmpeg
sudo apt-get install python-pip ffmpeg

# GPIO library
pip install RPi.GPIO

# ffmpeg bindings for python
pip install ffmpeg-python

# using pydub for playing all sorts of sound files.
pip install pydub

# using sounddevice for recording
