import random
import sys
import mido
try:
    import sys
    sys.path.append('./src')
    from music_drummer.music_drummer import Drummer
except ImportError:
    from music_drummer import Drummer

random_bits = lambda: f'{random.getrandbits(16):016b}' # 16-bit beat-string

port_name = sys.argv[1] if len(sys.argv) > 1 else 'USB MIDI Interface'

with mido.open_output(port_name) as outport:
    print(outport)
    d = Drummer()
    d.set_bpm(60)
    d.set_ts()
    kick = random_bits()
    snare = random_bits()
    hihat = random_bits()
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