"""Exercise explicit Classic fitting through the mode selector and Optimize button."""
import sys,time,tempfile
from pathlib import Path
from unittest.mock import patch
from dataclasses import replace
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from chrono.gui import App
from chrono.core import MODES, mode_description

with tempfile.TemporaryDirectory() as temp, patch('chrono.preferences.preferences_path',return_value=Path(temp)/'prefs.json'):
    app=App();errors=[]
    app.report_callback_exception=lambda *args:errors.append(str(args))
    def wait():
        start=time.monotonic()
        while app.busy or app.after_preview or app.result is None or app.pending_action:
            app.update();time.sleep(.02)
            assert time.monotonic()-start<120,app.status.get()
        app.update()
    def select(mode):
        app.combos['mode'].set(mode_description(mode))
        app.combos['mode'].event_generate('<<ComboboxSelected>>')
        app.update()
    try:
        wait()
        app._sync_vars(replace(app.read_settings(),brightness=.9,dither='Ordered 4×4',contrast=.9,gamma=1.1,crop_zoom=1.2))
        app.changed();wait()
        before=app.read_settings()
        select(MODES[0]);wait()
        after=app.read_settings()
        assert after.mode==MODES[0] and app.before_result is None
        assert after.brightness==.9 and app.pending_action is None
        for name in ('contrast','gamma','crop_zoom','dither','strength','red','green','blue'):
            assert getattr(after,name)==getattr(before,name),name
        assert app.vars['brightness'].get()==app.result[2].brightness
        assert app.vars['optimization_scope'].get()=='Image only'
        app.optimize_button.invoke();wait()
        after=app.read_settings()
        assert after.brightness!=.9 and app.before_result is not None
        app.undo_optimization();app.update()
        assert app.vars['brightness'].get()==.9
        app.start_optimization();wait()
        assert app.vars['brightness'].get()==after.brightness
        app.vars['brightness'].set(.61);app.changed();wait()
        assert app.result[2].brightness==.61 and app.before_result is None
        # Rapid mode switching must keep the manual brightness without scheduling a fit.
        select(MODES[1]);select(MODES[0]);wait()
        assert app.result[2].mode==MODES[0] and app.before_result is None
        assert app.result[2].brightness==.61 and app.pending_action is None
        # Cancel/switch modes must discard the old Classic worker's result.
        app.start_optimization();select(MODES[1]);wait()
        assert app.result[2].mode==MODES[1]
        select(MODES[0]);app.cancel_conversion();wait()
        assert app.pending_action is None
        assert not errors,errors
        print('Classic GUI passed: no mode-selection search, explicit Optimize button, controls preserved, visible brightness, undo, manual override, mode switching and cancel.')
    finally:app.close()
