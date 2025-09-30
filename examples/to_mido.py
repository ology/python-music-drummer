import mido
import random
import sys
# from music_drummer import Drummer
sys.path.append('./src')
from music_drummer.music_drummer import Drummer

port_name = sys.argv[1] if len(sys.argv) > 1 else 'USB MIDI Interface'
with mido.open_output(port_name) as outport:
    print(outport)
    d = Drummer()
    for _ in range(4):
        d.pattern(
            patterns={
                'kick':  ''.join(random.choices('01',k=16)),
                'snare': ''.join(random.choices('01',k=16)),
                'hihat': ''.join(random.choices('01',k=16)),
            },
        )
    d.sync_parts()
    m = d.to_mido()
    for msg in m.play():
        outport.send(msg)