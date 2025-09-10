import sys
sys.path.append('./src')
import unittest
from music_drummer.music_drummer import Drummer

class TestDrummer(unittest.TestCase):
    def test_basics(self):
        d = Drummer()
        self.assertEqual(d.counter, 0)
        self.assertEqual(d.volume, 100)
        self.assertEqual(d.bpm, 120)
        self.assertEqual(d.signature, '4/4')
        self.assertEqual(d.accent, 20)
        self.assertIn('kick', d.kit)
        self.assertIn('snare', d.kit)
        self.assertIn('hihat', d.kit)

    def test_bpm(self):
        d = Drummer()
        self.assertEqual(d.bpm, 120)
        d.set_bpm(99)
        self.assertEqual(d.bpm, 99)

    def test_time_signature(self):
        d = Drummer()
        d.set_ts()
        self.assertEqual(d.kit['kick']['part'].timeSignature.ratioString, '4/4')
        self.assertEqual(d.beats, 4)
        self.assertEqual(d.divisions, 4)
        d.set_ts('5/8')
        self.assertEqual(d.kit['kick']['part'].timeSignature.ratioString, '5/8')
        self.assertEqual(d.beats, 5)
        self.assertEqual(d.divisions, 8)
        d = Drummer(signature='5/4')
        d.set_ts()
        self.assertEqual(d.kit['kick']['part'].timeSignature.ratioString, '5/4')
        self.assertEqual(d.beats, 5)
        self.assertEqual(d.divisions, 4)

    def test_instrument(self):
        d = Drummer()
        kit = d.instrument_map()
        self.assertEqual(len(kit), 38)
        patch = d.instrument_map(d.kit['kick']['instrument'])
        self.assertEqual(patch['num'], 35)
        d.set_instrument('kick', 'kick2')
        patch = d.instrument_map(d.kit['kick']['instrument'])
        self.assertEqual(patch['num'], 36)
        d.set_instrument('crash', 'crash1')
        patch = d.instrument_map(d.kit['crash']['instrument'])
        d.note('crash')
        self.assertEqual(len(d.kit['crash']['part'].getElementsByClass('Note')), 1)

    def test_pattern(self):
        d = Drummer()
        d.set_ts()
        d.count_in()
        d.rest(['kick', 'snare', 'cymbals'], duration=4)
        self.assertEqual(len(d.kit['hihat']['part'].getElementsByClass('Note')), d.beats)
        d.pattern(
            patterns={
                'kick':   '1000000010100000',
                'snare':  '0000100000001000',
                'hihat':  '0010101010101010',
                'crash1': '1000000000000000'
            }
        )
        self.assertEqual(len(d.kit['kick']['part'].getElementsByClass('Note')), 3)
        self.assertEqual(len(d.kit['snare']['part'].getElementsByClass('Note')), 2)
        self.assertEqual(len(d.kit['hihat']['part'].getElementsByClass('Note')), 11)
        d.sync_parts()
        self.assertEqual(len(d.score.recurse().getElementsByClass('Note')), 17)
        self.assertEqual(d.kit['hihat']['counter'], 8.0)
        self.assertEqual(d.kit['hihat']['counter'], d.kit['kick']['counter'])
        self.assertEqual(d.kit['hihat']['counter'], d.kit['snare']['counter'])
        # d.score.show('midi')

    def test_roll(self):
        d = Drummer()
        d.roll('snare')
        self.assertEqual(d.kit['snare']['part'].getElementsByClass('Note')[0].duration.quarterLength, 1/4)
        self.assertEqual(len(d.kit['snare']['part'].getElementsByClass('Note')), 4)
        self.assertEqual(d.kit['snare']['counter'], 1.0)
        d = Drummer()
        d.roll('snare', subdivisions=8)
        self.assertEqual(d.kit['snare']['part'].getElementsByClass('Note')[0].duration.quarterLength, 1/8)
        self.assertEqual(len(d.kit['snare']['part'].getElementsByClass('Note')), 8)
        self.assertEqual(d.kit['snare']['counter'], 1.0)
        d = Drummer()
        d.roll('snare', duration=1/2, subdivisions=7)
        self.assertEqual(float(d.kit['snare']['part'].getElementsByClass('Note')[0].duration.quarterLength), 1/14)
        self.assertEqual(len(d.kit['snare']['part'].getElementsByClass('Note')), 7)
        self.assertGreaterEqual(d.kit['snare']['counter'], 0.49)
        self.assertLessEqual(d.kit['snare']['counter'], 0.5)
        d = Drummer()
        d.roll('snare', crescendo=[100, 127])
        self.assertEqual(d.kit['snare']['part'].getElementsByClass('Note')[0].volume.velocity, 100)
        self.assertEqual(d.kit['snare']['part'].getElementsByClass('Note')[-1].volume.velocity, 127)
        self.assertEqual(d.kit['snare']['counter'], 1.0)

    def test_flam(self):
        d = Drummer()
        d.note('snare', duration=1/2, flam=0)
        d.note('snare', duration=1/2, flam=1/16)
        d.note('snare', duration=1/2, flam=0)
        self.assertEqual(len(d.kit['snare']['part'].getElementsByClass('Note')), 4)
        self.assertEqual(d.kit['snare']['part'].getElementsByClass('Note')[1].duration.quarterLength, 1/16)
        self.assertEqual(d.kit['snare']['part'].getElementsByClass('Note')[2].duration.quarterLength, 1/2 - 1/16)
        self.assertEqual(d.kit['snare']['counter'], 1.5)

    def test_hihats(self):
        d = Drummer()
        d.note('closed', duration=1/2)
        d.note('open', duration=1/2)
        d.note('pedal', duration=1/2)
        d.note('closed', duration=1/2)
        self.assertEqual(len(d.kit['hihat']['part'].getElementsByClass('Note')), 4)
        self.assertEqual(d.kit['hihat']['counter'], 2.0)

    def test_toms(self):
        d = Drummer()
        d.note('tom1', duration=1/3)
        d.note('tom2', duration=1/3)
        d.note('tom3', duration=1/3)
        d.note('tom4', duration=1/3)
        d.note('tom5', duration=1/3)
        d.note('tom6', duration=1/3)
        self.assertEqual(len(d.kit['toms']['part'].getElementsByClass('Note')), 6)
        self.assertGreater(d.kit['toms']['counter'], 1.9)
        self.assertLessEqual(d.kit['toms']['counter'], 2.0)

    def test_cymbals(self):
        d = Drummer()
        d.note('crash1', duration=1/2)
        d.note('crash2', duration=1/2)
        d.note('china', duration=1/2)
        d.note('splash', duration=1/2)
        d.note('ride1', duration=1/2)
        d.note('ride2', duration=1/2)
        d.note('ridebell', duration=1/2)
        self.assertEqual(len(d.kit['cymbals']['part'].getElementsByClass('Note')), 7)
        self.assertEqual(d.kit['cymbals']['counter'], 3.5)

    def test_percussion(self):
        d = Drummer()
        d.note('bongo1')
        d.note('bongo2')
        d.note('cabasa')
        d.note('clap')
        d.note('claves')
        d.note('conga1')
        d.note('conga2')
        d.note('conga3')
        d.note('cowbell')
        d.note('shaker')
        d.note('tambourine')
        d.note('timbale1')
        d.note('timbale2')
        d.note('triangle1')
        d.note('triangle2')
        d.note('woodblock1')
        d.note('woodblock2')
        self.assertEqual(len(d.kit['percussion']['part'].getElementsByClass('Note')), 17)
        self.assertEqual(d.kit['percussion']['counter'], 17.0)
        # d.sync_parts()
        # d.score.show('midi')

if __name__ == '__main__':
    unittest.main()
