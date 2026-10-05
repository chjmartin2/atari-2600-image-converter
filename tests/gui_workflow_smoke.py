"""Real Tk controls: scopes, crop zoom, fixed palettes, comparison and cancellation."""
import sys,time,threading,tempfile
from dataclasses import replace
from pathlib import Path
from unittest.mock import patch
import numpy as np
from PIL import Image
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from chrono.gui import App
from chrono.core import Settings,MODES,prepare

app=App();errors=[]
app.report_callback_exception=lambda *args:errors.append(str(args))
def wait():
    start=time.monotonic()
    while app.busy or app.after_preview or not app.result_current:
        app.update();time.sleep(.01)
        assert time.monotonic()-start<120,app.status.get()
    app.update()
def choose(scope,effort='Standard'):
    app.vars['optimization_scope'].set(scope);app.vars['search_effort'].set(effort)
    app.scope_changed();app.optimize_button.invoke();wait()
release=threading.Event()
try:
    wait()
    for size in ('1000x700','1320x850'):
        app.geometry(size);app.update()
        for widget in (app.export_button,app.optimize_button,app.undo_button,app.combos['optimization_scope']):
            assert widget.winfo_rooty()+widget.winfo_height()<=app.winfo_rooty()+app.winfo_height()
            assert widget.winfo_rootx()+widget.winfo_width()<=app.winfo_rootx()+app.winfo_width()
        assert app.input_preview.canvas.winfo_height()>100
        assert abs(app.input_preview.canvas.winfo_height()-app.output_preview.canvas.winfo_height())<3
    original=app.result
    choose('Image only')
    assert app.result[2].codes==original[2].codes
    assert app.before_result is not None
    app.compare_before.set(True);app.show_result()
    np.testing.assert_array_equal(app.input_preview.image,original[0])
    app.undo_button.invoke();wait()
    np.testing.assert_array_equal(app.result[1],original[1])
    assert app.result[2].brightness==original[2].brightness
    tone=tuple(getattr(app.result[2],n) for n in ('brightness','contrast','red','green','blue'))
    choose('Colors only')
    assert tone==tuple(getattr(app.result[2],n) for n in ('brightness','contrast','red','green','blue'))
    choose('Image + colors')
    assert app.before_result is not None
    app.vars['preset'].set('Grayscale');app.preset_changed();wait()
    assert app.vars['optimization_scope'].get()=='Image only'
    picker=app.open_palette_picker(0);picker.buttons['4E'].invoke();picker.apply();wait()
    assert app.vars['optimization_scope'].get()=='Image only' and app.result[2].codes[0]=='4E'
    assert app.swatches.find_withtag('component0')
    for mode in (MODES[0],MODES[2],MODES[4],MODES[7],MODES[11],MODES[13]):
        app.vars['mode'].set(mode);app.mode_changed();wait()
        assert str(app.edit_palette_button.cget('state'))==('normal' if mode==MODES[2] else 'disabled')
        if mode in (MODES[0],MODES[7]):assert app.vars['optimization_scope'].get()=='Image only'
        if app.result[2].line_codes:
            rows=app.result[2].line_codes
            app.vars['brightness'].set(.85);wait()
            # Phase balancing can permute equivalent assignments in temporal modes;
            # a static row palette must be exactly unchanged.
            if mode==MODES[4]:assert app.result[2].line_codes==rows
            app.inspect_row.set(0);app.draw_swatches();app.update()
        if mode==MODES[11]:
            rows=app.result[2].line_codes;choose('Image only');assert app.result[2].line_codes==rows
    # Use distinct source quadrants so drag tests must alter real output pixels.
    a=np.zeros((240,640,3),np.uint8);a[:120,:320]=[255,0,0];a[:120,320:]=[0,255,0]
    a[120:,:320]=[0,0,255];a[120:,320:]=[255,255,0]
    app.reset_all_options();wait()
    with tempfile.TemporaryDirectory() as tmp:
        image=Path(tmp)/'quadrants.png';Image.fromarray(a).save(image);app.open_image(image);wait()
        app.vars['scale'].set('Stretch');app.vars['crop_zoom'].set(2);wait()
        before=np.array(app.result[0]);canvas=app.input_preview.canvas
        x0,y0,x1,y1=app.input_preview.image_bounds;x,y=int((x0+x1)/2),int((y0+y1)/2)
        canvas.event_generate('<ButtonPress-1>',x=x,y=y)
        canvas.event_generate('<B1-Motion>',x=x+50,y=y+30)
        canvas.event_generate('<ButtonRelease-1>',x=x+50,y=y+30);wait()
        assert app.result[2].crop_x<.5 and app.result[2].crop_y<.5
        assert not np.array_equal(before,app.result[0])
        crop=tuple(getattr(app.result[2],n) for n in ('crop_x','crop_y','crop_zoom','scale'))
        choose('Image only')
        assert crop==tuple(getattr(app.result[2],n) for n in ('crop_x','crop_y','crop_zoom','scale'))
        export=Path(tmp)/'export';app.export_to(export)
        saved=Settings.load(export/'settings.json');assert saved.crop_zoom==2
        assert saved.crop_x==app.result[2].crop_x and (export/'image.bin').stat().st_size==4096
        np.testing.assert_array_equal(app.result[0],prepare(app.source,saved))
        app.input_view.set('Original input');app.show_result()
        np.testing.assert_array_equal(app.input_preview.image,app.source)
        app.input_view.set('Adjusted input');app.show_result()
        app.reset_crop();wait();assert app.result[2].crop_zoom==1
        assert (app.result[2].crop_x,app.result[2].crop_y)==(.5,.5)
    # Editing during a search cancels it. It must not silently rerun optimization.
    started=threading.Event()
    def blocked_fit(image,s,*args,**kwargs):
        started.set();assert release.wait(5);return replace(s,brightness=.1)
    with patch('chrono.gui.fit_controls',side_effect=blocked_fit) as fit:
        app.vars['optimization_scope'].set('Image only');app.start_optimization()
        assert started.wait(5)
        app.vars['contrast'].set(.93);release.set();wait()
        assert fit.call_count==1 and app.result[2].contrast==.93
        assert app.result[2].brightness!=.1
    # Reset while work is pending cannot apply a stale result afterwards.
    started.clear();release.clear()
    with patch('chrono.gui.fit_controls',side_effect=blocked_fit):
        app.start_optimization();assert started.wait(5)
        app.reset_all_options();release.set();wait()
    assert app.result[2]==Settings(),app.result[2]
    assert not errors,errors
    print('Workflow GUI passed: scopes, fixed palettes, comparison/undo, modes, actual Stretch crop drag, settings/export, edit cancellation and reset.')
finally:
    release.set();app.close()
