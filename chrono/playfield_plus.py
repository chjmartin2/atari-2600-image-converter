"""40x192 static, score-mode playfield with a timed midline background change.

Four 4K F6 banks: three unrolled 64-row banks and one frame-control bank.
Rows store (left foreground, left background, right foreground, right background).
"""
import hashlib,json
import numpy as np
from .core import DATA,CODES

ROW_BYTES=44
OPERANDS=(3,7,11,15,19,23,27,31,35,41)

def values(indices,rows):
    a=np.asarray(indices)
    if a.shape!=(192,40) or not np.issubdtype(a.dtype,np.integer) or np.any((a!=0)&(a!=7)):
        raise ValueError('Playfield Plus requires 40x192 solid on/off pixels')
    if len(rows)!=192 or any(len(r)!=4 or any(c not in CODES for c in r) for r in rows):
        raise ValueError('Playfield Plus requires four legal color codes per row')
    on=a==0;strips=[]
    for half in range(2):
        p=on[:,half*20:(half+1)*20]
        for lo,hi,weights in ((0,4,[16,32,64,128]),(4,12,[128,64,32,16,8,4,2,1]),(12,20,[1,2,4,8,16,32,64,128])):
            strips.append(p[:,lo:hi]@np.array(weights))
    return [(int(r[0],16),int(r[2],16),int(r[1],16),*(int(strip[y]) for strip in strips[:5]),int(r[3],16),int(strips[5][y])) for y,r in enumerate(rows)]

def assembly(indices,rows):
    data=values(indices,rows)
    out=['; Atari 2600 Image Optimizer Playfield Plus. NTSC, 16 KB F6.','; Score colors per half; background changes at x=76, score colors at x=80.',' processor 6502',' SEG']
    for bank in range(4):
        out += [f' ORG ${bank*4096:04X}',' RORG $F000']
        if bank<3:
            for y in range(bank*64,(bank+1)*64):
                v=data[y];out += [f'; Row {y}; CPU completion cycles: colors 5/10/15, PF 20/25/30/35/40, BG 48, PF2 53.',' sta $02']
                for n,reg in enumerate((6,7,9,13,14,15,13,14,9,15)):
                    out += [f' lda #${v[n]:02X}']
                    if n==8:out += [' bit $80']
                    out += [f' sta ${reg:02X}']
            out += [f' jmp ${[0xFF00,0xFF06,0xFF0C][bank]:04X}']
        else:
            out += ['Init',' sei',' cld',' ldx #$FF',' txs',' lda #0','Clear',' sta 0,x',' dex',' bne Clear',
                    ' lda #2',' sta $0A', # CTRLPF score mode, no reflection/priority.
                    'Frame',' lda #2',' sta $01',' sta $00',' sta $02',' sta $02',' sta $02',
                    ' lda #0',' sta $00',' ldx #37','Blank',' sta $02',' dex',' bne Blank',
                    ' lda #0',' sta $09',' sta $01',' jmp $FF12']
            out += [f' ORG ${bank*4096+0x100:04X}',' RORG $F100','Overscan',' sta $02',
                    ' lda #2',' sta $01',' lda #0',' sta $0D',' sta $0E',' sta $0F',
                    ' ldx #29','Over',' sta $02',' dex',' bne Over',' jmp Frame']
        # Identical cross-bank trampolines: instruction after hotspot read must
        # exist at the same address in the newly selected bank.
        out += [f' ORG ${bank*4096+0xF00:04X}',' RORG $FF00',
                ' lda $FFF7',' jmp $F000',' lda $FFF8',' jmp $F000',
                ' lda $FFF9',' jmp $F100',' lda $FFF6',' jmp $F000',
                ' lda $FFF9',' jmp $F000',
                f' ORG ${bank*4096+0xFFA:04X}',' RORG $FFFA',' .word $FF18,$FF18,$FF18']
    return '\n'.join(out+[' END',''])

def binary(indices,rows):
    data=values(indices,rows)
    result=bytearray((DATA/'playfield-plus.bin').read_bytes())
    meta=json.loads((DATA/'playfield-plus.json').read_text(encoding='utf-8'))
    if len(result)!=16384 or hashlib.sha256(result).hexdigest()!=meta['sha256']:
        raise ValueError('Playfield Plus template integrity check failed')
    for y,row in enumerate(data):
        base=(y//64)*4096+(y%64)*ROW_BYTES
        for offset,value in zip(OPERANDS,row):result[base+offset]=value
    return bytes(result)
