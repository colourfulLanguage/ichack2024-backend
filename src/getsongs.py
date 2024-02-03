import requests
from pydub import AudioSegment
from io import BytesIO
from pydub.playback import play
from bs4 import BeautifulSoup

if __name__ == '__main__':

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
    results = search_track('Faure: Requiem') #put title of song you are searching in frontend

    url = results['data'][0]['link'] #return link acquired
    print(url)
    #get soundbites
    def get_audio_bytes(url):
        try:
            # Make an HTTP GET request to the URL
            response = requests.get(url)

            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                # Retrieve the content in bytes
                audio_bytes = response.content
                return audio_bytes
            else:
                print(f"Error: Unable to fetch audio content. Status code: {response.status_code}")
                return None

        except Exception as e:
            print(f"Error: {e}")
            return None

    def cut_audio_bytes(audio_bytes, start_ms, end_ms):
        try:
            # Convert the bytes to AudioSegment
            audio_segment = AudioSegment.from_file(BytesIO(audio_bytes), format="mp3")

            # Cut the audio segment
            cut_segment = audio_segment[start_ms:end_ms]

            # Export the cut segment to bytes
            cut_bytes = cut_segment.export(format="mp3").read()

            return cut_bytes

        except Exception as e:
            print(f"Error: {e}")
            return None

    def cut_and_play_audio(audio_bytes, start_ms, end_ms):
        try:
            # Convert the bytes to AudioSegment
            audio_segment = AudioSegment.from_file(BytesIO(audio_bytes), format="mp3")

            # Cut the audio segment
            cut_segment = audio_segment[start_ms:end_ms]

            # Play the cut segment
            play(cut_segment)

        except Exception as e:
            print(f"Error: {e}")

    def get_audio_url(html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        audio_url = soup.find('meta', {'property': 'og:audio'})['content']
        return audio_url

    def download_and_play_audio(audio_url, start_ms, end_ms):
        audio_bytes = requests.get(audio_url).content
        audio_segment = AudioSegment.from_file(BytesIO(audio_bytes), format="mp3")
        cut_segment = audio_segment[start_ms:end_ms]
        print(cut_segment)
        play(cut_segment)

    html_bytes = requests.get(url).content
    audio_url = get_audio_url(html_bytes)

    import time
    start = time.time()
    download_and_play_audio(audio_url, 20000, 60000)
    end = time.time()

    print(- start + end)

    #TODO get it to identify which key the song is in
    #TODO put in websocket.send

