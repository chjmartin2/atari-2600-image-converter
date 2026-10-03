import os,subprocess,tempfile,threading,unittest
from pathlib import Path
from dataclasses import replace
import numpy as np
from PIL import Image
from chrono.core import Settings,MODES,CODES,frame_pixels,target_palette,frame_count,dimensions,Cancelled
from chrono.modes import convert_image
from chrono.optimization import fit_controls,conversion_score,neutral_reference,flicker_score,joint_optimize
from chrono.rom import assembly,binary

class FlickerTests(unittest.TestCase):
    def setUp(self):
        y,x=np.indices((128,48));a=np.stack([x*5,y*2,255-x*5],axis=2).astype(np.uint8)
        a[(x//4+y//8)%2==0]//=2
        self.image=Image.fromarray(a)

    def test_default_and_saved_opt_out(self):
        self.assertTrue(Settings().flicker_aware)
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'s.json';s=Settings(flicker_aware=False);s.save(p)
            self.assertEqual(Settings.load(p),s)
        with self.assertRaises(ValueError):Settings(flicker_aware='yes').validate()

    def test_detail_and_field_difference_cost(self):
        ref=np.asarray(self.image);dim=np.uint8(ref*.5)
        stable=np.stack([dim,dim]);alternating=np.stack([ref,np.zeros_like(ref)])
        good=flicker_score(ref,stable,MODES[11])
        self.assertGreater(flicker_score(ref,alternating,MODES[11]),good)
        for v in (0,128,255):
            self.assertGreater(flicker_score(ref,np.full_like(stable,v),MODES[11]),good+.01)

    def test_fixed_palette_fit_rgb_and_nonregression(self):
        s=Settings(dither='None',red=.35,green=1.8,blue=.4)
        _,i,s=convert_image(self.image,s);reference=neutral_reference(self.image,s)
        initial=conversion_score(reference,i,s)
        winner=fit_controls(self.image,s,global_fit=True)
        _,j,winner=convert_image(self.image,winner)
        self.assertEqual(winner.codes,s.codes);self.assertEqual(winner.line_codes,s.line_codes)
        self.assertFalse(winner.auto_input)
        self.assertNotEqual((winner.red,winner.green,winner.blue),(s.red,s.green,s.blue))
        self.assertLessEqual(conversion_score(reference,j,winner),initial+1e-9)
        self.assertGreater(len(np.unique(j)),1)

    def test_pair_conversion_roundtrip(self):
        for mode in MODES[12:]:
            _,i,s=convert_image(self.image,Settings(mode=mode,dither='Ordered 4×4'))
            f=frame_pixels(i,s.codes,s.line_codes,mode);self.assertEqual(len(f),2)
            self.assertEqual(frame_count(mode),2);self.assertFalse(np.array_equal(f[0],f[1]))
            yy,xx=np.indices(i.shape);p=target_palette(s)
            np.testing.assert_array_equal(np.rint(np.mean(f,axis=0)).astype(np.uint8),p[yy,xx,i])
            with tempfile.TemporaryDirectory() as tmp:
                path=Path(tmp)/'s.json';s.save(path)
                _,j,t=convert_image(self.image,Settings.load(path));np.testing.assert_array_equal(i,j)
                self.assertEqual(t,s)

    def test_pair_dasm_parity(self):
        dasm=os.environ.get('DASM_PATH')
        if not dasm:self.skipTest('DASM_PATH missing')
        rng=np.random.default_rng(71)
        for mode in MODES[12:]:
            w,h=dimensions(Settings(mode=mode));i=rng.integers(0,4,(h,w),dtype=np.uint8);rows=[]
            for y in range(h):
                a,b,c,d=rng.choice(CODES,4)
                if mode not in MODES[15:]:b=a;d=c
                rows.append((a,b,a,'22',c,d,c,'84'))
            if mode==MODES[12]:rows=[rows[0]]*h
            with tempfile.TemporaryDirectory() as tmp:
                tmp=Path(tmp);(tmp/'image.asm').write_text(assembly(i,rows[0][:4],mode,rows),encoding='utf-8')
                result=subprocess.run([dasm,'image.asm','-f3','-oimage.bin'],cwd=tmp,capture_output=True)
                self.assertEqual(result.returncode,0,result.stdout)
                self.assertEqual((tmp/'image.bin').read_bytes(),binary(i,rows[0][:4],mode,rows))

    def test_row_palette_fit_keeps_entire_table(self):
        _,i,s=convert_image(self.image,Settings(mode=MODES[11],dither='None'))
        winner=fit_controls(self.image,s)
        self.assertEqual(winner.line_codes,s.line_codes);self.assertEqual(winner.codes,s.codes)
        ref=neutral_reference(self.image,s);_,j,t=convert_image(self.image,winner)
        self.assertLessEqual(conversion_score(ref,j,t),conversion_score(ref,i,s)+1e-9)
        stop=threading.Event();stop.set()
        with self.assertRaises(Cancelled):fit_controls(self.image,s,cancel=stop)

    def test_joint_flicker_nonregression_and_classic_palette(self):
        s=Settings(mode=MODES[0],dither='None')
        _,i,s=convert_image(self.image,s);ref=neutral_reference(self.image,s)
        winner=joint_optimize(self.image,s)
        _,j,t=convert_image(self.image,winner)
        self.assertEqual(t.codes,s.codes)
        self.assertLessEqual(conversion_score(ref,j,t),conversion_score(ref,i,s)+1e-9)
