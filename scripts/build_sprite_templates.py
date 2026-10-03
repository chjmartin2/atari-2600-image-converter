from pathlib import Path
import sys,subprocess,json,hashlib
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from chrono.sprite_rom import assembly
from chrono.drivers import strip_template
p=Path('chrono/resources')
for name,kind in [('sprites48','4K'),('sprites-dpc','DPC+'),('sprites-cdfj','CDFJ+')]:
 (p/(name+'.asm')).write_text(assembly(np.zeros((192,48),dtype=np.uint8),('48','48','48','00'),kind=kind))
 subprocess.run([sys.argv[1],str(p/(name+'.asm')),'-f3','-o'+str(p/(name+'.bin'))],check=True,capture_output=True)
 (p/(name+'.bin')).write_bytes(strip_template(name,(p/(name+'.bin')).read_bytes()))
 (p/(name+'.json')).write_text(json.dumps({'sha256':hashlib.sha256((p/(name+'.bin')).read_bytes()).hexdigest()}))
