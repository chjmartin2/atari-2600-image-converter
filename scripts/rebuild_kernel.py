"""Rebuild reproducibly: python scripts/rebuild_kernel.py path/to/dasm.exe"""
from pathlib import Path
import sys,tempfile,subprocess,json,hashlib
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from chrono.core import DATA
from chrono.rom import assembly

def main():
    dasm=Path(sys.argv[1]).resolve()
    with tempfile.TemporaryDirectory() as temp:
        temp=Path(temp)
        def build(codes):
            (temp/'image.asm').write_text(assembly(np.full((128,48),7,np.uint8),codes))
            run=subprocess.run([str(dasm),'image.asm','-f3','-oimage.bin'],cwd=temp,capture_output=True)
            if run.returncode:raise RuntimeError(run.stdout+run.stderr)
            data=(temp/'image.bin').read_bytes()
            if len(data)!=4096:raise ValueError('Kernel is not 4 KB')
            return data
        base=build(('00',)*4);offsets=[]
        for axis in range(4):
            codes=['00']*4;codes[axis]='FE';changed=build(codes)
            positions=[i for i,(a,b) in enumerate(zip(base,changed)) if a!=b]
            if not positions or any(i<2328 or base[i]!=0 or changed[i]!=254 for i in positions):raise ValueError('Unexpected kernel layout')
            offsets.append(positions)
        (DATA/'kernel.bin').write_bytes(base)
        (DATA/'kernel-patches.json').write_text(json.dumps({'sha256':hashlib.sha256(base).hexdigest(),'colorOffsets':offsets},indent=2))
        print('Rebuilt kernel. Run assembler parity tests before committing.')

if __name__=='__main__':main()
