import threading
import unittest
import numpy as np
from PIL import Image
from chrono.core import (Settings, PRESETS, Cancelled, optimize_input,
                         prepare, target_palette)
from chrono.modes import convert_image,render
from chrono.weighted_search import SpatialTarget
from chrono.optimization import neutral_reference,conversion_score

class InputOptimizationTests(unittest.TestCase):
    def test_bright_gradient_fits_palette_without_collapsing_detail(self):
        ramp=np.broadcast_to(np.linspace(0,255,128,dtype=np.uint8)[:,None,None],(128,48,3)).copy()
        image=Image.fromarray(ramp);s=Settings(dither='Floyd–Steinberg')
        result=optimize_input(image,s)
        _,before,start=convert_image(image,s);_,after,end=convert_image(image,result)
        # Fidelity is measured against the palette-fitted target, not full white.
        ref=prepare(image,result)
        spatial=SpatialTarget(ref)
        self.assertLessEqual(spatial.score(render(after,end)),spatial.score(render(before,start)))
        # Judge visible shading: saturated RGB components can legitimately map a
        # neutral ramp to only black/white without dithering. With diffusion on,
        # the local averages must retain many ordered brightness levels.
        output=target_palette(end)[after].mean(axis=(1,2))
        bands=output.reshape(16,8).mean(axis=1)
        self.assertGreater(len(np.unique(np.round(bands))),10)
        self.assertGreater(np.corrcoef(np.arange(128),output)[0,1],.95)
        self.assertLess(bands[0],5);self.assertGreater(bands[-1],90)
        self.assertEqual(result.codes,s.codes)

    def test_repeat_does_not_keep_darkening_and_other_controls_survive(self):
        image=Image.fromarray(np.random.default_rng(9).integers(0,256,(128,48,3),dtype=np.uint8))
        s=Settings(gamma=1.2,saturation=.8,red=.9,codes=PRESETS['Blue'],preset='Blue')
        first=optimize_input(image,s);second=optimize_input(image,first)
        ref=neutral_reference(image,s)
        _,a,first=convert_image(image,first);_,b,second=convert_image(image,second)
        self.assertLessEqual(conversion_score(ref,b,second),conversion_score(ref,a,first)+1e-9)
        for field in ('codes','preset','dither','crop_zoom','scale'):
            self.assertEqual(getattr(first,field),getattr(s,field))

    def test_flat_channels_remain_finite_and_white_does_not_become_black(self):
        for color in ('white','black'):
            image=Image.new('RGB',(48,128),color)
            result=optimize_input(image,Settings(dither='None'))
            out=np.asarray(prepare(image,result))
            self.assertTrue(np.isfinite(out).all())
            if color=='white':self.assertGreater(out.mean(),20)
            else:self.assertEqual(out.max(),0)

    def test_cancel(self):
        cancel=threading.Event();cancel.set()
        with self.assertRaises(Cancelled):optimize_input(Image.new('RGB',(48,128),'white'),Settings(),cancel=cancel)

if __name__=='__main__':unittest.main()
