import os,subprocess,tempfile,unittest,threading
from pathlib import Path
from dataclasses import replace
from unittest.mock import patch
import numpy as np
from PIL import Image
from chrono.core import Settings,MODES,CODES,TIA,DITHERS,Cancelled,dimensions,cartridge_type,prepare,quantize,target_palette
from chrono.color import srgb_to_linear,linear_to_srgb
from chrono.modes import convert_image,search_palette,render,best_pair
from chrono.scanline_search import raster,convert,row_score,search
from chrono.rom import assembly,binary

class ScanlineSearchTests(unittest.TestCase):
 def test_background_choices_and_rows_roundtrip(self):
  pixels=np.empty((4,48,3),np.uint8)
  pairs=[('2E','28'),('8E','88'),('CE','C8'),('4E','48')]
  for y,(fg,bg) in enumerate(pairs):
   pixels[y,:24]=TIA[CODES.index(fg)];pixels[y,24:]=TIA[CODES.index(bg)]
  im=Image.fromarray(pixels)
  for option in ('Black','White','Any Atari color','Per line'):
   s=Settings(mode=MODES[4],background=option,dither='None')
   r=search(im,s);bgs={row[3] for row in r.line_codes}
   if option=='Black':self.assertEqual(bgs,{'00'})
   elif option=='White':self.assertEqual(bgs,{'0E'})
   elif option=='Any Atari color':self.assertEqual(len(bgs),1)
   else:
    self.assertGreater(len(bgs),1)
    np.testing.assert_array_equal(render(convert(im,r),r),pixels)
  with self.assertRaises(ValueError):Settings(mode=MODES[1],background='Per line').validate()
  for h in (128,192):
   s=Settings(mode=MODES[4],height=h,background='Per line',dither='None')
   _,i,r=convert_image(im,s)
   r=replace(r,line_codes=tuple(r.line_codes[y%h][:3]+(pairs[y%4][1],) for y in range(h)))
   with tempfile.TemporaryDirectory() as tmp:
    path=Path(tmp)/'state.json';r.save(path);self.assertEqual(Settings.load(path),r)
   self.assertEqual(dimensions(r),(48,h));self.assertEqual(cartridge_type(r),'F6')

 def test_search_and_conversion_identical_for_every_dither(self):
  im=Image.fromarray(np.random.default_rng(37).integers(0,256,(4,48,3),dtype=np.uint8))
  for method in DITHERS:
   for strength in (0.,.7):
    s=Settings(mode=MODES[4],background='Per line',dither=method,strength=strength,serpentine=True)
    pairs=[(CODES.index('0E'),CODES.index('00')),(CODES.index('4E'),CODES.index('84'))]
    indices,rows,_=raster(srgb_to_linear(im),s,lambda y,row:pairs)
    np.testing.assert_array_equal(indices,convert(im,replace(s,line_codes=rows)))
    self.assertTrue(set(indices.ravel())<={0,7})

 def test_selected_dither_changes_search_and_beats_old_point_fit(self):
  # Reproducible broad colored patches expose dither-dependent choices.
  light=np.repeat(np.random.default_rng(3).random((4,12,3)),4,axis=1)*.6
  im=Image.fromarray(linear_to_srgb(light))
  base=Settings(mode=MODES[4],background='Black',dither='None')
  plain=search(im,base)
  s=replace(base,dither='Floyd–Steinberg',strength=1.)
  found=search(im,s)
  self.assertNotEqual(plain.line_codes,found.line_codes)
  old=[]
  for row in np.asarray(im):
   fg,bg=best_pair(row,[0]);old.append((CODES[fg],)*3+(CODES[bg],))
  previous=replace(s,line_codes=tuple(old))
  def score(settings):
   output=srgb_to_linear(render(convert(im,settings),settings))
   return np.mean(row_score(srgb_to_linear(im),output,True))
  self.assertLess(score(found),score(previous))

 def test_error_carries_between_rows_and_black_is_protected(self):
  im=Image.fromarray(np.full((4,48,3),100,np.uint8));s=Settings(mode=MODES[4],dither='Floyd–Steinberg')
  incoming=[]
  def choose(y,row):incoming.append(row.copy());return [(CODES.index('0E'),0)]
  raster(srgb_to_linear(im),s,choose)
  self.assertGreater(np.max(np.abs(incoming[1]-srgb_to_linear(im)[1])),0)
  a=np.asarray(im).copy();a[:,0:4]=0;im=Image.fromarray(a)
  r=replace(s,line_codes=(('0E','0E','0E','00'),)*4)
  np.testing.assert_array_equal(convert(im,r)[:,:4],7)
  event=threading.Event();event.set()
  with self.assertRaises(Cancelled):search(im,s,cancel=event)
  with self.assertRaises(Cancelled):convert(im,r,cancel=event)

 def test_actual_conversion_and_asm_match_for_both_heights(self):
  dasm=os.environ.get('DASM_PATH')
  if not dasm:self.skipTest('DASM_PATH missing')
  for h in (128,192):
   rng=np.random.default_rng(h);a=np.where(rng.integers(0,2,(h,48)),0,7).astype(np.uint8)
   rows=tuple((CODES[y%128],)*3+(CODES[(y*5+8)%128],) for y in range(h))
   s=Settings(mode=MODES[4],height=h,background='Per line',codes=rows[0],line_codes=rows).validate()
   with tempfile.TemporaryDirectory() as tmp:
    p=Path(tmp);(p/'image.asm').write_text(assembly(a,s.codes,s.mode,rows),encoding='utf-8')
    r=subprocess.run([dasm,'image.asm','-f3','-oimage.bin'],cwd=p,capture_output=True)
    self.assertEqual(r.returncode,0,r.stdout)
    self.assertEqual((p/'image.bin').read_bytes(),binary(a,s.codes,s.mode,rows))
    self.assertEqual(len((p/'image.bin').read_bytes()),16384)

class ExhaustiveScanlineTests(unittest.TestCase):
 def test_all_pairs_are_present_at_both_efforts(self):
  from itertools import combinations_with_replacement
  from chrono.scanline_search import ALL_PAIRS
  self.assertEqual(len(ALL_PAIRS),8256)
  self.assertEqual(list(map(tuple,ALL_PAIRS)),list(combinations_with_replacement(range(128),2)))
  im=Image.fromarray(np.random.default_rng(92).integers(0,256,(2,48,3),dtype=np.uint8))
  for effort in ('Standard','Thorough'):
   counts=[]
   def record(source,s,choose,*args,**kwargs):
    def tracked(y,row):
     pairs=choose(y,row);counts.append(len(pairs));return pairs
    return raster(source,s,tracked,*args,**kwargs)
   with patch('chrono.scanline_search.raster',side_effect=record),patch('chrono.scanline_search.pair_screen',side_effect=AssertionError('Per line must not shortlist')):
    search(im,Settings(mode=MODES[4],background='Per line',search_effort=effort,dither='Floyd–Steinberg'))
   self.assertEqual(counts.count(8256),2)

 def test_parallel_candidates_equal_single_batch_with_carried_error(self):
  from chrono.scanline_search import ALL_PAIRS,evaluate_row
  source=np.random.default_rng(333).random((3,48,3))
  s=Settings(mode=MODES[4],background='Per line',dither='Atkinson',serpentine=True)
  actual,rows,score=raster(source,s,lambda y,row:ALL_PAIRS)
  carry=np.zeros((5,48,3));expected=[];colors=[];total=0
  for y in range(3):
   out,future,scores=evaluate_row(source[y],carry[y],ALL_PAIRS,s,y)
   best=int(scores.argmin());fg,bg=ALL_PAIRS[best]
   colors.append((CODES[fg],)*3+(CODES[bg],));expected.append(np.where(out[best]==0,0,7))
   total+=scores[best];carry[y+1:y+3]+=future[best]
  np.testing.assert_array_equal(actual,expected)
  self.assertEqual(rows,tuple(colors));self.assertAlmostEqual(score,total/3,places=12)

 def test_cancellation_inside_a_candidate_batch(self):
  from chrono.scanline_search import ALL_PAIRS,evaluate_row
  import chrono.scanline_search as module
  event=threading.Event();original=module.delta_e_2000
  def stop(*args):event.set();return original(*args)
  with patch('chrono.scanline_search.delta_e_2000',side_effect=stop):
   with self.assertRaises(Cancelled):
    evaluate_row(np.ones((48,3))*.4,np.zeros((48,3)),ALL_PAIRS,Settings(dither='Floyd–Steinberg'),0,event)
