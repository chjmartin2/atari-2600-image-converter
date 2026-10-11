import unittest,tempfile,json,threading
from dataclasses import replace
from pathlib import Path
import numpy as np
from PIL import Image
from chrono.core import Settings,BUS128LINE,BUS128,CODES,TIA,Cancelled,prepare
from chrono.color import blend,distance
from chrono.modes import convert_image,render,search_palette
from chrono.bus128_pairs import pair_average,distinct_rows
from chrono.optimization import conversion_score,spatial_score
from chrono.rom import binary

class PairedBusTests(unittest.TestCase):
 def setUp(self):
  self.s=Settings(mode=BUS128LINE,bus_pair_rows=True,dither='None',scale='Stretch',aspect='Raw pixels')
  a=np.zeros((200,128,3),np.uint8)
  a[:,:64]=blend([TIA[CODES.index('46')],TIA[0]])
  a[:,64:]=blend([TIA[CODES.index('AC')],TIA[0]])
  self.image=Image.fromarray(a)
 def test_joint_fit_improves_pair_average_and_forces_real_color_difference(self):
  _,a,old=convert_image(self.image,replace(self.s,bus_pair_rows=False))
  _,b,new=convert_image(self.image,self.s)
  self.assertTrue(distinct_rows(new.line_codes));new.validate()
  ref=pair_average(self.image)
  before=np.mean(distance(ref,pair_average(render(a,old)))**2)
  after=np.mean(distance(ref,pair_average(render(b,new)))**2)
  self.assertLess(after,before*.8)
  self.assertEqual(len({r[3] for r in new.line_codes}),1)
  self.assertEqual(len(binary(b,new.codes,new.mode,new.line_codes)),32768)
 def test_strict_flat_area_and_black_protection(self):
  im=Image.new('RGB',(128,200),(90,90,90));im.paste((0,0,0),(0,0,8,200))
  _,a,s=convert_image(im,self.s);self.assertTrue(distinct_rows(s.line_codes))
  for method in ('None','Ordered 4×4','Floyd–Steinberg'):
   _,a,current=convert_image(im,replace(s,dither=method))
   self.assertEqual(current.line_codes,s.line_codes)
   self.assertTrue(np.all(render(a,current)[:,:8]==0))
 def test_rows_are_paired_locally_and_background_can_be_white(self):
  im=Image.new('RGB',(128,200),(240,200,100));im.paste((30,90,150),(0,100,128,200))
  s=search_palette(im,replace(self.s,background='Black or white'))
  self.assertTrue(distinct_rows(s.line_codes))
  self.assertNotEqual(s.line_codes[:2],s.line_codes[100:102])
  self.assertEqual(len({r[3] for r in s.line_codes}),1)
 def test_persistence_validation_cancel_and_other_modes_unchanged(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'s.json';self.s.save(p);self.assertEqual(Settings.load(p),self.s)
   data=json.loads(p.read_text());del data['settings']['bus_pair_rows'];p.write_text(json.dumps(data))
   self.assertFalse(Settings.load(p).bus_pair_rows)
  self.assertFalse(Settings().bus_pair_rows)
  with self.assertRaises(ValueError):replace(self.s,bus_pair_rows='yes').validate()
  with self.assertRaises(ValueError):replace(self.s,line_codes=(('0E',)*3+('00',),)*200).validate()
  stop=threading.Event();stop.set()
  with self.assertRaises(Cancelled):search_palette(self.image,self.s,cancel=stop)
  s=replace(self.s,mode=BUS128,codes=('0E',)*3+('00',))
  _,a,_=convert_image(self.image,s);_,b,_=convert_image(self.image,replace(s,bus_pair_rows=False))
  np.testing.assert_array_equal(a,b)
 def test_input_scoring_respects_pair_mix_and_flicker_toggle(self):
  _,a,s=convert_image(self.image,self.s);output=render(a,s)
  ref=np.asarray(self.image)
  noflicker=replace(s,flicker_aware=False)
  self.assertAlmostEqual(conversion_score(ref,a,noflicker),spatial_score(ref,output,True))
  self.assertGreaterEqual(conversion_score(ref,a,s),conversion_score(ref,a,noflicker))
  # A pair is averaged in linear light, not by averaging encoded RGB bytes.
  blackwhite=np.array([[[0,0,0]],[[255,255,255]]],np.uint8)
  self.assertTrue(np.all(pair_average(blackwhite)==188))

if __name__=='__main__':unittest.main()
