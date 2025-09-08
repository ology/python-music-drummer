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
        self._init_parts()

    def _init_score(self):
        self.score = stream.Score()
        # self.part = stream.Part()
        # self.score.append(self.part)
        self.set_ts(self.signature)
        self.set_bpm(self.bpm)
        self.score.append(instrument.Woodblock())

    def _init_parts(self):
        self.kick = stream.Measure()
        self.kick.append(instrument.BassDrum())
        self.snare = stream.Measure()
        self.snare.append(instrument.SnareDrum())
        self.hihat = stream.Measure()
        self.hihat.append(instrument.Cymbals())

    def append_parts(self):
        self.score.append(self.kick)
        self.score.append(self.snare)
        self.score.append(self.hihat)
        
    def set_ts(self, ts):
        ts = meter.TimeSignature(ts)
        self.score.timeSignature = ts
        self.beats = self.score.timeSignature.numerator
        self.divisions = self.score.timeSignature.denominator

    def set_bpm(self, bpm):
        self.bpm = bpm
        self.score.append(tempo.MetronomeMark(number=bpm))

    def rest(self, dur=1.0, part=None):
        n = note.Rest()
        n.duration = duration.Duration(dur)
        if part:
            part.append(n)
        else:
            self.score.append(n)
        if dur:
            self.counter += dur

    def note(self, num, dur=1.0, volume=None, part=None):
        if volume is None:
            volume = self.volume
        n = note.Note(num)
        n.volume.velocity = volume
        n.duration = duration.Duration(dur)
        if part:
            part.append(n)
        else:
            self.score.append(n)
        if dur:
            self.counter += dur
    
    def accent_note(self, num, dur=1.0, volume=None, accent=None, part=None):
        if volume is None:
            volume = self.volume
        if accent is None:
            accent = self.accent
        self.note(num, dur=dur, volume=volume + accent, part=part)

    def duck_note(self, num, dur=1.0, volume=None, accent=None, part=None):
        if volume is None:
            volume = self.volume
        if accent is None:
            accent = self.accent
        self.note(num, dur=dur, volume=volume - accent, part=part)

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
                '0': lambda self, **args: self.rest(dur=args['dur'], part=args['part']),
                '1': lambda self, **args: self.note(args['patch'], dur=args['dur'], part=args['part']),
            }

        if 'kick' in patterns:
            for pattern_str in patterns['kick']:
                for bit in pattern_str:
                    vary[bit](self, patch=35, dur=duration, part=self.kick)
        if 'snare' in patterns:
            for pattern_str in patterns['snare']:
                for bit in pattern_str:
                    vary[bit](self, patch=38, dur=duration, part=self.snare)
        if 'hihat' in patterns:
            for pattern_str in patterns['hihat']:
                for bit in pattern_str:
                    vary[bit](self, patch=42, dur=duration, part=self.hihat)
