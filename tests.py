import sys
sys.path.append('./src')
import unittest
import tempfile
import os
from music_drummer.music_drummer import Drummer
from music21 import *

class TestDrummer(unittest.TestCase):
    def test_basics(self):
        d = Drummer()
        self.assertIsInstance(d.score, stream.base.Score)
        self.assertEqual(d.counter, 0)
        self.assertEqual(d.beats, 4)
        self.assertEqual(d.divisions, 4)
        self.assertEqual(d.volume, 100)
        self.assertEqual(d.bars, 4)
        self.assertIn('kick', d.instruments)
        self.assertEqual(d.instruments['kick']['num'], 35)
        self.assertIn('snare', d.instruments)
        self.assertEqual(d.instruments['snare']['num'], 38)
        self.assertIn('hihat', d.instruments)
        self.assertEqual(d.instruments['hihat']['num'], 42)

    def test_bpm(self):
        d = Drummer()
        self.assertEqual(d.bpm, 120)
        d.set_bpm(99)
        self.assertEqual(d.bpm, 99)

    def test_time_signature(self):
        d = Drummer()
        self.assertEqual(d.score.timeSignature.ratioString, '4/4')
        d.set_ts('5/8')
        self.assertEqual(d.score.timeSignature.ratioString, '5/8')
        self.assertEqual(d.beats, 5)
        self.assertEqual(d.divisions, 8)
        d = Drummer(signature='5/4')
        self.assertEqual(d.score.timeSignature.ratioString, '5/4')
        self.assertEqual(d.beats, 5)
        self.assertEqual(d.divisions, 4)

    def test_patterns(self):
        d = Drummer()
        d.count_in()
        self.assertEqual(len(d.hihat.getElementsByClass('Note')), d.beats)
        d.pattern(patterns={'kick': '1000000010100000', 'snare': '0000100000001000', 'hihat': '1010101010101010'})
        self.assertEqual(len(d.kick.getElementsByClass('Note')), 3)
        self.assertEqual(len(d.snare.getElementsByClass('Note')), 2)
        self.assertEqual(len(d.hihat.getElementsByClass('Note')), 4 + 8)
        d.sync_parts()
        self.assertEqual(len(d.score.recurse().getElementsByClass('Note')), 3 + 2 + 4 + 8)
        d = Drummer(signature='5/4')
        d.pattern(patterns={'kick': '1000000010', 'snare': '0000100000', 'hihat': '1010101010'})
        d.sync_parts()
        d.score.show()

if __name__ == '__main__':
    unittest.main()
