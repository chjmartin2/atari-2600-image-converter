"""Drive all three extended modes through the actual optimization controls."""
from pathlib import Path
import sys,time,tempfile
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from chrono.gui import App
from chrono.core import MODES,dimensions,cartridge_size
app=App();errors=[]
app.report_callback_exception=lambda *args:errors.append(str(args))
def wait():
    start=time.monotonic()
    while app.busy or app.after_preview or not app.result_current:
        app.update();time.sleep(.01)
        assert time.monotonic()-start<120,app.status.get()
    app.update();assert not errors,errors
def optimize(scope):
    app.vars['optimization_scope'].set(scope);app.scope_changed();app.optimize_button.invoke();wait()
try:
    wait()
    with tempfile.TemporaryDirectory() as tmp:
        for mode in MODES[17:20]:
            app.vars['mode'].set(mode);app.mode_changed();wait()
            app.vars['crop_zoom'].set(1.7);app.vars['scale'].set('Stretch');wait()
            rows=app.result[2].line_codes
            optimize('Image only');assert app.result[2].line_codes==rows
            optimize('Image + colors')
            assert app.result[2].mode==mode and app.result[2].crop_zoom==1.7
            before=app.before_result
            app.compare_before.set(True);app.show_result();app.update()
            app.undo_button.invoke();wait();np.testing.assert_array_equal(app.result[1],before[1])
            app.show_animated_preview();app.update()
            assert app.animated_preview.frames[0].shape==(*dimensions(app.result[2])[::-1],3)
            app.animated_preview.close()
            folder=Path(tmp)/str(MODES.index(mode));app.export_to(folder)
            assert (folder/'image.bin').stat().st_size==cartridge_size(mode)
            assert (folder/'mode.txt').read_text(encoding='utf-8').count('Hardware untested') or 'hardware untested' in (folder/'mode.txt').read_text(encoding='utf-8') or 'Experimental' in (folder/'mode.txt').read_text(encoding='utf-8')
            print(mode,'GUI optimization, comparison, crop, preview, export passed',flush=True)
finally:app.close()
