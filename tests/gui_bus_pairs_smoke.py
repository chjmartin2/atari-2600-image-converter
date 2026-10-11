from pathlib import Path
import sys,time,tempfile
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from chrono.gui import App
from chrono.core import BUS128LINE,BUS128,Settings
from chrono.bus128_pairs import distinct_rows
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
 before=app.result[2].line_codes
 assert app.bus_pair_controls.winfo_manager() and not app.vars['bus_pair_rows'].get()
 app.bus_pair_check.invoke();wait()
 assert app.result[2].bus_pair_rows and distinct_rows(app.result[2].line_codes)
 rows=app.result[2].line_codes
 app.inspect_row.set(1);app.draw_swatches();app.update()
 assert any('PAIR 0: ROWS 0–1' in app.swatches.itemcget(i,'text') for i in app.swatches.find_all() if app.swatches.type(i)=='text')
 app.vars['optimization_scope'].set('Image only');app.scope_changed();app.optimize_button.invoke();wait()
 assert app.result[2].line_codes==rows
 app.vars['optimization_scope'].set('Colors only');app.scope_changed();app.optimize_button.invoke();wait()
 assert distinct_rows(app.result[2].line_codes)
 app.show_animated_preview();app.update();assert len(app.animated_preview.frames)==2;app.animated_preview.close()
 with tempfile.TemporaryDirectory() as d:
  folder=Path(d)/'export';app.export_to(folder)
  saved=Settings.load(folder/'settings.json');assert saved.bus_pair_rows and distinct_rows(saved.line_codes)
  assert (folder/'image.bin').stat().st_size==32768
 app.bus_pair_check.invoke();wait();assert not app.result[2].bus_pair_rows
 app.vars['mode'].set(BUS128);app.mode_changed();wait();assert not app.bus_pair_controls.winfo_manager()
 app.reset_all_options();wait();assert not app.vars['bus_pair_rows'].get()
 print('Paired-row GUI: on/off, refit, row inspector, image-only preservation, search, preview, export and reset passed')
finally:app.close()
