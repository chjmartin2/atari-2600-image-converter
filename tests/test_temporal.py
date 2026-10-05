import unittest,tempfile
from pathlib import Path
from dataclasses import replace
import numpy as np
from PIL import Image
from chrono.core import Settings,MODES,frame_pixels,mode_description,frame_count
from chrono.temporal import interleave,imbalance,canonicalize
from chrono.modes import convert_image,search_palette
class TemporalTests(unittest.TestCase):
 def test_two_color_distinct_palettes_interleave_every_row_and_preserve_pixels(self):
  rows=(('0E','0E','0E','00','42','42','42','00'),)*128
  s=Settings(mode=MODES[12],line_codes=rows)
  for a in (np.zeros((128,48),np.uint8),np.random.default_rng(38).integers(0,4,(128,48),dtype=np.uint8)):
   before=np.asarray(frame_pixels(a,s.codes,rows,s.mode));i,t=interleave(a,s);t.validate()
   after=np.asarray(frame_pixels(i,t.codes,t.line_codes,t.mode))
   np.testing.assert_array_equal(before.sum(axis=0),after.sum(axis=0))
   for y in range(128):self.assertEqual(t.line_codes[y],rows[0] if y%2==0 else rows[0][4:]+rows[0][:4])
   j,u=interleave(i,t);np.testing.assert_array_equal(j,i);self.assertEqual(u,t)
   if not a.any():self.assertLess(imbalance(after),imbalance(before)*.01)
  off=canonicalize(replace(t,balance_frames=False))
  self.assertEqual(len(set(off.line_codes)),1)

 def test_two_color_search_shares_background_and_legacy_palettes_stay_intact(self):
  image=Image.fromarray(np.random.default_rng(3).integers(0,256,(128,48,3),dtype=np.uint8))
  s=search_palette(image,Settings(mode=MODES[12],background='Any Atari color'))
  self.assertTrue(all(r[3]==r[7] for r in s.line_codes))
  old=replace(s,line_codes=(('0E','0E','0E','00','42','42','42','84'),)*128)
  a=np.zeros((128,48),np.uint8);i,t=interleave(a,old)
  np.testing.assert_array_equal(i,a);self.assertEqual(t,old)
  old.validate()
  bad=list(s.line_codes);bad[-1]=('0A','0A','0A',bad[0][3])+bad[-1][4:]
  with self.assertRaises(ValueError):replace(s,line_codes=tuple(bad)).validate()

 def test_two_color_interleaved_dasm_matches_binary(self):
  import os,subprocess
  from chrono.rom import assembly,binary
  dasm=os.environ.get('DASM_PATH')
  if not dasm:self.skipTest('DASM_PATH missing')
  s=Settings(mode=MODES[12],line_codes=(('0E','0E','0E','22','42','42','42','22'),)*128)
  a=np.random.default_rng(39).integers(0,4,(128,48),dtype=np.uint8);i,t=interleave(a,s)
  with tempfile.TemporaryDirectory() as tmp:
   tmp=Path(tmp);(tmp/'image.asm').write_text(assembly(i,t.codes,t.mode,t.line_codes))
   r=subprocess.run([dasm,'image.asm','-f3','-oimage.bin'],cwd=tmp,capture_output=True)
   self.assertEqual(r.returncode,0,r.stdout)
   self.assertEqual((tmp/'image.bin').read_bytes(),binary(i,t.codes,t.mode,t.line_codes))
 def test_two_frame_row_balance_preserves_every_average(self):
  for mode in MODES[13:17]:
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
  s=Settings(mode=MODES[12]);i,t=interleave(a,s);t.validate()
  np.testing.assert_array_equal(np.asarray(frame_pixels(a,s.codes,(),s.mode)).sum(axis=0),np.asarray(frame_pixels(i,t.codes,t.line_codes,t.mode)).sum(axis=0))
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
