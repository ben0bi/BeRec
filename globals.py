# global values for BURP

# BURP states.

# Endless Tape ET is one single file where all the stuff will be recorded to.
# ET only has this one file and does not recognize other (MP3-)Files.
# In the menu you may split ET in several files and such.
BURPSTATE_PAUSE = 0 # default state is not playing
BURPSTATE_PLAY = 1 # playing
BURPSTATE_REC = 2 # recording
BURPSTATE_RECPAUSE = 3 # pause record
BURPSTATE_FWD = 4 # fast forward
BURPSTATE_REW = 5 # fast backward

# File Tape FT does record to several files, one for each recording.
# FT also is the MP3 Player which reads full files from the SD-cards.
