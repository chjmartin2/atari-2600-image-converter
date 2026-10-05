from chrono.color import blend,dim,srgb_to_linear,distance
import os,subprocess,tempfile,unittest,threading
from dataclasses import replace
from pathlib import Path
import numpy as np
from PIL import Image
from chrono.core import Settings,MODES,DITHERS,Cancelled,dimensions,frame_pixels,target_palette,cartridge_size,mode_description
from chrono.extended import HYBRID,WIDE,INTERLACE,validate_indices,convert,rows_for,search
from chrono.modes import convert_image,render
from chrono.optimization import fit_controls,conversion_score,neutral_reference
from chrono.rom import assembly,binary

class ExtendedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        yy,xx=np.indices((240,320))
        cls.image=Image.fromarray(np.stack((xx%256,yy%256,(xx+yy)%256),axis=2).astype(np.uint8))
        cls.results={mode:convert_image(cls.image,Settings(mode=mode,dither='None')) for mode in MODES[17:20]}

    def test_constraints_and_saved_settings(self):
        for mode,(_,a,s) in self.results.items():
            s.validate();validate_indices(a,s)
            self.assertEqual(a.shape,dimensions(s)[::-1])
            self.assertTrue(mode_description(mode).endswith('Static' if mode==HYBRID else 'Flicker'))
            with tempfile.TemporaryDirectory() as d:
                p=Path(d)/'settings.json';s.save(p);loaded=Settings.load(p)
                np.testing.assert_array_equal(convert_image(self.image,loaded)[1],a)

    def test_hybrid_sprite_fitting_and_all_dithers_are_legal(self):
        adjusted,_,s=self.results[HYBRID]
        for dither in DITHERS:
            a=convert(adjusted,replace(s,dither=dither))
            validate_indices(a,s)
            self.assertEqual(render(a,s).shape,(192,160,3))
        # Two detail windows share sprite colors/positions for the whole picture.
        self.assertEqual(len({(r[1:3],r[4:]) for r in s.line_codes}),1)

    def test_spatial_fields_have_complementary_coverage(self):
        _,_,s=self.results[WIDE];a=np.ones((192,96),np.uint8)
        frames=frame_pixels(a,s.codes,s.line_codes,s.mode)
        p=target_palette(s)
        np.testing.assert_array_equal(blend(frames),np.repeat(p[:,1,None,:],96,axis=1))
        # Each field exposes three 16-pixel bands, not a duplicate whole bitmap.
        for f in range(2):
            bg=np.repeat(p[:,0,None,:],48,axis=1)
            np.testing.assert_array_equal(frames[f][:,(np.arange(96)//16)%2!=f],bg)

    def test_interlace_keeps_independent_odd_even_lines(self):
        _,a,s=self.results[INTERLACE]
        f=frame_pixels(a,s.codes,s.line_codes,s.mode)
        self.assertFalse(f[0][1::2].any());self.assertFalse(f[1][::2].any())
        self.assertTrue(f[0][::2].any());self.assertTrue(f[1][1::2].any())
        self.assertFalse(np.array_equal(f[0][::2],f[1][1::2]))

    def test_export_rejects_impossible_bitmaps_and_rows(self):
        _,a,s=self.results[HYBRID]
        bad=a.copy();bad[0,0]=2
        with self.assertRaises(ValueError):binary(bad,s.codes,s.mode,s.line_codes)
        bad=a.copy();bad[0,:4]=[0,1,0,1]
        with self.assertRaises(ValueError):binary(bad,s.codes,s.mode,s.line_codes)
        rows=list(s.line_codes);rows[-1]=(*rows[-1][:4],'20','22')
        with self.assertRaises(ValueError):replace(s,line_codes=tuple(rows)).validate()
        _,_,s=self.results[INTERLACE];rows=list(s.line_codes);rows[-1]=rows[-1][:3]+('0E',)
        with self.assertRaises(ValueError):replace(s,line_codes=tuple(rows)).validate()

    def test_cancelled_palette_search_does_not_finish(self):
        event=threading.Event();event.set()
        for mode,(adjusted,_,s) in self.results.items():
            with self.assertRaises(Cancelled):search(adjusted,s,cancel=event)

    def test_image_only_fit_preserves_colors_positions_and_crop(self):
        for mode,(_,indices,s) in self.results.items():
            fitted=fit_controls(self.image,s)
            self.assertEqual(fitted.line_codes,s.line_codes)
            self.assertEqual(fitted.codes,s.codes)
            self.assertEqual((fitted.crop_x,fitted.crop_y,fitted.crop_zoom),(s.crop_x,s.crop_y,s.crop_zoom))
            ref=neutral_reference(self.image,s)
            converted=convert_image(self.image,fitted)
            self.assertLessEqual(conversion_score(ref,converted[1],fitted),conversion_score(ref,indices,s)+1e-10)

    def test_dasm_matches_binary_with_nonzero_data_and_positions(self):
        dasm=os.environ.get('DASM_PATH')
        if not dasm:self.skipTest('DASM_PATH missing')
        for mode,(_,a,s) in self.results.items():
            with tempfile.TemporaryDirectory() as d:
                p=Path(d);(p/'image.asm').write_text(assembly(a,s.codes,mode,s.line_codes))
                r=subprocess.run([dasm,'image.asm','-f3','-oimage.bin'],cwd=p,capture_output=True)
                self.assertEqual(r.returncode,0,r.stdout)
                b=binary(a,s.codes,mode,s.line_codes)
                self.assertEqual(b,(p/'image.bin').read_bytes())
                self.assertEqual(len(b),cartridge_size(mode))

if __name__=='__main__':unittest.main()
