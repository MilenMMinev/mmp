import os

from madmom.features.key import CNNKeyRecognitionProcessor, key_prediction_to_label
from madmom.features.beats import RNNBeatProcessor
from madmom.features.downbeats import RNNDownBeatProcessor, DBNDownBeatTrackingProcessor
from scipy.io import wavfile
import numpy as np

debug = True

ffmpeg_bin = 'ffmpeg'
data_path = 'data'
sources_dir = os.path.join(data_path, 'sources')

if not os.path.exists(data_path):
    os.mkdir(data_path)

tmp_path = os.path.join(data_path, 'tmp')

if not os.path.exists(tmp_path):
    os.mkdir(tmp_path)

class Track:
    def __init__(self, filepath, start_chorus_time=None, end_chorus_time=None, name=None):
        assert os.path.exists(filepath), "{} does not exist.".format(filepath)
        self.orig_filepath = filepath
        self.decoded_f = None
        self.tempo = None
        self.key_root = None
        self.key_mode = None
        self.beats = None
        self.downbeats = None
        
        if name is None:
            name = os.path.splitext(os.path.split(filepath)[-1])[0]
        self.name = name
        if debug:
            print(self.name)
            
        self.decoded_f = None
        if filepath.endswith('wav'):
            self.decoded_f = filepath
        else:
            self.decoded_f = os.path.join(tmp_path, self.name + '.wav')
            decode_to_wav(filepath, self.decoded_f)
            
        self.sr, self.sig = wavfile.read(self.decoded_f)
        self.sig = self.sig.astype(np.float32)
        self.sig /= np.amax(np.abs(self.sig))  # normalize
        # convert to mono
        if (self.sig.ndim == 2):
            self.sig  = (self.sig[:, 0] + self.sig[:, 1]) / 2
        if start_chorus_time and end_chorus_time:
            self.sig =  self.sig[ int(start_chorus_time * self.sr) : int(end_chorus_time * self.sr) ]
            wavfile.write(self.decoded_f, self.sr, self.sig)
            self.decoded_f = self.name + '_chorus.wav'

        
    def play(self):
        print(self.decoded_f)
        return ipd.Audio(filename=self.decoded_f)
    
    def stretch_audio(self, stretch):
        return time_stretch(self.sig, stretch)
    
    def find_tempo(self):
        FPS = 100
        BPM_MIN = 40
        BPM_MAX =250
        SMOOTHING_ALPHA=0.79
        TAU_MIN = 60*FPS/BPM_MAX
        TAU_MAX = 60*FPS/BPM_MIN

        beat_act = RNNBeatProcessor()((self.decoded_f))
        tempo_hist = interval_histogram_comb(beat_act, alpha=SMOOTHING_ALPHA, min_tau=TAU_MIN, max_tau=TAU_MAX)
        smooth_hist = smooth_histogram(tempo_hist, smooth=7)
        tempi_and_strengths = detect_tempo(smooth_hist, fps=100)
        self.tempo = tempi_and_strengths[0][0]
        if debug:
            print("found tempo: {}".format(self.tempo))
    
    def find_key(self):
        proc = CNNKeyRecognitionProcessor()
        key_probs = proc(self.decoded_f)
        key_label = key_prediction_to_label(key_probs)
        if debug:
            print("Found key: {}".format(key_label))
        # Convert from note idx (0-11) to midi tone
        self.key_root = int(0 + (np.argmax(key_probs) % 12))
        self.key_mode = int(np.argmax(key_probs) // 12)
        
    def find_downbeats(self):
        self.beats, self.downbeats = get_beats_madmom(self.decoded_f)
        
    def process(self):
        self.find_key()
        self.find_tempo()
        self.find_downbeats()        

def get_beats_madmom(audio_path):
    act = RNNDownBeatProcessor()(audio_path)
    proc = DBNDownBeatTrackingProcessor(beats_per_bar=[3, 4], fps=100)

    beats_t, beat_idx = proc(act).T
    downbeats_t = beats_t[beat_idx == 1]
    return beats_t, downbeats_t

def decode_to_wav(in_file, out_file):
    if os.path.exists(out_file):
        print("{} already exists. will skip decoding.".format(out_file))
        return
    cmd = [ffmpeg_bin, '-i', in_file, out_file]
    log = subprocess.check_output(cmd)
    if debug:
        print(log)
