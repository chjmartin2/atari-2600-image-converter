import tempfile,unittest
from pathlib import Path
from dataclasses import replace
from unittest.mock import patch
import numpy as np
from PIL import Image
from chrono.core import Settings,MODES,dimensions,frame_pixels,display_aspect
from chrono.animation import persistence_frames
from chrono.web_preview import export_animation,preview_size

class WebPreviewTests(unittest.TestCase):
    def test_lossless_frame_order_persistence_geometry_and_timing(self):
        rng=np.random.default_rng(83)
        for mode,count in ((MODES[0],3),(MODES[12],2)):
            s=Settings(mode=mode,aspect='Raw pixels')
            indices=rng.integers(0,8 if count==3 else 4,(128,48),dtype=np.uint8)
            expected=persistence_frames(frame_pixels(indices,s.codes,s.line_codes,mode)[:count],.6)
            with tempfile.TemporaryDirectory() as folder:
                p=Path(folder)/'demo.webp';result=export_animation(p,indices,s,long_edge=320)
                with Image.open(p) as im:
                    self.assertEqual(im.info['loop'],0)
                    self.assertEqual(im.size,(120,320))
                    self.assertEqual(im.n_frames,3 if count==3 else 6)
                    duration=0
                    for k in range(im.n_frames):
                        im.seek(k);actual=np.asarray(im.convert('RGB'));duration+=im.info['duration']
                        frame=np.asarray(Image.fromarray(expected[k%count]).resize(im.size,Image.Resampling.NEAREST))
                        np.testing.assert_array_equal(actual,frame)
                    self.assertEqual(duration,50 if count==3 else 100)
                self.assertEqual(result['bytes'],p.stat().st_size)

    def test_static_export_has_no_invented_animation(self):
        s=Settings(mode=MODES[2]);i=np.zeros((128,48),np.uint8)
        with tempfile.TemporaryDirectory() as folder:
            p=Path(folder)/'static.webp';export_animation(p,i,s)
            with Image.open(p) as im:
                self.assertEqual(im.n_frames,1);self.assertEqual(im.size,(480,640))

    def test_all_modes_have_correct_display_geometry(self):
        for mode in MODES:
            s=Settings(mode=mode);w,h=preview_size(s)
            self.assertEqual(max(w,h),640)
            raw=replace(s,aspect='Raw pixels');rw,rh=preview_size(raw);a,b=dimensions(s)
            if display_aspect(raw)=='Raw pixels':self.assertAlmostEqual(rw/rh,a/b,delta=.003)
            else:self.assertEqual((rw,rh),(w,h))

    def test_error_does_not_replace_existing_file_or_leave_partial(self):
        with tempfile.TemporaryDirectory() as folder:
            p=Path(folder)/'demo.webp';p.write_bytes(b'original')
            with patch.object(Image.Image,'save',side_effect=OSError('encoder failed')):
                with self.assertRaises(OSError):export_animation(p,np.zeros((128,48),np.uint8),Settings())
            self.assertEqual(p.read_bytes(),b'original');self.assertEqual(list(Path(folder).iterdir()),[p])
            for kwargs in ({'rate':0},{'retention':1},{'long_edge':100000}):
                with self.assertRaises(ValueError):export_animation(p,np.zeros((128,48),np.uint8),Settings(),**kwargs)
