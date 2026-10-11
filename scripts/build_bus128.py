"""Build a driver-free BUS 128 template; DASM is a development dependency only."""
import sys,subprocess,hashlib,json,re,tempfile
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from chrono.core import DATA
from chrono.bus128_rom import assembly
from chrono.drivers import strip_template

with tempfile.TemporaryDirectory() as folder:
 p=Path(folder);(p/'image.asm').write_text(assembly(np.zeros((200,128),np.uint8),('0E','0E','0E','00')),encoding='utf-8')
 r=subprocess.run([sys.argv[1],'image.asm','-f3','-oimage.bin','-simage.sym'],cwd=p,capture_output=True,text=True)
 if r.returncode:raise RuntimeError(r.stdout+r.stderr)
 b=strip_template('bus128',(p/'image.bin').read_bytes());assert len(b)==32768 and not any(b[:2048])
 symbols=(p/'image.sym').read_text()
 meta={'sha256':hashlib.sha256(b).hexdigest()}
 for label in ('Foreground','Background'):
  meta[label]=int(re.search(r'^'+label+r'\s+([0-9a-fA-F]+)',symbols,re.M)[1],16)-0x8000
 (DATA/'bus128.bin').write_bytes(b);(DATA/'bus128.json').write_text(json.dumps(meta,indent=2)+'\n')
 print('BUS 128: driver-free template built',meta)
