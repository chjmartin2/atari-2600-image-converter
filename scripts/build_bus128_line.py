"""Rebuild the driver-free per-line BUS template using a local DASM executable."""
import sys,subprocess,hashlib,json,re,tempfile
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from chrono.core import DATA
from chrono.bus128_line_rom import assembly
from chrono.drivers import strip_template

with tempfile.TemporaryDirectory() as folder:
 p=Path(folder);(p/'image.asm').write_text(assembly(np.zeros((200,128),np.uint8),('0E',)*3+('00',)),encoding='utf-8')
 r=subprocess.run([sys.argv[1],'image.asm','-f3','-oimage.bin','-simage.sym'],cwd=p,capture_output=True,text=True)
 if r.returncode:raise RuntimeError(r.stdout+r.stderr)
 b=strip_template('bus128-line',(p/'image.bin').read_bytes());assert len(b)==32768 and not any(b[:2048])
 symbols=(p/'image.sym').read_text()
 meta={'sha256':hashlib.sha256(b).hexdigest(),'Background':int(re.search(r'^Background\s+([0-9a-fA-F]+)',symbols,re.M)[1],16)-0x8000}
 (DATA/'bus128-line.bin').write_bytes(b);(DATA/'bus128-line.json').write_text(json.dumps(meta,indent=2)+'\n')
 print('BUS 128 Color per Line: driver-free template built',meta)
