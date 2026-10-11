import json,os,subprocess,tempfile,unittest
from pathlib import Path
from dataclasses import replace
import numpy as np
from PIL import Image
from chrono.core import Settings,MODES,dimensions,cartridge_size,cartridge_type,geometry_target,frame_pixels
from chrono.modes import convert_image
from chrono.rom import assembly,binary
from chrono.tall_rom import parts
from chrono.web_preview import preview_size

class TallModeTests(unittest.TestCase):
    def test_defaults_and_unrelated_modes(self):
        for mode in MODES[1:4]:self.assertEqual(dimensions(Settings(mode=mode)),(48,128))
        for mode in [MODES[0],*MODES[5:]]:
            self.assertEqual(dimensions(Settings(mode=mode)),dimensions(Settings(mode=mode,height=192)))
        self.assertEqual(geometry_target((640,480),Settings(mode=MODES[12],height=192)),(384,512))
        with self.assertRaises(ValueError):Settings(height=200).validate()

    def test_geometry_and_web_preview(self):
        for mode in MODES[1:4]:
            s=Settings(mode=mode,height=192)
            self.assertEqual(geometry_target((640,480),s),(384,768))
            self.assertEqual(geometry_target((48,192),s),(48,192))
            self.assertEqual(preview_size(s),(320,640))
            self.assertEqual(preview_size(replace(s,aspect='Display 4:3')),(640,480))
            self.assertEqual(cartridge_type(s),'4K' if mode==MODES[2] else 'F6')

    def test_conversion_settings_and_exports(self):
        im=Image.fromarray(np.random.default_rng(29).integers(0,256,(192,48,3),dtype=np.uint8))
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'settings.json'
            for mode in MODES[1:4]:
                for height in (128,192):
                    a,i,s=convert_image(im,Settings(mode=mode,height=height,dither='Ordered 4×4'))
                    self.assertEqual(a.size,(48,height));self.assertEqual(i.shape,(height,48))
                    s.save(path);loaded=Settings.load(path);self.assertEqual(s,loaded)
                    _,j,t=convert_image(im,loaded);np.testing.assert_array_equal(i,j)
                    self.assertEqual(len(binary(i,s.codes,s.mode,s.line_codes)),cartridge_size(s))
                    self.assertEqual(frame_pixels(i,s.codes,s.line_codes,s.mode)[0].shape,(height,48,3))
            data=json.loads(path.read_text());data['settings'].pop('height');data['settings']['line_codes']=[]
            path.write_text(json.dumps(data));self.assertEqual(Settings.load(path).height,128)

    def test_exported_phases_match_preview_and_assembler(self):
        dasm=os.environ.get('DASM_PATH')
        if not dasm:self.skipTest('DASM_PATH missing')
        from chrono.core import CODES,TIA
        rng=np.random.default_rng(52)
        for mode in MODES[1:4]:
            a=rng.integers(0,8,(192,48),dtype=np.uint8)
            codes=('4A','C8','88','22') if mode!=MODES[2] else ('0E','0E','0E','22')
            rows=tuple(tuple(CODES[v] for v in rng.integers(0,128,3))+('22',) for _ in range(192)) if mode==MODES[3] else ()
            if mode==MODES[2]:a=np.where(a==7,7,0).astype(np.uint8)
            expected=frame_pixels(a,codes,rows,mode)
            for k,(indices,r) in enumerate(parts(a,codes,mode,rows)):
                for y in range(192):
                    actual=TIA[[CODES.index(r[y][0]),CODES.index(r[y][3])]][(indices[y]==7).astype(int)]
                    np.testing.assert_array_equal(actual,expected[k][y])
            with tempfile.TemporaryDirectory() as tmp:
                tmp=Path(tmp);(tmp/'image.asm').write_text(assembly(a,codes,mode,rows),encoding='utf-8')
                result=subprocess.run([dasm,'image.asm','-f3','-oimage.bin'],cwd=tmp,capture_output=True)
                self.assertEqual(result.returncode,0,result.stdout)
                self.assertEqual((tmp/'image.bin').read_bytes(),binary(a,codes,mode,rows))
