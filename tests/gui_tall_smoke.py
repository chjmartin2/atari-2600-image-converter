"""Exercise resolution selection, settings reload, previews, and portable exports."""
import sys,time,tempfile
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from chrono.gui import App
from chrono.core import MODES,cartridge_size
preferences_temp=tempfile.TemporaryDirectory()
preferences_patch=patch('chrono.preferences.preferences_path',return_value=Path(preferences_temp.name)/'preferences.json')
preferences_patch.start()
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
        for mode in MODES[1:4]:
            app.vars['mode'].set(mode);app.mode_changed();wait()
            assert app.height_controls.winfo_manager()
            for height in (192,128):
                combo=app.combos['height'];combo.current(1 if height==192 else 0)
                combo.event_generate('<<ComboboxSelected>>');wait()
                a,i,s=app.result
                assert a.size==(48,height) and i.shape==(height,48),(a.size,i.shape)
                assert s.height==height
                assert str(height) in app.mode_summary.get()
                if s.line_codes:assert len(s.line_codes)==height
                app.show_animated_preview();app.update()
                assert app.animated_preview.frames[0].shape==(height,48,3)
                app.animated_preview.close();app.update()
                folder=tmp/(mode+str(height));app.export_to(folder)
                assert (folder/'image.bin').stat().st_size==cartridge_size(s)
                with patch('chrono.gui.filedialog.askopenfilename',return_value=str(folder/'settings.json')):
                    app.load_settings();wait()
                assert app.result[2].height==height
        app.vars['height'].set(192)
        app.vars['mode'].set(MODES[0]);app.mode_changed();wait()
        assert not app.height_controls.winfo_manager()
        assert app.result[1].shape==(128,48)
        assert not errors,errors
        print('All three modes: 128/192 selector, animated preview, save/reload and ASM/BIN export passed; Classic unchanged.')
finally:
    app.close();preferences_patch.stop();preferences_temp.cleanup()
