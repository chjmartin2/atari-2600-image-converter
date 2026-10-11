import sys,time,tempfile
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from chrono.gui import App
from chrono.core import MODES
from chrono.modes import search_palette
prefs=tempfile.TemporaryDirectory()
with patch('chrono.preferences.preferences_path',return_value=Path(prefs.name)/'preferences.json'):
 app=App();errors=[];messages=[]
 app.report_callback_exception=lambda *args:errors.append(str(args))
 def wait():
  start=time.monotonic()
  while app.busy or app.after_preview or app.result is None:
   app.update();messages.append(app.status.get());time.sleep(.01)
   assert time.monotonic()-start<120,app.status.get()
  app.update()
 try:
  wait()
  with patch('chrono.modes.search_palette',side_effect=AssertionError('mode selection searched')):
   start=time.monotonic();app.vars['mode'].set(MODES[3]);app.mode_changed();wait()
   print('Select per-line mode:',round(time.monotonic()-start,2),'s',flush=True)
   assert len(app.result[2].line_codes)==128
   app.vars['height'].set(192);app.resolution_changed();wait()
   assert len(app.result[2].line_codes)==192
  assert 'Starts with the current palette' in app.palette_help.get()
  app.vars['optimization_scope'].set('Colors only');app.scope_changed()
  with patch('chrono.gui.search_palette',wraps=search_palette) as explicit:
   app.start_optimization();wait();assert explicit.call_count==1
  rows=app.result[2].line_codes
  assert len(rows)==192 and len(set(tuple(sorted(r[:3])) for r in rows))>1
  assert any('Fitting scanline colors:' in m for m in messages)
  with patch('chrono.modes.search_palette',side_effect=AssertionError('image edit searched')):
   app.vars['brightness'].set(.7);wait()
  assert [sorted(r[:3]) for r in rows]==[sorted(r[:3]) for r in app.result[2].line_codes]
  assert not errors,errors
  print('Fast mode/resolution changes, explicit row search/progress and retained colors passed')
 finally:app.close()
prefs.cleanup()
