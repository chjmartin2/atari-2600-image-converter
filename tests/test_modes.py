import os,subprocess,tempfile,unittest
from pathlib import Path
from dataclasses import replace
import numpy as np
from PIL import Image
from chrono.core import Settings,MODES,PRESETS,frame_pixels,quantize,target_palette
from chrono.modes import convert_image,normalize,render,search_palette
from chrono.rom import assembly,binary

class ModesTests(unittest.TestCase):
    def setUp(self):
        self.image=Image.fromarray(np.random.default_rng(123).integers(0,256,(128,48,3),dtype=np.uint8))

    def test_classic_locks_rgb_and_two_color_has_no_temporal_shades(self):
        s=normalize(Settings(mode=MODES[0],codes=PRESETS['Neon']))
        self.assertEqual(s.codes,PRESETS['RGB (original Chronocolour)'])
        a,indices,s=convert_image(self.image,Settings(mode=MODES[2],dither='Ordered 4×4'))
        self.assertTrue(set(np.unique(indices))<={0,7})
        frames=frame_pixels(indices,s.codes)
        np.testing.assert_array_equal(frames[0],frames[1]);np.testing.assert_array_equal(frames[1],frames[2])
        self.assertLessEqual(len(np.unique(render(indices,s).reshape(-1,3),axis=0)),2)

    def test_scanline_tables_persist_and_stable_modes_repeat(self):
        for mode in MODES[3:7]:
            adjusted,indices,s=convert_image(self.image,Settings(mode=mode,dither='None'))
            self.assertEqual(len(s.line_codes),indices.shape[0])
            with tempfile.TemporaryDirectory() as tmp:
                p=Path(tmp)/'settings.json';s.save(p);loaded=Settings.load(p)
                a2,i2,s2=convert_image(self.image,loaded)
                np.testing.assert_array_equal(indices,i2)
            if mode in MODES[4:]:
                f=frame_pixels(indices,s.codes,s.line_codes,s.mode)
                np.testing.assert_array_equal(f[0],f[1]);np.testing.assert_array_equal(f[0],f[2])

    def test_row_palette_dithers_use_current_row(self):
        rows=[('0E',)*3+('00',) if y%2 else ('4E',)*3+('00',) for y in range(128)]
        s=Settings(mode=MODES[4],line_codes=tuple(rows))
        for dither in ('None','Ordered 4×4','Floyd–Steinberg'):
            a,i,s=convert_image(self.image,replace(s,dither=dither))
            self.assertTrue(set(np.unique(i))<={0,7})

    def test_raster_assembly_matches_patch_template(self):
        dasm=os.environ.get('DASM_PATH')
        if not dasm:self.skipTest('DASM_PATH missing')
        rng=np.random.default_rng(44)
        for mode in MODES[3:7]:
            h,w=(192,40) if mode in MODES[5:] else (128,48)
            i=rng.integers(0,8,(h,w),dtype=np.uint8)
            if mode!=MODES[3]:i=np.where(i<4,0,7).astype(np.uint8)
            rows=[]
            for y in range(h):
                codes=tuple(f'{int(v):02X}' for v in rng.integers(0,128,4)*2)
                if mode in MODES[4:6]:codes=(codes[0],)*3+(codes[3],)
                if mode not in MODES[5:]:codes=codes[:3]+('00',)
                rows.append(codes)
            with tempfile.TemporaryDirectory() as tmp:
                tmp=Path(tmp);(tmp/'image.asm').write_text(assembly(i,rows[0],mode,rows))
                result=subprocess.run([dasm,'image.asm','-f3','-oimage.bin'],cwd=tmp,capture_output=True)
                self.assertEqual(result.returncode,0,result.stdout)
                self.assertEqual((tmp/'image.bin').read_bytes(),binary(i,rows[0],mode,rows))
                self.assertEqual(len((tmp/'image.bin').read_bytes()),16384 if mode==MODES[6] else 4096)

if __name__=='__main__':unittest.main()
