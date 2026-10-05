"""Reference vectors: Sharma/Wu/Dalal CIEDE2000 supplementary test data.
https://hajim.rochester.edu/ece/sites/gsharma/ciede2000/
"""
import unittest,json,tempfile
from pathlib import Path
import numpy as np
from chrono.color import *
from chrono.core import Settings,MODES,dimensions,target_palette,frame_pixels,quantize
from chrono.modes import normalize,render
from chrono.optimization import perceptual_score,flicker_score

VECTORS='''50 2.6772 -79.7751 50 0 -82.7485 2.0425
50 3.1571 -77.2803 50 0 -82.7485 2.8615
50 2.8361 -74.0200 50 0 -82.7485 3.4412
50 -1.3802 -84.2814 50 0 -82.7485 1
50 -1.1848 -84.8006 50 0 -82.7485 1
50 -.9009 -85.5211 50 0 -82.7485 1
50 0 0 50 -1 2 2.3669
50 -1 2 50 0 0 2.3669
50 2.49 -.001 50 -2.49 .0009 7.1792
50 2.49 -.001 50 -2.49 .0010 7.1792
50 2.49 -.001 50 -2.49 .0011 7.2195
50 2.49 -.001 50 -2.49 .0012 7.2195
50 -.001 2.49 50 .0009 -2.49 4.8045
50 -.001 2.49 50 .0010 -2.49 4.8045
50 -.001 2.49 50 .0011 -2.49 4.7461
50 2.5 0 50 0 -2.5 4.3065
50 2.5 0 73 25 -18 27.1492
50 2.5 0 61 -5 29 22.8977
50 2.5 0 56 -27 -3 31.9030
50 2.5 0 58 24 15 19.4535
50 2.5 0 50 3.1736 .5854 1
50 2.5 0 50 3.2972 0 1
50 2.5 0 50 1.8634 .5757 1
50 2.5 0 50 3.2592 .3350 1
60.2574 -34.0099 36.2677 60.4626 -34.1751 39.4387 1.2644
63.0109 -31.0961 -5.8663 62.8187 -29.7946 -4.0864 1.2630
61.2901 3.7196 -5.3901 61.4292 2.2480 -4.9620 1.8731
35.0831 -44.1164 3.7933 35.0232 -40.0716 1.5901 1.8645
22.7233 20.0904 -46.6940 23.0331 14.9730 -42.5619 2.0373
36.4612 47.8580 18.3852 36.2715 50.5065 21.2231 1.4146
90.8027 -2.0831 1.441 91.1528 -1.6435 .0447 1.4441
90.9257 -.5406 -.9208 88.6381 -.8985 -.7239 1.5381
6.7747 -.2908 -2.4247 5.8714 -.0985 -2.2286 .6377
2.0776 .0795 -1.135 .9033 -.0636 -.5514 .9082'''

class ColorTests(unittest.TestCase):
    def test_published_ciede2000_vectors_and_symmetry(self):
        v=np.fromstring(VECTORS,sep=' ').reshape(-1,7)
        np.testing.assert_allclose(delta_e_2000(v[:,:3],v[:,3:6]),v[:,6],atol=5e-5,rtol=0)
        np.testing.assert_allclose(delta_e_2000(v[:,3:6],v[:,:3]),v[:,6],atol=5e-5,rtol=0)

    def test_transfer_roundtrip_and_known_light_levels(self):
        a=np.arange(256)
        np.testing.assert_array_equal(linear_to_srgb(srgb_to_linear(a)),a)
        np.testing.assert_array_equal(blend(np.eye(3)*255),[156,156,156])
        np.testing.assert_array_equal(blend([[255,255,255],[0,0,0]]),[188]*3)
        np.testing.assert_allclose(rgb_to_lab([255]*3),[100,0,0],atol=2e-5)
        self.assertAlmostEqual(float(srgb_to_linear(128)),.2158605,places=6)

    def test_scalar_diffusion_matches_vector_metric(self):
        rng=np.random.default_rng(8);palette=rng.uniform(0,255,(128,3));lab=rgb_to_lab(palette)
        for light in rng.uniform(0,1,(100,3)):
            self.assertEqual(nearest_linear(light,lab.tolist()),int(delta_e_2000(linear_to_lab(light),lab).argmin()))

    def test_all_twenty_modes_palette_matches_physical_frame_light(self):
        for mode in MODES:
            s=normalize(Settings(mode=mode,dither='None'));w,h=dimensions(s)
            if mode==MODES[11]:
                rows=[(s.codes[0],)*10+(s.codes[3],)]*h;rows[0]=rows[-1]=('00',)*11
                from dataclasses import replace
                s=replace(s,line_codes=tuple(rows))
            p=target_palette(s)
            # Uniform legal states also exercise the blank fields and backgrounds.
            choices=(0,1) if mode in MODES[17:] else (0,3) if mode in MODES[12:17] else (0,7)
            for k in choices:
                i=np.full((h,w),k,np.uint8)
                f=np.asarray(frame_pixels(i,s.codes,s.line_codes,mode),float)/255
                light=np.where(f<=.04045,f/12.92,((f+.055)/1.055)**2.4).mean(axis=0)
                expected=np.rint(255*np.where(light<=.0031308,12.92*light,1.055*light**(1/2.4)-.055)).astype(np.uint8)
                np.testing.assert_array_equal(render(i,s),expected,err_msg=mode)
                prediction=p[k] if p.ndim==2 else p[:,k,None,:] if p.ndim==3 else p[:,:,k]
                np.testing.assert_array_equal(np.broadcast_to(prediction,expected.shape),expected,err_msg=mode)

    def test_dither_preserves_linear_gray_energy(self):
        source=np.full((128,48,3),188,np.uint8);p=np.array([[0]*3,[255]*3])
        for method in ('Ordered 8×8','Floyd–Steinberg','Burkes'):
            i=quantize(source,p,method,serpentine=True)
            self.assertAlmostEqual(float(i.mean()),.5,delta=.025,msg=method)

    def test_fixed_absolute_score_and_separate_flicker_cost(self):
        ref=np.full((8,8,3),188,np.uint8)
        steady=np.stack([ref,ref]);pulse=np.stack([np.full_like(ref,255),np.zeros_like(ref)])
        self.assertEqual(perceptual_score(ref,ref),0)
        self.assertEqual(flicker_score(ref,steady,MODES[0]),0)
        self.assertGreater(flicker_score(ref,pulse,MODES[0]),0)
        self.assertGreater(perceptual_score(ref,ref//2),.01)

    def test_old_settings_load_and_new_settings_document_model(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'s.json';Settings(mapping='Legacy RGB targets').save(p)
            self.assertEqual(json.loads(p.read_text())['color_model'],MODEL)
            self.assertEqual(Settings.load(p).mapping,'Temporal blend')
