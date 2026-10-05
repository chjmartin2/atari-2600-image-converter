import unittest
import numpy as np
from chrono.core import quantize,KERNELS,hardware_palette,Settings
from chrono.color import srgb_to_linear,diffusion_target

class DitherErrorTests(unittest.TestCase):
    def test_kernel_weights_are_normalized(self):
        for name,(divisor,taps) in KERNELS.items():
            self.assertEqual(sum(w for x,y,w in taps)/divisor,.75 if name=='Atkinson' else 1.)
            self.assertTrue(all(y>0 or (y==0 and x>0) for x,y,w in taps))

    def test_unavailable_highlight_excess_does_not_spread_into_shadows(self):
        palette=np.array([[0,0,0],[100,100,100]],np.uint8)
        source=np.full((32,48,3),40,np.uint8);source[:,:24]=200
        clipped=np.minimum(source,100)
        for name in KERNELS:
            for serpentine in (False,True):
                for strength in (.5,1.):
                    actual=quantize(source,palette,name,strength,serpentine)
                    expected=quantize(clipped,palette,name,strength,serpentine)
                    np.testing.assert_array_equal(actual,expected,err_msg=f'{name}, {serpentine}, {strength}')

    def test_signed_error_keeps_dark_in_range_signal_unbiased(self):
        palette=np.array([[0,0,0],[100,100,100]],np.uint8)
        for value in (20,40,60,80):
            source=np.full((192,96,3),value,np.uint8)
            for serpentine in (False,True):
                indices=quantize(source,palette,'Floyd–Steinberg',serpentine=serpentine)
                actual=srgb_to_linear(palette[indices])[16:-16,16:-16].mean()
                self.assertAlmostEqual(actual,float(srgb_to_linear(value)),delta=.0004,msg=f'{value}, {serpentine}')

    def test_spatial_palette_bounds_are_local(self):
        palette=np.zeros((32,48,2,3),np.uint8)
        palette[:,:24,1]=80;palette[:,24:,1]=180
        source=np.full((32,48,3),210,np.uint8);source[16:]=50
        clipped=np.minimum(source,palette.max(axis=2))
        np.testing.assert_array_equal(quantize(source,palette,'Stucki'),quantize(clipped,palette,'Stucki'))

    def test_black_border_stays_black_for_every_diffuser_and_direction(self):
        source=np.zeros((40,48,3),np.uint8)
        source[5:-5,5:-5]=np.random.default_rng(40).integers(0,256,(30,38,3),dtype=np.uint8)
        border=np.all(source==0,axis=2);palette=hardware_palette(Settings().codes)
        for method in KERNELS:
            for serpentine in (False,True):
                result=palette[quantize(source,palette,method,serpentine=serpentine)]
                self.assertFalse(result[border].any(),f'{method}, {serpentine}')

    def test_black_protection_does_not_invent_a_missing_color(self):
        source=np.zeros((16,16,3),np.uint8)
        palette=np.array([[50,20,10],[200,180,160]],np.uint8)
        i=quantize(source,palette,'Floyd–Steinberg')
        np.testing.assert_array_equal(palette[i],np.broadcast_to(palette[0],source.shape))

    def test_gamut_projection_does_not_carry_impossible_yellow(self):
        # Yellow lies inside the RGB channel box but outside this triangle.
        p=np.array([[0,0,0],[1,0,0],[0,1,0]],float)
        palette=np.broadcast_to(p,(1,3,3,3))
        light=np.array([[[1,1,0],[.2,.3,0],[1,0,0]]])
        result=diffusion_target(light,palette)
        np.testing.assert_allclose(result[0,0],[.5,.5,0],atol=1e-6)
        np.testing.assert_allclose(result[0,1],[.2,.3,0],atol=1e-5)
        np.testing.assert_array_equal(result[0,2],[1,0,0])
