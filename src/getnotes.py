import requests
from pydub import AudioSegment
from io import BytesIO
from pydub.playback import play
from bs4 import BeautifulSoup

file_path = 'src/piano_chromatic_scale.mp3'

try:
    with open(file_path, 'rb') as file:
        audio_bytes = file.read()

except Exception as e:
    print(f"Error: {e}")

def cut_audio(audio, start_ms, end_ms):
    audio_segment = AudioSegment.from_file(BytesIO(audio), format="mp3")
    cut_segment = audio_segment[start_ms:end_ms]
    return cut_segment

def get_bytes_data(note):
    cut_bytesio = BytesIO()
    note.export(cut_bytesio, format="mp3")
    note_bytes = cut_bytesio.getvalue()  # get bytes data
    return note_bytes



notes = ['C', 'Csharp', 'D', 'Dsharp', 'E', 'F', 'Fsharp', 'G', 'Gsharp', 'A', 'Asharp', 'B', 'C_high', 'Csharp_high']
notes_dict = dict()
for i in range(0, 7):
    print(i)
    note = cut_audio(audio_bytes, 1000*i, 1000*(i+1))
    #play(note)
    notes_dict[f"{notes[i]}"] = get_bytes_data(note)

print(notes_dict)

note = cut_audio(audio_bytes, 1000*7, 950*(7+1))
#play(note)
notes_dict[f"{notes[7]}"] = get_bytes_data(note)

note = cut_audio(audio_bytes, 1200*7, 1200*8)
#play(note)
notes_dict[f"{notes[8]}"] = get_bytes_data(note)
note = cut_audio(audio_bytes, 1200*8, 1300*8)
#play(note)
notes_dict[f"{notes[9]}"] = get_bytes_data(note)

note = cut_audio(audio_bytes, 1300*8, 1250*9)
#play(note)
notes_dict[f"{notes[10]}"] = get_bytes_data(note)

note = cut_audio(audio_bytes, 1250*9, 1250*10)
#play(note)
notes_dict[f"{notes[11]}"] = get_bytes_data(note)

note = cut_audio(audio_bytes, 1250*10, 1200*11)
#play(note)
notes_dict[f"{notes[12]}"] = get_bytes_data(note)

note = cut_audio(audio_bytes, 1200*11, 1150*12)
#play(note)
notes_dict[f"{notes[13]}"] = get_bytes_data(note)

print(notes_dict.keys())

def save_dict_to_txt(dictionary, file_path):
    try:
        with open(file_path, 'w') as file:
            for key, value in dictionary.items():
                file.write(f"{key}: {value}\n")
        print(f"Dictionary saved to {file_path}")

    except Exception as e:
        print(f"Error: {e}")

save_dict_to_txt(notes_dict, 'src/notes_data.txt')