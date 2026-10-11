from dataclasses import replace,asdict
import threading,unittest
from unittest.mock import patch
import numpy as np
from PIL import Image
from chrono.core import Settings,MODES,TIA,CODES,prepare,Cancelled,frame_pixels
from chrono.modes import search_palette,convert_image
from chrono.optimization import fit_controls,joint_optimize,neutral_reference,conversion_score

class TwoColorMatchTests(unittest.TestCase):
    def setUp(self):
        y,x=np.indices((192,48))
        self.image=Image.fromarray(np.stack((x*5,y,(x*3+y)//2),axis=2).astype(np.uint8))
        self.s=Settings(mode=MODES[2],height=192,codes=('0E','0E','0E','00'),dither='None')

    def test_exact_two_color_recovery_and_population(self):
        for fraction in (1,24,47):
            a=np.empty((192,48,3),dtype=np.uint8)
            a[:,:fraction]=TIA[CODES.index('46')];a[:,fraction:]=TIA[CODES.index('B4')]
            result=search_palette(Image.fromarray(a),replace(self.s,background='Any Atari color'))
            self.assertEqual(set((result.codes[0],result.codes[3])),{'46','B4'})

    def test_background_constraints_repetition_and_controls(self):
        for background,allowed in [('Black',('00',)),('Black or white',('00','0E')),('Any Atari color',CODES)]:
            s=replace(self.s,background=background,brightness=.73,contrast=1.2,red=.8,brightness_trim=.7)
            result=search_palette(prepare(self.image,s),s)
            self.assertIn(result.codes[3],allowed)
            self.assertEqual(result.codes[:3],(result.codes[0],)*3)
            self.assertFalse(np.array_equal(TIA[CODES.index(result.codes[0])],TIA[CODES.index(result.codes[3])]))
            self.assertEqual(result,search_palette(prepare(self.image,s),s))
            for key,value in asdict(s).items():
                if key not in ('codes','preset'):self.assertEqual(getattr(result,key),value)

    def test_flat_black_white_and_color_do_not_fail(self):
        for color in ('black','white',(210,15,60)):
            for bg in ('Black','Black or white','Any Atari color'):
                s=replace(self.s,background=bg)
                result=joint_optimize(Image.new('RGB',(48,192),color),s)
                result.validate();self.assertTrue(np.isfinite(np.asarray(prepare(self.image,result))).all())

    def test_input_is_two_candidates_and_never_worsens_fixed_reference(self):
        s=replace(self.s,brightness_trim=.6,dither='Floyd–Steinberg')
        with patch('chrono.modes.convert_image',wraps=convert_image) as render:
            fitted=fit_controls(self.image,s,global_fit=True)
            self.assertEqual(render.call_count,2)
        self.assertEqual(fitted.codes,s.codes);self.assertEqual(fitted.brightness_trim,.6)
        self.assertEqual(fitted,fit_controls(self.image,fitted))
        ref=neutral_reference(self.image,s)
        _,before,start=convert_image(self.image,s);_,after,end=convert_image(self.image,fitted)
        self.assertLessEqual(conversion_score(ref,after,end),conversion_score(ref,before,start))

    def test_joint_matches_once_and_both_heights_keep_static_frames(self):
        from chrono import two_color_match as fast
        for height in (128,192):
            s=replace(self.s,height=height,brightness_trim=.5)
            with patch.object(fast,'search',wraps=fast.search) as search:
                result=joint_optimize(self.image,s,global_search=True)
                self.assertEqual(search.call_count,1)
            self.assertEqual(result.brightness_trim,1.)
            _,i,result=convert_image(self.image,result)
            self.assertEqual(i.shape,(height,48));self.assertTrue(set(np.unique(i)).issubset({0,7}))
            frames=frame_pixels(i,result.codes,result.line_codes,result.mode)
            np.testing.assert_array_equal(frames[0],frames[1]);np.testing.assert_array_equal(frames[1],frames[2])

    def test_cancel_all_scopes(self):
        cancel=threading.Event();cancel.set()
        for call in (lambda:search_palette(self.image,self.s,cancel=cancel),lambda:fit_controls(self.image,self.s,cancel=cancel),lambda:joint_optimize(self.image,self.s,cancel=cancel)):
            with self.assertRaises(Cancelled):call()
