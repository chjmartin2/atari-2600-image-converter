"""Build independent raster templates with DASM; then run parity/Stella checks."""
import sys,subprocess,json,hashlib,tempfile
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from chrono.core import DATA
from chrono.raster_rom import assembly

with tempfile.TemporaryDirectory() as tmp:
    tmp=Path(tmp)
    for pf in (False,True):
        name='raster40' if pf else 'raster48'
        a=np.full((192,40) if pf else (128,48),7,np.uint8)
        source=assembly(a,('00',)*4,playfield=pf)
        (tmp/'image.asm').write_text(source)
        result=subprocess.run([sys.argv[1],'image.asm','-f3','-oimage.bin','-simage.sym','-limage.lst'],cwd=tmp,capture_output=True,text=True)
        if result.returncode:raise RuntimeError(result.stdout+result.stderr)
        data=(tmp/'image.bin').read_bytes();assert len(data)==4096
        (DATA/(name+'.asm')).write_text(source)
        (DATA/(name+'.bin')).write_bytes(data)
        (DATA/(name+'.json')).write_text(json.dumps({'sha256':hashlib.sha256(data).hexdigest()},indent=2))
        print(name,len(data),result.stdout.strip())

    from chrono.playfield_plus import assembly as plus
    name='playfield-plus'
    source=plus(np.full((192,40),7,np.uint8),[('00',)*4]*192)
    (tmp/'image.asm').write_text(source,encoding='utf-8')
    result=subprocess.run([sys.argv[1],'image.asm','-f3','-oimage.bin','-simage.sym','-limage.lst'],cwd=tmp,capture_output=True,text=True)
    if result.returncode:raise RuntimeError(result.stdout+result.stderr)
    data=(tmp/'image.bin').read_bytes();assert len(data)==16384
    (DATA/(name+'.asm')).write_text(source,encoding='utf-8')
    (DATA/(name+'.bin')).write_bytes(data)
    (DATA/(name+'.json')).write_text(json.dumps({'sha256':hashlib.sha256(data).hexdigest()},indent=2),encoding='utf-8')
    print(name,len(data),result.stdout.strip())
