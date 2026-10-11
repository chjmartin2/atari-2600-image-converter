from dataclasses import asdict,replace
from pathlib import Path
from unittest.mock import patch
import tempfile,threading,unittest
import numpy as np
from chrono import core
from chrono.modes import normalize,search_palette
from chrono.indexed_search import Catalog,Screening,search,NAME,get_catalog,neighbors
from chrono.color import rgb_to_lab
from chrono.exhaustive_black import DitherTarget


class IndexedSearchTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.allowed=(0,7,20,60,64,112)
        cls.catalog=Catalog(cls.allowed)

    def setUp(self):
        y,x=np.indices((128,48))
        self.image=np.stack((x*4,y,((x//6+y//16)%2)*160),axis=2).astype(np.uint8)
        self.s=core.Settings(dither='None',codes=tuple(core.CODES[i] for i in (20,60,64,0)))

    def test_cached_blends_match_direct_hardware_for_arbitrary_background(self):
        catalog=get_catalog()
        self.assertIs(catalog,get_catalog())
        self.assertEqual(len(catalog.triples),357760)
        rng=np.random.default_rng(129)
        codes=rng.integers(0,128,(200,4))
        np.testing.assert_array_equal(catalog.labs(codes),rgb_to_lab(core._mixtures(codes)))

    def test_screen_matches_independent_full_pixel_scoring(self):
        screen=Screening(self.catalog,self.image,None)
        codes=neighbors([(20,60,64,7)],self.allowed,self.allowed)
        screen.score(codes)
        pixels=rgb_to_lab(self.image.reshape(-1,3))
        for code in codes[::9]:
            lab=rgb_to_lab(core.hardware_palette(tuple(core.CODES[c] for c in code)))
            d=pixels[:,None,:]-lab[None,:,:]
            expected=np.mean(np.min(np.sum(d*d,axis=2),axis=1))
            self.assertAlmostEqual(screen.known[code],expected,places=8)

    def test_constraints_input_preservation_progress_and_current_guard(self):
        for bg,allowed in [('Black',{0}),('Black or white',{0,112}),('Any Atari color',set(self.allowed))]:
            s=replace(self.s,background=bg);before=asdict(s);pixels=self.image.copy();progress=[]
            with patch('chrono.indexed_search.get_catalog',return_value=self.catalog):
                codes,score=search(self.image,s,lambda p,t:progress.append(p))
                repeated=search(self.image,s)
            self.assertEqual(repeated,(codes,score))
            self.assertIn(core.CODES.index(codes[3]),allowed)
            self.assertEqual(before,asdict(s));np.testing.assert_array_equal(self.image,pixels)
            self.assertEqual(progress[-1],1)
            self.assertTrue(all(a<=b for a,b in zip(progress,progress[1:])))
            target=DitherTarget(self.image)
            idx=core.quantize(self.image,core.hardware_palette(s.codes),s.dither,s.strength,s.serpentine)
            self.assertLessEqual(score,target.score(idx,s)+1e-12)

    def test_arbitrary_search_actually_proposes_every_allowed_background(self):
        seen=set();original=self.catalog.labs
        def capture(codes):
            seen.update(c[3] for c in codes);return original(codes)
        with patch('chrono.indexed_search.get_catalog',return_value=self.catalog),patch.object(self.catalog,'labs',side_effect=capture):
            search(self.image,replace(self.s,background='Any Atari color'))
        self.assertEqual(seen,set(self.allowed))

    def test_dither_controls_are_used_during_refinement(self):
        s=replace(self.s,dither='Floyd–Steinberg',strength=.3,serpentine=True,search_effort='Standard')
        calls=[];target=DitherTarget(self.image)
        def quantize(image,palette,method,strength,serpentine,cancel):
            calls.append((method,strength,serpentine))
            return core.quantize(image,palette,method,strength,serpentine,cancel)
        with patch('chrono.indexed_search.get_catalog',return_value=self.catalog),patch('chrono.indexed_search.quantize',side_effect=quantize):
            codes,score=search(self.image,s)
        self.assertGreater(len(calls),32);self.assertLessEqual(len(calls),64)
        self.assertEqual(set(calls),{(s.dither,s.strength,s.serpentine)})
        idx=core.quantize(self.image,core.hardware_palette(codes),s.dither,s.strength,s.serpentine)
        self.assertAlmostEqual(score,target.score(idx,replace(s,codes=codes)))

    def test_arbitrary_background_can_recover_a_white_background_palette(self):
        wanted=tuple(core.CODES[i] for i in (20,60,64,112))
        palette=core.hardware_palette(wanted)
        y,x=np.indices((128,48));image=palette[(y//16)%8]
        s=replace(self.s,background='Any Atari color',flicker_aware=False)
        with patch('chrono.indexed_search.get_catalog',return_value=self.catalog):
            codes,score=search(image,s)
        self.assertEqual(codes[3],'0E')
        self.assertAlmostEqual(score,0.,places=12)

    def test_saved_settings_migrate_and_old_names_cannot_select_old_engines(self):
        self.assertEqual(core.SEARCHES,['Weighted eight-color'])
        with tempfile.TemporaryDirectory() as folder:
            for name in core.LEGACY_SEARCHES:
                s=replace(self.s,search=name,background='Any Atari color',brightness=.73)
                p=Path(folder)/'settings.json';s.save(p);loaded=core.Settings.load(p)
                self.assertEqual(loaded.search,'Weighted eight-color');self.assertEqual(loaded.background,s.background)
                self.assertEqual(loaded.brightness,s.brightness)
                self.assertEqual(normalize(s).search,'Weighted eight-color')
                with patch('chrono.weighted_search.search',return_value=(s.codes,0)) as new,patch('chrono.core.optimize_legacy') as old:
                    core.optimize(self.image,s);new.assert_called_once();old.assert_not_called()
        with patch('chrono.weighted_search.get_catalog',return_value=self.catalog):
            t=search_palette(self.image,replace(self.s,background='Any Atari color'))
        self.assertEqual(t.search,'Weighted eight-color');self.assertEqual(t.background,'Any Atari color')

    def test_cancellation_during_cache_screening_and_rendering(self):
        event=threading.Event();event.set()
        with self.assertRaises(core.Cancelled):get_catalog(event)
        for phase in (0,.08,.43):
            event.clear()
            def progress(p,t):
                if p>=phase:event.set()
            with patch('chrono.indexed_search.get_catalog',return_value=self.catalog),self.assertRaises(core.Cancelled):
                search(self.image,self.s,progress,event)

if __name__=='__main__':unittest.main()
