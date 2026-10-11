"""Static 48-pixel raster with independent foreground/background per line.

Unrolled immediate image data trades 16 KiB F6 ROM for enough time to write
COLUBK every line. Sprite multiplexing follows the credited Davie kernel.
"""
import hashlib,json
import numpy as np
from .core import DATA,CODES
from .raster_rom import REGISTERS
from .sprite_rom import assembly as sprite_assembly


def values(indices,codes,rows=()):
    a=np.asarray(indices)
    if a.shape not in ((128,48),(192,48)) or not np.issubdtype(a.dtype,np.integer) or np.any((a!=0)&(a!=7)):
        raise ValueError('Scanline raster requires 48x128 or 48x192 binary indices')
    h=len(a);rows=rows or (tuple(codes),)*h
    if len(rows)!=h or any(len(r)!=4 or any(c not in CODES for c in r) or len(set(r[:3]))!=1 for r in rows):
        raise ValueError('Scanline raster requires one foreground and one background per row')
    bits=(a==0).reshape(h,6,8)@np.array([128,64,32,16,8,4,2,1])
    return [(int(r[0],16),int(r[3],16),*map(int,b)) for r,b in zip(rows,bits)]


def assembly(indices,codes,rows=()):
    data=values(indices,codes,rows);h=len(data);per=h//4
    # Reuse proven reset/player positioning/frame setup. No drivers or streams.
    base=sprite_assembly(np.zeros((192,48),dtype=np.uint8),('00',)*4)
    reset=base[base.index('Reset\n'):base.index(' ORG $FFFA')]
    reset=reset.replace(' lda $F800\n sta COLUBK',' lda #0\n sta COLUBK')
    # First unrolled Draw must begin at the same cycle as the indexed kernel.
    reset=reset.replace(' jmp Draw',' bit $FFF6\n jmp Draw')
    # The bank switch adds four cycles; remove two setup NOPs.
    start=reset.index(' sty row\n')+len(' sty row\n')
    reset=reset[:start]+reset[start:].replace(' nop\n nop\n','',1)
    if h==128:
        reset=reset.replace(' ldy #192',' ldy #128')
        reset=reset.replace(' lda #0\n sta VBLANK\n sta WSYNC',
            ' lda #0\n sta VBLANK\n ldx #32\nTop\n sta WSYNC\n dex\n bne Top\n sta WSYNC')
        reset=reset.replace(' ldx #27',' ldx #59')
    reset=reset.replace(' ldx #27',' ldx #28').replace(' ldx #59',' ldx #60')
    out=['; Static Scanline Color: independent FG/BG; 48x%d NTSC; 16 KiB F6.'%h,
         '; 48-pixel multiplexing: Andrew Davie / Eckhard Stohlberg / Thomas Jentzsch.',REGISTERS.split(' SEG')[0],' SEG']
    for bank in range(4):
        out += [f' ORG ${bank*4096:04X}',' RORG $F000',f'Draw{bank}']
        for local in range(per):
            y=bank*per+local;fg,bg,*b=data[y]
            # 13 cycles: same length as LDY row/LDA fg,Y/STA P0/STA P1.
            out += [f'FG{y}',f' lda #${fg:02X}',' sta COLUP0',' sta COLUP1',f'BG{y}',f' lda #${bg:02X}',' sta COLUBK']
            for k,reg in ((0,'GRP0'),(1,'GRP1'),(2,'GRP0')):
                out += [f'P{y}_{k}',f' lda #${b[k]:02X}',' nop',f' sta {reg}']
            out += [f'P{y}_5',f' ldy #${b[5]:02X}',f'P{y}_4',f' ldx #${b[4]:02X}',f'P{y}_3',f' lda #${b[3]:02X}']
            # Switch inside the 16-cycle padding, preserving A/X/Y graphics.
            # The next bank has an identical tail at this address.
            if local==per-1:out += [' nop']*4+[f' bit ${0xFFF6+(bank+1)%4:04X}']+[' nop']*2
            else:out += [' nop']*8
            out += [' sta GRP1',' stx GRP0',' sty GRP1',' sta GRP0']
            if local==per-1:
                out += [' bit row',' nop',' jmp EndPicture0' if bank==0 else ' jmp $F000']
            else:out+=[' nop']*4
        out += [f' ORG ${bank*4096+0xD00:04X}',' RORG $FD00']
        text=reset
        import re
        for label in ('Reset','Clear','Frame','Blank','Over','EndPicture','Top','Draw'):
            text=re.sub(r'\b'+label+r'\b',label+str(bank),text)
        # After switching to bank zero, shared addresses execute bank-zero labels.
        out.append(text)
        out += [f' ORG ${bank*4096+0xFFA:04X}',' RORG $FFFA',f' .word Reset{bank},Reset{bank},Reset{bank}']
    return '\n'.join(out)+'\n END\n'


def binary(indices,codes,rows=()):
    data=values(indices,codes,rows);name='scanline'+str(len(data))
    rom=bytearray((DATA/(name+'.bin')).read_bytes())
    meta=json.loads((DATA/(name+'.json')).read_text(encoding='utf-8'))
    if hashlib.sha256(rom).hexdigest()!=meta['sha256']:raise ValueError('Scanline template integrity failure')
    for row,offsets in zip(data,meta['offsets']):
        for value,offset in zip(row,offsets):rom[offset]=value
    return bytes(rom)
