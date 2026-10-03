"""Exercise overlapping optimization requests through the real Tk event loop."""
import sys,time,threading
from dataclasses import replace
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from chrono.gui import App

app=App();errors=[]
app.report_callback_exception=lambda *args:errors.append(str(args))

def wait():
    start=time.monotonic()
    while app.busy or app.after_preview:
        app.update();time.sleep(.01)
        assert time.monotonic()-start<20,app.status.get()
    app.update()

def widget(text):
    def walk(parent):
        for child in parent.winfo_children():
            if child.winfo_class() in ('TButton','TCheckbutton') and child.cget('text')==text:return child
            found=walk(child)
            if found:return found
    result=walk(app);assert result is not None,text
    return result

release=threading.Event()
try:
    wait()
    # Palette request queued during a conversion, then followed by a slider edit.
    with patch('chrono.gui.search_palette',side_effect=lambda im,s,*args:replace(s,codes=('4E','AE','6E','00'))) as search:
        app.busy=True
        widget('Optimize palette').invoke()
        app.vars['contrast'].set(.9)
        app.busy=False;wait()
        assert search.call_count==1,search.call_count
        assert app.result[2].codes==('4E','AE','6E','00')
    # Input fit underway when another control changes: discarded work must rerun.
    started=threading.Event()
    def fit(image,settings,*args,**kwargs):
        started.set();assert release.wait(5)
        return replace(settings,brightness=.45,contrast=.65)
    with patch('chrono.gui.fit_controls',side_effect=fit) as fitting:
        widget('Optimize input').invoke();app.convert()
        assert started.wait(5)
        app.vars['strength'].set(.8)
        release.set();wait()
        assert fitting.call_count==2,fitting.call_count
        assert app.result[2].brightness==.45
        assert app.result[2].strength==.8
        assert app.vars['brightness'].get()==.45
    # Disabling the option during a fit keeps the last displayed adjustments.
    widget('Optimize input').invoke();wait()
    started.clear();release.clear()
    with patch('chrono.gui.fit_controls',side_effect=fit) as fitting:
        widget('Optimize input').invoke();app.convert();assert started.wait(5)
        widget('Optimize input').invoke()
        release.set();wait()
        assert fitting.call_count==1
        assert not app.result[2].auto_input
        assert app.result[2].brightness==.45
    # Cancel clears queued search instead of launching it after cancellation.
    with patch('chrono.gui.search_palette') as search:
        app.busy=True;widget('Optimize palette').invoke();widget('Cancel').invoke()
        app.busy=False;app.update()
        assert not app.after_preview and not app.pending_palette_search
        search.assert_not_called()
    assert not errors,errors
    print('Optimization regression passed: queued palette search, interrupted input fit, toggle off, cancel')
finally:
    release.set();app.close()
