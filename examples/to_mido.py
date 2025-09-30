from music21 import midi
import mido
import time
import io
import sys
sys.path.append('../src')
from music_drummer.music_drummer import Drummer

def to_mido(score):
    mf = midi.translate.streamToMidiFile(score)
    midi_data_in_memory = mf.writestr()
    bytes_stream = io.BytesIO(midi_data_in_memory)
    bytes_stream.seek(0)
    try:
        mido_midi = mido.MidiFile(file=bytes_stream)
        print(f"\nMido file has {len(mido_midi_file.tracks)} tracks.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    return mido_midi

if __name__ == "__main__":
    port_name = sys.argv[1] if len(sys.argv) > 1 else 'USB MIDI Interface'
    with mido.open_output(port_name) as outport:
        print(outport)
        d = Drummer()
        d.pattern(
            patterns={
                'kick':  '1000000010000000',
                'snare': '0000100000001000',
                'hihat': '2310101010101010',
            },
        )
        d.sync_parts()
        x = to_mido(d.score)
        print(x)