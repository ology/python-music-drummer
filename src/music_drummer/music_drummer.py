from music21 import stream, note, tempo, meter, duration, instrument

class Drummer:
    STRAIGHT = 50

    def __init__(self, file='Drummer.mid', bpm=120, volume=100, accent=20, signature='4/4', bars=4):
        self.file = file
        self.volume = volume
        self.bars = bars
        self.counter = 0
        self.channel = 9
        self.accent = accent
        self.signature = signature
        self.bpm = bpm
        self._init_score()

    def _init_score(self):
        self.score = stream.Score()
        # self.part = stream.Part()
        # self.score.append(self.part)
        self.set_ts(self.signature)
        self.set_bpm(self.bpm)
        self.score.append(instrument.Woodblock())

    def set_ts(self, ts):
        ts = meter.TimeSignature(ts)
        self.score.timeSignature = ts
        self.beats = self.score.timeSignature.numerator
        self.divisions = self.score.timeSignature.denominator

    def set_bpm(self, bpm):
        self.bpm = bpm
        self.score.append(tempo.MetronomeMark(number=bpm))

    def rest(self, dur=1.0):
        n = note.Rest()
        n.duration = duration.Duration(dur)
        self.score.append(n)
        self.counter += dur

    def note(self, num, dur=1.0, volume=None):
        if volume is None:
            volume = self.volume
        n = note.Note(num)
        n.volume.velocity = volume
        n.duration = duration.Duration(dur)
        self.score.append(n)
        self.counter += dur
    
    def accent_note(self, num, dur=1.0, volume=None, accent=None):
        if volume is None:
            volume = self.volume
        if accent is None:
            accent = self.accent
        self.note(num, dur, volume + accent)
    
    def duck_note(self, num, dur=1.0, volume=None, accent=None):
        if volume is None:
            volume = self.volume
        if accent is None:
            accent = self.accent
        self.note(num, dur, volume - accent)

    def count_in(self, bars=1):
        for _ in range(bars):
            self.accent_note(75)
            for i in range(self.beats - 1):
                self.note(75)

    def pattern(self, patch=38, patterns=None, duration=1/4, vary=None):
        if not patterns:
            return
        if vary is None:
            vary = {
                '0': lambda self, **args: self.rest(dur=duration),
                '1': lambda self, **args: self.note(patch, dur=duration),
            }
        for pattern_str in patterns:
            for bit in pattern_str:
                vary[bit](self, patch=patch, dur=duration)