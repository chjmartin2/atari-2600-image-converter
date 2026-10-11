import sys,time,tempfile
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from chrono.gui import App
from chrono.core import MODES
pref=tempfile.TemporaryDirectory()
with patch('chrono.preferences.preferences_path',return_value=Path(pref.name)/'preferences.json'):
 app=App();errors=[]
 app.report_callback_exception=lambda *args:errors.append(str(args))
 def wait():
  start=time.monotonic()
  while app.busy or app.after_preview or app.result is None:
   app.update();time.sleep(.01)
   assert time.monotonic()-start<60,app.status.get()
  app.update()
 try:
  wait();app.vars['mode'].set(MODES[2]);app.mode_changed();wait()
  assert str(app.combos['search_effort'].cget('state'))=='disabled'
  for height in (128,192):
   app.vars['height'].set(height);app.resolution_changed();wait()
   for scope in ('Colors only','Image only','Image + colors'):
    app.vars['optimization_scope'].set(scope);app.scope_changed()
    before=app.read_settings();start=time.monotonic();app.start_optimization();wait()
    result=app.result[2]
    assert app.result_current and result.height==height
    assert result.codes[:3]==(result.codes[0],)*3
    if scope=='Colors only':assert result.brightness==before.brightness and result.contrast==before.contrast
    if scope=='Image only':assert result.codes==before.codes
    print(height,scope,round(time.monotonic()-start,2),'seconds',flush=True)
    assert app.before_result is not None
  app.vars['mode'].set(MODES[1]);app.mode_changed();wait()
  assert str(app.combos['search_effort'].cget('state'))=='readonly'
  assert not errors,errors
  print('Two Color GUI scopes, resolution choices, comparison, and mode isolation passed')
 finally:app.close()
pref.cleanup()
