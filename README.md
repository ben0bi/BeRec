# BeRec a.k.a. BURP
## Benobis Universal Recorder & Player

A digital music recorder behaving like an old music tape.    

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
