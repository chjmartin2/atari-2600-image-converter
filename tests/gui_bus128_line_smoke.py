from pathlib import Path
import sys,time,tempfile
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from chrono.gui import App
from chrono.core import BUS128LINE,BUS128,MODES,Settings,mode_description
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
 wait();app.vars['mode'].set(BUS128LINE);app.mode_changed();wait()
 assert tuple(app.combos['mode']['values'])[9]==mode_description(BUS128LINE)
 assert app.result[1].shape==(200,128) and len(app.result[2].line_codes)==200
 assert str(app.edit_palette_button['state'])=='disabled'
 assert str(app.balance_check['state'])=='disabled'
 assert app.row_controls.winfo_manager() and int(app.row_spinner['to'])==199
 rows=app.result[2].line_codes
 app.inspect_row.set(199);app.draw_swatches();app.update()
 assert any('Foreground' in app.swatches.itemcget(i,'text') for i in app.swatches.find_all() if app.swatches.type(i)=='text')
 app.vars['crop_zoom'].set(1.8);app.vars['scale'].set('Stretch');wait()
 assert app.result[2].line_codes==rows and app.result[2].crop_zoom==1.8
 app.vars['background'].set('Any Atari color')
 app.vars['optimization_scope'].set('Colors only');app.scope_changed();app.optimize_button.invoke();wait()
 rows=app.result[2].line_codes;assert len({r[3] for r in rows})==1
 app.vars['optimization_scope'].set('Image only');app.scope_changed();app.optimize_button.invoke();wait()
 assert app.result[2].line_codes==rows
 for view in ('Temporal blend','Quantization targets','Frame 1','Frame 2'):
  app.view.set(view);app.show_result();app.update();assert not errors,errors
 app.show_animated_preview();app.update()
 assert len(app.animated_preview.frames)==2 and app.animated_preview.frames[0].shape==(200,128,3)
 app.animated_preview.close()
 with tempfile.TemporaryDirectory() as d:
  folder=Path(d)/'export';app.export_to(folder);assert (folder/'image.bin').stat().st_size==32768
  assert Settings.load(folder/'settings.json').line_codes==rows
 app.vars['mode'].set(BUS128);app.mode_changed();wait();assert not app.result[2].line_codes
 app.vars['mode'].set(MODES[7]);app.mode_changed();wait();assert app.result[1].shape==(192,16)
 print('BUS per-line GUI: selector, row inspection, crop, any-background search, image-only preservation, rendering and export passed')
finally:app.close()
