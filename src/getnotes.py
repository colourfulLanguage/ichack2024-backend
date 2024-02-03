import requests
from pydub import AudioSegment
from io import BytesIO
from pydub.playback import play
from bs4 import BeautifulSoup

file_path = 'data/piano_chromatic_scale.mp3'

try:
    with open(file_path, 'rb') as file:
        audio_bytes = file.read()

except Exception as e:
    print(f"Error: {e}")

def cut_audio(audio, start_ms, end_ms):
    audio_segment = AudioSegment.from_file(BytesIO(audio), format="mp3")
    cut_segment = audio_segment[start_ms:end_ms]
    print(cut_segment)
    return cut_segment

for i in range(0, 12):
    note = cut_audio(audio_bytes, 1000*i, 1000*(i+1))
    play(note)