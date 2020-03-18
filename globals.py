# Global Variables and Statics for BURP.

BURP_WELCOME = "Welcome to BURP! http://masterbit.net"

# if this is 1, it will NOT try to mount the SD cards
# with the belowish values and instead use BURP_rootDir.
BURP_USE_INTERNAL_DRIVE = 0
BURP_rootDir = "/var/www/html/MUSIC/FILESYS"

# array with the drives and mount points
# for all your sd card devices.
# first value is the drive in /dev,
# second value is the mount point.
# third value is if the sd is mounted or not
# and will be changed by program.

# YOU NEED TO SET THE 3rd PARAMETER TO 0 HERE!

# Check device name with lsblk

BURP_SDdirs = [
    ["sdb1", "/media/sdcard1", 0]
]

# Button BCM Values.
# Define the ports for some unspecific buttons so you
# can fiddle with the configuration without having to
# remember all BCM values.

# those are the buttons on the display.
PBTN_1 = 16
PBTN_2 = 17
PBTN_3 = 18
PBTN_4 = 19
PBTN_5 = 20

# BURP buttons: The standard tape buttons.
BTN_PLAYPAUSE = BTN_PP = PBTN_2
BTN_STOP = PBTN_3
BTN_FWD = PBTN_5
BTN_REW = PBTN_4

#BTN_VOLUP = -10
#BTN_VOLDOWN = -20
#BTN_REC = PBTN_1
BTN_MODECHANGE = PBTN_1  # change the mode, get to the menu etc,
# we need 7 buttons for direct access on the player
# which are: playpause, stop, fwd, rew, rec, volup and voldown
# it would be great if volup and voldown could be realized with a poti.
# and with this 6th button we can change the mode
# and then use those buttons for other stuff.

# but there are only 5 buttons on the pad, so rec is modechange.

# The button-is-pressed flags.
PRESS_PP = 0 # play/pause
PRESS_REC = 0
PRESS_FWD = 0
PRESS_REW = 0
PRESS_STOP = 0

PRESS_VOLDOWN = 0
PRESS_VOLUP = 0

PRESS_MODECHANGE = 0

# global values for BURP

# BURP states.

# first the button states.
# if it is with pulldown, button down is 1, with pullup it is 0
BUTTON_DOWN = 1
BUTTON_UP = 0

# Endless Tape ET is one single file where all the stuff will be recorded to.
# ET only has this one file and does not recognize other (MP3-)Files.
# In the menu you may split ET in several files and such.

# File Tape FT does record to several files, one for each recording.
# FT also is the MP3 Player which reads full files from the SD-cards.
# FT mode does not recognize the ET file and
# ET mode ONLY recognizes the ET file.

# NOT USED YET
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
BURP_actualDir = "/"

# time in seconds.
BURP_ActualTime = 0
BURP_SecPart = 0.0

# is the player in random or straight mode?
BURP_ISRANDOMPLAY = 0
