import requests
from pydub import AudioSegment
from io import BytesIO
from pydub.playback import play
from bs4 import BeautifulSoup

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
    notes = ['C', 'Csharp', 'D', 'Dsharp', 'E', 'F', 'Fsharp', 'G', 'Gsharp', 'A', 'Asharp', 'B', 'C_high', 'Csharp_high']
    notes_dict = dict()
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

    note = cut_audio(audio_bytes, 1250*10, 1200*11)
    if testing:
        play(note)
    notes_dict[f"{notes[12]}"] = get_bytes_data(note)

    note = cut_audio(audio_bytes, 1200*11, 1150*12)
    if testing:
        play(note)
    notes_dict[f"{notes[13]}"] = get_bytes_data(note)

    save_dict_to_txt(notes_dict, 'src/notes_data.txt')

    return notes_dict

if __name__ == "__main__":

    file_path = 'src/piano_chromatic_scale.mp3'

    try:
        with open(file_path, 'rb') as file:
            audio_bytes = file.read()

    except Exception as e:
        print(f"Error: {e}")

    generate_notes_dict(audio_bytes)



