import lyricsgenius as genius
import pandas as pd

def fetch_lyrics(artist, title):
    CREDENTIALS = 'V4oVeuiltkj9RYwzEGaAhp34xCQ2FQwI-WuepQIyZ5TQ2WrLNMl8s5jO25qBofEL'

    api=genius.Genius(CREDENTIALS)
    song = api.search_song(title, artist )
    lyrics = song.lyrics

    # get chorus lyrics by tag. TODO: what happens if there is no Chorus tag?
    CHORUS_TAG = '[Chorus]'
    idx_chorus = lyrics.find(CHORUS_TAG)
    letter_idx_start_chorus = idx_chorus + len(CHORUS_TAG)
    letter_idx_end_chorus = lyrics.find('[', idx_chorus+1, len(lyrics))
    chorus_lyrics = (lyrics[letter_idx_start_chorus : letter_idx_end_chorus])
    print("Chorus is: \n{}".format(chorus_lyrics))
    
    # word index.  TODO: convert from letter_idx_start_chorus to word index 
    idx_start_chorus = 58 
    idx_end_chorus = 100
    
# TODO search in other cover song by fuzzy search for this lyrics
    # get again without section headers
    api.remove_section_headers=True
    song = api.search_song(title, artist )
    song.lyrics
    lyrics_file = "aligned/{}-{}.txt".format(artist,title)
    print('stored lyrics in file {}'.format(lyrics_file))
    song.to_text(filename = lyrics_file)
    return idx_start_chorus, idx_end_chorus

def get_chorus_segment(aligned_lyrics_path, start_chorus_lyric_idx, end_chorus_lyric_idx):
    aligned_txt_df = pd.read_csv(aligned_lyrics_path, delimiter=' ')
    start_chorus_time = aligned_txt_df.iloc[start_chorus_lyric_idx,0] - 0.3 # give some tolerance
    end_chorus_time = aligned_txt_df.iloc[end_chorus_lyric_idx,1]
    print("extracted chorus audio segment between {} and {}".format(start_chorus_time, end_chorus_time) )
    return start_chorus_time, end_chorus_time
