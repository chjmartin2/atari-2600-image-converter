import sys,time,tempfile
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from chrono.gui import App
from chrono.core import MODES
prefs=tempfile.TemporaryDirectory()
with patch('chrono.preferences.preferences_path',return_value=Path(prefs.name)/'preferences.json'):
 app=App();errors=[];messages=[]
 app.report_callback_exception=lambda *args:errors.append(str(args))
 def wait():
  start=time.monotonic()
  while app.busy or app.after_preview or app.result is None:
   app.update();messages.append(app.status.get());time.sleep(.01)
   assert time.monotonic()-start<240,app.status.get()
  app.update()
 try:
  wait();app.vars['mode'].set(MODES[4]);app.mode_changed();wait()
  assert tuple(app.combos['background']['values'])==('Black','White','Any Atari color','Per line')
  assert app.height_controls.winfo_manager()
  assert 'disabled' in app.combos['search_effort'].state()
  app.vars['height'].set(192);app.resolution_changed();wait()
  app.vars['dither'].set('Floyd–Steinberg');app.vars['background'].set('Per line');app.vars['optimization_scope'].set('Colors only');app.scope_changed();wait()
  app.start_optimization();wait()
  _,ix,s=app.result;assert ix.shape==(192,48) and len({r[3] for r in s.line_codes})>1
  assert any('all 8,256 pairs' in m for m in messages)
  from chrono.rom import binary
  assert len(binary(ix,s.codes,s.mode,s.line_codes))==16384
  for bg,code in [('White','0E'),('Black','00')]:
   app.vars['background'].set(bg);wait();app.start_optimization();wait()
   assert {r[3] for r in app.result[2].line_codes}=={code}
  app.vars['mode'].set(MODES[1]);app.mode_changed();wait()
  assert 'Per line' not in app.combos['background']['values']
  assert not errors,errors
  print('Scanline GUI: 192 rows, dither-aware optimization, all background constraints and cartridge export passed')
 finally:app.close()
prefs.cleanup()
