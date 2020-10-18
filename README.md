
# Mad Mashup Generator (with madmom beats)

The mashup consists of an original and a cover version of your favourite song. 
Their chorus segments are played in alternating way bar-by-bar based on the music bars. 
Hack done during https://www.ismir2020.net/hamr/ following the https://www.ismir2020.net/ conference. 

## License: MIT LICENSE

## Requirements
pip install -r requirements.txt

## Documentation
The hack is based on state of the art MIR methods for beat tracking, downbeat tracking, music key detection and lyric-to-audio alignment. 

### Step 1 
Lyrics-to-Audio Alignment based on the MIREX 2020 winning method [1] and take the chorus audio segment based on the tagged "chorus" section in Genius.com

### Step 2
Detect tempo based on detected beats [2] implemented in the https://github.com/CPJKU/madmom.  
Time stretching using the librosa https://librosa.org/ in order to match the tempo

### Step 3
 Key detection based on [3] implemented in https://github.com/CPJKU/madmom and then  pitch-shifting with https://pypi.org/project/rubberband/ 

### Step 4 Mashup:
Detect downbeats (music bars) with downbeat tracking [2] as implemented in https://github.com/CPJKU/madmom. 

## REFERENCES:
[1] Gao et al. - Lyrics Transcription And Lyrics-to-audio Alignment With
Music-informed Acoustic Models, MIREX 2020 https://www.music-ir.org/mirex/abstracts/2020/GL1.pdf

[2] Böck et al. - Joint Beat and Downbeat Tracking with Recurrent Neural Networks, Proceedings of the 17th International Society for Music Information Retrieval Conference (ISMIR), 2016.

[3] Korzeniowski et al. - Genre-Agnostic Key Classification with Convolutional Neural Networks, Proceedings of the 19th International Society for Music Information Retrieval Conference (ISMIR), 2018.

## Contact
georgi.dzhmabazov@smule.com
milen.minev@smule.com