"""Check both sprite kernels against every predicted pixel and frame timing."""
from pathlib import Path
import subprocess,time,sys,re,json
import numpy as np
from PIL import Image
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from chrono.core import CODES,TIA
from chrono.sprite_rom import binary
for kind in sys.argv[2:] or ['4K','DPC+']:
 run=(Path('test-output/stella-sprites')/(kind+'-'+str(time.time_ns()))).resolve();run.mkdir(parents=True)
 a=np.where(np.random.default_rng(19).integers(0,2,(192,48)),0,7).astype(np.uint8);a[:,[0,-1]]=0;a[[0,-1],:]=0
 rows=[(f'{y//16%15+1:X}8',f'{(y//16+5)%15+1:X}A' if kind!='4K' else f'{y//16%15+1:X}8',f'{y//16%15+1:X}8','00') for y in range(192)]
 palette=bytes(TIA[[CODES.index(f'{i*2:02X}') for i in range(128)]].astype(np.uint8).ravel())
 (run/'stella.pal').write_bytes(palette+palette+bytes(24))
 rom=run/'sprites.bin';rom.write_bytes(binary(a,rows[0],rows,kind))
 (run/'autoexec.script').write_text('frame #12\nsaveSnap\nframe #1\nsaveSnap\nframe #1\nsaveSnap\nram $f0 _scanEnd\nram $f1 (_scanEnd/#256)\ndump $f0 $ff #1\n')
 with (run/'process.log').open('w') as log:
  proc=subprocess.Popen([sys.argv[1],'-basedir',str(run),'-userdir',str(run),'-snapsavedir',str(run),'-palette','user','-pal.gamma','0','-pal.brightness','0','-pal.contrast','0','-pal.saturation','0','-pal.hue','0','-debug','-fullscreen','0','-maxres','1400x1000','-format','NTSC','-type','CDF' if kind=='CDFJ+' else kind,str(rom)],stdout=log,stderr=log)
  try:
   end=time.monotonic()+20
   while time.monotonic()<end:
    if len(list(run.glob('*.png')))>=3 and list(run.glob('*.dump')):break
    if proc.poll() is not None:break
    time.sleep(.2)
  finally:
   if proc.poll() is None:proc.terminate()
   proc.wait(timeout=5)
 print('Evidence:',run)
 dumps=list(run.glob('*.dump'));assert dumps,'No debugger dump'
 v=re.search(r'f0:\s*([0-9a-f]{2})\s+([0-9a-f]{2})',dumps[0].read_text(),re.I)
 lines=int(v[1],16)+256*int(v[2],16);print('Scanlines:',lines)
 expected=np.empty((192,48,3))
 for y in range(192):
  for x in range(48):expected[y,x]=TIA[CODES.index(rows[y][3 if a[y,x]==7 else (x//8)%2])]
 expected=np.repeat(expected,2,axis=1);expected=np.clip((expected/255)**1.1333*256+.5,0,255).astype(np.uint8)
 shots=list(run.glob('*.png'));assert len(shots)==3
 for shot in shots:
  pixels=np.asarray(Image.open(shot).convert('RGB'));ys,xs=np.where(pixels.any(axis=2))
  bounds=[int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)];print('Bounds:',bounds)
  crop=pixels[bounds[1]:bounds[3],bounds[0]:bounds[2]]
  assert crop.shape==expected.shape,crop.shape
  delta=np.abs(crop.astype(int)-expected.astype(int));print('Max delta',delta.max())
  assert delta.max()<=2,('Pixel mismatch',np.argwhere(delta>2)[:8])
 assert lines==262,lines
 (run/'result.json').write_text(json.dumps({'scanlines':lines,'frames':3,'all_pixels_match':True,'mode':kind}))
