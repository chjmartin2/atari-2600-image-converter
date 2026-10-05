"""Developer-only: rebuild public F4/F8 templates with DASM and operand maps."""
import sys,subprocess,tempfile,json,hashlib,re
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from chrono.core import Settings,MODES,dimensions,DATA
from chrono.extended_rom import assembly,stem
for mode in MODES[17:20]:
    with tempfile.TemporaryDirectory() as tmp:
        tmp=Path(tmp);name=stem(mode)
        text=assembly(np.zeros(dimensions(Settings(mode=mode))[::-1],np.uint8),('00',)*4,mode)
        (tmp/'image.asm').write_text(text)
        r=subprocess.run([sys.argv[1],'image.asm','-f3','-oimage.bin','-simage.sym'],cwd=tmp,capture_output=True)
        if r.returncode:raise RuntimeError(r.stdout.decode()+r.stderr.decode())
        data=(tmp/'image.bin').read_bytes();offsets={}
        for match in re.finditer(r'^(P_(\d+)_\d+)\s+([0-9a-fA-F]+)',(tmp/'image.sym').read_text(),re.M):
            offsets[match[1]]=int(match[2])*4096+int(match[3],16)-0xF000
        (DATA/(name+'.bin')).write_bytes(data)
        (DATA/(name+'.json')).write_text(json.dumps({'sha256':hashlib.sha256(data).hexdigest(),'offsets':offsets},indent=2))
        (DATA/(name+'.asm')).write_text(text)
        print(name,len(data),len(offsets))
