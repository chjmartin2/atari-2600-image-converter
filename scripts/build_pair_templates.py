from pathlib import Path
import sys,subprocess,hashlib,json
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from chrono.core import MODES,DATA
from chrono.drivers import strip_template
from chrono.twoframe_rom import name,assembly
for mode in (MODES[12],*MODES[14:]):
 h=128 if mode==MODES[12] else 192
 source=assembly(np.zeros((h,48),dtype=np.uint8),('00',)*4,mode,(('00',)*8,)*h)
 stem=name(mode);(DATA/(stem+'.asm')).write_text(source,encoding='utf-8')
 r=subprocess.run([sys.argv[1],str(DATA/(stem+'.asm')),'-f3','-o'+str(DATA/(stem+'.bin'))],capture_output=True)
 if r.returncode:print(r.stdout.decode(errors='replace'));raise SystemExit(r.returncode)
 b=strip_template(stem,(DATA/(stem+'.bin')).read_bytes());(DATA/(stem+'.bin')).write_bytes(b);print(stem,len(b))
 (DATA/(stem+'.json')).write_text(json.dumps({'sha256':hashlib.sha256(b).hexdigest()}))
