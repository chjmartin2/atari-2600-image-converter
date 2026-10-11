from dataclasses import asdict,replace
import itertools,math,tempfile,threading,unittest
from pathlib import Path
from unittest.mock import patch
import numpy as np
from PIL import Image
from chrono import core
from chrono.color import rgb_to_lab
from chrono.modes import search_palette
from chrono.exhaustive_black import (NAME, build_catalog, histogram, errors, screen,
                                     DitherTarget, search)


class ExhaustiveBlackTests(unittest.TestCase):
    def setUp(self):
        self.image=Image.fromarray(np.random.default_rng(22).integers(0,256,(8,12,3),dtype=np.uint8))
        self.subset=[core.CODES.index(c) for c in ('00','42','C6','74','0E')]
        self.triples,self.palettes=build_catalog(self.subset)

    def test_full_catalog_count_repeats_and_hardware_mixtures(self):
        triples,palettes=build_catalog()
        self.assertEqual(len(triples),math.comb(130,3))
        self.assertEqual(len(triples),357760)
        self.assertTrue(np.all(triples[:,0]<=triples[:,1]))
        self.assertTrue(np.all(triples[:,1]<=triples[:,2]))
        self.assertEqual(np.count_nonzero(np.all(triples==triples[:,0,None],axis=1)),128)
        for i in (0,1000,125000,357759):
            codes=tuple(core.CODES[j] for j in triples[i])+('00',)
            np.testing.assert_array_equal(palettes[i],core.hardware_palette(codes))

    def test_screen_matches_independent_bruteforce_all_pixels(self):
        ids,scores=screen(self.palettes,self.image,limit=7)
        colors=rgb_to_lab(np.asarray(self.image).reshape(-1,3))
        brute=[]
        for p in self.palettes:
            d=colors[:,None,:]-rgb_to_lab(p)[None,:,:]
            brute.append(np.mean(np.min(np.sum(d*d,axis=2),axis=1)))
        expected=np.argsort(brute,kind='stable')[:7]
        np.testing.assert_array_equal(ids,expected)
        np.testing.assert_allclose(scores,np.asarray(brute)[expected],rtol=1e-12)

    def test_rare_colors_are_retained_and_seed_walk_does_not_restrict_scan(self):
        image=np.zeros((128,48,3),np.uint8);image[0,0]=[251,123,9]
        colors,weights=histogram(image)
        self.assertEqual(len(colors),2)
        self.assertAlmostEqual(weights.min(),1/6144)
        plain=screen(self.palettes,image,limit=5)
        seeded=screen(self.palettes,image,limit=5,triples=self.triples)
        np.testing.assert_array_equal(plain[0],seeded[0])
        np.testing.assert_allclose(plain[1],seeded[1])

    def test_dither_finalists_and_input_are_fixed_with_black_background(self):
        s=core.Settings(search=NAME,background='Any Atari color',brightness=.7,
                        contrast=.8,gamma=1.2,dither='Floyd–Steinberg',strength=.6,serpentine=True)
        saved=asdict(s);pixels=np.asarray(self.image).copy();seen=[]
        with patch('chrono.exhaustive_black.build_catalog',return_value=(self.triples,self.palettes)), \
             patch('chrono.exhaustive_black.quantize',wraps=core.quantize) as spy:
            codes,score=search(self.image,s,lambda p,t:seen.append(p))
        self.assertEqual(codes[3],'00')
        self.assertEqual(asdict(s),saved)
        np.testing.assert_array_equal(self.image,pixels)
        self.assertGreater(spy.call_count,1)
        for call in spy.call_args_list:self.assertEqual(call.args[2:5],(s.dither,s.strength,s.serpentine))
        start=replace(s,codes=tuple(s.codes[:3])+('00',),background='Black')
        indices=core.quantize(self.image,core.hardware_palette(start.codes),s.dither,s.strength,s.serpentine)
        self.assertLessEqual(score,DitherTarget(self.image).score(indices,start)+1e-12)
        self.assertEqual(seen[-1],1.)
        self.assertTrue(all(a<=b for a,b in zip(seen,seen[1:])))

    def test_cancellation_during_catalog_scan_and_finalists(self):
        cancel=threading.Event();cancel.set()
        with self.assertRaises(core.Cancelled):search(self.image,core.Settings(),cancel=cancel)
        cancel.clear()
        with self.assertRaises(core.Cancelled):
            build_catalog(cancel=cancel,progress=lambda p,t:cancel.set())
        cancel.clear()
        with self.assertRaises(core.Cancelled):
            screen(self.palettes,self.image,cancel=cancel,progress=lambda p,t:cancel.set())
        cancel.clear()
        with patch('chrono.exhaustive_black.build_catalog',return_value=(self.triples,self.palettes)):
            def stop(p,t):
                if p>.85:cancel.set()
            with self.assertRaises(core.Cancelled):search(self.image,core.Settings(),progress=stop,cancel=cancel)


if __name__=='__main__':unittest.main()
