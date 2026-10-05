from dataclasses import replace,asdict
from pathlib import Path
import json,tempfile,unittest
from unittest.mock import patch
import numpy as np
from PIL import Image
import chrono.core as core

class JointOptimizationTests(unittest.TestCase):
    def setUp(self):
        self.image=Image.fromarray(np.random.default_rng(24).integers(0,256,(128,48,3),dtype=np.uint8))

    def test_both_search_models_use_fixed_source_when_auto_input_is_saved(self):
        for search in ('Legacy exhaustive','Improved weighted'):
            with patch.object(core,'_legacy_component_ranges',return_value=[(127,64,1)]):
                s=core.Settings(search=search,background='Any Atari color')
                a=core.optimize(self.image,s)
                b=core.optimize(self.image,replace(s,auto_input=True))
            self.assertEqual(a,b)

    def test_detail_penalty_rejects_collapsed_black_palette(self):
        a=np.broadcast_to(np.linspace(0,255,128)[:,None,None],(128,48,3)).astype(np.uint8)
        image=Image.fromarray(a);colors=core.representative_colors(image)
        black=[0,0,0,0];gray=[core.CODES.index(c) for c in core.PRESETS['Grayscale']]
        scores=core._score([black,gray],colors)
        self.assertGreater(scores[0],scores[1])

    def test_toggle_is_reversible_repeatable_and_saved(self):
        s=core.Settings(auto_input=True,brightness=.7,contrast=.8)
        a=core.prepare(self.image,s)
        np.testing.assert_array_equal(a,core.prepare(self.image,s))
        np.testing.assert_array_equal(a,core.prepare(self.image,replace(s,auto_input=False)))
        self.assertEqual((s.brightness,s.contrast),(.7,.8))
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'settings.json';s.save(p);self.assertTrue(core.Settings.load(p).auto_input)
            old=asdict(s);old.pop('auto_input');p.write_text(json.dumps({'schema':1,'settings':old}))
            self.assertFalse(core.Settings.load(p).auto_input)
        self.assertEqual(core.Settings().scale,'Fill / crop')
        self.assertEqual(core.Settings().search,'Improved weighted')
        self.assertEqual(core.Settings().background,'Black')

    def test_fitted_controls_persist_off_and_refit_for_current_palette(self):
        first=core.optimize_input(self.image,core.Settings(auto_input=True))
        self.assertNotEqual((first.brightness,first.contrast),(1.,1.))
        off=replace(first,auto_input=False)
        np.testing.assert_array_equal(core.prepare(self.image,first),core.prepare(self.image,off))
        second=core.optimize_input(self.image,replace(off,auto_input=True,codes=core.PRESETS['Grayscale']))
        self.assertNotEqual((first.brightness,first.contrast),(second.brightness,second.contrast))
        repeated=core.optimize_input(self.image,second)
        self.assertAlmostEqual(second.brightness,repeated.brightness,places=3)
        self.assertAlmostEqual(second.contrast,repeated.contrast,places=3)

if __name__=='__main__':unittest.main()
