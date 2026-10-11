import unittest,os,subprocess,tempfile,threading
from pathlib import Path
from dataclasses import replace
import numpy as np
from PIL import Image
from chrono.core import Settings,CODES,TIA,BUS128LINE,MODE_CHOICES,dimensions,frame_count,frame_pixels,target_palette,Cancelled,DATA
from chrono.bus128 import coverage
from chrono.bus128_line_rom import image_bytes,STREAM_STRIPS,rows_for
from chrono.modes import convert_image,search_palette,render
from chrono.rom import binary,assembly
from chrono.web_preview import preview_size,export_animation

class Bus128LineTests(unittest.TestCase):
 def setUp(self):
  self.rows=tuple((CODES[(y*13)%128],)*3+('00',) for y in range(200))
  self.s=Settings(mode=BUS128LINE,codes=self.rows[100],line_codes=self.rows,scale='Stretch',aspect='Raw pixels',dither='None')
  self.a=np.random.default_rng(81).integers(0,2,(200,128),dtype=np.uint8)
 def test_stream_roundtrip(self):
  data=image_bytes(self.a,self.s.codes,self.rows);self.assertEqual(len(data),4000);out=np.zeros_like(self.a)
  for f in range(2):
   for y in range(200):
    start=(f*200+y)*10
    self.assertEqual(data[start:start+2],bytes([int(self.rows[y][0],16)])*2)
    cols=[x+k for x in STREAM_STRIPS[(y+f)%2] for k in range(8)]
    out[y,cols]=np.unpackbits(np.frombuffer(data[start+2:start+10],np.uint8))
  np.testing.assert_array_equal(out,self.a)
 def test_preview_conversion_and_black_border(self):
  p=target_palette(self.s);self.assertEqual(p.shape,(200,2,3))
  im=Image.fromarray(p[np.arange(200)[:,None],self.a]);im.paste((0,0,0),(0,0,8,200))
  for d in ('None','Ordered 4×4','Floyd–Steinberg'):
   _,a,s=convert_image(im,replace(self.s,dither=d));self.assertEqual(s.line_codes,self.rows)
   self.assertTrue(np.all(a[:,:8]==0));np.testing.assert_array_equal(render(a,s),np.asarray(im))
  fs=frame_pixels(a,s.codes,s.line_codes,s.mode);self.assertEqual(len(fs),2)
  for f in range(2):
   fg=TIA[[CODES.index(r[0]) for r in self.rows]].astype(np.uint8)[:,None,:]
   np.testing.assert_array_equal(fs[f],np.where((a.astype(bool)&coverage(f))[:,:,None],fg,0))
 def test_search_varies_per_row_and_save_load(self):
  rows=tuple(('46',)*3+('00',) if y<100 else ('AC',)*3+('00',) for y in range(200))
  s=replace(self.s,line_codes=rows);p=target_palette(s)
  im=Image.fromarray(p[np.arange(200)[:,None],self.a])
  found=search_palette(im,replace(s,line_codes=()))
  self.assertEqual(found.line_codes,rows)
  with tempfile.TemporaryDirectory() as d:
   path=Path(d)/'settings.json';found.save(path);self.assertEqual(Settings.load(path),found)
  self.assertEqual(MODE_CHOICES[9],BUS128LINE);self.assertEqual(dimensions(s),(128,200));self.assertEqual(frame_count(s.mode),2)
  event=threading.Event();event.set()
  with self.assertRaises(Cancelled):search_palette(im,s,cancel=event)
 def test_validation(self):
  self.assertFalse(any((DATA/'bus128-line.bin').read_bytes()[:2048]))
  badrows=[self.rows[:199],(('00','02','04','00'),)*200,self.rows[:199]+(('0E',)*3+('22',),)]
  for rows in badrows:
   with self.assertRaises(ValueError):replace(self.s,line_codes=rows).validate()
   with self.assertRaises(ValueError):binary(self.a,self.s.codes,BUS128LINE,rows)
  for bad in (np.zeros((200,127),int),np.full((200,128),2),self.a.astype(float)):
   with self.assertRaises(ValueError):binary(bad,self.s.codes,BUS128LINE,self.rows)
  self.assertEqual(len(rows_for(Settings().codes)),200)
 def test_export_parity_and_animation(self):
  rows=tuple(r[:3]+('22',) for r in self.rows);s=replace(self.s,line_codes=rows,codes=rows[100])
  b=binary(self.a,s.codes,BUS128LINE,rows);self.assertEqual(len(b),32768)
  self.assertEqual(b[0x1000:0x1FA0],image_bytes(self.a,s.codes,rows))
  self.assertEqual(preview_size(replace(s,aspect='Atari pixels 2:1')),(640,500))
  with tempfile.TemporaryDirectory() as d:
   p=Path(d);export_animation(p/'preview.webp',self.a,s,retention=0)
   with Image.open(p/'preview.webp') as im:self.assertTrue(im.is_animated)
   dasm=os.environ.get('DASM_PATH')
   if not dasm:self.skipTest('DASM_PATH missing')
   (p/'image.asm').write_text(assembly(self.a,s.codes,BUS128LINE,rows),encoding='utf-8')
   r=subprocess.run([dasm,'image.asm','-f3','-oimage.bin'],cwd=p,capture_output=True)
   self.assertEqual(r.returncode,0,r.stdout);self.assertEqual((p/'image.bin').read_bytes(),b)

if __name__=='__main__':unittest.main()
