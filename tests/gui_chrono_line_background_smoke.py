import sys,time,tempfile
from pathlib import Path
from unittest.mock import patch
import numpy as np
from PIL import Image
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from chrono.gui import App
from chrono.core import MODES,Settings,cartridge_type
from chrono.rom import binary
prefs=tempfile.TemporaryDirectory()
with patch('chrono.preferences.preferences_path',return_value=Path(prefs.name)/'preferences.json'):
 app=App();errors=[]
 app.report_callback_exception=lambda *args:errors.append(str(args))
 def wait():
  start=time.monotonic()
  while app.busy or app.after_preview or app.result is None:
   app.update();time.sleep(.01)
   assert time.monotonic()-start<180,app.status.get()
  app.update()
 try:
  wait();app.vars['mode'].set(MODES[3]);app.mode_changed();wait()
  assert 'Any color by line' in app.combos['background']['values']
  app.vars['background'].set('Any color by line');wait()
  app.vars['optimization_scope'].set('Colors only');app.scope_changed()
  app.start_optimization();wait()
  s=app.result[2];s.validate()
  assert s.background=='Any color by line'
  assert len({r[3] for r in s.line_codes})>1
  assert cartridge_type(s)=='EF'
  assert len(binary(app.result[1],s.codes,s.mode,s.line_codes))==65536
  with tempfile.TemporaryDirectory() as tmp:
   p=Path(tmp)/'settings.json';s.save(p);assert Settings.load(p)==s
  app.vars['height'].set(192);app.resolution_changed();wait()
  assert app.vars['background'].get()=='Any color by line'
  assert len(app.result[2].line_codes)==192
  app.vars['mode'].set(MODES[1]);app.mode_changed();wait()
  assert 'Any color by line' not in app.combos['background']['values']
  assert app.vars['background'].get()=='Black'
  assert not errors,errors
  print('Per-line background selector, actual optimization, EF export, saved settings, 192 rows and mode switching passed',flush=True)
 finally:app.close()
prefs.cleanup()
