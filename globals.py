# Button BCM Values.
# BURP buttons: The standard tape buttons.
BTN_PLAYPAUSE = BTN_PP = 14
BTN_STOP = 15
BTN_FWD = 18
BTN_REW = 17

BTN_VOLUP = 21
BTN_VOLDOWN = 20
BTN_REC = 16
BTN_ANYTHING = 26 # there is an 8th button on my pads.

# The button-is-pressed flags.
PRESS_PP = 0
PRESS_REC = 0

# global values for BURP

# BURP states.

# Endless Tape ET is one single file where all the stuff will be recorded to.
# ET only has this one file and does not recognize other (MP3-)Files.
# In the menu you may split ET in several files and such.

# File Tape FT does record to several files, one for each recording.
# FT also is the MP3 Player which reads full files from the SD-cards.
# FT mode does not recognize the ET file and 
# ET mode ONLY recognizes the ET file.
BURPMODE_ET = 0
BURPMODE_FT = 1

BURP_MODE = BURPMODE_ET

# The several states of the player.
# If there is a REC state, you cannot FWD and REW.
BURPSTATE_PAUSE = 0 # default state is not playing
BURPSTATE_PLAY = 1 # playing
BURPSTATE_REC = 2 # recording
BURPSTATE_RECPAUSE = 3 # pause record
BURPSTATE_FWD = 4 # fast forward
BURPSTATE_REW = 5 # fast backward

# the actual burpstate
BURP_STATE = BURPSTATE_PAUSE
