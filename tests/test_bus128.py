import unittest,os,subprocess,tempfile,json,threading
from pathlib import Path
from dataclasses import replace
import numpy as np
from PIL import Image
from chrono.core import Settings,MODES,BUS128,MODE_CHOICES,dimensions,frame_count,frame_pixels,target_palette,Cancelled,DATA
from chrono.bus128 import coverage
from chrono.bus128_rom import image_bytes,STREAM_STRIPS
from chrono.modes import convert_image,search_palette,render
from chrono.rom import binary,assembly
from chrono.web_preview import preview_size,export_animation

class Bus128Tests(unittest.TestCase):
 def setUp(self):
  self.s=Settings(mode=BUS128,codes=('0E',)*3+('00',),scale='Stretch',aspect='Raw pixels',dither='None')
  self.a=np.random.default_rng(81).integers(0,2,(200,128),dtype=np.uint8)
 def test_coverage_and_stream_roundtrip(self):
  m0,m1=coverage(0),coverage(1)
  self.assertTrue(np.all(m0^m1));self.assertTrue(np.all(m0.sum(axis=1)==64))
  data=image_bytes(self.a,self.s.codes);out=np.zeros_like(self.a)
  for f in range(2):
   for y in range(200):
    cols=[x+k for x in STREAM_STRIPS[(y+f)%2] for k in range(8)]
    out[y,cols]=np.unpackbits(np.frombuffer(data[(f*200+y)*8:(f*200+y+1)*8],np.uint8))
  np.testing.assert_array_equal(out,self.a)
 def test_conversion_keeps_chosen_color_and_black_border(self):
  p=target_palette(self.s);im=Image.fromarray(p[self.a]);im.paste((0,0,0),(0,0,8,200))
  for d in ('None','Ordered 4×4','Floyd–Steinberg'):
   _,a,s=convert_image(im,replace(self.s,dither=d))
   self.assertEqual(s.codes,self.s.codes);self.assertEqual(s.line_codes,())
   self.assertTrue(np.all(a[:,:8]==0));np.testing.assert_array_equal(render(a,s),np.asarray(im))
  fs=frame_pixels(a,s.codes,(),s.mode);self.assertEqual(len(fs),2)
  self.assertTrue(np.all(np.any(fs[0]!=fs[1],axis=2)==a.astype(bool)))
 def test_search_save_load_and_old_name_migration(self):
  im=Image.fromarray(target_palette(self.s)[self.a])
  s=search_palette(im,self.s);self.assertEqual(s.codes,self.s.codes)
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'s.json';s.save(p);self.assertEqual(Settings.load(p),s)
   data=json.loads(p.read_text());data['settings']['mode']='Bus stuffing (experimental)';p.write_text(json.dumps(data))
   self.assertEqual(Settings.load(p).mode,MODES[7])
  self.assertEqual(MODE_CHOICES[8],BUS128);self.assertEqual(dimensions(s),(128,200));self.assertEqual(frame_count(s.mode),2)
  event=threading.Event();event.set()
  with self.assertRaises(Cancelled):search_palette(im,s,cancel=event)
 def test_validation_and_driver_free_template(self):
  self.assertFalse(any((DATA/'bus128.bin').read_bytes()[:2048]))
  for bad in (np.zeros((200,127),int),np.full((200,128),2),self.a.astype(float)):
   with self.assertRaises(ValueError):binary(bad,self.s.codes,BUS128)
  with self.assertRaises(ValueError):replace(self.s,line_codes=(self.s.codes,)*200).validate()
 def test_export_parity_and_animation(self):
  b=binary(self.a,self.s.codes,BUS128);self.assertEqual(len(b),32768)
  self.assertEqual(b[0x4000:0x4C80],image_bytes(self.a,self.s.codes))
  self.assertEqual(preview_size(replace(self.s,aspect='Atari pixels 2:1')),(640,500))
  with tempfile.TemporaryDirectory() as d:
   p=Path(d);export_animation(p/'preview.webp',self.a,self.s,retention=0)
   with Image.open(p/'preview.webp') as im:self.assertTrue(im.is_animated)
   dasm=os.environ.get('DASM_PATH')
   if not dasm:self.skipTest('DASM_PATH missing')
   (p/'image.asm').write_text(assembly(self.a,self.s.codes,BUS128),encoding='utf-8')
   r=subprocess.run([dasm,'image.asm','-f3','-oimage.bin'],cwd=p,capture_output=True)
   self.assertEqual(r.returncode,0,r.stdout);self.assertEqual((p/'image.bin').read_bytes(),b)

if __name__=='__main__':unittest.main()
