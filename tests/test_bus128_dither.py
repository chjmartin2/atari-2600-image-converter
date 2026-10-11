import unittest,tempfile,threading
from pathlib import Path
from dataclasses import replace
from unittest.mock import patch
import numpy as np
from PIL import Image
from chrono.core import Settings,BUS128LINE,CODES,TIA,Cancelled,quantize,target_palette
from chrono.bus128_dither import random_rows
from chrono.bus128_line import search,propose
from chrono.modes import convert_image
from chrono.optimization import conversion_score
from chrono.rom import binary

class BusDitherTests(unittest.TestCase):
 def setUp(self):
  self.s=Settings(mode=BUS128LINE,dither='Ordered 4×4',scale='Stretch',aspect='Raw pixels')
  y,x=np.indices((200,128));a=np.stack((x*2,y*255//199,(x+y)*255//326),axis=-1).astype(np.uint8)
  a[:,:8]=0;self.image=Image.fromarray(a)
 def test_random_colors_do_not_repeat_and_are_persistent(self):
  for paired in (False,True):
   s=random_rows(replace(self.s,bus_pair_rows=paired,codes=('0E',)*3+('22',)),np.random.default_rng(712))
   s.validate();rgb=TIA[[CODES.index(r[0]) for r in s.line_codes]]
   self.assertTrue(np.all(np.any(rgb[1:]!=rgb[:-1],axis=1)))
   self.assertTrue(all(r[3]=='22' for r in s.line_codes));self.assertEqual(s.optimization_scope,'Image only')
   _,a,again=convert_image(self.image,s);self.assertEqual(again.line_codes,s.line_codes)
   self.assertEqual(len(binary(a,s.codes,s.mode,s.line_codes)),32768)
   with tempfile.TemporaryDirectory() as d:
    p=Path(d)/'settings.json';s.save(p);self.assertEqual(Settings.load(p),s)
   other=random_rows(s,np.random.default_rng(713));self.assertNotEqual(s.line_codes,other.line_codes)
 def test_selected_dither_runs_during_each_row_and_cannot_regress_seed(self):
  from chrono.scanline_search import evaluate_row,raster
  from chrono.color import srgb_to_linear
  for paired,method in ((False,'Floyd–Steinberg'),(True,'Ordered 4×4')):
   s=replace(self.s,bus_pair_rows=paired,dither=method,strength=.63,serpentine=True)
   seed=propose(self.image,s)
   def score(settings):
    return raster(srgb_to_linear(self.image),settings,lambda y,row:[(CODES.index(settings.line_codes[y][0]),CODES.index(settings.line_codes[y][3]))])[2]
   before=score(seed);calls=[]
   def record(row,incoming,pairs,settings,y,*args,**kwargs):
    calls.append((len(pairs),settings.dither,settings.strength,settings.serpentine,np.any(incoming)))
    return evaluate_row(row,incoming,pairs,settings,y,*args,**kwargs)
   with patch('chrono.scanline_search.evaluate_row',side_effect=record):found=search(self.image,s)
   trials=[c for c in calls if c[0]>1]
   self.assertEqual(len(trials),200)
   if not paired:self.assertTrue(all(c[0]==128 for c in trials))
   self.assertTrue(all(c[1:4]==(method,.63,True) for c in trials))
   if method=='Floyd–Steinberg':self.assertTrue(any(c[4] for c in trials[1:]))
   self.assertLessEqual(score(found),before+1e-12)
   _,output,_=convert_image(self.image,found)
   self.assertTrue(np.all(output[:,:8]==0));found.validate()
 def test_display_model_matches_real_bus_frames_and_keeps_background_shared(self):
  from chrono.scanline_search import display_pairs
  from chrono.color import srgb_to_linear
  pairs=np.column_stack((np.arange(128),np.roll(np.arange(128),17)))
  rows=tuple((CODES[f],)*3+(CODES[b],) for f,b in pairs)
  from chrono.color import blend
  expected=np.stack((blend(np.stack((TIA[pairs[:,0]],TIA[pairs[:,1]]))),TIA[pairs[:,1]]),axis=1)
  np.testing.assert_array_equal(display_pairs(pairs,self.s),srgb_to_linear(expected))
  from chrono.core import MODES
  np.testing.assert_array_equal(display_pairs(pairs,replace(self.s,mode=MODES[4])),srgb_to_linear(TIA[pairs]))
  with self.assertRaisesRegex(ValueError,'shared background'):
   search(self.image,replace(self.s,background='Per line'))
 def test_no_dither_still_tests_all_foregrounds_and_cancel_during_search(self):
  from chrono.scanline_search import evaluate_row
  s=replace(self.s,dither='None');counts=[]
  def record(row,incoming,pairs,*args,**kwargs):
   counts.append(len(pairs));return evaluate_row(row,incoming,pairs,*args,**kwargs)
  with patch('chrono.scanline_search.evaluate_row',side_effect=record):search(self.image,s)
  self.assertEqual(counts.count(128),200)
  stop=threading.Event()
  def progress(p,text):
   if 'every legal foreground' in text:stop.set()
  with self.assertRaises(Cancelled):search(self.image,self.s,progress,stop)

if __name__=='__main__':unittest.main()
