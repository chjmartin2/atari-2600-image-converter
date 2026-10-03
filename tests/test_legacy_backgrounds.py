import threading
import unittest
from unittest.mock import patch
import numpy as np
from PIL import Image
import chrono.core as core

class LegacyBackgroundTests(unittest.TestCase):
    def test_any_background_can_find_colored_exact_match(self):
        image=Image.new('RGB',(48,128),tuple(core.TIA[127].astype(int)))
        progress=[]
        # Keep real palette scoring; restrict component triples so all backgrounds
        # are compared independently of a long component search.
        with patch.object(core,'_legacy_component_ranges',return_value=[(0,0,1)]):
            codes,score=core.optimize(image,core.Settings(search='Legacy exhaustive',background='Any Atari color'),lambda p,t:progress.append(p))
        self.assertEqual(codes[3],core.CODES[127]);self.assertEqual(score,0)
        self.assertEqual(progress[0],0);self.assertEqual(progress[-1],1)

    def test_selector_limits_candidates_and_preserves_diversity(self):
        for option,expected in [('Black',{0}),('Black or white',{0,112}),('Any Atari color',set(range(128)))]:
            seen=set()
            def score(batch,colors,weights=None,diversity=False,tone=None):
                self.assertTrue(diversity)
                seen.update(batch[:,3].tolist())
                return np.ones(len(batch)) # force completion, not early zero-error exit
            with patch.object(core,'_legacy_component_ranges',return_value=[(0,0,1)]),patch.object(core,'_score',side_effect=score):
                core.optimize(Image.new('RGB',(48,128),'red'),core.Settings(search='Legacy exhaustive',background=option,diversity=True))
            self.assertEqual(seen,expected)

    def test_cancel_after_search_starts(self):
        cancel=threading.Event()
        def progress(p,text):cancel.set()
        with self.assertRaises(core.Cancelled):
            core.optimize(Image.new('RGB',(48,128),'red'),core.Settings(search='Legacy exhaustive',background='Any Atari color'),progress,cancel)

if __name__=='__main__':unittest.main()
