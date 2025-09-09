import sys
sys.path.append('./src')
import unittest
import tempfile
import os
from music_drummer.music_drummer import Drummer
from music21 import stream

class TestDrummer(unittest.TestCase):
    def test_basics(self):
        d = Drummer()
        self.assertIsInstance(d.score, stream.base.Score)
        self.assertEqual(d.counter, 0)
        self.assertEqual(d.volume, 100)
        self.assertEqual(d.bars, 4)
        self.assertIn('kick', d.instruments)
        self.assertEqual(d.instruments['kick']['num'], 35)
        self.assertIn('snare', d.instruments)
        self.assertEqual(d.instruments['snare']['num'], 38)
        self.assertIn('hihat', d.instruments)
        self.assertEqual(d.instruments['hihat']['num'], 42)
        d.instruments['kick']['num'] = 36
        self.assertEqual(d.instruments['kick']['num'], 36)

    def test_bpm(self):
        d = Drummer()
        self.assertEqual(d.bpm, 120)
        d.set_bpm(99)
        self.assertEqual(d.bpm, 99)

    def test_time_signature(self):
        d = Drummer()
        d.set_ts()
        self.assertEqual(d.instruments['kick']['part'].timeSignature.ratioString, '4/4')
        self.assertEqual(d.beats, 4)
        self.assertEqual(d.divisions, 4)
        d.set_ts('5/8')
        self.assertEqual(d.instruments['kick']['part'].timeSignature.ratioString, '5/8')
        self.assertEqual(d.beats, 5)
        self.assertEqual(d.divisions, 8)
        d = Drummer(signature='5/4')
        d.set_ts()
        self.assertEqual(d.instruments['kick']['part'].timeSignature.ratioString, '5/4')
        self.assertEqual(d.beats, 5)
        self.assertEqual(d.divisions, 4)

    def test_instrument(self):
        d = Drummer()
        d.set_instrument('kick', 36)
        self.assertEqual(d.instruments['kick']['num'], 36)

    def test_patterns(self):
        d = Drummer()
        d.set_ts()
        d.count_in()
        self.assertEqual(len(d.instruments['hihat']['part'].getElementsByClass('Note')), d.beats)
        d.pattern(patterns={'kick': '1000000010100000', 'snare': '0000100000001000', 'hihat': '1010101010101010'})
        self.assertEqual(len(d.instruments['kick']['part'].getElementsByClass('Note')), 3)
        self.assertEqual(len(d.instruments['snare']['part'].getElementsByClass('Note')), 2)
        self.assertEqual(len(d.instruments['hihat']['part'].getElementsByClass('Note')), 4 + 8)
        d.sync_parts()
        self.assertEqual(len(d.score.recurse().getElementsByClass('Note')), 3 + 2 + 4 + 8)

    # def test_5_8_signature(self):
    #     d = Drummer(signature='5/8')
    #     d.count_in()
    #     for _ in range(4):
    #         d.pattern(patterns={'kick': '1000000010', 'snare': '0000001000', 'hihat': '1111111111'}, duration=1/2)
    #     d.sync_parts()
    #     d.score.show('midi')

    def test_roll(self):
        d = Drummer()
        d.roll()
        self.assertEqual(d.instruments['snare']['part'].getElementsByClass('Note')[0].duration.quarterLength, 1/4)
        self.assertEqual(len(d.instruments['snare']['part'].getElementsByClass('Note')), 4)
        d = Drummer()
        d.roll(subdivisions=8)
        self.assertEqual(d.instruments['snare']['part'].getElementsByClass('Note')[0].duration.quarterLength, 1/8)
        self.assertEqual(len(d.instruments['snare']['part'].getElementsByClass('Note')), 8)
        d = Drummer()
        d.roll(duration=1/2, subdivisions=7)
        self.assertEqual(float(d.instruments['snare']['part'].getElementsByClass('Note')[0].duration.quarterLength), 1/14)
        self.assertEqual(len(d.instruments['snare']['part'].getElementsByClass('Note')), 7)
        d = Drummer()
        d.roll(crescendo=[100, 127])
        self.assertEqual(d.instruments['snare']['part'].getElementsByClass('Note')[0].volume.velocity, 100)
        self.assertEqual(d.instruments['snare']['part'].getElementsByClass('Note')[-1].volume.velocity, 127)

    def test_flam(self):
        d = Drummer()
        d.note('snare', duration=1/2, flam=0)
        d.note('snare', duration=1/2, flam=1/16)
        d.note('snare', duration=1/2, flam=0)
        self.assertEqual(len(d.instruments['snare']['part'].getElementsByClass('Note')), 4)
        self.assertEqual(d.instruments['snare']['part'].getElementsByClass('Note')[1].duration.quarterLength, 1/16)
        self.assertEqual(d.instruments['snare']['part'].getElementsByClass('Note')[2].duration.quarterLength, 1/2 - 1/16)
        # d.sync_parts()
        # d.snare.show('midi')

if __name__ == '__main__':
    unittest.main()
