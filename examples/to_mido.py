import mido
import random
import re
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
                'kick':  re.sub(r'^0b', '', bin(random.getrandbits(16))),
                'snare': re.sub(r'^0b', '', bin(random.getrandbits(16))),
                'hihat': re.sub(r'^0b', '', bin(random.getrandbits(16))),
            },
        )
    d.sync_parts()
    m = d.to_mido()
    for msg in m.play():
        outport.send(msg)