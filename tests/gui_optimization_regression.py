"""Explicit actions never restart after edits, and cancellation preserves results."""
import sys,time,threading
from dataclasses import replace
from pathlib import Path
from unittest.mock import patch
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from chrono.gui import App
app=App();errors=[];release=threading.Event()
app.report_callback_exception=lambda *args:errors.append(str(args))
def wait():
    start=time.monotonic()
    while app.busy or app.after_preview:
        app.update();time.sleep(.01)
        assert time.monotonic()-start<30,app.status.get()
    app.update()
try:
    wait();original=app.result
    started=threading.Event()
    def fit(image,s,*args,**kwargs):
        started.set();assert release.wait(5)
        return replace(s,brightness=.25,contrast=.65)
    with patch('chrono.gui.fit_controls',side_effect=fit) as fitting:
        app.adjust_input_to_palette();assert started.wait(5)
        app.cancel_conversion();release.set();wait()
        assert fitting.call_count==1 and app.result is original
        assert app.result_current
    started.clear();release.clear()
    with patch('chrono.gui.fit_controls',side_effect=fit) as fitting:
        app.adjust_input_to_palette();assert started.wait(5)
        app.vars['strength'].set(.8);release.set();wait()
        assert fitting.call_count==1
        assert app.result[2].strength==.8 and app.result[2].brightness==original[2].brightness
    # A queued explicit request can be cancelled before its worker starts.
    with patch('chrono.gui.search_palette') as search:
        app.busy=True;app.vars['optimization_scope'].set('Colors only');app.start_optimization()
        app.cancel_conversion();app.busy=False;app.update()
        assert not app.after_preview and app.pending_action is None
        search.assert_not_called()
    assert not errors,errors
    print('Optimization regression passed: explicit scopes, edit cancels without restart, cancellation retains previous result, queued cancellation')
finally:
    release.set();app.close()
