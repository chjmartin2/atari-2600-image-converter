"""Pixel-compare the 192-row static/three-phase modes and measure NTSC timing."""
from pathlib import Path
import subprocess,time,sys,re,json
import numpy as np
from PIL import Image
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from chrono.core import CODES,TIA,MODES,frame_pixels,cartridge_type,Settings
from chrono.rom import binary
from chrono.temporal import interleave
from chrono.preferences import stella_path
for n in (1,2,3):
 mode=MODES[n];h=192
 run=(Path('test-output/stella-tall')/(str(n)+'-'+str(time.time_ns()))).resolve();run.mkdir(parents=True)
 rng=np.random.default_rng(92);a=rng.integers(0,8,(h,48),dtype=np.uint8);a[:,[0,-1]]=0;a[[0,-1]]=0
 codes=('42','C6','74','00') if n!=2 else ('0E','0E','0E','00')
 rows=tuple((f'{y//16%15+1:X}8',f'{(y//16+5)%15+1:X}A',f'{(y//16+9)%15+1:X}6','00') for y in range(h)) if n==3 else ()
 if n==2:a=np.where(a==7,7,0).astype(np.uint8)
 settings=Settings(mode=mode,height=192,codes=codes,line_codes=rows)
 palette=bytes(TIA[[CODES.index(f'{i*2:02X}') for i in range(128)]].astype(np.uint8).ravel())
 (run/'stella.pal').write_bytes(palette+palette+bytes(24));rom=run/'pair.bin';rom.write_bytes(binary(a,codes,mode,rows))
 (run/'autoexec.script').write_text('frame #12\nsaveSnap\nram $e0 _scanEnd\nram $e1 (_scanEnd/#256)\nframe #1\nsaveSnap\nram $e2 _scanEnd\nram $e3 (_scanEnd/#256)\nframe #1\nsaveSnap\nram $e4 _scanEnd\nram $e5 (_scanEnd/#256)\nframe #1\nsaveSnap\nram $e6 _scanEnd\nram $e7 (_scanEnd/#256)\ndump $e0 $ef #1\n')
 with (run/'process.log').open('w') as log:
  proc=subprocess.Popen([str(stella_path()),'-basedir',str(run),'-userdir',str(run),'-snapsavedir',str(run),'-palette','user','-pal.gamma','0','-pal.brightness','0','-pal.contrast','0','-pal.saturation','0','-pal.hue','0','-debug','-fullscreen','0','-maxres','1400x1000','-format','NTSC','-type',cartridge_type(settings),str(rom)],stdout=log,stderr=log)
  try:
   end=time.monotonic()+20
   while time.monotonic()<end:
    if len(list(run.glob('*.png')))>=4 and list(run.glob('*.dump')):break
    if proc.poll() is not None:break
    time.sleep(.2)
  finally:
   if proc.poll() is None:proc.terminate()
   proc.wait(timeout=5)
 print('Evidence:',run)
 dump=next(run.glob('*.dump')).read_text();values=re.search(r'e0:\s*((?:[0-9a-f]{2}\s+){8})',dump,re.I)[1].split();lines=[int(values[k],16)+256*int(values[k+1],16) for k in (0,2,4,6)];print('Scanlines',lines)
 expected=[np.clip((np.repeat(f,2,axis=1)/255)**1.1333*256+.5,0,255).astype(np.uint8) for f in frame_pixels(a,codes,rows,mode)]
 phases=[]
 for shot in sorted(run.glob('*.png')):
  p=np.asarray(Image.open(shot).convert('RGB'));ys,xs=np.where(p.any(axis=2));crop=p[ys.min():ys.max()+1,xs.min():xs.max()+1]
  assert crop.shape==expected[0].shape,(crop.shape,expected[0].shape)
  diffs=[np.abs(crop.astype(int)-f.astype(int)) for f in expected];phase=min(range(1 if n==2 else 3),key=lambda k:diffs[k].sum());delta=diffs[phase]
  print('Phase',phase,'max error',delta.max());assert delta.max()<=2,np.argwhere(delta>2)[:10];phases.append(phase)
 assert len(phases)==4 and phases[0]==phases[3],phases
 if n!=2:assert len(set(phases[:3]))==3,phases
 assert lines==[262]*4,lines
 (run/'result.json').write_text(json.dumps({'mode':mode,'frames':phases,'scanlines':lines,'all_pixels_match':True}))
