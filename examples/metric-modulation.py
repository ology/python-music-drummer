try:
    import sys
    sys.path.append('./src')
    from music_drummer.music_drummer import Drummer
except ImportError:
    from music_drummer import Drummer

bpm = sys.argv[1] if len(sys.argv) > 1 else 70

d = Drummer()

d.count_in()

for i in range(1,4):
    d.set_bpm(bpm)
    d.pattern(
        patterns={
            'kick':  '1000000010100000',
            'snare': '0000100000001000',
            'hihat': '0010101010101010',
        }
    )
    d.set_bpm(bpm * 1/3)
    d.pattern(
        patterns={
            'kick':  '1000000010100000',
            'snare': '0000100000001000',
            'hihat': '0010101010101010',
        }
    )

d.sync_parts()
d.show(format='midi')
