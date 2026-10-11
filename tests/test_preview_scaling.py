import unittest
from chrono.gui import pixel_perfect_size


class PreviewScalingTests(unittest.TestCase):
    def test_atari_pixels_remain_exact_two_by_one_blocks(self):
        for viewport in ((350,500),(517,613),(30,40),(1000,800)):
            w,h=pixel_perfect_size((48,128),(384,512),viewport)
            self.assertEqual(w%48,0);self.assertEqual(h%128,0)
            self.assertEqual(w//48,2*(h//128))

    def test_fractional_aspect_has_uniform_blocks_and_fits(self):
        w,h=pixel_perfect_size((48,128),(512,384),(420,500))
        self.assertEqual(w%48,0);self.assertEqual(h%128,0)
        self.assertLessEqual(w,404);self.assertLessEqual(h,484)
        self.assertLess(abs((w/h)/(4/3)-1),.03)

    def test_exact_fractional_aspect_when_enough_room(self):
        w,h=pixel_perfect_size((48,128),(512,384),(2000,1400))
        self.assertEqual(w*3,h*4)
        self.assertEqual(w%48,0);self.assertEqual(h%128,0)

    def test_large_original_scrolls_instead_of_downsampling(self):
        self.assertEqual(pixel_perfect_size((800,600),(800,600),(350,400)),(800,600))

    def test_tall_pixels_remain_tall(self):
        w,h=pixel_perfect_size((96,192),(288,1152),(500,650))
        self.assertEqual(2*(w//96),h//192)


if __name__=='__main__':unittest.main()
