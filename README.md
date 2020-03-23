# BeRec a.k.a. BURP
## Benobis Universal Recorder & Player

See here:
https://www.youtube.com/watch?v=fXjCIICesxU

Updates: 
-> You can switch between INTERNAL DIRECTORY or SD CARDS now.
	-> It will try to mount sdb1 to /media/sdcard1 and sdb2 to /media/sdcard2
	-> you can change those values in the globals.py
	-> Including DID.py update for showing SD-cards mounted or not, or ID for internal drive.
-> MP3 Player fully working. 
	Maybe almost, there may be some errors but I tried to eliminate all upcoming bugs like
	"wrong file format, i will crash now" -> only loading mp3s, wavs, oggs, and flacs now.
	No Buttons for Volume right now.   
-> Renames all (relevant) files and directories for convenience 
	(replaces spaces with _ in directories,
	and much other characters like äàüè in the filenames.)     

-> Display Library DID.py "for musicplayers", with special features, see below Appendix A.    
-> SoundPlayer library and DFRobot-Displaydriver-Library used: All files put together here,
	like in a trash can, no hassle with downloading the external stuff - 
	just get this one and dive into the directories. Remember their licences. I don't. :)

You need to:    

sudo python BURP.py

(using sudo)    
..so that the renaming works without hassle.

Working now with this display-button-HAT:    
https://www.pi-shop.ch/iic-16x2-rgb-lcd-keypad-hat-v1-0    
https://wiki.dfrobot.com/IIC_16X2_RGB_LCD_KeyPad_HAT_1.0)_SKU%3ADFR0514%2FDFR0603    
see Appendix A

also see the installation guide below.

## A digital music recorder behaving like an old music tape.    

I miss the times when we put in a cassette, listen to the radio and when we liked a song,
we just pressed on the record button and got it for ourselves. Then we used another tape
in our 2-tape-deck and made a mixtape for our beloved girlfriends. You know what? I never had a girlfriend then but now - I cannot make a mixtape anymore. It's not the same if you
say, "Hey girl, I bought you some music on spotify." or "Hey girl, here is my mix for you on this
MP3-player but I want it back because it was expensive." or "Hey girl, I have some music on 
my server for you but you need to have a 500$ computer to copy it to your 20 bucks MP3-player."
and on top of this, you need to say - everytime - "You need to listen the tracks in THAT order 
and no other." This sounds like a command, not like a proof of love, don't you think?

BURP shall guide us out of this digital mess.

That said, BURP should record not several files but at several positions
in the same file. The recording is digital but it behaves like an analog recording.

Also, a BURP-Player should have at least one (normal) SD-card slot. NOT microSD. You can put
your microSD into an SD-converter but not vice-versa. And you cannot write that much on a microSD. Also, not on an SD but I could not find a bigger medium which is broadly accepted, digital,
rewritable and stabil. Some old camera-cards should have done the job but I could not find those, either. So I decided to use SD-cards as new "Cassettes".

A "good" BURP-player should have two SD-card slots so you can copy music and ET-files without the
need of a computer. That sounds fantastic? But why? A standard Nikon camera has 2 SD-card-slots
and no one gives a shit. I think, there it is really not of use because you will edit your
images on a computer anyway. But this does not count for music. You do not have to edit your
music after you got it (as whole MP3-file, not as recording), like an image with Lightroom.
So, two SD-cards on an MP3-player are way more logical than in a camera. 
But...tell that the industry.

## Working Mode:

The actual position in the file will be saved as tape position.
On Play, the position will be advanced, the data will not be changed but output as sound.
If you press the record button, it will overwrite the file at this position and the position
itself changes, too, like in Play mode. If the recording is < EOF, the data from the new position
until EOF remains the same.
Rewind will subtract some time from the position and play the file backwards-fast if possible.
Forward the same, but advancing the position.
If you forward over EOF of this file, the missing time will be filled with ambient white noise.
Stop will stop playing/recording and set the position to 0. 
(? Stop works not really like that on the original but more like Pause but what was Pause for then?
- i know, the mechanics - but now?)

Another button or (UI-)mechanic will switch to a normal MP3-Player. More on that if the above works.

## Non-Ben0bi-Code / External Contributions
The player actually uses the SoundPlayer-module found here:    
http://www.python-exemplarisch.ch/raspi/de/sound.inc.php    

It's a wrapper for the SoX sound API.    
Use setup.sh for installing it.

Also it uses the lcd library, no idea how I installed it. It comes with the DFRobot stuff.
Ah yes, you may just need to copy this lcd1602.py file out of their folders.

## Installation (autoboot)

Download this repo onto your linux machine, into your home folder or somewhere you want:
git clone https://github.com/ben0bi/BeRec.git

then open rc.local, cd to your BeRec folder (you need to be in this folder) and..

(    
Open rc.local:    
sudo nano /etc/rc.local    
)    

..write this into it (on a raspbian):    

cd /home/pi/BeRec/    
sudo ./burpscreen.sh    

Ctrl-O, Ctrl-X, reboot - the player should now run.    
If not, check directories and permissions.    

As said above, BURP may need to run in rootlevel-mode because
of file/directory permissions when renaming the files.
This is way easier than checking all those permissions. :)
Also, in a while, when the SD-card option will follow,
the end user may have locked directories on the card which
he doesn't even know about. (Mac to PC to Linux to Mac ;) )
So better start BURP in root mode.

You may need to change the directory to your sound files in the
globals.py file.    

If you want to edit something after autoboot, you can kill the
BURP-screen before with the killscreen.sh-script.

First, check the name of the screen:
sudo screen -ls 

It's sudo because the screen is on the root level.
You should see a number.BURP screen here.

Now just    
sudo ./killscreen.sh XXX.BURP    

where XXX is the number given above.    

and then you can do your work. :)

Hope this helps on your way.    

## Appendix A: The Display Driver

DID.py is the display driver used with the DFRobot 16x2 lcd display seen in the links above.
It has some special features for music players:

### Icon set
The following icons are available:
Play, Pause, Stop, Rec, Recpause, Smiley, Clock, Arrow in each direction.

### Player menu
The lower line can display a prebuilt player menu (icons in brackets) which looks like this below.
This icons must be initialized first on positions 1 through 7. Position 0 is for the direct icon
and the display seems to support only 8 icons at once. You can use the DIREF_ variables for the
positions of the icon set or the DISYM_ arrays for direct icon.

Menu:    

[ID] [RND]

or

[SD1][SD2] [RND]

where ID = INTERNAL DRIVE symbol,
RND = RANDOM or STRAIGHT symbol,
SD1, SD2 = SD_MOUNTED or SD_EMPTY symbols, in the number of sdcards defined in the globals.py.

### Symbol
In the upper left, a (direct, position 0) symbol will be displayed. Set it with:
DID.symbol(symbol_array_name)

### Scrolling text
The upper line can have a scrolling text which will be updated with the
DI_UPDATE-function. Call this function after some time, whereelse it would be to fast.
It starts at position 1 so the symbol will not be interfered.

# Time
In the lower right there can be a time display. It looks like this:    

[Clock]MM:SS    
or    
[Clock]H:MM:SS    

If the track was playing longer than a hour (>60 minutes), the hours will 
be shown, too.    

When the player is in play or pause mode, the track time will be shown.    
In stop and welcome (after boot) mode, the player menu above will be shown.

It does NOT count the track time from the file, so you cannot reverse the time right now.
Sorry for that.
The player just counts the frametime and makes it's own "time-marks".

### Fade-Out
Last but not least, and this is the most useful function beneath the scrolltext: 
The display fades out all colours in a step of 3/frame after 5 seconds. When it is black,
the flag DION will be set to 0. If you turn the display back on with DI_ON(), 
it will restart the counter. When the display is black, the scrolling will
stop, too. Also, the time-UI will not be updated anymore until DION==1.
Saves power and eye-attraction. :)
