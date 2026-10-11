"""Three-phase 8 color per line mode with independent row backgrounds, 64 KiB EF.

Reuse the cycle-verified unrolled static raster four banks per phase. The final
row switches straight into the next phase's EndPicture, preserving all 76
cycles. Banks 12-15 duplicate phase zero for reset safety. No ARM driver.
EF hotspots: https://github.com/stella-emu/stella/blob/master/src/emucore/CartEF.hxx
"""
import hashlib,json,re
import numpy as np
from .core import BITS,CODES,DATA,MODES,Settings
from .scanline_rom import assembly as static_assembly,values


def parts(indices,codes,rows=()):
    a=np.asarray(indices)
    if a.shape not in ((128,48),(192,48)) or not np.issubdtype(a.dtype,np.integer) or np.any((a<0)|(a>7)):
        raise ValueError('8 color per line raster requires 48x128 or 48x192 indices 0-7')
    h=len(a);rows=rows or (tuple(codes),)*h
    Settings(mode=MODES[3],height=h,codes=tuple(codes),line_codes=tuple(rows)).validate()
    result=[]
    for phase in range(3):
        components=(np.arange(h)+phase)%3
        on=np.take_along_axis(BITS[a],np.broadcast_to(components[:,None,None],(h,48,1)),axis=2)[:,:,0]
        colors=tuple((r[k],)*3+(r[3],) for r,k in zip(rows,components))
        result.append((np.where(on,0,7).astype(np.uint8),colors))
    return result


def assembly(indices,codes,rows=()):
    frames=parts(indices,codes,rows);out=[]
    for group,phase in enumerate((0,1,2,0)):
        a,r=frames[phase];source=static_assembly(a,r[0],r)
        # Sprites occupy color clocks 56..103. A reflected, priority playfield
        # covers both margins in black without spending any per-row cycles.
        # PF0/PF1/PF2 = F0/FF/03 mask the outer 14 four-clock blocks per side.
        source=source.replace(' sta HMOVE\n',
            ' sta HMOVE\n lda #$F0\n sta PF0\n lda #$FF\n sta PF1\n'
            ' lda #3\n sta PF2\n lda #5\n sta CTRLPF\n lda #0\n sta COLUPF\n')
        # Clear the final row background before the following blank scanline.
        source=source.replace(' sta GRP1\n sta GRP0\n sta WSYNC',
                              ' sta GRP1\n sta GRP0\n sta WSYNC\n sta COLUBK')

        header,body=source.split(' ORG $0000',1)
        body=' ORG $0000'+body.replace(' END\n','')
        # The static raster wraps bank 3 to bank 0. Only its final Draw switch
        # changes phase; the Frame entry switch stays within the current group.
        before,after=body.split(' ORG $3D00',1)
        before=before.rsplit(' bit $FFF6',1)
        assert len(before)==2
        following=4*((phase+1)%3)
        body=before[0]+f' bit $FFE{following:X}'+before[1]+' ORG $3D00'+after
        body=re.sub(r'\$FFF([6-9])',lambda m:f'${0xFFE0+group*4+int(m[1])-6:04X}',body)
        body=re.sub(r' ORG \$([0-9A-F]{4})',lambda m:f' ORG ${int(m[1],16)+group*16384:04X}',body)
        # EF autodetection tag occupies the unused NMI vector on the 6507;
        # RESET and IRQ remain intact at FFFC/FFFE in every bank.
        body=re.sub(r' ORG \$([0-9A-F]{4})\n RORG \$FFFA\n \.word (Reset\d+),\2,\2',
            lambda m:f' ORG ${int(m[1],16)-2:04X}\n RORG $FFF8\n .byte $45,$46,$45,$46\n .word {m[2]},{m[2]}',body)
        labels=re.findall(r'^(\w+)\s*$',body,re.M)
        body=re.sub(r'\b('+ '|'.join(map(re.escape,labels))+r')\b',lambda m:f'G{group}_{m[0]}',body)
        if group==0:
            out.append(header.replace('Static Scanline Color: independent FG/BG','8 color per line mode: three phases, independent row BG').replace('16 KiB F6','64 KiB EF'))
        out.append(body)
    return '\n'.join(out)+'\n END\n'


def binary(indices,codes,rows=()):
    frames=parts(indices,codes,rows);name='chrono-line'+str(len(indices))
    rom=bytearray((DATA/(name+'.bin')).read_bytes())
    meta=json.loads((DATA/(name+'.json')).read_text(encoding='utf-8'))
    if hashlib.sha256(rom).hexdigest()!=meta['sha256']:raise ValueError('8 color per line template integrity failure')
    for group,phase in enumerate((0,1,2,0)):
        a,r=frames[phase]
        for row,offsets in zip(values(a,r[0],r),meta['offsets'][group]):
            for value,offset in zip(row,offsets):rom[offset]=value
    return bytes(rom)
