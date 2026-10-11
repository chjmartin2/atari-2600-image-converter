from dataclasses import replace
from pathlib import Path
import os,subprocess,tempfile,threading,unittest
from unittest.mock import patch
import numpy as np
from PIL import Image
from chrono.core import Settings,MODES,CODES,Cancelled,cartridge_type,cartridge_size,frame_pixels
from chrono.modes import search_palette,convert_image,render
from chrono.rom import assembly,binary
from chrono.chrono_line_rom import parts

class ChronoLineBackgroundTests(unittest.TestCase):
 def test_real_search_fits_background_per_row_without_global_search(self):
  im=Image.fromarray(np.random.default_rng(332).integers(0,256,(3,48,3),dtype=np.uint8))
  s=Settings(mode=MODES[3],background='Any color by line',brightness=.7)
  with patch('chrono.modes.optimize_legacy',side_effect=AssertionError('Must not pick one global background')):
   result=search_palette(im,s)
  self.assertGreater(len({r[3] for r in result.line_codes}),1)
  self.assertEqual(result.brightness,.7)
  black=search_palette(im,replace(s,background='Black'))
  self.assertEqual({r[3] for r in black.line_codes},{'00'})
  event=threading.Event();event.set()
  with self.assertRaises(Cancelled):search_palette(im,s,cancel=event)

 def test_validation_and_saved_settings_reproduce_preview(self):
  for h in (128,192):
   rows=tuple((CODES[y%128],'46','88',CODES[(y*11)%128]) for y in range(h))
   s=Settings(mode=MODES[3],height=h,background='Any color by line',line_codes=rows,balance_frames=False).validate()
   with tempfile.TemporaryDirectory() as tmp:
    p=Path(tmp)/'image.json';s.save(p);loaded=Settings.load(p)
   self.assertEqual(s,loaded)
   im=Image.new('RGB',(48,h),(104,83,49))
   with patch('chrono.modes.search_palette',side_effect=AssertionError('Do not search saved row palettes')):
    _,a,r=convert_image(im,loaded)
   self.assertEqual(r.line_codes,rows)
   self.assertEqual(cartridge_type(r),'EF');self.assertEqual(cartridge_size(r),65536)
   self.assertEqual(render(a,r).shape,(h,48,3))
  for mode in (MODES[1],MODES[4],MODES[8],MODES[21]):
   with self.assertRaises(ValueError):Settings(mode=mode,background='Any color by line').validate()

 def test_cartridge_phases_and_dasm_parity(self):
  for h in (128,192):
   rng=np.random.default_rng(h);a=rng.integers(0,8,(h,48),dtype=np.uint8)
   rows=tuple(tuple(CODES[c] for c in rng.integers(0,128,4)) for y in range(h))
   s=Settings(mode=MODES[3],height=h,background='Any color by line',codes=rows[0],line_codes=rows)
   frames=parts(a,s.codes,rows)
   for phase,(indices,colors) in enumerate(frames):
    np.testing.assert_array_equal(frame_pixels(indices,colors[0],colors,MODES[4])[0],frame_pixels(a,s.codes,rows,s.mode)[phase])
   rom=binary(a,s.codes,s.mode,rows);self.assertEqual(len(rom),cartridge_size(s))
   self.assertEqual(rom[-8:-4],b'EFEF')
   dasm=os.environ.get('DASM_PATH')
   if not dasm:self.skipTest('DASM_PATH missing')
   with tempfile.TemporaryDirectory() as tmp:
    p=Path(tmp);(p/'image.asm').write_text(assembly(a,s.codes,s.mode,rows),encoding='utf-8')
    r=subprocess.run([dasm,'image.asm','-f3','-oimage.bin'],cwd=p,capture_output=True)
    self.assertEqual(r.returncode,0,r.stdout)
    self.assertEqual((p/'image.bin').read_bytes(),rom)

 def test_uniform_background_retains_compact_existing_format(self):
  for h,size,kind in ((128,4096,'4K'),(192,16384,'F6')):
   rows=(('46','C6','84','00'),)*h
   s=Settings(mode=MODES[3],height=h,background='Any color by line',line_codes=rows)
   self.assertEqual(cartridge_type(s),kind)
   self.assertEqual(len(binary(np.zeros((h,48),dtype=np.uint8),s.codes,s.mode,rows)),size)
