#!/bin/bash

# Setup for BURP
# Install all dependencies.

# pip, ffmpeg
apt-get install python-pip ffmpeg

# GPIO library
pip install RPi.GPIO

# using pydub for playing

# ffmpeg bindings for python
pip install ffmpeg-python

# using sounddevice for recording
