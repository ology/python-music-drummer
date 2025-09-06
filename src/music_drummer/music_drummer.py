from music21 import stream, note, tempo, meter, midi, instrument
from music21 import duration as m21duration

class Drummer:
    STRAIGHT = 50

    def __init__(self, file='MIDI-Drummer.mid', bpm=120, volume=100, signature='4/4', bars=4):
        self.file = file
        self.bpm = bpm
        self.volume = volume
        self.bars = bars
        self.counter = 0
        self.channel = 9
        self.signature = signature
        self._init_score()

    def _init_score(self):
        self.score = stream.Score()
        # self.part = stream.Part()
        # self.score.append(self.part)
        self.set_ts(self.signature)

    def set_ts(self, ts):
        ts = meter.TimeSignature(ts)
        self.score.timeSignature = ts
        self.beats = self.score.timeSignature.numerator
        self.divisions = self.score.timeSignature.denominator

    def set_bpm(self, bpm: int):
        self.bpm = bpm
        self.score.append(tempo.MetronomeMark(number=bpm))
