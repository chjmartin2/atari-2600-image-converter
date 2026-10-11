from dataclasses import replace
from pathlib import Path
import tempfile,threading,unittest
from unittest.mock import patch
import numpy as np
from PIL import Image
from chrono.core import Settings,MODES,Cancelled,prepare
from chrono.modes import convert_image,render,search_palette

class LineInitializationTests(unittest.TestCase):
    def setUp(self):
        y,x=np.indices((192,48))
        self.image=Image.fromarray(np.stack((x*5,y,(x*3+y)//2),axis=2).astype(np.uint8))

    def test_mode_selection_never_searches_and_preserves_visible_colors(self):
        for height in (128,192):
            base=Settings(mode=MODES[1],height=height,dither='Floyd–Steinberg',brightness=.7,contrast=1.2)
            _,old,original=convert_image(self.image,base)
            with patch('chrono.modes.search_palette',side_effect=AssertionError('automatic color search')):
                _,indices,s=convert_image(self.image,replace(base,mode=MODES[3]))
            self.assertEqual(len(s.line_codes),height)
            self.assertEqual(s.brightness,.7);self.assertEqual(s.contrast,1.2)
            self.assertTrue(all(sorted(r[:3])==sorted(base.codes[:3]) and r[3]==base.codes[3] for r in s.line_codes))
            np.testing.assert_allclose(render(indices,s),render(old,original),atol=1)

    def test_saved_row_colors_are_loaded_without_search(self):
        rows=tuple((('46','C6','84','00') if y<64 else ('2C','AE','68','00')) for y in range(128))
        s=Settings(mode=MODES[3],line_codes=rows,balance_frames=False,dither='None')
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'settings.json';s.save(path)
            with patch('chrono.modes.search_palette',side_effect=AssertionError('automatic color search')):
                _,_,loaded=convert_image(self.image,Settings.load(path))
            self.assertEqual(loaded.line_codes,rows)

    def test_explicit_color_search_still_fits_rows_and_reports_progress(self):
        # A short input exercises the real search; GUI passes the full 128/192 rows.
        image=Image.new('RGB',(48,2));image.paste((220,15,30),(0,0,48,1));image.paste((10,180,100),(0,1,48,2))
        progress=[];s=Settings(mode=MODES[3])
        result=search_palette(image,s,lambda p,t:progress.append((p,t)))
        self.assertEqual(len(result.line_codes),2)
        self.assertNotEqual(result.line_codes[0],result.line_codes[1])
        self.assertTrue(progress)
        stop=threading.Event();stop.set()
        with self.assertRaises(Cancelled):convert_image(self.image,s,stop)
