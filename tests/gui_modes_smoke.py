"""Exercise all twenty mode selections, global optimization, and portable exports."""
import sys,time,tempfile
from pathlib import Path
from unittest.mock import patch
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from chrono.gui import App
from chrono.core import MODES,Settings,frame_pixels,dimensions,cartridge_size,frame_count

app=App();errors=[]
app.report_callback_exception=lambda *args:errors.append(str(args))
def wait():
    start=time.monotonic()
    while app.busy or app.after_preview or app.result is None:
        app.update();time.sleep(.01)
        assert time.monotonic()-start<120,app.status.get()
    app.update()
try:
    wait()
    with tempfile.TemporaryDirectory() as tmp:
        tmp=Path(tmp)
        for n,mode in enumerate(MODES):
            app.vars['mode'].set(mode);app.mode_changed();wait()
            app.convert(True);wait()
            a,i,s=app.result
            assert s.mode==mode
            assert a.size==dimensions(s)
            app.show_animated_preview();app.update()
            assert app.animated_preview.frames[0].shape==(*i.shape,3)
            assert len(app.animated_preview.photos)==frame_count(mode)
            app.animated_preview.close();app.update()
            for view in ('Temporal blend','Quantization targets','Frame 2'):
                app.view.set(view);app.show_result();app.update()
            folder=tmp/str(n);app.export_to(folder)
            assert (folder/('image.mvc' if mode==MODES[11] else 'image.bin')).stat().st_size==cartridge_size(mode)
            with patch('chrono.gui.filedialog.askopenfilename',return_value=str(folder/'settings.json')):
                app.load_settings();wait()
            np.testing.assert_array_equal(i,app.result[1])
            assert app.result[2].line_codes==s.line_codes
            if mode in (MODES[2],*MODES[4:11]):
                frames=frame_pixels(i,s.codes,s.line_codes,s.mode)
                np.testing.assert_array_equal(frames[0],frames[1])
        # Global optimize and Stella routing also exercise the banked mode.
        app.vars['mode'].set(MODES[11]);app.mode_changed();wait()
        app.vars['optimization_scope'].set('Image only');app.start_optimization();wait()
        app.convert(True,True);wait()
        assert app.result[2].mode==MODES[11]
        with patch('chrono.gui.subprocess.Popen') as launch:
            app.launch_stella();assert launch.call_args.args[0][-2]=='MVC'
            assert launch.call_args.args[0][-1].endswith('.mvc')
        app.vars['mode'].set(MODES[7]);app.mode_changed();wait()
        app.convert(True,True);wait()
        assert app.result[2].mode==MODES[7]
        with patch('chrono.gui.subprocess.Popen') as launch:
            app.launch_stella()
            assert launch.call_args.args[0][-2]=='BUS'
        app.vars['mode'].set(MODES[1]);app.mode_changed();wait()
        app.convert(True,True);wait()
        assert len(np.unique(app.result[1]))>1
        assert not errors,errors
        print('All twenty GUI modes, row-palette settings reload, ASM/BIN and MVC exports, animation and Global optimize passed')
finally:app.close()
