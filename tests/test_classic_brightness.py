from dataclasses import replace, asdict
import unittest, threading
from unittest.mock import patch
import numpy as np
from PIL import Image
from chrono.core import Settings, MODES, prepare, Cancelled, optimize_input, target_palette
from chrono.modes import convert_image, render
from chrono.optimization import fit_controls, joint_optimize
from chrono.classic_brightness import ClassicToneTarget


class ClassicBrightnessTests(unittest.TestCase):
    def setUp(self):
        y,x=np.indices((128,48))
        self.image=Image.fromarray(np.stack((x*5,y*2,(x*3+y)%256),axis=2).astype(np.uint8))
        self.settings=Settings(mode=MODES[0],dither='None')

    def score(self, image, s):
        reference=prepare(image,replace(s,brightness=1.))
        target=ClassicToneTarget(reference,target_palette(s))
        _,indices,t=convert_image(image,s)
        return target.score(render(indices,t))

    def test_only_brightness_changes_in_all_entry_points(self):
        s=replace(self.settings,brightness=.8,contrast=.85,gamma=1.15,saturation=.75,
                  red=.9,green=1.1,blue=.95,sharpness=1.2,crop_zoom=1.4)
        results=[]
        for fn in (fit_controls,joint_optimize,optimize_input):
            t=fn(self.image,s)
            changed={k for k in asdict(s) if getattr(s,k)!=getattr(t,k)}
            self.assertEqual(changed,{'brightness'})
            self.assertLessEqual(self.score(self.image,t),self.score(self.image,s)+1e-12)
            results.append(t.brightness)
        self.assertEqual(len(set(results)),1)

    def test_adapts_to_image_and_beats_baselines(self):
        a=np.tile(np.linspace(0,255,48,dtype=np.uint8),(128,1))
        ramp=Image.fromarray(np.stack([a,a,a],axis=2))
        results=[]
        for image in (ramp,self.image):
            result=fit_controls(image,self.settings)
            results.append(result.brightness)
            for brightness in (.47,.54,1.,self.settings.brightness):
                self.assertLessEqual(self.score(image,result),self.score(image,replace(result,brightness=brightness))+1e-12)
        self.assertNotEqual(*results)
        self.assertGreater(min(results),.1)
        self.assertLess(max(results),1.)

    def test_selected_dither_is_evaluated_and_fixed(self):
        from chrono.classic_brightness import quantize
        s=replace(self.settings,dither='Ordered 4×4',strength=.65,serpentine=True)
        with patch('chrono.classic_brightness.quantize',wraps=quantize) as spy:
            t=fit_controls(self.image,s)
        self.assertGreater(spy.call_count,20)
        for call in spy.call_args_list:
            self.assertEqual(call.args[2:5],(s.dither,s.strength,s.serpentine))
        self.assertEqual((t.dither,t.strength,t.serpentine),(s.dither,s.strength,s.serpentine))

    def test_flicker_switch_and_effort_do_not_double_adjust(self):
        s=replace(self.settings,brightness=.3)
        a=fit_controls(self.image,s)
        b=fit_controls(self.image,replace(s,flicker_aware=False),global_fit=True)
        self.assertEqual(a.brightness,b.brightness)
        np.testing.assert_array_equal(convert_image(self.image,a)[1],convert_image(self.image,b)[1])
        repeated=fit_controls(self.image,a)
        self.assertLessEqual(self.score(self.image,repeated),self.score(self.image,a)+1e-12)
        self.assertGreater(repeated.brightness,.15)

    def test_fixed_white_and_penalty_for_collapsed_detail(self):
        s=self.settings
        ramp=np.tile(np.linspace(0,255,48,dtype=np.uint8),(128,1))
        reference=np.stack([ramp,ramp,ramp],axis=2)
        palette=target_palette(s)
        target=ClassicToneTarget(reference,palette)
        white=target.white
        fitted=fit_controls(Image.fromarray(reference),s)
        _,indices,t=convert_image(Image.fromarray(reference),fitted)
        good=target.score(render(indices,t))
        self.assertLess(good,target.score(np.broadcast_to(palette[0],reference.shape)))
        self.assertLess(good,target.score(np.zeros_like(reference)))
        self.assertEqual(target.white,white)
        flat=ClassicToneTarget(np.full_like(reference,255),palette)
        self.assertAlmostEqual(flat.score(np.broadcast_to(palette[0],reference.shape)),0.)

    def test_black_retains_current_and_cancellation_during_search(self):
        s=replace(self.settings,brightness=.63)
        self.assertEqual(fit_controls(Image.new('RGB',(48,128),'black'),s).brightness,.63)
        stop=threading.Event()
        progress=lambda p,t:stop.set()
        with self.assertRaises(Cancelled):fit_controls(self.image,s,cancel=stop,progress=progress)
        with self.assertRaises(Cancelled):fit_controls(self.image,s,cancel=stop)

    def test_brightness_is_applied_once(self):
        s=replace(self.settings,brightness=.3,scale='Stretch',resample='Nearest')
        im=Image.new('RGB',(48,128),(200,100,50))
        np.testing.assert_array_equal(np.asarray(prepare(im,s))[0,0],[60,30,15])


if __name__=='__main__':unittest.main()
