from track import Track
from scipy.io import wavfile
debug = True

def match_tempo_by_stretch(t1, t2, reverse=1):
    # Modify the first track (slower or faster). Return the second unchanged
    # if reverse == -1: faster will be slowed down, if reverse == 1 slower will be sped up.
    tracks = sorted([t1, t2], key=lambda x: reverse*x.tempo)
    stretch_amt = tracks[1].tempo / tracks[0].tempo
    if debug:
        print("Stretching {}:".format(tracks[0].name))
        print(tracks[0].tempo, tracks[1].tempo, stretch_amt)
    
    sig = tracks[0].stretch_audio(stretch_amt)
    stretched_wav_filename = os.path.join(tmp_path, "{}_stretched.wav".format(tracks[0].name))
    wavfile.write(stretched_wav_filename, tracks[0].sr, sig)
    
    new_track = Track(stretched_wav_filename)
    return new_track, tracks[1]
