"""Capture the MovieCart stream and compare its two fields with the preview."""
from pathlib import Path
import subprocess,time,sys,re,json
import numpy as np
from PIL import Image
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from chrono.core import CODES,TIA
from chrono.moviecart import binary,frames
run=(Path('test-output/stella-movie')/str(time.time_ns())).resolve();run.mkdir(parents=True)
rng=np.random.default_rng(70)
a=np.where(rng.integers(0,2,(192,80)),0,7).astype(np.uint8)
rows=[tuple(f'{int(c):02X}' for c in rng.integers(1,128,11)*2) for y in range(192)]
rows[0]=rows[-1]=('00',)*11
rows[1]=rows[1][:-1]+('00',)
palette=bytes(TIA[[CODES.index(f'{i*2:02X}') for i in range(128)]].astype(np.uint8).ravel())
(run/'stella.pal').write_bytes(palette+palette+bytes(24))
rom=run/'movie.mvc';rom.write_bytes(binary(a,rows))
(run/'autoexec.script').write_text('frame #'+(sys.argv[2] if len(sys.argv)>2 else '700')+'\nsaveSnap\nram $f0 _scanEnd\nram $f1 (_scanEnd/#256)\ndump $f0 $ff #1\n')
with (run/'process.log').open('w') as log:
 proc=subprocess.Popen([sys.argv[1],'-basedir',str(run),'-userdir',str(run),'-snapsavedir',str(run),'-palette','user','-pal.gamma','0','-pal.brightness','0','-pal.contrast','0','-pal.saturation','0','-pal.hue','0','-debug','-fullscreen','0','-maxres','1400x1000','-format','NTSC','-type','MVC',str(rom)],stdout=log,stderr=log)
 try:
  end=time.monotonic()+25
  while time.monotonic()<end:
   if len(list(run.glob('*.png')))>=1 and list(run.glob('*.dump')):break
   if proc.poll() is not None:break
   time.sleep(.2)
 finally:
  if proc.poll() is None:proc.terminate()
  proc.wait(timeout=5)
print('Evidence:',run)
v=re.search(r'f0:\s*([0-9a-f]{2})\s+([0-9a-f]{2})',next(run.glob('*.dump')).read_text(),re.I)
lines=int(v[1],16)+256*int(v[2],16);assert lines==262,lines
p=np.asarray(Image.open(next(run.glob('*.png'))).convert('RGB'))
# Fixed capture geometry from the reference kernel: centered 80 color clocks,
# 190 content rows surrounded by two deliberately blank safety rows.
crop=p[14:206,80:240]
expected=[np.clip((np.repeat(f,2,axis=1)/255)**1.1333*256+.5,0,255).astype(np.uint8) for f in frames(a,rows)]
deltas=[np.abs(crop.astype(int)-f.astype(int)) for f in expected]
winner=min(range(2),key=lambda k:deltas[k].sum());delta=deltas[winner]
print('Field',winner,'max delta',delta.max(),'mismatches',np.count_nonzero(delta>2))
assert delta.max()<=2,np.argwhere(delta>2)[:12]
(run/'result.json').write_text(json.dumps({'scanlines':lines,'field':winner,'all_pixels_match':True,'bounds':[80,14,240,206]}))
