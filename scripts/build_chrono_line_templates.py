"""Build driver-free EF templates and immediate operand patch locations."""
import sys,subprocess,tempfile,json,hashlib,re
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from chrono.core import DATA
from chrono.chrono_line_rom import assembly
for h in (128,192):
 with tempfile.TemporaryDirectory() as tmp:
  p=Path(tmp);(p/'image.asm').write_text(assembly(np.zeros((h,48),dtype=np.uint8),('00',)*4),encoding='utf-8')
  r=subprocess.run([sys.argv[1],'image.asm','-f3','-oimage.bin','-simage.sym'],cwd=p,capture_output=True,text=True)
  if r.returncode:raise RuntimeError(r.stdout+r.stderr)
  data=(p/'image.bin').read_bytes();assert len(data)==65536
  symbols={m[0]:int(m[1],16) for m in re.findall(r'^(\S+)\s+([0-9a-fA-F]{4,8})\s', (p/'image.sym').read_text(),re.M)}
  offsets=[]
  for group in range(4):
   group_offsets=[]
   for y in range(h):
    bank=4*group+y//(h//4)
    group_offsets.append([bank*4096+symbols[f'G{group}_{name}']-0xF000+1 for name in [f'FG{y}',f'BG{y}',*[f'P{y}_{k}' for k in range(6)]]])
   offsets.append(group_offsets)
  (DATA/f'chrono-line{h}.bin').write_bytes(data)
  (DATA/f'chrono-line{h}.json').write_text(json.dumps({'sha256':hashlib.sha256(data).hexdigest(),'offsets':offsets}),encoding='utf-8')
  print('Built Chronocolor',h,'rows')
