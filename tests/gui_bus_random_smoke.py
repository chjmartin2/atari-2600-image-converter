from pathlib import Path
import sys,time,tempfile
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from chrono.gui import App
from chrono.core import BUS128LINE,CODES,TIA,Settings
app=App();errors=[]
app.report_callback_exception=lambda *args:errors.append(str(args))
def wait():
 start=time.monotonic()
 while app.busy or app.after_preview or not app.result_current:
  app.update();time.sleep(.01)
  assert not errors,errors
  assert time.monotonic()-start<240,app.status.get()
 app.update();assert not errors,errors
try:
 wait();app.vars['mode'].set(BUS128LINE);app.mode_changed();wait()
 app.random_rows_button.invoke();wait()
 rows=app.result[2].line_codes;bg=rows[0][3]
 assert app.result[2].preset=='Custom / random rows'
 assert app.vars['optimization_scope'].get()=='Image only'
 rgb=TIA[[CODES.index(r[0]) for r in rows]];assert np.all(np.any(rgb[1:]!=rgb[:-1],axis=1))
 app.vars['brightness'].set(.8);app.changed();wait();assert app.result[2].line_codes==rows
 app.vars['dither'].set('Ordered 4×4');app.changed();wait();assert app.result[2].line_codes==rows
 with tempfile.TemporaryDirectory() as d:
  folder=Path(d)/'export';app.export_to(folder);assert Settings.load(folder/'settings.json').line_codes==rows
 app.random_rows_button.invoke();wait();assert app.result[2].line_codes!=rows
 assert all(r[3]==bg for r in app.result[2].line_codes)
 app.vars['optimization_scope'].set('Colors only');app.scope_changed();app.optimize_button.invoke();wait()
 assert app.result[2].mode==BUS128LINE and app.result_current
 app.bus_pair_check.invoke();wait();app.random_rows_button.invoke();wait();app.result[2].validate()
 app.show_animated_preview();app.update();assert len(app.animated_preview.frames)==2;app.animated_preview.close()
 print('Random BUS GUI: random button, no adjacent matches, stability, reroll, saved export, dither-aware Optimize and paired mode passed')
finally:app.close()
