from dataclasses import replace,asdict
import itertools,tempfile,threading,unittest
from pathlib import Path
from unittest.mock import patch
import numpy as np
from PIL import Image
from chrono import core
from chrono.indexed_search import Catalog
from chrono import weighted_search as ws
from chrono.color import rgb_to_lab,delta_e_2000


class WeightedSearchTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog=Catalog((0,7,20,60,64,112))

    def setUp(self):
        y,x=np.indices((128,48))
        self.image=np.stack((x*4,y,((x//6+y//16)%2)*160),axis=2).astype(np.uint8)
        self.s=core.Settings(dither='None',flicker_aware=False,search_effort='Standard')

    def test_ideal_pool_membership_dither_weights_and_budget(self):
        s=replace(self.s,dither='Floyd–Steinberg',strength=.3,serpentine=True)
        calls=[];quantize=core.quantize
        def capture(image,palette,method,strength,serpentine,cancel):
            calls.append((method,strength,serpentine));return quantize(image,palette,method,strength,serpentine,cancel)
        with patch.object(ws,'quantize',side_effect=capture):
            ideal=ws.ideal_palette(self.image,s,self.catalog)
        pool={tuple(v) for v in self.catalog.rgb}
        self.assertTrue(all(tuple(v) in pool for v in ideal.colors))
        self.assertEqual(tuple(ideal.colors[0]),(0,0,0))
        np.testing.assert_allclose(ideal.weights,np.bincount(ideal.indices.ravel(),minlength=8)/ideal.indices.size)
        self.assertGreater(len(calls),0);self.assertLessEqual(len(calls),8)
        self.assertEqual(set(calls),{(s.dither,s.strength,s.serpentine)})

    def test_exact_weighted_match_all_backgrounds_against_direct_enumeration(self):
        ideal=ws.ideal_palette(self.image,self.s,self.catalog)
        for background,bgs in [('Black',(0,)),('Black or white',(0,112)),('Any Atari color',self.catalog.allowed)]:
            s=replace(self.s,background=background);before=asdict(s)
            codes,score,_=ws.match_palette(ideal,s,self.catalog)
            best=float('inf')
            for triple in self.catalog.triples:
                for bg in bgs:
                    p=core.hardware_palette(tuple(core.CODES[int(c)] for c in (*triple,bg)))
                    d=delta_e_2000(rgb_to_lab(ideal.colors)[:,None],rgb_to_lab(p)[None,:])**2
                    best=min(best,float(d.min(axis=1)@ideal.weights))
            self.assertAlmostEqual(score,best,delta=.002)
            self.assertIn(core.CODES.index(codes[3]),bgs);self.assertEqual(asdict(s),before)

    def test_native_and_portable_matcher_parity_with_and_without_toning(self):
        if ws._NATIVE is None:self.skipTest('Native matcher unavailable')
        ideal=ws.ideal_palette(self.image,self.s,self.catalog)
        for tone in (False,True):
            for flicker in (False,True):
                s=replace(self.s,background='Any Atari color',flicker_aware=flicker)
                native=ws.match_palette(ideal,s,self.catalog,tone)
                with patch.object(ws,'_NATIVE',None):portable=ws.match_palette(ideal,s,self.catalog,tone)
                self.assertAlmostEqual(native[1],portable[1],delta=.002)

    def test_exact_palette_recovery_including_white_background(self):
        codes=tuple(core.CODES[c] for c in (20,60,64,112));palette=core.hardware_palette(codes)
        y,x=np.indices((128,48));image=palette[(y//16)%8]
        s=replace(self.s,background='Any Atari color')
        ideal=ws.ideal_palette(image,s,self.catalog)
        result,score,_=ws.match_palette(ideal,s,self.catalog)
        self.assertAlmostEqual(score,0.,places=5);self.assertEqual(result[3],'0E')

    def test_all_three_scopes_and_offset_roundtrip(self):
        from chrono.optimization import fit_controls,joint_optimize
        from chrono.modes import search_palette
        image=Image.fromarray(self.image);s=replace(self.s,brightness=.8,brightness_trim=.6)
        with patch.object(ws,'get_catalog',return_value=self.catalog):
            colors=search_palette(core.prepare(image,s),s)
            for key,value in asdict(s).items():
                if key not in ('codes','preset'):self.assertEqual(getattr(colors,key),value,key)
            fitted=fit_controls(image,s);self.assertEqual(fitted.codes,s.codes)
            self.assertEqual(fitted.brightness_trim,.6)
            winner=joint_optimize(image,s)
            self.assertEqual(winner.brightness_trim,1.)
        with tempfile.TemporaryDirectory() as folder:
            p=Path(folder)/'settings.json';winner.save(p);loaded=core.Settings.load(p)
            self.assertEqual(winner,loaded)
            np.testing.assert_array_equal(core.prepare(image,winner),core.prepare(image,loaded))
        repeated=fit_controls(image,fitted)
        self.assertEqual(fitted,repeated)

    def test_joint_fit_penalizes_casts_but_not_uniform_brightness(self):
        colors=np.array([[0,0,0],[64,64,64],[128,128,128],[255,255,255]],np.uint8)
        ideal=ws.Ideal(colors,np.full(4,.25),np.arange(4),0,0)
        for gain in (.2,.47,1.,1.5):
            self.assertAlmostEqual(float(ws.fit_distortion(ideal,np.full(3,gain),np.zeros(3))),0.)
        for gain in ([.5,.1,.1],[.1,.1,.5]):
            self.assertGreater(float(ws.fit_distortion(ideal,np.array(gain),np.zeros(3))),.02)
        self.assertGreater(float(ws.fit_distortion(ideal,np.full(3,.5),np.full(3,40.))),.02)

    def test_migration_and_only_search_dispatch(self):
        self.assertEqual(core.SEARCHES,[ws.NAME])
        with tempfile.TemporaryDirectory() as folder:
            for old in core.LEGACY_SEARCHES:
                s=replace(self.s,search=old);p=Path(folder)/'settings.json';s.save(p)
                self.assertEqual(core.Settings.load(p).search,ws.NAME)
                with patch.object(ws,'search',return_value=(s.codes,0)) as new,patch('chrono.core.optimize_legacy') as legacy:
                    core.optimize(self.image,s);new.assert_called_once();legacy.assert_not_called()

    def test_cancellation_and_progress(self):
        stop=threading.Event();stop.set()
        with self.assertRaises(core.Cancelled):ws.ideal_palette(self.image,self.s,self.catalog,cancel=stop)
        stop.clear();seen=[]
        with patch.object(ws,'get_catalog',return_value=self.catalog):
            ws.search(self.image,self.s,lambda p,t:seen.append(p))
        self.assertEqual(seen[-1],1.);self.assertTrue(all(a<=b for a,b in zip(seen,seen[1:])))
        ideal=ws.ideal_palette(self.image,self.s,self.catalog)
        def cancel(p,t):stop.set()
        with self.assertRaises(core.Cancelled):ws.match_palette(ideal,replace(self.s,background='Any Atari color'),self.catalog,progress=cancel,cancel=stop)


if __name__=='__main__':unittest.main()
