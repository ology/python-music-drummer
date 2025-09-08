import sys
sys.path.append('./src')
import unittest
import tempfile
import os
from music_drummer.music_drummer import Drummer
from music21 import *

class TestDrummer(unittest.TestCase):
    def test_basic(self):
        d = Drummer()
        self.assertIsInstance(d.score, stream.base.Score)

        self.assertEqual(d.channel, 9)
        self.assertEqual(d.counter, 0)
        self.assertEqual(d.beats, 4)
        self.assertEqual(d.divisions, 4)
        self.assertEqual(d.volume, 100)
        self.assertEqual(d.bars, 4)

        self.assertEqual(d.bpm, 120)
        d.set_bpm(99)
        self.assertEqual(d.bpm, 99)

        self.assertEqual(d.score.timeSignature.ratioString, '4/4')
        d.set_ts('5/8')
        self.assertEqual(d.score.timeSignature.ratioString, '5/8')
        self.assertEqual(d.beats, 5)
        self.assertEqual(d.divisions, 8)
        d = Drummer(signature='5/4')
        self.assertEqual(d.score.timeSignature.ratioString, '5/4')
        self.assertEqual(d.beats, 5)
        self.assertEqual(d.divisions, 4)

        d = Drummer()
        d.count_in()
        self.assertEqual(len(d.hihat.getElementsByClass('Note')), d.beats)

        d.pattern(patterns={'kick': '1000000010100000', 'snare': '0000100000001000', 'hihat': '1010101010101010'})
        self.assertEqual(len(d.kick.getElementsByClass('Note')), 3)
        self.assertEqual(len(d.snare.getElementsByClass('Note')), 2)
        self.assertEqual(len(d.hihat.getElementsByClass('Note')), 4 + 8)

        d.sync_parts()
        self.assertEqual(len(d.score.recurse().getElementsByClass('Note')), 3 + 2 + 4 + 8)
        
        # print(d.counter)
        d.score.show('text')

    # def test_pattern(self):
    #     d = Drummer()
    #     d.pattern(instrument=d.open_hh, patterns=['11111'])
    #     expect = [
    #         ['note',   0, 96, 9, 46, 100],
    #         ['note',  96, 96, 9, 46, 100],
    #         ['note', 192, 96, 9, 46, 100],
    #         ['note', 288, 96, 9, 46, 100],
    #         ['note', 384, 96, 9, 46, 100],
    #     ]
    #     self.assertEqual(d.score[4:9], expect)

if __name__ == '__main__':
    unittest.main()
