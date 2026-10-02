"""Exercise the application event loop and real GUI callbacks on a desktop."""
import sys,time,tempfile
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from chrono.gui import App,sample_image
from chrono.core import PRESETS,Settings

app=App()
errors=[]
app.report_callback_exception=lambda *args:errors.append(str(args))
def wait():
    start=time.monotonic()
    while app.busy or app.after_preview or app.result is None:
        app.update();time.sleep(.03)
        assert time.monotonic()-start<90,app.status.get()
    app.update()
try:
    wait()
    for width,height in ((1000,700),(1320,850)):
        app.geometry(f'{width}x{height}');app.update()
        for child in app.winfo_children():
            if hasattr(child,'winfo_children'):
                for button in child.winfo_children():
                    if getattr(button,'cget',None) and button.winfo_class()=='TButton' and 'Export ASM' in button.cget('text'):
                        assert button.winfo_rooty()+button.winfo_height()<=app.winfo_rooty()+app.winfo_height(),'Export controls fall below window'
    with tempfile.TemporaryDirectory() as temp:
        temp=Path(temp)
        sample_image().save(temp/'input.png');app.open_image(temp/'input.png');wait()
        for name in PRESETS:
            app.vars['preset'].set(name);app.preset_changed();wait()
        app.vars['brightness'].set(.85);wait()
        app.vars['dither'].set('Ordered 4×4');app.changed();wait()
        app.convert(True);wait()
        for view in ('Temporal blend','Quantization targets','Frame 1','Frame 2','Frame 3'):
            app.view.set(view);app.zoom.set('200%');app.smooth.set(True);app.show_result();app.update()
        app.export_to(temp/'export')
        assert (temp/'export'/'image.bin').stat().st_size==4096
        assert 'processor 6502' in (temp/'export'/'image.asm').read_text()
        settings=Settings.load(temp/'export'/'settings.json');app._sync_vars(settings);app.changed();wait()
        app.reset_adjustments();wait()
        assert not errors,errors
        print('GUI smoke passed: import, presets, adjustments, dither, optimization, five views, zoom, export, settings, reset')
finally:app.close()
