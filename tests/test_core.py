from chrono.color import blend,dim,srgb_to_linear,distance
import os
from pathlib import Path
import subprocess
import tempfile
import threading
import unittest
import numpy as np
from PIL import Image
from chrono.core import *
from chrono.rom import assembly,binary,bank_bytes

class ConversionTests(unittest.TestCase):
    def setUp(self):
        self.image = Image.fromarray(np.random.default_rng(42).integers(0,256,(128,48,3),dtype=np.uint8))

    def test_every_scaling_filter_and_adjustments(self):
        source = Image.new('RGB',(800,600),'red')
        for scale in ('Fit','Fill / crop','Stretch'):
            for filt in FILTERS:
                s=Settings(scale=scale,resample=filt,brightness=.8,gamma=1.2,rotate=90,mirror=True)
                out=prepare(source,s)
                self.assertEqual(out.size,(48,128))
                self.assertEqual(out.mode,'RGB')

    def test_all_dithers_and_presets(self):
        for preset,codes in PRESETS.items():
            p=hardware_palette(codes)
            self.assertEqual(p.shape,(8,3))
            for dither in DITHERS:
                out=quantize(self.image,p,dither,serpentine=True)
                self.assertEqual(out.shape,(128,48))
                self.assertLessEqual(out.max(),7)

    def test_zero_strength_is_no_dither(self):
        p=hardware_palette(PRESETS['Sepia'])
        np.testing.assert_array_equal(quantize(self.image,p),quantize(self.image,p,'Stucki',0))

    def test_single_exact_color(self):
        p=hardware_palette(PRESETS['Neon'])
        image=Image.new('RGB',(48,128),tuple(p[4]))
        for d in DITHERS:
            self.assertTrue((quantize(image,p,d)==4).all())

    def test_transparency_import_and_settings_roundtrip(self):
        with tempfile.TemporaryDirectory() as temp:
            path=Path(temp)/'transparent.png';Image.new('RGBA',(20,20),(255,0,0,0)).save(path)
            self.assertEqual(load_image(path).getpixel((0,0)),(0,0,0))
            s=Settings(codes=PRESETS['Blue'],preset='Blue');path=Path(temp)/'settings.json';s.save(path)
            self.assertEqual(tuple(Settings.load(path).codes),s.codes)
            path.write_text('{"schema":999}')
            with self.assertRaises(ValueError):Settings.load(path)

    def test_improved_search_valid_deterministic_and_improves_start(self):
        im=Image.new('RGB',(48,128),(100,150,190));s=Settings(search='Improved weighted')
        codes,score=optimize(im,s)
        self.assertEqual(optimize(im,s)[0],codes)
        self.assertTrue(all(c in CODES for c in codes))
        self.assertLessEqual(score,float(_weighted_error(im,hardware_palette(s.codes))))

    def test_search_and_dither_cancel(self):
        cancel=threading.Event();cancel.set()
        for method in ('Legacy exhaustive','Improved weighted'):
            with self.assertRaises(Cancelled):optimize(self.image,Settings(search=method),cancel=cancel)
        with self.assertRaises(Cancelled):quantize(self.image,hardware_palette(Settings().codes),'Floyd–Steinberg',cancel=cancel)

    def test_legacy_search_exact_representable_color(self):
        codes,score=optimize(Image.new('RGB',(48,128),'black'),Settings(search='Legacy exhaustive'))
        self.assertEqual(score,0)
        self.assertEqual(codes[3],'00')

class CartridgeTests(unittest.TestCase):
    def test_bit_order_row_order_component_order(self):
        idx=np.full((128,48),7,np.uint8)
        idx[127,0]=2  # green, bottom row: (127+0)%3 = green
        idx[0,47]=1   # red, top row, last strip, least significant bit
        data=bank_bytes(idx)
        self.assertEqual(data[0],128)
        self.assertEqual(data[5*128+127],1)
        self.assertEqual(data[768],0)
        self.assertEqual(data[2304:],bytes([24,0,12,13,14,15,16,17,24,0,6,7,8,9,10,11,24,0,0,1,2,3,4,5]))

    def test_roundtrip_all_indices_and_temporal_average(self):
        idx=np.random.default_rng(123).integers(0,8,(128,48),dtype=np.uint8)
        data=bank_bytes(idx);components=np.zeros((128,48,3),np.uint8)
        for f in range(3):
            for strip in range(6):
                for y in range(128):
                    byte=data[f*768+strip*128+127-y]
                    components[y,strip*8:strip*8+8,(y+f)%3]=np.unpackbits(np.uint8([byte]))
        np.testing.assert_array_equal(components,BITS[idx])
        colors=PRESETS['Neon'];frames=frame_pixels(idx,colors)
        np.testing.assert_array_equal(blend(frames),hardware_palette(colors)[idx])

    def test_invalid_dimensions_and_codes(self):
        with self.assertRaises(ValueError):binary(np.zeros((48,128),np.uint8),Settings().codes)
        with self.assertRaises(ValueError):binary(np.zeros((128,48),np.uint8),('FF',)*4)

    @unittest.skipUnless(os.environ.get('DASM_PATH'),'Set DASM_PATH for independent assembler verification')
    def test_assembler_matches_direct_rom_all_presets_and_random_codes(self):
        rng=np.random.default_rng(123)
        palettes=list(PRESETS.values())+[tuple(rng.choice(CODES,4)) for _ in range(12)]
        with tempfile.TemporaryDirectory() as temp:
            temp=Path(temp)
            for codes in palettes:
                idx=rng.integers(0,8,(128,48),dtype=np.uint8)
                source=assembly(idx,codes)
                self.assertNotIn('include "',source.lower())
                (temp/'test.asm').write_text(source)
                p=subprocess.run([os.environ['DASM_PATH'],'test.asm','-f3','-otest.bin'],cwd=temp,capture_output=True)
                self.assertEqual(p.returncode,0,p.stdout+p.stderr)
                rom=binary(idx,codes)
                self.assertEqual(rom,(temp/'test.bin').read_bytes())
                self.assertEqual(len(rom),4096)
                self.assertGreaterEqual(int.from_bytes(rom[-4:-2],'little'),0xF000)

def _weighted_error(image,p):
    return (distance(np.asarray(image)[:,:,None,:],p)**2).min(axis=2).mean()

if __name__=='__main__':unittest.main()
