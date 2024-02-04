import requests
from pydub import AudioSegment
from io import BytesIO
from pydub.playback import play
from bs4 import BeautifulSoup
import base64

# Deezer API key
api_key = "ea4dcc8d4e5393ca37b7cfc53147a0f0"

query_dict = {
    "C major": "Let It Be",
    "G major": "Part of Your World",
    "D major": "Hotel California",
    "A major": "I want it that Way",
    "E major": "Under the Bridge",
    "B major": "Poker Face",
    "F# major": "Born This Way",
    "Db major": "Nocturne",
    "Ab major": "All of Me",
    "Eb major": "Titanium",
    "Bb major": "Allegro",
    "F major": "Yellow Submarine",
}


# search for a track
def search_track(query):
    search_url = f"https://api.deezer.com/search"
    params = {"q": query, "api_key": api_key}
    response = requests.get(search_url, params=params)
    search_results = response.json()
    return search_results


# Get soundbites
def get_audio_url(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    audio_url = soup.find("meta", {"property": "og:audio"})["content"]
    return audio_url


def download_and_play_audio(audio_url, start_ms, end_ms, testing=True):
    audio_bytes = requests.get(audio_url).content

    # Turn into audio
    audio_segment = AudioSegment.from_file(BytesIO(audio_bytes))

    # Cut the segment to a certain interval based on realtime data
    cut_segment = audio_segment[start_ms:end_ms]
    cut_bytesio = BytesIO()
    cut_segment.export(cut_bytesio, format="wav")
    cut_bytes = cut_bytesio.getvalue()  # get bytes data

    if testing:
        play(cut_segment)
    else:
        pass

    return cut_bytes


def get_song_and_key(name):
    song_names = []
    for key in query_dict:
        song_names.append(query_dict[key])

    if name in song_names:
        results = search_track(name)  # put title of song you are searching in frontend
        key = [i for i in query_dict if query_dict[i] == name]  # gets the key
    else:
        raise ValueError("invalid name")

    url = results["data"][0]["link"]  # return link acquired

    html_bytes = requests.get(url).content
    audio_url = get_audio_url(html_bytes)

    cut_bytes = download_and_play_audio(audio_url, 20000, 60000)

    data = [key, base64.b64encode(cut_bytes).decode("ascii")]

    return data
