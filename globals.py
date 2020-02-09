# global values for BURP

# BURP states.

# Endless Tape ET is one single file where all the stuff will be recorded to.
# ET only has this one file and does not recognize other (MP3-)Files.
# In the menu you may split ET in several files and such.
BURPSTATE_ET_PAUSE = 0 # default state is endless tape, not playing
BURPSTATE_ET_PLAY = 1 # endless tape, playing
BURPSTATE_ET_REC = 2 # endless tape, recording

# File Tape FT does record to several files, one for each recording.
# FT also is the MP3 Player which reads full files from the SD-cards.
BURPSTATE_FT_PAUSE = 3 # File Tape, not playing
BURPSTATE_FT_PLAY = 4 # File Tape, playing
BURPSTATE_FT_REC = 5 # File Tape, recording
