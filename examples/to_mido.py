import mido
import sys
sys.path.append('./src')
from music_drummer.music_drummer import Drummer

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
    m = d.to_mido()
    for msg in m.play():
        outport.send(msg)