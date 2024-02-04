import base64
from pydub import AudioSegment
from io import BytesIO

note_frequencies = {
    27.5: "A0",
    29.135: "A0#",
    30.868: "B0",
    32.703: "C1",
    34.648: "C1#",
    36.708: "D1",
    38.891: "D1#",
    41.203: "E1",
    43.654: "F1",
    46.249: "F1#",
    48.999: "G1",
    51.913: "G1#",
    55.000: "A1",
    58.270: "A1#",
    61.735: "B1",
    65.406: "C2",
    69.296: "C2#",
    73.416: "D2",
    77.782: "D2#",
    82.407: "E2",
    87.307: "F2",
    92.499: "F2#",
    97.999: "G2",
    103.83: "G2#",
    110.00: "A2",
    116.54: "A2#",
    123.47: "B2",
    130.81: "C3",
    138.59: "C3#",
    146.83: "D3",
    155.56: "D3#",
    164.81: "E3",
    174.61: "F3",
    185.00: "F3#",
    196.00: "G3",
    207.65: "G3#",
    220.00: "A3",
    233.08: "A3#",
    246.94: "B3",
    261.63: "C4",
    277.18: "C4#",
    293.67: "D4",
    311.13: "D4#",
    329.63: "E4",
    349.23: "F4",
    369.99: "F4#",
    392.00: "G4",
    415.30: "G4#",
    440.00: "A4",
    466.16: "A4#",
    493.88: "B4",
    523.25: "C5",
    554.37: "C5#",
    587.33: "D5",
    622.25: "D5#",
    659.26: "E5",
    698.46: "F5",
    739.99: "F5#",
    783.99: "G5",
    830.61: "G5#",
    880.00: "A5",
    932.33: "A5#",
    987.77: "B5",
    1046.5: "C6",
    1108.7: "C6#",
    1174.7: "D6",
    1244.5: "D6#",
    1318.5: "E6",
    1396.9: "F6",
    1480.0: "F6#",
    1568.0: "G6",
    1661.2: "G6#",
    1760.0: "A6",
    1864.7: "A6#",
    1975.5: "B6",
    2093.0: "C7",
    2217.5: "C7#",
    2349.3: "D7",
    2489.0: "D7#",
    2637.0: "E7",
    2793.0: "F7",
    2960.0: "F7#",
    3136.0: "G7",
    3322.4: "G7#",
    3520.0: "A7",
    3729.3: "A7#",
    3951.1: "B7",
    4186.0: "C8",
}


def closest_value(dict, searched_value):
    closest_key = min(dict.keys(), key=lambda k: abs(k - searched_value))
    return dict[closest_key]


def b64_to_webm(b64_audio):
    return base64.b64decode(b64_audio)


def webm_to_wav(webm_audio):
    webm_audio_stream = BytesIO(webm_audio)  # Create a stream from WebM bytes
    audio = AudioSegment.from_file(webm_audio_stream, format="webm")  # Load WebM audio
    wav_audio_stream = BytesIO()
    audio.export(wav_audio_stream, format="wav")
    wav_audio_bytes = wav_audio_stream.getvalue()
    return wav_audio_bytes
