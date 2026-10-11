"""Standalone setup and reproducible packaged-application smoke check."""
from pathlib import Path
import json,queue,threading,time,traceback

def setup_window():
    import tkinter as tk
    from tkinter import ttk
    from .drivers import SPECS,load,download,support_directory
    root=tk.Tk();root.title('Atari cartridge support');root.geometry('580x220')
    status=tk.StringVar(value='BUS, DPC+ and CDFJ+ support is downloaded from the original sources.\nInternet access is needed once. Other modes work without this setup.')
    ttk.Label(root,textvariable=status,wraplength=540,padding=20).pack(fill='x')
    events=queue.Queue()
    def work():
        try:
            for name in SPECS:
                try:load(name);continue
                except (ValueError,OSError):pass
                events.put((False,'Downloading and verifying '+name+'…'))
                data=download(name);directory=support_directory();directory.mkdir(parents=True,exist_ok=True)
                path=directory/(name+'-driver.bin');temp=path.with_suffix('.tmp')
                temp.write_bytes(data);temp.replace(path)
            events.put((True,'Cartridge support is ready. You can close this window.'))
        except Exception as exc:events.put((True,'Setup failed: '+str(exc)+'\nCheck your connection and try again.'))
    def poll():
        try:
            while True:
                done,text=events.get_nowait();status.set(text)
                if done:button.config(state='normal')
        except queue.Empty:pass
        root.after(100,poll)
    def start():
        button.config(state='disabled');threading.Thread(target=work,daemon=True).start()
    button=ttk.Button(root,text='Download cartridge support',command=start);button.pack(pady=8)
    ttk.Button(root,text='Close',command=root.destroy).pack();poll();root.mainloop()

def self_test(folder):
    """Run without a system Python installation; never download drivers here."""
    import numpy as np
    from PIL import Image
    from . import __version__
    from .core import Settings,MODES,DATA
    from .gui import App,sample_image
    from .modes import convert_image,render
    from .rom import binary,assembly
    from .web_preview import export_animation
    folder=Path(folder);folder.mkdir(parents=True,exist_ok=True)
    result={'version':__version__,'modes':[]};app=None
    try:
        for name in ('ADVANCED-MODES.md','BUS-RESEARCH.md'):
            assert (Path(__file__).resolve().parents[1]/name).is_file(),name
        sample=sample_image();sample.save(folder/'input.png')
        for n,mode in enumerate(MODES):
            _,indices,s=convert_image(sample,Settings(mode=mode,dither='None'))
            Image.fromarray(render(indices,s)).save(folder/f'mode-{n}.png')
            export_animation(folder/f'mode-{n}.webp',indices,s,long_edge=320)
            entry={'mode':mode}
            try:
                data=binary(indices,s.codes,mode,s.line_codes)
                (folder/f'mode-{n}.bin').write_bytes(data);entry['bytes']=len(data)
                if n!=11:assert assembly(indices,s.codes,mode,s.line_codes)
            except ValueError as exc:
                if 'Cartridge support missing' not in str(exc):raise
                entry['optional_support']='not installed; clear setup guidance verified'
            result['modes'].append(entry)
        app=App(str(folder/'input.png'));errors=[]
        app.report_callback_exception=lambda *args:errors.append(str(args))
        deadline=time.monotonic()+90
        while app.busy or app.after_preview or app.result is None:
            app.update();time.sleep(.03)
            assert time.monotonic()<deadline,'GUI conversion timed out'
        app.show_animated_preview();app.update()
        assert app.animated_preview.winfo_exists()
        assert not errors,errors
        result['gui']='image import, default conversion and rendering window passed'
        result['status']='passed'
    except Exception:
        result['status']='failed';result['error']=traceback.format_exc()
        raise
    finally:
        if app is not None:app.close()
        (folder/'self-test.json').write_text(json.dumps(result,indent=2),encoding='utf-8')


def palette_self_test(path):
    """Focused packaging check: no GUI, downloads, or runtime catalog generation."""
    import numpy as np
    from .indexed_search import get_catalog
    from .core import _mixtures,_mixtures_direct
    from .palette_store import DIRECTORY
    from .weighted_search import blend_cube
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    result={'resource_directory':str(DIRECTORY)}
    try:
        start=time.perf_counter();catalog=get_catalog()
        result['load_seconds']=time.perf_counter()-start
        assert isinstance(catalog.rgb,np.memmap) and not catalog.rgb.flags.writeable
        assert get_catalog() is catalog
        assert blend_cube(catalog) is catalog.blend_cube
        codes=np.random.default_rng(44).integers(0,128,(256,4))
        np.testing.assert_array_equal(_mixtures(codes),_mixtures_direct(codes))
        result.update(status='passed',mixed_colors=len(catalog.rgb),triples=len(catalog.triples))
    except Exception:
        result.update(status='failed',error=traceback.format_exc())
        raise
    finally:path.write_text(json.dumps(result,indent=2),encoding='utf-8')
