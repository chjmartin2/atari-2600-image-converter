"""Verify the real BUS datastream raster, colors, bank seams and frame timing."""
from pathlib import Path
import subprocess,time,sys,re,json
import numpy as np
from PIL import Image
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from chrono.core import CODES,TIA
from chrono.bus_rom import binary
run=Path('test-output/stella-bus')/str(time.time_ns());run=run.resolve();run.mkdir(parents=True)
indices=np.random.default_rng(781).integers(0,128,(192,16),dtype=np.uint8)
# Avoid black so that crop bounds can be measured, including every bank seam.
indices[indices==0]=1
palette=bytes(TIA[[CODES.index(f'{i*2:02X}') for i in range(128)]].astype(np.uint8).ravel())
(run/'stella.pal').write_bytes(palette+palette+bytes(24))
rom=run/'bus.bin';rom.write_bytes(binary(indices))
(run/'autoexec.script').write_text('frame #12\nsaveSnap\nframe #1\nsaveSnap\nframe #1\nsaveSnap\nram $f0 _scanEnd\nram $f1 (_scanEnd/#256)\ndump $f0 $ff #1\n')
with (run/'process.log').open('w') as log:
    proc=subprocess.Popen([sys.argv[1],'-basedir',str(run),'-userdir',str(run),'-snapsavedir',str(run),'-palette','user','-pal.gamma','0','-pal.brightness','0','-pal.contrast','0','-pal.saturation','0','-pal.hue','0','-debug','-fullscreen','0','-maxres','1400x1000','-format','NTSC','-type','BUS',str(rom)],stdout=log,stderr=log)
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
assert lines==262,lines
expected=np.repeat(TIA[indices],18,axis=1)
expected=np.clip((expected/255)**np.float32(1.1333)*256+.5,0,255).astype(np.uint8)
shots=list(run.glob('*.png'));assert len(shots)==3
for shot in shots:
    a=np.asarray(Image.open(shot).convert('RGB'))
    ys,xs=np.where(a.any(axis=2));bounds=[int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)]
    print('Bounds:',bounds)
    crop=a[bounds[1]:bounds[3],bounds[0]:bounds[2]]
    assert crop.shape==(192,288,3),crop.shape
    delta=np.abs(crop.astype(int)-expected.astype(int))
    assert delta.max()<=2,('Colors or positions mismatch',int(delta.max()),np.argwhere(delta>2)[:8])
(run/'result.json').write_text(json.dumps({'scanlines':lines,'frames':3,'all_pixels_match':True,'mode':'BUS2','logical_size':[16,192],'bounds':bounds},indent=2))
print('BUS: 262 lines; 3 static frames; all 3072 color samples and bank seams match.')
