from chrono.color import blend,dim,srgb_to_linear,distance
import json,os,subprocess,tempfile,threading,unittest
from pathlib import Path
from dataclasses import replace
import numpy as np
from PIL import Image
from chrono.core import Settings,MODES,CODES,TIA,Cancelled,frame_pixels,target_palette,dimensions,cartridge_size
from chrono.modes import convert_image,search_palette,render
from chrono.rom import assembly,binary
from chrono.animation import persistence_frames

class AdvancedModesTests(unittest.TestCase):
 def setUp(self):self.image=Image.fromarray(np.random.default_rng(127).integers(0,256,(96,80,3),dtype=np.uint8))

 def test_conversion_roundtrip_and_actual_temporal_palette(self):
  for mode in MODES[8:12]:
   a,i,s=convert_image(self.image,Settings(mode=mode,dither='Ordered 4×4'))
   self.assertEqual(a.size,dimensions(s));s.validate()
   f=frame_pixels(i,s.codes,s.line_codes,s.mode)
   self.assertEqual(len(f),2 if mode==MODES[11] else 3)
   p=target_palette(s);yy,xx=np.indices(i.shape)
   np.testing.assert_array_equal(blend(f),p[yy,xx,i])
   if mode==MODES[11]:
    self.assertFalse(np.array_equal(f[0],f[1]));self.assertEqual(len(s.line_codes[0]),11)
    self.assertTrue(np.all(f[0][[0,-1]]==0))
   else:np.testing.assert_array_equal(f[0],f[1])
   self.assertEqual(len(binary(i,s.codes,s.mode,s.line_codes)),cartridge_size(mode))
   with tempfile.TemporaryDirectory() as tmp:
    path=Path(tmp)/'settings.json';s.save(path)
    _,j,t=convert_image(self.image,Settings.load(path));np.testing.assert_array_equal(i,j)
    self.assertEqual(s,t)

 def test_sprites_dasm_parity_nonblack_background(self):
  dasm=os.environ.get('DASM_PATH')
  if not dasm:self.skipTest('DASM_PATH missing')
  rng=np.random.default_rng(671);i=np.where(rng.integers(0,2,(192,48)),0,7).astype(np.uint8)
  for mode in MODES[8:11]:
   rows=[]
   for y in range(192):
    fg=CODES[rng.integers(128)];other=fg if mode==MODES[8] else CODES[rng.integers(128)]
    rows.append((fg,other,fg,'22'))
   with tempfile.TemporaryDirectory() as tmp:
    tmp=Path(tmp);(tmp/'image.asm').write_text(assembly(i,rows[0],mode,rows),encoding='utf-8')
    result=subprocess.run([dasm,'image.asm','-f3','-oimage.bin'],cwd=tmp,capture_output=True)
    self.assertEqual(result.returncode,0,result.stdout)
    self.assertEqual((tmp/'image.bin').read_bytes(),binary(i,rows[0],mode,rows))

 def test_movie_stream_structure_and_rejection(self):
  from chrono.moviecart import binary as mvc
  _,i,s=convert_image(self.image,Settings(mode=MODES[11],dither='None'))
  b=mvc(i,s.line_codes,1);self.assertEqual(len(b),60*4096)
  for n in range(60):
   f=b[n*4096:(n+1)*4096];self.assertEqual(f[:4],b'MVC\0');self.assertEqual(int.from_bytes(f[4:7],'big'),n+2)
   self.assertEqual(f[7:269],bytes(262));self.assertEqual(f[7+262+960:7+262+960+60],bytes(60))
  with self.assertRaises(ValueError):assembly(i,s.codes,s.mode,s.line_codes)
  with self.assertRaises(ValueError):mvc(i,s.line_codes,0)
  with self.assertRaises(ValueError):mvc(i[:100],s.line_codes)
  bad=list(s.line_codes);bad[1]=bad[1][:-1]+('0E',)
  with self.assertRaises(ValueError):replace(s,line_codes=tuple(bad)).validate()

 def test_cancel_and_two_field_persistence(self):
  cancel=threading.Event();cancel.set()
  with self.assertRaises(Cancelled):search_palette(self.image,Settings(mode=MODES[11]),cancel=cancel)
  f=np.array([[[[200,0,0]]],[[[0,0,100]]]],dtype=np.uint8)
  p=persistence_frames(f,.5)
  np.testing.assert_array_equal(p[0,0,0],blend(f,weights=[2,1])[0,0]);np.testing.assert_array_equal(p[1,0,0],blend(f,weights=[1,2])[0,0])
