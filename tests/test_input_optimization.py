import threading
import unittest
import numpy as np
from PIL import Image
from chrono.core import (Settings, PRESETS, Cancelled, optimize_input,
                         prepare, target_palette, input_tone_target)

class InputOptimizationTests(unittest.TestCase):
    def test_bright_gradient_fits_palette_without_collapsing_detail(self):
        ramp=np.broadcast_to(np.linspace(0,255,128,dtype=np.uint8)[:,None,None],(128,48,3)).copy()
        image=Image.fromarray(ramp);s=Settings(dither='None')
        result=optimize_input(image,s)
        self.assertLess(result.brightness,.8)
        out=np.asarray(prepare(image,result),dtype=float)
        target=input_tone_target(prepare(image,Settings()),target_palette(s))
        before=np.asarray(prepare(image,s),dtype=float)
        self.assertLess(np.mean((out-target)**2),np.mean((before-target)**2)*.25)
        self.assertGreater(np.std(out),10)
        self.assertGreater(len(np.unique(out[:,:,0])),30)
        self.assertEqual(result.codes,s.codes)

    def test_repeat_does_not_keep_darkening_and_other_controls_survive(self):
        image=Image.fromarray(np.random.default_rng(9).integers(0,256,(128,48,3),dtype=np.uint8))
        s=Settings(gamma=1.2,saturation=.8,red=.9,codes=PRESETS['Blue'],preset='Blue')
        first=optimize_input(image,s);second=optimize_input(image,first)
        self.assertAlmostEqual(first.brightness,second.brightness,places=3)
        self.assertAlmostEqual(first.contrast,second.contrast,places=3)
        for field in ('gamma','saturation','red','codes','preset','dither'):
            self.assertEqual(getattr(first,field),getattr(s,field))

    def test_flat_channels_remain_finite_and_white_does_not_become_black(self):
        palette=target_palette(Settings())
        target=input_tone_target(Image.new('RGB',(48,128),'white'),palette)
        self.assertTrue(np.isfinite(target).all());self.assertGreater(target.mean(),20)
        black=input_tone_target(Image.new('RGB',(48,128),'black'),palette)
        self.assertEqual(black.max(),0)

    def test_cancel(self):
        cancel=threading.Event();cancel.set()
        with self.assertRaises(Cancelled):optimize_input(Image.new('RGB',(48,128),'white'),Settings(),cancel=cancel)

if __name__=='__main__':unittest.main()
