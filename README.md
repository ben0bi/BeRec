# BeRec a.k.a. BURP
## Benobis Universal Music Recorder & Player

A digital music recorder behaving like an old music tape.    

That said, BURP should record not several files but at several positions
in the same file. The recording is digital but it behaves like an analog recording.

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