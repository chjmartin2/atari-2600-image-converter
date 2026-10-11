"""Rebuild the driver-free F6 template with an explicitly supplied DASM path."""
from pathlib import Path
import hashlib,json,subprocess,sys,tempfile
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from chrono.core import DATA,MODES
from chrono.tall_rom import assembly
with tempfile.TemporaryDirectory() as tmp:
    folder=Path(tmp)
    (folder/'image.asm').write_text(assembly(np.zeros((192,48),dtype=np.uint8),('00',)*4,MODES[1]),encoding='utf-8')
    result=subprocess.run([sys.argv[1],'image.asm','-f3','-oimage.bin'],cwd=folder,capture_output=True)
    if result.returncode:raise RuntimeError(result.stdout.decode(errors='replace'))
    data=(folder/'image.bin').read_bytes()
    assert len(data)==16384
    (DATA/'chrono192.bin').write_bytes(data)
    (DATA/'chrono192.json').write_text(json.dumps({'sha256':hashlib.sha256(data).hexdigest()}),encoding='utf-8')
    print('Built 16 KiB F6 template')
