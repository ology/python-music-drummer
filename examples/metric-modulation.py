# XXX currently not working :\

try:
    import sys
    sys.path.append('./src')
    from music_drummer.music_drummer import Drummer
except ImportError:
    from music_drummer import Drummer

bpm = sys.argv[1] if len(sys.argv) > 1 else 70
ql = 1

d = Drummer()
d.set_ts()
d.set_bpm(bpm)

d.count_in()

for i in range(4):
    d.pattern(
        patterns={
            'kick':  '1000000010100000',
            'snare': '0000100000001000',
            'hihat': '0010101010101010',
        }
    )
    if i > 0:
        bpm /= 2
        ql /= 2
    d.set_bpm(bpm, ql=ql)

d.sync_parts()
d.show(format='midi')
