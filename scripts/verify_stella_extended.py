"""Isolated Stella captures: compare raster pixels and field timing for new modes."""
from pathlib import Path
import subprocess,time,sys,re,json
import numpy as np
from PIL import Image
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from chrono.core import CODES,TIA,MODES,frame_pixels,cartridge_type,Settings,dimensions
from chrono.rom import binary,assembly

def fixture(n,positions=(56,104),colored=False):
    mode=MODES[n];w,h=dimensions(Settings(mode=mode));rng=np.random.default_rng(319)
    a=rng.integers(0,2,(h,w),dtype=np.uint8)
    rows=[(f'{y//16%15+1:X}8',)*3+(('02' if y%2 else '62') if colored else '00',) for y in range(h)]
    if n==17:
        a=np.repeat(a[:,:40],4,axis=1)
        for k,x in enumerate(positions):
            a[:,x:x+8]=np.where(rng.integers(0,2,(h,8)),k+2,a[:,x:x+8])
        rows=[(r[0],'0E','4C',r[3],*(f'{x:02X}' for x in positions)) for r in rows]
    a[:,[0,-1]]=1;a[[0,-1]]=1
    if n==17:a[:,:4]=1;a[:,-4:]=1
    return a,tuple(rows)

def verify(n,positions=(56,104),colored=False):
    mode=MODES[n];a,rows=fixture(n,positions,colored)
    run=(Path('test-output/stella-extended')/(str(n)+'-'+str(time.time_ns()))).resolve();run.mkdir(parents=True)
    palette=bytes(TIA[[CODES.index(f'{i*2:02X}') for i in range(128)]].astype(np.uint8).ravel())
    (run/'stella.pal').write_bytes(palette+palette+bytes(24));rom=run/'extended.bin'
    rom.write_bytes(binary(a,rows[0][:4],mode,rows));(run/'extended.asm').write_text(assembly(a,rows[0][:4],mode,rows))
    (run/'autoexec.script').write_text('frame #12\nsaveSnap\nram $e0 _scanEnd\nram $e1 (_scanEnd/#256)\nframe #1\nsaveSnap\nram $e2 _scanEnd\nram $e3 (_scanEnd/#256)\nframe #1\nsaveSnap\nram $e4 _scanEnd\nram $e5 (_scanEnd/#256)\ndump $e0 $ef #1\n')
    with (run/'process.log').open('w') as log:
        proc=subprocess.Popen([sys.argv[1],'-basedir',str(run),'-userdir',str(run),'-snapsavedir',str(run),'-palette','user','-pal.gamma','0','-pal.brightness','0','-pal.contrast','0','-pal.saturation','0','-pal.hue','0','-debug','-fullscreen','0','-maxres','1400x1000','-format','NTSC','-type',cartridge_type(mode),str(rom)],stdout=log,stderr=log)
        try:
            end=time.monotonic()+25
            while time.monotonic()<end:
                if len(list(run.glob('*.png')))>=3 and list(run.glob('*.dump')):break
                if proc.poll() is not None:break
                time.sleep(.2)
        finally:
            if proc.poll() is None:proc.terminate()
            proc.wait(timeout=5)
    print('Evidence:',run,flush=True)
    dump=next(run.glob('*.dump')).read_text();values=re.search(r'e0:\s*((?:[0-9a-f]{2}\s+){6})',dump,re.I)[1].split()
    lines=[int(values[k],16)+256*int(values[k+1],16) for k in (0,2,4)];print('Scanlines',lines,flush=True)
    raw=frame_pixels(a,rows[0][:4],rows,mode)
    if n==19:raw=[f[k::2] for k,f in enumerate(raw)]
    if n==18:
        bg=TIA[[CODES.index(r[3]) for r in rows]].astype(np.uint8)
        margin=np.repeat(bg[:,None,:],32,axis=1)
        raw=[np.concatenate((margin,f,margin),axis=1) for f in raw]
    expected=[np.clip((np.repeat(f,2,axis=1)/255)**1.1333*256+.5,0,255).astype(np.uint8) for f in raw]
    phases=[]
    for shot in sorted(run.glob('*.png')):
        p=np.asarray(Image.open(shot).convert('RGB'));ys,xs=np.where(p.any(axis=2))
        crop=p[ys.min():ys.max()+1] if n in (17,18) else p[ys.min():ys.max()+1,xs.min():xs.max()+1]
        print('bounds',(ys.min(),ys.max(),xs.min(),xs.max()),'shape',crop.shape,flush=True)
        assert crop.shape==expected[0].shape,(crop.shape,expected[0].shape)
        diffs=[np.abs(crop.astype(int)-f.astype(int)) for f in expected];phase=min(range(len(expected)),key=lambda k:diffs[k].sum());delta=diffs[phase]
        Image.fromarray(expected[phase]).save(run/('expected-'+shot.name))
        print('Phase',phase,'max error',delta.max(),'bad pixels',np.any(delta>2,axis=2).sum(),flush=True)
        assert delta.max()<=2,np.argwhere(delta>2)[:20]
        phases.append(phase)
    if n!=17:assert phases[0]!=phases[1] and phases[0]==phases[2],phases
    assert lines==[262]*3 if n!=19 else set(lines)=={262,263},lines
    (run/'result.json').write_text(json.dumps({'mode':mode,'frames':phases,'scanlines':lines,'all_pixels_match':True}))

if __name__=='__main__':
    for n in [int(v) for v in sys.argv[2:]] or [17,18,19]:verify(n)
    if not sys.argv[2:]:
        for positions in ((32,48),(63,97),(144,152)):verify(17,positions,True)
        verify(18,colored=True)
