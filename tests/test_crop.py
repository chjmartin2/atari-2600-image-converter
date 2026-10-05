from dataclasses import replace,asdict
import json
from pathlib import Path
import tempfile
import unittest
import numpy as np
from PIL import Image
from chrono.core import Settings,prepare,drag_crop_position,crop_bounds

class CropTests(unittest.TestCase):
    def test_zoom_selects_region_and_stretch_ignores_aspect(self):
        # A 4:1 source selection must fill a 3:4 display without padding/cropping.
        a=np.zeros((80,320,3),np.uint8)
        a[:40,:160]=[255,0,0];a[:40,160:]=[0,255,0]
        a[40:,:160]=[0,0,255];a[40:,160:]=[255,255,0]
        image=Image.fromarray(a)
        s=Settings(scale='Stretch',crop_zoom=2,resample='Nearest')
        for x,y,color in [(0,0,(255,0,0)),(1,0,(0,255,0)),(0,1,(0,0,255)),(1,1,(255,255,0))]:
            out=prepare(image,replace(s,crop_x=x,crop_y=y))
            self.assertEqual(out.getextrema(),tuple((v,v) for v in color))
        self.assertEqual(crop_bounds(image.size,s),(80,20,240,60))

    def test_zoom_drag_tracks_pixels_in_all_scaling_modes(self):
        for scale in ('Stretch','Fit','Fill / crop'):
            s=Settings(scale=scale,crop_zoom=2)
            x,y=drag_crop_position((320,80),s,(30,30),(300,400))
            self.assertLess(x,.5);self.assertLess(y,.5)
            left,top,right,bottom=crop_bounds((320,80),replace(s,crop_x=x,crop_y=y))
            self.assertGreaterEqual(left,0);self.assertGreaterEqual(top,0)
            self.assertLessEqual(right,320);self.assertLessEqual(bottom,80)

    def test_zoom_rotated_mirrored_and_saved(self):
        a=np.zeros((80,320,3),np.uint8);a[:,:160]=[255,0,0];a[:,160:]=[0,255,0]
        s=Settings(scale='Stretch',crop_zoom=2,crop_x=0,mirror=True,resample='Nearest')
        self.assertEqual(prepare(Image.fromarray(a),s).getpixel((24,64)),(0,255,0))
        x,y=drag_crop_position((320,80),replace(s,rotate=90),(0,-20),(300,400))
        self.assertGreater(y,s.crop_y)
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'settings.json';s.save(path);self.assertEqual(Settings.load(path),s)
            old=asdict(Settings());old.pop('crop_zoom')
            path.write_text(json.dumps({'schema':1,'settings':old}))
            self.assertEqual(Settings.load(path).crop_zoom,1)
        for bad in (.5,9,float('nan'),float('inf')):
            with self.assertRaises(ValueError):replace(s,crop_zoom=bad).validate()

    def test_crop_edges_select_actual_source_regions(self):
        a=np.zeros((100,300,3),np.uint8)
        a[:,:100]=[255,0,0];a[:,100:200]=[0,255,0];a[:,200:]=[0,0,255]
        im=Image.fromarray(a);s=Settings(scale='Fill / crop',resample='Nearest')
        for pos,color in [(0,(255,0,0)),(.5,(0,255,0)),(1,(0,0,255))]:
            self.assertEqual(prepare(im,replace(s,crop_x=pos)).getpixel((24,64)),color)

    def test_picture_follows_horizontal_and_vertical_drag_and_clamps(self):
        s=Settings(scale='Fill / crop')
        x,y=drag_crop_position((300,100),s,(100,0),(300,400))
        self.assertLess(x,.5);self.assertEqual(y,.5)
        x,y=drag_crop_position((100,300),s,(0,100),(300,400))
        self.assertEqual(x,.5);self.assertLess(y,.5)
        self.assertEqual(drag_crop_position((300,100),s,(10000,0),(300,400)),(0,.5))
        self.assertEqual(drag_crop_position((300,100),s,(-10000,0),(300,400)),(1,.5))

    def test_rotated_mirrored_and_prepared_input(self):
        s=Settings(scale='Fill / crop',rotate=90,mirror=True)
        x,y=drag_crop_position((300,100),s,(100,100),(300,400))
        self.assertEqual(x,.5);self.assertLess(y,.5)
        self.assertEqual(drag_crop_position((48,128),Settings(scale='Fill / crop'),(100,100),(300,400)),(.5,.5))

    def test_crop_does_not_change_fit_or_stretch(self):
        image=Image.fromarray(np.random.default_rng(4).integers(0,256,(50,170,3),dtype=np.uint8))
        for mode in ('Fit','Stretch'):
            s=Settings(scale=mode)
            np.testing.assert_array_equal(prepare(image,s),prepare(image,replace(s,crop_x=0,crop_y=1)))

    def test_settings_persist_crop_and_old_settings_default_to_center(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'settings.json';s=Settings(crop_x=.2,crop_y=.8);s.save(path)
            loaded=Settings.load(path);self.assertEqual((loaded.crop_x,loaded.crop_y),(.2,.8))
            old=asdict(s);old.pop('crop_x');old.pop('crop_y')
            path.write_text(json.dumps({'schema':1,'settings':old}))
            loaded=Settings.load(path);self.assertEqual((loaded.crop_x,loaded.crop_y),(.5,.5))
        with self.assertRaises(ValueError):Settings(crop_x=1.2).validate()

if __name__=='__main__':unittest.main()
