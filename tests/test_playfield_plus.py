import unittest
from dataclasses import replace
import numpy as np
from PIL import Image
from chrono.core import Settings, CODES, TIA, DITHERS, frame_pixels, target_palette, quantize
from chrono.modes import convert_image
from chrono.playfield_plus import binary


class PlayfieldPlusTests(unittest.TestCase):
    def test_spatial_color_constraints_and_all_dithers(self):
        rows=(('48','02','C8','86'),)*192
        s=Settings(mode='Playfield Plus',line_codes=rows,codes=rows[0],aspect='Raw pixels',dither='None')
        palette=target_palette(s)
        indices=np.where(np.indices((192,40)).sum(axis=0)%2,7,0).astype(np.uint8)
        expected=palette[np.arange(192)[:,None],np.arange(40)[None,:],indices]
        self.assertEqual(len(np.unique(expected.reshape(-1,3),axis=0)),4)
        # Logical pixel 19 retains the left foreground but has the right background.
        np.testing.assert_array_equal(palette[0,19,0],TIA[CODES.index('48')])
        np.testing.assert_array_equal(palette[0,19,7],TIA[CODES.index('86')])
        for dither in DITHERS:
            result=quantize(Image.fromarray(expected),palette,dither)
            np.testing.assert_array_equal(result,indices,err_msg=dither)
        frames=frame_pixels(indices,s.codes,s.line_codes,s.mode)
        for frame in frames:np.testing.assert_array_equal(frame,expected)
        self.assertEqual(len(binary(indices,rows)),16384)

    def test_ordered_dither_uses_second_distinct_color(self):
        s=Settings(mode='Playfield Plus',line_codes=(('0E','00','0E','00'),)*192)
        p=target_palette(s)
        image=Image.new('RGB',(40,192),(110,110,110))
        result=quantize(image,p,'Ordered 4\u00d74')
        self.assertEqual(set(np.unique(result)),{0,7})
        for bad in (np.zeros((128,48),np.uint8),np.full((192,40),3,np.uint8)):
            with self.assertRaises(ValueError):binary(bad,s.line_codes)

if __name__=='__main__':unittest.main()
