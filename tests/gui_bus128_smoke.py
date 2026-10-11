from pathlib import Path
import sys,time,tempfile
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from chrono.gui import App
from chrono.core import BUS128,MODES,mode_description
app=App();errors=[]
app.report_callback_exception=lambda *args:errors.append(str(args))
def wait():
 start=time.monotonic()
 while app.busy or app.after_preview or not app.result_current:
  app.update();time.sleep(.01)
  assert not errors,errors
  assert time.monotonic()-start<180,app.status.get()
 app.update();assert not errors,errors
try:
 wait();app.vars['mode'].set(BUS128);app.mode_changed();wait()
 assert app.result[1].shape==(200,128)
 assert tuple(app.combos['mode']['values'])[8]==mode_description(BUS128)
 assert app.result[2].codes==('0E','0E','0E','00')
 assert str(app.edit_palette_button['state'])=='normal'
 assert str(app.balance_check['state'])=='disabled'
 app.open_palette_picker(component=0);app.update();app.palette_picker.destroy()
 app.vars['code0'].set('AC');app.code_changed();wait()
 assert app.result[2].codes==('AC','AC','AC','00')
 app.vars['crop_zoom'].set(1.8);app.vars['scale'].set('Stretch');wait()
 assert app.result[2].crop_zoom==1.8 and app.result[2].codes[0]=='AC'
 app.vars['optimization_scope'].set('Colors only');app.scope_changed();app.optimize_button.invoke();wait()
 assert not app.result[2].line_codes
 app.vars['optimization_scope'].set('Image only');app.scope_changed();codes=app.result[2].codes
 app.optimize_button.invoke();wait();assert app.result[2].codes==codes
 app.show_animated_preview();app.update()
 assert len(app.animated_preview.frames)==2 and app.animated_preview.frames[0].shape==(200,128,3)
 app.animated_preview.close()
 with tempfile.TemporaryDirectory() as d:
  app.export_to(Path(d)/'export');assert (Path(d)/'export/image.bin').stat().st_size==32768
 app.vars['mode'].set(MODES[7]);app.mode_changed();wait();assert app.result[1].shape==(192,16)
 print('BUS modes: selector, palette picker, manual color, crop, optimization, preview and export passed')
finally:app.close()
