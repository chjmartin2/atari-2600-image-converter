import sys,time
from pathlib import Path
import numpy as np
from PIL import Image
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from chrono.gui import App
from chrono.core import MODES,KERNELS
from chrono.modes import render
app=App();errors=[]
app.report_callback_exception=lambda *args:errors.append(str(args))
def wait():
    t=time.monotonic()
    while app.busy or app.after_preview or not app.result_current:
        app.update();time.sleep(.01);assert time.monotonic()-t<90,app.status.get()
    app.update()
try:
    wait();a=np.zeros((128,48,3),np.uint8)
    a[8:-8,6:-6]=np.random.default_rng(46).integers(0,256,(112,36,3),dtype=np.uint8)
    app.source=Image.fromarray(a)
    app.vars['mode'].set(MODES[0]);app.mode_changed()
    app.vars['scale'].set('Stretch');app.vars['resample'].set('Nearest');wait()
    app.adjust_input_to_palette();wait();assert app.vars['brightness'].get()==.47
    for method in KERNELS:
        app.vars['dither'].set(method);app.changed();wait()
        source,indices,s=app.result;black=np.all(np.asarray(source)==0,axis=2)
        assert black.any() and not render(indices,s)[black].any(),method
    app.show_animated_preview();app.update()
    for frame in app.animated_preview.frames:assert not frame[black].any()
    app.animated_preview.close();assert not errors,errors
    print('Dither GUI passed: all six diffusion choices retain black borders, Classic 0.47 remains, raw animation frames agree')
finally:app.close()
