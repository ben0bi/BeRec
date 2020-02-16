# Button BCM Values.
# Define the ports for some unspecific buttons so you
# can fiddle with the configuration without having to
# remember all BCM values.

PBTN_1 = 14
PBTN_2 = 15
PBTN_3 = 16
PBTN_4 = 17
PBTN_5 = 18
PBTN_6 = 20
PBTN_7 = 21
PBTN_8 = 26

# BURP buttons: The standard tape buttons.
BTN_PLAYPAUSE = BTN_PP = PBTN_1 # confirmed
BTN_STOP = PBTN_5 # confirmed
BTN_FWD = PBTN_4 # confirmed
BTN_REW = PBTN_2

BTN_VOLUP = PBTN_3
BTN_VOLDOWN = PBTN_6
BTN_REC = PBTN_7 # confirmed
# BTN_ANYTHING = 26 # there is an 8th button on my pads.

# The button-is-pressed flags.
PRESS_PP = 0 # play/pause
PRESS_REC = 0
PRESS_FWD = 0
PRESS_REW = 0
PRESS_STOP = 0

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
BURPSTATE_STOP = BURPSTATE_STOPPED = 0 # default state is stopped.
BURPSTATE_PAUSE = 1 # resumeable pause song.
BURPSTATE_PLAY = 2 # playing
BURPSTATE_REC = 3 # recording
BURPSTATE_RECPAUSE = 4 # pause record
BURPSTATE_FWD = 5 # fast forward
BURPSTATE_REW = 6 # fast backward

# the actual burpstate
BURP_STATE = BURPSTATE_STOP

# the actual track.
BURP_Song = 0

# the index of the filename in the list for the actual track.
BURP_fileIDX = -1
BURP_actualDir = "MUSIC/"
