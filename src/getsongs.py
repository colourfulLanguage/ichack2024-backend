import requests
from pydub import AudioSegment
from io import BytesIO
from pydub.playback import play
from bs4 import BeautifulSoup

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
results = search_track('Classical Guitar') #put title of song you are searching in frontend

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

    return cut_bytes

html_bytes = requests.get(url).content
audio_url = get_audio_url(html_bytes)

import time
start = time.time()
cut_bytes = download_and_play_audio(audio_url, 20000, 60000)
end = time.time()

print(- start + end)

#TODO get it to identify which key the song is in
#TODO put in websocket.send

