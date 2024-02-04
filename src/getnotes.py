import json

import requests
from pydub import AudioSegment
from io import BytesIO
from pydub.playback import play
from bs4 import BeautifulSoup
import random
import os
import base64
from utils import closest_value, note_frequencies
def cut_audio(audio, start_ms, end_ms):
    # returns actual sound
    audio_segment = AudioSegment.from_file(BytesIO(audio), format="mp3")
    cut_segment = audio_segment[start_ms:end_ms]
    return cut_segment

def get_bytes_data(note):
    # returns bytes data
    cut_bytesio = BytesIO()
    note.export(cut_bytesio, format="mp3")
    note_bytes = cut_bytesio.getvalue()  # get bytes data
    return note_bytes

def save_dict_to_txt(dictionary, file_path):
    try:
        with open(file_path, 'w') as file:
            for key, value in dictionary.items():
                file.write(f"{key}: {value}\n")
        print(f"Dictionary saved to {file_path}")

    except Exception as e:
        print(f"Error: {e}")
def generate_notes_dict(audio_bytes, testing=False):
    file_path = 'notes_data.json'

    if os.path.exists(file_path):
        # Read the JSON data from the file
        with open(file_path, 'r') as file:
            json_data = file.read()

        # Deserialize the JSON data back into a dictionary
        notes_dict = json.loads(json_data)

    else:
        notes = ['C3', 'C3#', 'D3', 'D3#', 'E3', 'F3', 'F3#', 'G3', 'G3#', 'A3', 'A3#', 'B3',
                 #'C_high', 'Csharp_high'
                 ]
        notes_dict = {}
        for i in range(0, 7):
            note = cut_audio(audio_bytes, 1000*i, 1000*(i+1))
            if testing:
                play(note)
            notes_dict[f"{notes[i]}"] = get_bytes_data(note)

        note = cut_audio(audio_bytes, 1000*7, 950*(7+1))
        if testing:
            play(note)
        notes_dict[f"{notes[7]}"] = get_bytes_data(note)

        note = cut_audio(audio_bytes, 1200*7, 1200*8)
        if testing:
            play(note)
        notes_dict[f"{notes[8]}"] = get_bytes_data(note)
        note = cut_audio(audio_bytes, 1200*8, 1300*8)
        if testing:
            play(note)
        notes_dict[f"{notes[9]}"] = get_bytes_data(note)

        note = cut_audio(audio_bytes, 1300*8, 1250*9)
        if testing:
            play(note)
        notes_dict[f"{notes[10]}"] = get_bytes_data(note)

        note = cut_audio(audio_bytes, 1250*9, 1250*10)
        if testing:
            play(note)
        notes_dict[f"{notes[11]}"] = get_bytes_data(note)

        """note = cut_audio(audio_bytes, 1250*10, 1200*11)
        if testing:
            play(note)
        notes_dict[f"{notes[12]}"] = get_bytes_data(note)

        note = cut_audio(audio_bytes, 1200*11, 1150*12)
        if testing:
            play(note)
        notes_dict[f"{notes[13]}"] = get_bytes_data(note)"""

        # convert bytes values to base64-encoded strings
        encoded_dict = {key: base64.b64encode(value).decode('utf-8') for key, value in notes_dict.items()}
        # save json
        out_file = open("notes_data.json", "w")
        json.dump(encoded_dict, out_file)
        #out_file.close()

    #print(notes_dict)
    return notes_dict

def bytes_for_note(note_name, notes_dict):
    if note_name in notes_dict.keys():
        bytes = notes_dict[note_name]
        return bytes
    else:
        raise ValueError("Incorrect format")

def random_note(notes_dict):
    return random.choice(list(notes_dict.keys()))


def get_note():
    file_path = 'src/data/piano_chromatic_scale.mp3'

    try:
        with open(file_path, 'rb') as file:
            audio_bytes = file.read()

    except Exception as e:
        print(f"Error: {e}")

    notes_dict = generate_notes_dict(audio_bytes)
    note_name = random_note(notes_dict)
    bytes = bytes_for_note(note_name, notes_dict)
    expected_freq = [key for key, value in note_frequencies.items() if value == note_name][0]

    return note_name, bytes, expected_freq

get_note()




