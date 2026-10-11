import json
import tempfile
import unittest
from pathlib import Path
from dataclasses import replace
import numpy as np
from PIL import Image
from chrono.core import Settings, MODES, prepare
from chrono.optimization import neutral_reference, fit_controls, joint_optimize, conversion_score
from chrono.modes import convert_image, render, search_palette


class BrightnessTrimTests(unittest.TestCase):
    def test_all_modes_apply_trim_once_and_keep_black(self):
        image=Image.new('RGB',(48,128),(160,120,80))
        for mode in MODES:
            with self.subTest(mode=mode):
                s=Settings(mode=mode,scale='Stretch',resample='Nearest')
                neutral=np.asarray(prepare(image,s))
                trimmed=np.asarray(prepare(image,replace(s,brightness_trim=.5)))
                np.testing.assert_array_equal(trimmed,np.rint(neutral*.5).astype(np.uint8))
                self.assertFalse(np.asarray(prepare(Image.new('RGB',(48,128)),replace(s,brightness_trim=.5))).any())

    def test_fixed_reference_keeps_trim_but_not_fitted_brightness(self):
        image=Image.new('RGB',(48,128),(160,120,80))
        for mode in (MODES[0],MODES[1],MODES[2],MODES[11]):
            s=Settings(mode=mode,brightness=1.8,brightness_trim=.5)
            np.testing.assert_array_equal(neutral_reference(image,s),prepare(image,replace(s,brightness=1.)))
            self.assertLess(np.asarray(neutral_reference(image,s)).mean(),np.asarray(neutral_reference(image,replace(s,brightness_trim=1.))).mean())

    def test_lower_trim_changes_real_dither_pixels_and_preserves_black_border(self):
        image=Image.new('RGB',(48,128),(180,180,180))
        a=np.asarray(image).copy();a[:4]=0;a[-4:]=0;a[:,:4]=0;a[:,-4:]=0
        image=Image.fromarray(a)
        s=Settings(mode=MODES[2],codes=('0E','0E','0E','00'),resample='Nearest',dither='Floyd–Steinberg')
        _,full,s=convert_image(image,s)
        _,dim,t=convert_image(image,replace(s,brightness_trim=.65))
        self.assertGreater(np.count_nonzero(dim==7),np.count_nonzero(full==7))
        self.assertLess(render(dim,t).mean(),render(full,s).mean())
        self.assertTrue((dim[:4]==7).all());self.assertTrue((dim[:,:4]==7).all())

    def test_image_and_palette_preserve_trim_joint_search_can_change_it(self):
        y,x=np.indices((128,48));a=np.repeat(((x*3+y)%220)[...,None],3,axis=2).astype(np.uint8)
        image=Image.fromarray(a)
        s=Settings(mode=MODES[2],codes=('0E','0E','0E','00'),brightness_trim=.6,dither='None',search_effort='Standard')
        reference=neutral_reference(image,s)
        _,idx,start=convert_image(image,s)
        fitted=fit_controls(image,s)
        _,out,fitted=convert_image(image,fitted)
        self.assertEqual(fitted.brightness_trim,.6)
        self.assertLessEqual(conversion_score(reference,out,fitted),conversion_score(reference,idx,start)+1e-12)
        colors=search_palette(prepare(image,s),s)
        self.assertEqual(colors.brightness_trim,.6)
        winner=joint_optimize(image,s)
        self.assertNotEqual(winner.brightness_trim,.6)
        self.assertGreaterEqual(winner.brightness_trim,.25)
        self.assertLessEqual(winner.brightness_trim,1.5)

    def test_settings_roundtrip_old_files_and_validation(self):
        with tempfile.TemporaryDirectory() as folder:
            p=Path(folder)/'settings.json';Settings(brightness_trim=.73).save(p)
            self.assertEqual(Settings.load(p).brightness_trim,.73)
            data=json.loads(p.read_text(encoding='utf-8'));del data['settings']['brightness_trim']
            p.write_text(json.dumps(data),encoding='utf-8')
            self.assertEqual(Settings.load(p).brightness_trim,1.)
        for bad in (0.,1.51,float('nan'),float('inf')):
            with self.assertRaises(ValueError):Settings(brightness_trim=bad).validate()


if __name__=='__main__':unittest.main()
