import requests
from pydub import AudioSegment
from io import BytesIO
import io
from pydub.playback import play
from bs4 import BeautifulSoup
import base64
import json
import librosa
import numpy as np

# Deezer API key
api_key = 'ea4dcc8d4e5393ca37b7cfc53147a0f0'

# search for a track
def search_track(query):
    search_url = f'https://api.deezer.com/search'
    params = {'q': query, 'api_key': api_key}
    response = requests.get(search_url, params=params)
    search_results = response.json()
    return search_results

# Usage
results = search_track('Faure requiem d minor') #put title of song you are searching in frontend

url = results['data'][0]['link'] #return link acquired

#Get soundbites
def get_audio_url(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    audio_url = soup.find('meta', {'property': 'og:audio'})['content']
    return audio_url

def download_and_play_audio(audio_url, start_ms, end_ms, testing=True):
    audio_bytes = requests.get(audio_url).content

    # Turn into audio
    audio_segment = AudioSegment.from_file(BytesIO(audio_bytes), format="mp3")

    # Cut the segment to a certain interval based on realtime data
    cut_segment = audio_segment[start_ms:end_ms]
    cut_bytesio = BytesIO()
    cut_segment.export(cut_bytesio, format="mp3")
    cut_bytes = cut_bytesio.getvalue() #get bytes data

    if testing:
        play(cut_segment)
    else:
        pass

    return audio_bytes, cut_bytes

html_bytes = requests.get(url).content
audio_url = get_audio_url(html_bytes)

import time
start = time.time()
audio_bytes, cut_bytes = download_and_play_audio(audio_url, 20000, 60000, testing=False)
end = time.time()

#TODO get it to identify which key the song is in
import tempfile


# class that uses the librosa library to analyze the key that an mp3 is in
# arguments:
#     waveform: an mp3 file loaded by librosa, ideally separated out from any percussive sources
#     sr: sampling rate of the mp3, which can be obtained when the file is read with librosa
#     tstart and tend: the range in seconds of the file to be analyzed; default to the beginning and end of file if not specified
class Tonal_Fragment():
    def __init__(self, waveform, sr, tstart=None, tend=None):
        self.waveform = waveform
        self.sr = sr
        self.tstart = tstart
        self.tend = tend

        if self.tstart is not None:
            self.tstart = librosa.time_to_samples(self.tstart, sr=self.sr)
        if self.tend is not None:
            self.tend = librosa.time_to_samples(self.tend, sr=self.sr)
        self.y_segment = self.waveform[self.tstart:self.tend]
        self.chromograph = librosa.feature.chroma_cqt(y=self.y_segment, sr=self.sr, bins_per_octave=24)

        # chroma_vals is the amount of each pitch class present in this time interval
        self.chroma_vals = []
        for i in range(12):
            self.chroma_vals.append(np.sum(self.chromograph[i]))
        pitches = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        # dictionary relating pitch names to the associated intensity in the song
        self.keyfreqs = {pitches[i]: self.chroma_vals[i] for i in range(12)}

        keys = [pitches[i] + ' major' for i in range(12)] + [pitches[i] + ' minor' for i in range(12)]

        # use of the Krumhansl-Schmuckler key-finding algorithm, which compares the chroma
        # data above to typical profiles of major and minor keys:
        maj_profile = [6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88]
        min_profile = [6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17]

        # finds correlations between the amount of each pitch class in the time interval and the above profiles,
        # starting on each of the 12 pitches. then creates dict of the musical keys (major/minor) to the correlation
        self.min_key_corrs = []
        self.maj_key_corrs = []
        for i in range(12):
            key_test = [self.keyfreqs.get(pitches[(i + m) % 12]) for m in range(12)]
            # correlation coefficients (strengths of correlation for each key)
            self.maj_key_corrs.append(round(np.corrcoef(maj_profile, key_test)[1, 0], 3))
            self.min_key_corrs.append(round(np.corrcoef(min_profile, key_test)[1, 0], 3))

        # names of all major and minor keys
        self.key_dict = {**{keys[i]: self.maj_key_corrs[i] for i in range(12)},
                         **{keys[i + 12]: self.min_key_corrs[i] for i in range(12)}}

        # this attribute represents the key determined by the algorithm
        self.key = max(self.key_dict, key=self.key_dict.get)
        self.bestcorr = max(self.key_dict.values())

        # this attribute represents the second-best key determined by the algorithm,
        # if the correlation is close to that of the actual key determined
        self.altkey = None
        self.altbestcorr = None

        for key, corr in self.key_dict.items():
            if corr > self.bestcorr * 0.9 and corr != self.bestcorr:
                self.altkey = key
                self.altbestcorr = corr

    # prints the relative prominence of each pitch class
    def print_chroma(self):
        self.chroma_max = max(self.chroma_vals)
        for key, chrom in self.keyfreqs.items():
            print(key, '\t', f'{chrom / self.chroma_max:5.3f}')

    def corr_table(self):
        # prints the correlation coefficients associated with each major/minor key
        for key, corr in self.key_dict.items():
            print(key, '\t', f'{corr:6.3f}')

    # printout of the key determined by the algorithm; if another key is close, that key is mentioned
    def print_key(self):
        print("likely key: ", max(self.key_dict, key=self.key_dict.get), ", correlation: ", self.bestcorr, sep='')
        if self.altkey is not None:
            print("also possible: ", self.altkey, ", correlation: ", self.altbestcorr, sep='')

        return max(self.key_dict, key=self.key_dict.get)


def get_key_from_bytes(audio_bytes):
    try:

        # Create a temporary file to store the audio bytes
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(audio_bytes)
            temp_filename = temp_file.name

        # Load audio file using librosa
        y, sr = librosa.load(temp_filename)

        y_harmonic, y_percussive = librosa.effects.hpss(y)

        song = Tonal_Fragment(y_harmonic, sr)
        key = song.print_key()
        song.corr_table()
        return key

    except Exception as e:
        print(f"Error: {e}")
        return None

song_key = get_key_from_bytes(audio_bytes)
if song_key:
    print(f"The key of the song is: {song_key}")