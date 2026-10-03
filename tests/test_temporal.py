import unittest,tempfile
from pathlib import Path
from dataclasses import replace
import numpy as np
from PIL import Image
from chrono.core import Settings,MODES,frame_pixels,mode_description,frame_count
from chrono.temporal import interleave,imbalance
from chrono.modes import convert_image
class TemporalTests(unittest.TestCase):
 def test_two_frame_row_balance_preserves_every_average(self):
  for mode in MODES[13:]:
   h=128 if mode==MODES[13] else 192
   s=Settings(mode=mode,line_codes=(('0E','0E','0E','00','42','42','42','00'),)*h)
   a=np.zeros((h,48),dtype=np.uint8);before=np.asarray(frame_pixels(a,s.codes,s.line_codes,mode))
   i,t=interleave(a,s);after=np.asarray(frame_pixels(i,t.codes,t.line_codes,mode))
   np.testing.assert_array_equal(before.sum(axis=0),after.sum(axis=0))
   self.assertLess(imbalance(after),imbalance(before)*.01)
 def test_three_frame_row_balance(self):
  rows=[]
  for y in range(128):
   r=['42']*3;r[y%3]='0E';rows.append(tuple(r)+('00',))
  s=Settings(mode=MODES[3],line_codes=tuple(rows));a=np.zeros((128,48),dtype=np.uint8)
  before=np.asarray(frame_pixels(a,s.codes,s.line_codes,s.mode));i,t=interleave(a,s)
  after=np.asarray(frame_pixels(i,t.codes,t.line_codes,t.mode))
  np.testing.assert_array_equal(before.sum(axis=0),after.sum(axis=0))
  self.assertLess(imbalance(after),imbalance(before)*.6)
 def test_identical_pair_pixel_interleave(self):
  s=Settings(mode=MODES[12],line_codes=(('0E','0E','0E','00')*2,)*128)
  a=np.ones((128,48),dtype=np.uint8);i,t=interleave(a,s)
  self.assertEqual(imbalance(frame_pixels(i,t.codes,t.line_codes,t.mode)),0)
  self.assertEqual(set(np.unique(i)),{1,2})
 def test_static_classic_movie_and_disabled_are_not_illegally_rephased(self):
  for mode in (MODES[0],MODES[2],MODES[11],MODES[13]):
   _,a,s=convert_image(Image.new('RGB',(80,192),'orange'),Settings(mode=mode,balance_frames=False,dither='None'))
   i,t=interleave(a,s);np.testing.assert_array_equal(a,i);self.assertEqual(t,s)
 def test_all_mode_labels_and_legacy_settings(self):
  for mode in MODES:self.assertTrue(mode_description(mode).endswith('Flicker' if frame_count(mode)>1 else 'Static'))
  with tempfile.TemporaryDirectory() as tmp:
   p=Path(tmp)/'old.json';Settings().save(p)
   import json
   d=json.loads(p.read_text());d['settings'].pop('balance_frames');p.write_text(json.dumps(d))
   self.assertTrue(Settings.load(p).balance_frames)
