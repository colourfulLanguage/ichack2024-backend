from schemas import SingUserInput, SingGameState
from utils import b64_to_webm, webm_to_wav, note_frequencies
import io
import random


def new_sing_state(websocket, sing_game_init):

    actual_note = random.choice(list(note_frequencies.keys()))

    state = SingGameState(actual_note=actual_note, user_audio_key=b"")
    return state


from scipy.fft import *
from scipy.io import wavfile
import numpy as np
import matplotlib.pyplot as plt
from utils import closest_value, note_frequencies
import asyncio


async def handle_sing_input(webocket, state, input):
    print("Received audio")
    freq_and_note = await freq(input)
    state.user_note = freq_and_note["note"]
    print("User note detected as ", state.user_note)
    return state


async def freq(state, start_time=0, end_time=100):

    b64_audio = state.user_audio_bytes
    webm_audio = b64_to_webm(b64_audio)
    wav_audio = webm_to_wav(webm_audio)

    with open("output.webm", "wb") as audio_file:
        audio_file.write(webm_audio)
    with open("output.wav", "wb") as audio_file:
        audio_file.write(wav_audio)

    virtual_bytes_file = io.BytesIO(wav_audio)
    sr, data = wavfile.read(virtual_bytes_file)
    if data.ndim > 1:
        data = data[:, 0]
    else:
        pass
    # Return a slice of the data from start_time to end_time
    data_to_read = data[int(start_time * sr / 1000) : int(end_time * sr / 1000) + 1]

    # Fourier Transform
    N = len(data_to_read)
    yf = rfft(data_to_read)
    xf = rfftfreq(N, 1 / sr)

    # Uncomment these to see the frequency spectrum as a plot
    plt.plot(xf, np.abs(yf))
    plt.xlim([0, 1000])
    plt.show()

    # Get the most dominant frequency and return it
    idx = np.argmax(np.abs(yf))
    freq = xf[idx]
    return {"freq": freq, "note": closest_value(note_frequencies, freq)}


async def main():
    most_prevalent_note = await freq()

    if most_prevalent_note is not None:
        print(f"Most prevalent note: {most_prevalent_note} Hz")
    else:
        print("No clear peak found in the audio data.")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
