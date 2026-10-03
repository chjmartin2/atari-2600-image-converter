import os,subprocess,tempfile,unittest,threading
from dataclasses import replace
from pathlib import Path
import numpy as np
from PIL import Image
from chrono.core import Settings,MODES,DITHERS,CODES,TIA,Cancelled,frame_pixels,dimensions
from chrono.modes import convert_image,search_palette,render
from chrono.rom import binary,assembly
from chrono.bus_rom import image_bytes,thumb_initializer,IMAGE_OFFSET
from chrono.optimization import joint_optimize,perceptual_score

class BusTests(unittest.TestCase):
    def setUp(self):
        self.s=Settings(mode=MODES[7],scale='Stretch',aspect='Raw pixels',dither='None')
        self.indices=np.tile(np.arange(128,dtype=np.uint8).reshape(8,16),(24,1))
        self.image=Image.fromarray(TIA[self.indices].astype(np.uint8))

    def test_all_colors_survive_every_dither_and_frames_are_static(self):
        for dither in DITHERS:
            a,i,s=convert_image(self.image,replace(self.s,dither=dither))
            self.assertEqual(a.size,(16,192));self.assertEqual(s.line_codes,())
            np.testing.assert_array_equal(render(i,s),TIA[self.indices])
            frames=frame_pixels(i,s.codes,s.line_codes,s.mode)
            for f in frames:np.testing.assert_array_equal(f,TIA[self.indices])

    def test_palette_is_unrestricted_and_settings_roundtrip(self):
        s=search_palette(self.image,self.s)
        self.assertEqual(s.preset,'Full NTSC palette')
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'settings.json';s.save(p);loaded=Settings.load(p)
            self.assertEqual(s,loaded)
            self.assertEqual(dimensions(loaded),(16,192))
        cancel=threading.Event();cancel.set()
        with self.assertRaises(Cancelled):convert_image(self.image,s,cancel)
        with self.assertRaises(ValueError):replace(s,line_codes=(('00',)*4,)*192).validate()

    def test_packing_and_invalid_input(self):
        b=binary(self.indices,self.s.codes,self.s.mode)
        self.assertEqual(len(b),32768)
        self.assertEqual(b[0x778:0x77C],b'BUS\0')
        self.assertEqual(b[0x800:0x800+len(thumb_initializer())],thumb_initializer())
        self.assertEqual(b[IMAGE_OFFSET:IMAGE_OFFSET+3072],image_bytes(self.indices))
        expected=np.array([int(c,16) for c in CODES],dtype=np.uint8)[self.indices]
        self.assertEqual(b[IMAGE_OFFSET:IMAGE_OFFSET+3072],expected.tobytes())
        for bad in (np.zeros((192,40),int),np.full((192,16),128),np.full((192,16),-1),np.zeros((192,16),float)):
            with self.assertRaises(ValueError):binary(bad,self.s.codes,self.s.mode)

    def test_assembler_matches_export(self):
        dasm=os.environ.get('DASM_PATH')
        if not dasm:self.skipTest('DASM_PATH missing')
        with tempfile.TemporaryDirectory() as d:
            p=Path(d);(p/'image.asm').write_text(assembly(self.indices,self.s.codes,self.s.mode),encoding='utf-8')
            r=subprocess.run([dasm,'image.asm','-f3','-oimage.bin'],cwd=p,capture_output=True)
            self.assertEqual(r.returncode,0,r.stdout)
            self.assertEqual((p/'image.bin').read_bytes(),binary(self.indices,self.s.codes,self.s.mode))

    def test_global_optimizer_keeps_full_palette_and_detail(self):
        # A known representable input must never be replaced by a washed-out result.
        s=joint_optimize(self.image,replace(self.s,auto_input=True),global_search=True)
        a,i,s=convert_image(self.image,s)
        self.assertEqual(s.mode,MODES[7]);self.assertEqual(s.line_codes,())
        self.assertLessEqual(perceptual_score(self.image,render(i,s)),1e-10)
        self.assertGreater(len(np.unique(i)),100)

if __name__=='__main__':unittest.main()
