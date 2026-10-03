import unittest,threading
from dataclasses import replace
import numpy as np
from PIL import Image
from chrono.core import Settings,prepare,Cancelled,MODES
from chrono.optimization import perceptual_score,joint_optimize,fit_controls
from chrono.modes import convert_image,render

class PerceptualTests(unittest.TestCase):
    def setUp(self):
        y,x=np.indices((128,48));a=np.stack([x*5,y*2,255-x*5],axis=2).astype(np.uint8)
        a[(x//4+y//8)%2==0]//=2
        self.image=Image.fromarray(a)

    def test_flat_white_and_black_cannot_win_by_erasing_signal(self):
        ref=np.asarray(self.image)
        dim=(ref.astype(float)*.55).astype(np.uint8)
        good=perceptual_score(ref,dim)
        for value in (0,128,255):
            self.assertGreater(perceptual_score(ref,np.full_like(ref,value)),good*2)

    def test_joint_cycles_visible_controls_and_keeps_best(self):
        s=Settings(auto_input=True,dither='None',flicker_aware=False);passes=[]
        a,i,start=convert_image(self.image,s)
        ref=prepare(self.image,replace(s,brightness=1,contrast=1))
        initial=perceptual_score(ref,render(i,start))
        winner=joint_optimize(self.image,s,iteration=lambda a,i,s,score:passes.append((s,score)))
        a,i,final=convert_image(self.image,winner)
        self.assertGreaterEqual(len(passes),2)
        self.assertLessEqual(perceptual_score(ref,render(i,final)),initial+1e-9)
        self.assertGreater(len(np.unique(i)),1)
        off=replace(final,auto_input=False)
        np.testing.assert_array_equal(prepare(self.image,final),prepare(self.image,off))

    def test_global_keeps_detail_and_cancels(self):
        s=Settings(dither='None');winner=joint_optimize(self.image,s,global_search=True)
        a,i,final=convert_image(self.image,winner)
        self.assertGreater(len(np.unique(i)),1)
        self.assertGreater(np.std(render(i,final)),15)
        stop=threading.Event();stop.set()
        with self.assertRaises(Cancelled):joint_optimize(self.image,s,cancel=stop)

if __name__=='__main__':unittest.main()
