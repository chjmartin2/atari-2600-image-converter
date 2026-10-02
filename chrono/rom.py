"""Unmodified legacy NTSC kernel; ROM patching verified against DASM assembly."""
import hashlib
import json
import re
from pathlib import Path
import numpy as np
from .core import DATA, BITS, CODES

def bank_bytes(indices):
    indices = np.asarray(indices)
    if indices.shape != (128,48) or not np.issubdtype(indices.dtype,np.integer) or np.any(indices < 0) or np.any(indices > 7):
        raise ValueError("The cartridge requires 48×128 indices in the range 0–7")
    out = bytearray()
    for f in range(3):
        for strip in range(6):
            for y in range(127,-1,-1):
                bits = BITS[indices[y,strip*8:strip*8+8],(y+f)%3]
                out.append(int(bits @ np.array([128,64,32,16,8,4,2,1])))
    for start in (12,6,0): out.extend([24,0,*range(start,start+6)])
    return bytes(out)

def assembly(indices, codes):
    if len(codes) != 4 or any(c not in CODES for c in codes): raise ValueError("Invalid NTSC codes")
    data = bank_bytes(indices)
    lines = ["; Generated image data: three frames, six strips, 128 rows bottom-up"]
    for i in range(0,2304,16): lines.append(" .byte " + ",".join(f"${b:02X}" for b in data[i:i+16]))
    for n,label in enumerate(("BLUE_png_0","GREEN_png_1","RED_png_2")):
        lines += [f"FRAME_{label}", " .byte " + ",".join(str(b) for b in data[2304+n*8:2312+n*8])]
    source = (DATA/"kernel.asm").read_text()
    source = re.sub(r'^\s*include\s+"Bank00.asm".*$', "\n".join(lines),source,flags=re.I|re.M)
    source = re.sub(r'^\s*include\s+"Bank_Frametable.asm".*$',lambda m:(DATA/"frametable.asm").read_text(),source,flags=re.I|re.M)
    for name,code in zip(("NTSC_RED","NTSC_GREEN","NTSC_BLUE","BGCOL"),codes):
        source = re.sub(rf'^{name}\s*=.*$',f"{name} = ${code}",source,flags=re.M)
    return "; Chrono2 Studio. NTSC / 4KB. Retain the acknowledgements below.\n"+source

def binary(indices,codes):
    if len(codes) != 4 or any(c not in CODES for c in codes): raise ValueError("Invalid NTSC codes")
    meta = json.loads((DATA/"kernel-patches.json").read_text())
    template = (DATA/"kernel.bin").read_bytes()
    if hashlib.sha256(template).hexdigest() != meta["sha256"]:
        raise ValueError("The bundled ROM template failed its integrity check")
    result = bytearray(template)
    result[:2328] = bank_bytes(indices)
    for code,positions in zip(codes,meta["colorOffsets"]):
        for pos in positions: result[pos] = int(code,16)
    if len(result) != 4096: raise ValueError("Invalid cartridge size")
    return bytes(result)
