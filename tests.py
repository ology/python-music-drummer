import sys
sys.path.append('./src')
import unittest
import tempfile
import os
from music_drummer.music_drummer import Drummer
from music21 import *

class TestMIDIDrummer(unittest.TestCase):
    def test_basic(self):
        d = Drummer()
        self.assertIsInstance(d.score, stream.base.Score)

        self.assertEqual(d.channel, 9)
        self.assertEqual(d.counter, 0)
        self.assertEqual(d.score.timeSignature.ratioString, '4/4')
        self.assertEqual(d.beats, 4)
        self.assertEqual(d.divisions, 4)
        self.assertEqual(d.volume, 100)
        self.assertEqual(d.bpm, 120)
        self.assertEqual(d.bars, 4)

        d.set_ts('5/8')
        self.assertEqual(d.score.timeSignature.ratioString, '5/8')
        self.assertEqual(d.beats, 5)
        self.assertEqual(d.divisions, 8)

        d = Drummer(signature='5/4')
        self.assertEqual(d.score.timeSignature.ratioString, '5/4')
        self.assertEqual(d.beats, 5)
        self.assertEqual(d.divisions, 4)

        d.set_bpm(99)
        self.assertEqual(d.bpm, 99)

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

    # def test_fill(self):
    #     d = Drummer()
    #     expect = [
    #         {35: ['10000000'], 38: ['00000111'], 46: ['10000000']},
    #         {35: ['10001000'], 38: ['00000111'], 46: ['10001000']},
    #         {35: ['100000001000000000000000'],
    #          38: ['000000000000000100100100'],
    #          46: ['100000001000000000000000']},
    #         {35: ['10101000'], 38: ['00000111'], 46: ['10101000']},
    #         {35: ['1000000010000000100000001000000000000000'],
    #          38: ['0000000000000000000000000000001000010000'],
    #          46: ['1000000010000000100000001000000000000000']},
    #         {35: ['100010001000100000000000'],
    #          38: ['000000000000000100100100'],
    #          46: ['100010001000100000000000']},
    #         {35: ['10000000100000001000000010000000100000000000000000000000'],
    #          38: ['00000000000000000000000000000000000000000010000001000000'],
    #          46: ['10000000100000001000000010000000100000000000000000000000']},
    #         {35: ['11111000'], 38: ['00000111'], 46: ['11111000']},
    #     ]
    #     for n in range(1, 9):
    #         got = d.add_fill(
    #             None,
    #             **{
    #                 d.open_hh: ['1' * n],
    #                 d.snare: ['0' * n],
    #                 d.kick: ['1' * n],
    #             }
    #         )
    #         self.assertEqual(got, expect[n - 1])

    #     expect = {35: ['10101000'], 38: ['00000111'], 46: ['11111000']}
    #     got = d.add_fill(
    #         None,
    #         **{
    #             d.open_hh: ['11111111'],
    #             d.snare: ['0000'],
    #             d.kick: ['1111'],
    #         }
    #     )
    #     self.assertEqual(got, expect)

    #     expect = {35: ['100100100100100000000000'],
    #               38: ['000000000000000100100100'],
    #               46: ['101010101010101000000000']}
    #     got = d.add_fill(
    #         None,
    #         **{
    #             d.open_hh: ['111111111111'],
    #             d.snare: ['00000000'],
    #             d.kick: ['11111111'],
    #         }
    #     )
    #     self.assertEqual(got, expect)

    #     expect = {35: ['1000000010000000'], 38: ['0000100011111111'], 46: ['1010101000000000']}
    #     got = d.add_fill(
    #         lambda self: {
    #             'duration': 16,
    #             self.open_hh: '00000000',
    #             self.snare: '11111111',
    #             self.kick: '10000000',
    #         },
    #         **{
    #             d.open_hh: ['11111111'],
    #             d.snare: ['0101'],
    #             d.kick: ['1010'],
    #         }
    #     )
    #     self.assertEqual(got, expect)

    # def test_timidity_conf(self):
    #     with tempfile.NamedTemporaryFile(suffix='.sf2', delete=True) as sf_fh, \
    #          tempfile.NamedTemporaryFile(suffix='.conf', delete=True) as timidity_fh:
    #         d = Drummer(soundfont=sf_fh.name)
    #         sf = d.soundfont
    #         self.assertRegex(d.timidity_cfg, sf)
    #         d.timidity_cfg = timidity_fh.name
    #         self.assertTrue(os.path.exists(timidity_fh.name))

if __name__ == '__main__':
    unittest.main()
