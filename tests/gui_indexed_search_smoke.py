"""Exercise the actual Custom search and simplified controls through Tk."""
import sys,time,tempfile
from pathlib import Path
from dataclasses import asdict
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from chrono.gui import App
from chrono.core import SEARCHES,MODES

with tempfile.TemporaryDirectory() as folder,patch('chrono.preferences.preferences_path',return_value=Path(folder)/'preferences.json'):
    app=App();errors=[];pulses=set()
    app.report_callback_exception=lambda *args:errors.append(str(args))
    def wait():
        start=time.monotonic()
        while app.busy or app.after_preview or app.result is None or app.pending_action:
            app.update();time.sleep(.03)
            pulses.add(app.heartbeat_canvas.itemcget(app.heartbeat_canvas.find_withtag('heartbeat-logo')[0],'fill'))
            assert time.monotonic()-start<300,app.status.get()
        app.update()
    try:
        wait()
        assert 'search' not in app.combos
        assert not hasattr(app,'diversity_check')
        assert app.vars['search'].get()==SEARCHES[0]
        assert str(app.combos['background'].cget('state'))=='readonly'
        for background in ['Black','Any Atari color']:
            app.vars['background'].set(background);app.changed();wait()
            before=asdict(app.read_settings());start=time.monotonic()
            app.start_optimization();wait();after=asdict(app.read_settings())
            assert after['background']==background
            if background=='Black':assert app.result[2].codes[3]=='00'
            for key in before:
                if key not in ('codes','preset'):assert before[key]==after[key],key
            print(f'{background}: {time.monotonic()-start:.1f}s, {app.result[2].codes}',flush=True)
        assert len(pulses)>3 and not errors,errors
        app.start_optimization();app.cancel_conversion();wait()
        assert app.pending_action is None
        app.vars['mode'].set(MODES[2]);app.mode_changed();wait()
        assert str(app.combos['background'].cget('state'))=='readonly'
        print('PASS: single Custom search; black/any background; fixed inputs; responsive progress; cancellation; mode switching.',flush=True)
    finally:app.close()
