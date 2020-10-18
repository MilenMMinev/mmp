import pyrubberband as pyrb
def get_pitch_shift_amt(key_1, key_2):
    # Calculate the shift amount so the keys match. If the mode is different
    # then transpose to target key mode.
    root_1, mode_1 = key_1
    root_2, mode_2 = key_2
    
    # Convert to same mode
    if mode_1 != mode_2:
        if mode_2 == 1:  #minor
            root_1 = (root_1 - 3) % 12
        if mode_2 == 0:  #major
            root_1 = (root_1 + 3) % 12
            
    pitch_shift_amt = root_2 - root_1
    return pitch_shift_amt


def match_key_by_pitchshift(t1, t2):
    # Modify the first track. Return the second unchanged
    pitch_shift_amt = get_pitch_shift_amt((t1.key_root, t1.key_mode), (t2.key_root, t2.key_mode))
    if pitch_shift_amt == 0:
        if debug:
            print("tracks are in same key already.")
        return t1, t2
    
    if debug:
        print("pitch shift amt: {}".format(pitch_shift_amt))
    shifted = pyrb.pitch_shift(t1.sig, int(t1.sr), pitch_shift_amt)
    
    pitch_shifted_filename = os.path.join(tmp_path, "{}_pshifted.wav".format(t1.name))
    if debug:
        print("pitch shift filename: {}".format(pitch_shifted_filename))
    wavfile.write(pitch_shifted_filename, t1.sr, shifted)
    return Track(pitch_shifted_filename), t2