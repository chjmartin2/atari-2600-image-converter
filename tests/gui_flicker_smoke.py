"""Real GUI actions: palette-preserving input fit and reset during a worker."""
import sys,time,threading
from dataclasses import replace
from pathlib import Path
from unittest.mock import patch
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from chrono.gui import App
from chrono.core import Settings,MODES,mode_description
app=App();errors=[]
app.report_callback_exception=lambda *args:errors.append(str(args))
def wait():
    start=time.monotonic()
    while app.busy or app.after_preview or app.result is None:
        app.update();time.sleep(.01)
        assert time.monotonic()-start<90,app.status.get()
    app.update()
def button(text,parent=None):
    for w in (parent or app).winfo_children():
        if w.winfo_class() in ('TButton','TCheckbutton') and w.cget('text')==text:return w
        found=button(text,w)
        if found:return found
release=threading.Event()
try:
    wait();assert app.vars['flicker_aware'].get()
    assert app.title().startswith('Atari 2600 Image Optimizer')
    assert all(v.endswith(('Static','Flicker')) for v in app.combos['mode'].cget('values'))
    app.combos['mode'].set(mode_description(MODES[13]));app.combos['mode'].event_generate('<<ComboboxSelected>>');wait()
    assert app.result[2].mode==MODES[13]
    app.vars['mode'].set(MODES[12]);app.mode_changed();wait()
    s=app.result[2];assert all(r[3]==r[7] for r in s.line_codes)
    assert s.line_codes[1]==s.line_codes[0][4:]+s.line_codes[0][:4]
    assert 'Alternating A/B scanlines' in app.mode_info.get()
    app.balance_check.invoke();wait()
    assert len(set(app.result[2].line_codes))==1
    app.balance_check.invoke();wait()
    s=app.result[2];assert s.line_codes[1]==s.line_codes[0][4:]+s.line_codes[0][:4]
    app.show_animated_preview();app.update();assert len(app.animated_preview.frames)==2
    app.animated_preview.close()
    app.vars['mode'].set(MODES[0]);app.mode_changed();wait()
    assert str(app.flicker_check.cget('state'))=='normal'
    assert 'brightness only' in app.scope_help.get().lower()
    app.vars['brightness'].set(.8);app.vars['contrast'].set(.8);app.vars['red'].set(.9);wait()
    before=app.result[2]
    app.adjust_input_to_palette();wait()
    after=app.result[2]
    for name in ('contrast','gamma','saturation','red','green','blue','sharpness','crop_zoom','codes'):
        assert getattr(before,name)==getattr(after,name),name
    assert after.brightness==.47 and app.vars['brightness'].get()==.47
    assert str(app.combos['search_effort'].cget('state'))=='disabled'
    app.reset_all_options();wait()
    app.vars['red'].set(.35);app.vars['green'].set(1.8);wait()
    original=app.result[2]
    app.adjust_input_to_palette();wait()
    fitted=app.result[2]
    assert not fitted.auto_input and fitted.codes==original.codes
    assert (fitted.red,fitted.green,fitted.blue)!=(original.red,original.green,original.blue)
    for name in ('brightness','contrast','gamma','saturation','red','green','blue'):
        assert app.vars[name].get()==getattr(fitted,name)
    app.vars['mode'].set(MODES[11]);app.mode_changed();wait()
    palette=app.result[2].line_codes
    app.adjust_input_to_palette();wait()
    assert app.result[2].line_codes==palette
    app.vars['mode'].set(MODES[8]);app.mode_changed();wait()
    assert str(app.flicker_check.cget('state'))=='disabled'
    app.show_animated_preview();app.update()
    assert len(app.animated_preview.frames)==1
    app.vars['mode'].set(MODES[15]);app.mode_changed();wait()
    assert str(app.flicker_check.cget('state'))=='normal'
    app.show_animated_preview();app.update()
    assert len(app.animated_preview.frames)==2
    assert 'Frame 3' not in app.output_combo.cget('values')
    source=app.source.copy();source_path=app.source_path
    started=threading.Event()
    def fit(image,s,*args,**kwargs):
        started.set();assert release.wait(5)
        return replace(s,brightness=.25,red=.2)
    with patch('chrono.gui.fit_controls',side_effect=fit):
        app.adjust_input_to_palette();app.convert();assert started.wait(5)
        button('Reset all options').invoke();release.set();wait()
    assert app.result[2]==Settings(),app.result[2]
    np.testing.assert_array_equal(app.source,source);assert app.source_path==source_path
    assert app.zoom.get()=='Fit' and not app.smooth.get()
    assert app.animated_preview is None
    assert app.pending_action is None
    assert not errors,errors
    print('Flicker GUI passed: standalone tone/RGB fitting, fixed row palettes, defaults, frame counts, reset during optimization')
finally:
    release.set();app.close()
