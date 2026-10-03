"""Rebuild the experimental BUS template using DASM_PATH or a supplied path."""
from pathlib import Path
import sys,os,subprocess,hashlib,json
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from chrono.bus_rom import assembly
from chrono.core import DATA
from chrono.drivers import strip_template
p=DATA/'bus-raster'
p.with_suffix('.asm').write_text(assembly(np.zeros((192,16),np.uint8)),encoding='utf-8')
r=subprocess.run([sys.argv[1] if len(sys.argv)>1 else os.environ['DASM_PATH'],str(p.with_suffix('.asm')),'-f3','-o'+str(p.with_suffix('.bin'))],capture_output=True,text=True)
if r.returncode:raise RuntimeError(r.stdout+r.stderr)
b=strip_template('bus-raster',p.with_suffix('.bin').read_bytes());assert len(b)==32768
p.with_suffix('.bin').write_bytes(b)
p.with_suffix('.json').write_text(json.dumps({'sha256':hashlib.sha256(b).hexdigest()},indent=2),encoding='utf-8')
print('BUS template rebuilt: 32768 bytes')
