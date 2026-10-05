from dataclasses import replace,asdict
import unittest,threading
import numpy as np
from PIL import Image
from chrono.core import Settings,MODES,prepare,Cancelled,optimize_input
from chrono.modes import convert_image
from chrono.optimization import fit_controls,joint_optimize,flicker_enabled

class ClassicBrightnessTests(unittest.TestCase):
    def setUp(self):
        y,x=np.indices((128,48));self.image=Image.fromarray(np.stack((x*5,y*2,(x*3+y)%256),axis=2).astype(np.uint8))

    def test_only_brightness_changes_in_both_entry_points(self):
        s=Settings(mode=MODES[0],dither='None',brightness=.8,contrast=.85,gamma=1.15,saturation=.75,red=.9,green=1.1,blue=.95,sharpness=1.2,crop_zoom=1.4)
        for fn in (fit_controls,joint_optimize,optimize_input):
            t=fn(self.image,s)
            changed={k for k in asdict(s) if getattr(s,k)!=getattr(t,k)}
            self.assertEqual(changed,{'brightness'})
            self.assertEqual(t.brightness,.47)

    def test_flicker_switch_never_applies_a_second_adjustment(self):
        s=Settings(mode=MODES[0],dither='None',brightness=.3)
        self.assertTrue(flicker_enabled(s))
        off=replace(s,flicker_aware=False)
        np.testing.assert_array_equal(prepare(self.image,s),prepare(self.image,off))
        a=fit_controls(self.image,s);b=fit_controls(self.image,off)
        # Neither the flicker policy nor search effort changes the Classic preset.
        self.assertEqual(a.brightness,.47);self.assertEqual(b.brightness,.47)
        self.assertEqual(fit_controls(self.image,s,global_fit=True).brightness,.47)
        self.assertEqual(joint_optimize(self.image,s,global_search=True).brightness,.47)
        np.testing.assert_array_equal(convert_image(self.image,a)[1],convert_image(self.image,replace(a,flicker_aware=False))[1])
        repeated=fit_controls(self.image,a)
        self.assertEqual(repeated.brightness,a.brightness)
        self.assertGreater(a.brightness,.15)

    def test_brightness_is_applied_once_and_can_cancel(self):
        s=Settings(mode=MODES[0],brightness=.3,scale='Stretch',resample='Nearest')
        im=Image.new('RGB',(48,128),(200,100,50))
        np.testing.assert_array_equal(np.asarray(prepare(im,s))[0,0],[60,30,15])
        stop=threading.Event();stop.set()
        with self.assertRaises(Cancelled):fit_controls(self.image,s,cancel=stop)

if __name__=='__main__':unittest.main()
