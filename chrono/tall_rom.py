"""48x192 basic modes: 4K static sprites or three interleaved F6 banks.

Reuse the verified single-scanline sprite kernel. All four banks have identical
code addresses; the fourth is a reset-safe copy of phase zero. No ARM driver.
"""
import hashlib
import json
import re
import numpy as np
from .core import BITS, DATA, MODES, Settings
from .sprite_rom import payload, assembly as sprite_assembly, binary as sprite_binary
from .twoframe_rom import _body


def parts(indices,codes,mode,rows=()):
    a=np.asarray(indices)
    if mode not in MODES[1:4] or a.shape!=(192,48) or not np.issubdtype(a.dtype,np.integer) or np.any((a<0)|(a>7)):
        raise ValueError('Tall raster requires 48x192 indices in the range 0-7')
    Settings(mode=mode,height=192,codes=tuple(codes),line_codes=tuple(rows)).validate()
    if mode==MODES[2]:
        if len(set(codes[:3]))!=1:raise ValueError('Two Color requires one foreground')
        # Duplicate foreground palette entries all mean the same static color.
        return [(np.where(a==7,7,0).astype(np.uint8),(tuple(codes),)*192)]
    rows=rows or (tuple(codes),)*192
    result=[]
    for phase in range(3):
        components=(np.arange(192)+phase)%3
        on=np.take_along_axis(BITS[a],np.broadcast_to(components[:,None,None],(192,48,1)),axis=2)[:,:,0]
        colors=tuple((r[k],)*3+(r[3],) for r,k in zip(rows,components))
        result.append((np.where(on,0,7).astype(np.uint8),colors))
    return result


def assembly(indices,codes,mode,rows=()):
    frames=parts(indices,codes,mode,rows)
    if mode==MODES[2]:
        a,r=frames[0]
        return sprite_assembly(a,r[0],r)
    out=['; 48x192 8 color modes: three actual NTSC phases, standard 16 KiB F6.']
    for bank,phase in enumerate((0,1,2,0)):
        a,r=frames[phase]
        source=_body(payload(a,r[0],r),'4K')
        if bank:source=source[source.index(' ORG $F000'):]
        next_bank=(phase+1)%3
        source=source.replace(' jmp Frame',' jmp $FF80')
        source=source.replace(' ORG $FFFA',f' ORG $FF80\n bit ${0xFFF6+next_bank:04X}\n jmp Frame\n ORG $FFFA')
        for label in ('Draw','Reset','Clear','Frame','Blank','Over','EndPicture'):
            source=re.sub(r'\b'+label+r'\b',label+str(bank),source)
        source=re.sub(r' ORG \$([A-F0-9]{4})',lambda m:f' ORG ${bank*4096+int(m[1],16)-0xF000:04X}\n RORG ${m[1]}',source)
        out.append(source.replace(' END\n',''))
    return '\n'.join(out)+'\n END\n'


def binary(indices,codes,mode,rows=()):
    frames=parts(indices,codes,mode,rows)
    if mode==MODES[2]:
        a,r=frames[0]
        return sprite_binary(a,r[0],r)
    result=bytearray((DATA/'chrono192.bin').read_bytes())
    meta=json.loads((DATA/'chrono192.json').read_text())
    if hashlib.sha256(result).hexdigest()!=meta['sha256']:
        raise ValueError('48x192 8 color modes template integrity failure')
    for bank,phase in enumerate((0,1,2,0)):
        a,r=frames[phase];data=payload(a,r[0],r)
        result[bank*4096:bank*4096+len(data)]=data
    return bytes(result)
