"""Exercise the application event loop and real GUI callbacks on a desktop."""
import sys,time,tempfile
from unittest.mock import patch
from pathlib import Path
from PIL import Image
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
    assert app.vars['search'].get()=='Improved weighted'
    assert app.vars['background'].get()=='Black'
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
        # Exercise missing/install guidance and manual selection without launching
        # a real emulator or writing the user's machine preferences.
        with patch('chrono.gui.stella_path',return_value=None),patch('chrono.gui.messagebox.askyesno',return_value=False) as prompt,patch('chrono.gui.filedialog.askopenfilename') as browse,patch('chrono.gui.subprocess.Popen') as launch:
            app.launch_stella();prompt.assert_called_once();browse.assert_not_called();launch.assert_not_called()
            assert 'install Stella' in prompt.call_args.args[1]
        fake_stella=temp/'Stella.exe';fake_stella.write_bytes(b'test placeholder')
        with patch('chrono.preferences.preferences_path',return_value=temp/'preferences.json'),patch.dict('os.environ',{'PROGRAMFILES':str(temp/'absent'),'PROGRAMFILES(X86)':str(temp/'absent32')}),patch('chrono.gui.messagebox.askyesno',return_value=True) as prompt,patch('chrono.gui.filedialog.askopenfilename',return_value=str(fake_stella)) as browse,patch('chrono.gui.subprocess.Popen') as launch,patch('chrono.gui.tempfile.mkdtemp',return_value=str(temp)):
            app.launch_stella();app.launch_stella()
            prompt.assert_called_once();browse.assert_called_once()
            assert launch.call_count==2
            assert launch.call_args.args[0]==[str(fake_stella.resolve()),'-format','NTSC','-type','4K',str(temp/'preview.bin')]
            assert (temp/'preview.bin').stat().st_size==4096
            with patch('chrono.gui.messagebox.showerror') as error:
                launch.side_effect=OSError('Cannot start emulator')
                app.launch_stella();error.assert_called_once()
        for name in PRESETS:
            app.vars['preset'].set(name);app.preset_changed();wait()
        app.vars['brightness'].set(.85);wait()
        app.vars['dither'].set('Ordered 4×4');app.changed();wait()
        app.vars['search'].set('Improved weighted')
        app.convert(True);wait()
        app.vars['optimization_scope'].set('Image only');app.start_optimization();wait()
        from chrono.core import prepare
        import numpy as np
        np.testing.assert_array_equal(app.result[0],prepare(app.source,app.result[2]))
        assert app.before_result is not None
        frozen=app.result[0].copy();frozen_indices=app.result[1].copy()
        app.compare_before.set(True);app.show_result();app.compare_before.set(False);app.show_result()
        np.testing.assert_array_equal(frozen,app.result[0]);np.testing.assert_array_equal(frozen_indices,app.result[1])
        app.vars['preset'].set('Grayscale');app.preset_changed();wait()
        assert app.vars['optimization_scope'].get()=='Image only'
        # Real swatch click opens the picker; cancel preserves the live palette.
        for width in (1000,1320):
            app.geometry(f'{width}x850');app.update()
            assert app.swatches.bbox('component3')[2]<=app.swatches.winfo_width()+1
        before=app.read_settings().codes
        bounds=app.swatches.bbox('component0')
        app.swatches.event_generate('<Button-1>',x=(bounds[0]+bounds[2])//2,y=35);app.update()
        picker=app.palette_picker
        picker.buttons['4E'].invoke();picker.destroy();app.update()
        assert app.read_settings().codes==before
        picker=app.open_palette_picker(0);picker.buttons['4E'].invoke();picker.apply();wait()
        assert app.result[2].codes[0]=='4E' and app.result[2].mapping=='Temporal blend'
        picker=app.open_palette_picker(output=7)
        assert picker.component.get()==3
        picker.buttons['08'].invoke();picker.apply();wait()
        assert app.result[2].codes[3]=='08'
        assert app.vars['preset'].get()=='Custom / optimized'
        app.show_animated_preview();app.update()
        animation=app.animated_preview
        assert animation.winfo_exists() and len(animation.photos)==3
        assert animation.persistence.get()==.6
        animation.toggle();app.update();assert not animation.clock.running
        old=animation.clock.number(time.perf_counter())
        animation.step();app.update();assert animation.clock.number(time.perf_counter())==old+1
        animation.rate.set('Slow motion (10 fps)');animation.change_rate()
        assert animation.clock.rate==10
        animation.persistence.set(.5);animation.change_persistence();animation.rebuild();app.update()
        animation.geometry('540x510');app.update();animation.rebuild()
        assert animation.canvas.winfo_height()>20
        animation.toggle()
        until=time.monotonic()+.35
        while time.monotonic()<until:app.update();time.sleep(.01)
        assert animation.clock.number(time.perf_counter())>old+1
        app.show_animated_preview();assert app.animated_preview is animation
        animation.close();app.update();assert animation.job is None and animation.resize_job is None
        app.show_animated_preview();app.update();assert app.animated_preview is not animation
        app.animated_preview.close();app.update()
        for view in ('Temporal blend','Quantization targets','Frame 1','Frame 2','Frame 3'):
            app.view.set(view);app.zoom.set('200%');app.smooth.set(True);app.show_result();app.update()
        app.export_to(temp/'export')
        assert (temp/'export'/'image.bin').stat().st_size==4096
        assert 'processor 6502' in (temp/'export'/'image.asm').read_text()
        settings=Settings.load(temp/'export'/'settings.json');app._sync_vars(settings);app.changed();wait()
        app.reset_adjustments();wait()
        # Exercise the actual mouse bindings, including immediate input refresh.
        app.source=Image.new('RGB',(800,200),'orange')
        app.vars['scale'].set('Fill / crop');app.zoom.set('Fit');app.changed();wait()
        app.show_result();app.update()
        canvas=app.input_preview.canvas
        x0,y0,x1,y1=app.input_preview.image_bounds
        x,y=int((x0+x1)/2),int((y0+y1)/2)
        canvas.event_generate('<ButtonPress-1>',x=x,y=y)
        canvas.event_generate('<B1-Motion>',x=x+50,y=y)
        canvas.event_generate('<ButtonRelease-1>',x=x+50,y=y)
        wait()
        assert app.vars['crop_x'].get()<.5
        assert app.result[2].crop_x==app.vars['crop_x'].get()
        app.center_crop();wait();assert app.vars['crop_x'].get()==.5
        app.source=Image.new('RGB',(48,128),'black')
        app.vars['search'].set('Legacy exhaustive');app.vars['background'].set('Any Atari color')
        app.vars['gamma'].set(1);app.changed();wait()
        app.convert(True);wait()
        assert app.result[2].background=='Any Atari color'
        assert app.vars['background'].get()=='Any Atari color'
        assert not errors,errors
        print('GUI smoke passed: visible input fitting, explicit scopes, comparison, swatch picker apply/cancel, layout, import, animation, crop, export, settings')
finally:app.close()
