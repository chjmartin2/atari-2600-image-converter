"""Check exported BUS 128 frames against the preview, including timing/colors."""
from pathlib import Path
import sys,subprocess,time,re,json
import numpy as np
from PIL import Image
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from chrono.core import CODES,TIA,BUS128,frame_pixels
from chrono.rom import binary

def verify(codes):
 run=(Path('test-output/stella-bus128')/str(time.time_ns())).resolve();run.mkdir(parents=True)
 a=np.random.default_rng(991).integers(0,2,(200,128),dtype=np.uint8)
 a[[0,-1]]=1;a[:,[0,-1]]=1
 palette=bytes(TIA[[CODES.index(f'{i*2:02X}') for i in range(128)]].astype(np.uint8).ravel())
 (run/'stella.pal').write_bytes(palette+palette+bytes(24));rom=run/'image.bin';rom.write_bytes(binary(a,codes,BUS128))
 (run/'autoexec.script').write_text('frame #12\nsaveSnap\nram $e0 _scanEnd\nram $e1 (_scanEnd/#256)\nframe #1\nsaveSnap\nram $e2 _scanEnd\nram $e3 (_scanEnd/#256)\nframe #1\nsaveSnap\nram $e4 _scanEnd\nram $e5 (_scanEnd/#256)\ndump $e0 $ef #1\n')
 with (run/'process.log').open('w') as log:
  proc=subprocess.Popen([sys.argv[1],'-basedir',str(run),'-userdir',str(run),'-snapsavedir',str(run),'-palette','user','-pal.gamma','0','-pal.brightness','0','-pal.contrast','0','-pal.saturation','0','-pal.hue','0','-debug','-fullscreen','0','-maxres','1400x1000','-format','NTSC','-type','BUS',str(rom)],stdout=log,stderr=log)
  try:
   end=time.monotonic()+25
   while time.monotonic()<end:
    if len(list(run.glob('*.png')))>=3 and list(run.glob('*.dump')):break
    if proc.poll() is not None:break
    time.sleep(.2)
  finally:
   if proc.poll() is None:proc.terminate()
   proc.wait(timeout=5)
 dump=next(run.glob('*.dump')).read_text();v=re.search(r'e0:\s*((?:[0-9a-f]{2}\s+){6})',dump,re.I)[1].split()
 lines=[int(v[k],16)+256*int(v[k+1],16) for k in (0,2,4)];assert lines==[262]*3,lines
 raw=frame_pixels(a,codes,(),BUS128)
 expected=[np.clip((np.repeat(f,2,axis=1)/255)**1.1333*256+.5,0,255).astype(np.uint8) for f in raw]
 phases=[];shots=sorted(run.glob('*.png'));assert len(shots)==3
 for shot in shots:
  p=np.asarray(Image.open(shot).convert('RGB'))
  # The original positioning centers 128 color clocks at x16..143.
  crop=p[14:214,32:288];assert crop.shape==(200,256,3)
  errors=[np.abs(crop.astype(int)-f.astype(int)) for f in expected]
  phase=min(range(2),key=lambda k:errors[k].sum());assert errors[phase].max()<=2,(shot,errors[phase].max())
  phases.append(phase)
 assert phases[0]!=phases[1] and phases[0]==phases[2],phases
 evidence={'mode':BUS128,'codes':codes,'scanlines':lines,'phases':phases,'all_pixels_match':True,'logical_size':[128,200]}
 (run/'result.json').write_text(json.dumps(evidence,indent=2));print(run,evidence,flush=True)

if __name__=='__main__':
 verify(('0E',)*3+('00',))
 verify(('AC',)*3+('22',))
