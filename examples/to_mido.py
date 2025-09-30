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
    kick = f'{random.getrandbits(16):016b}' # 16-bit beat-string
    snare = f'{random.getrandbits(16):016b}'
    hihat = f'{random.getrandbits(16):016b}'
    for _ in range(8):
        d.pattern(
            patterns={
                'kick':  kick,
                'snare': snare,
                'hihat': hihat,
            },
        )
    d.sync_parts()
    m = d.to_mido()
    for msg in m.play():
        outport.send(msg)