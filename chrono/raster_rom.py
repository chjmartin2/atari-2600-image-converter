"""Separate 4K raster kernels; classic cartridge kernel remains untouched.

48-pixel sprite multiplexing derives from the credited Andrew Davie kernel.
New fixed-address loops and playfield scheduling are documented in RESEARCH.md.
"""
import hashlib,json
import numpy as np
from .core import DATA,BITS,MODES,CODES

REGISTERS=''' processor 6502
VSYNC = $00
VBLANK = $01
WSYNC = $02
NUSIZ0 = $04
NUSIZ1 = $05
COLUP0 = $06
COLUP1 = $07
COLUPF = $08
COLUBK = $09
CTRLPF = $0A
PF0 = $0D
PF1 = $0E
PF2 = $0F
RESP0 = $10
RESP1 = $11
GRP0 = $1B
GRP1 = $1C
HMP0 = $20
HMP1 = $21
VDELP0 = $25
VDELP1 = $26
HMOVE = $2A
row = $80
temp = $81
phase = $82
vector = $83
 SEG
 ORG $F000
'''

def payload(indices,codes,line_codes,playfield=False):
    h,w=(192,40) if playfield else (128,48)
    a=np.asarray(indices)
    if a.shape!=(h,w) or not np.issubdtype(a.dtype,np.integer) or np.any(a<0) or np.any(a>7):raise ValueError('Invalid raster image')
    rows=line_codes or [codes]*h
    if len(rows)!=h or any(len(r)!=4 or any(c not in CODES for c in r) for r in rows):raise ValueError('Invalid raster colors')
    if playfield:
        if np.any((a!=0)&(a!=7)) or any(r[0]!=r[1] or r[1]!=r[2] for r in rows):raise ValueError('Playfield requires two solid colors per line')
        result=bytearray(2048)
        on=a==0
        for half in range(2):
            part=on[:,half*20:(half+1)*20]
            for section,(lo,hi,weights) in enumerate(((0,4,[16,32,64,128]),(4,12,[128,64,32,16,8,4,2,1]),(12,20,[1,2,4,8,16,32,64,128]))):
                result[(half*3+section)*256:(half*3+section)*256+h]=bytes((part[:,lo:hi]@np.array(weights)).astype(np.uint8))
        result[1536:1536+h]=bytes(int(r[0],16) for r in rows)
        result[1792:1792+h]=bytes(int(r[3],16) for r in rows)
        return bytes(result)
    if len({r[3] for r in rows})!=1:raise ValueError('48-pixel raster kernel requires a constant background')
    result=bytearray()
    for f in range(3):
        for strip in range(6):
            for y in range(127,-1,-1):
                result.append(int(BITS[a[y,strip*8:strip*8+8],(y+f)%3]@np.array([128,64,32,16,8,4,2,1])))
        result.extend(int(rows[y][(y+f)%3],16) for y in range(127,-1,-1))
    result.append(int(rows[0][3],16))
    return bytes(result)

def assembly(indices,codes,line_codes=(),playfield=False):
    data=payload(indices,codes,line_codes,playfield)
    source='; Atari 2600 Image Optimizer raster kernel. NTSC 4K.\n; 48-pixel technique: Andrew Davie, with Eckhard Stohlberg and Thomas Jentzsch.\n'+REGISTERS
    for start in range(0,len(data),16):source+=' .byte '+','.join(f'${v:02X}' for v in data[start:start+16])+'\n'
    if not playfield:
        for f in range(3):
            base=0xF000+f*896
            source+=f''' ORG ${0xFB00+f*256:04X}
Draw{f}
 ldy row
 lda ${base+768:04X},y
 sta COLUP0
 sta COLUP1
 lda ${base:04X},y
 sta GRP0
 lda ${base+128:04X},y
 sta GRP1
 lda ${base+256:04X},y
 sta GRP0
 lda ${base+640:04X},y
 sta temp
 .byte $BF
 .word ${base+512:04X}
 lda ${base+384:04X},y
 ldy temp
 nop
 nop
 sta GRP1
 stx GRP0
 sty GRP1
 sta GRP0
 dec row
 bpl Draw{f}
 jmp EndPicture
'''
    source+=' ORG $F800\n' if playfield else ' ORG $FE00\n'
    source+='''Reset
 sei
 cld
 ldx #$FF
 txs
 lda #0
Clear
 sta 0,x
 dex
 bne Clear
'''
    if not playfield:
        source+=''' sta phase
 sta WSYNC
 lda #3
 sta NUSIZ0
 sta NUSIZ1
 lda #$80
 sta HMP0
 lda #$90
 sta HMP1
 lda #1
 sta VDELP0
 sta VDELP1
 bit row
 bit row
 nop
 sta RESP0
 sta RESP1
 sta WSYNC
 sta HMOVE
'''
    source+='''Frame
 lda #2
 sta VBLANK
 sta VSYNC
 sta WSYNC
 sta WSYNC
 sta WSYNC
 lda #0
 sta VSYNC
'''
    if not playfield:
        source+=''' ldx phase
 lda VectorLo,x
 sta vector
 lda VectorHi,x
 sta vector+1
 lda $FA80
 sta COLUBK
'''
    source+=''' ldx #37
Blank
 sta WSYNC
 dex
 bne Blank
 lda #0
'''
    if playfield:source+=' sta COLUBK\n'
    source+=' sta VBLANK\n'
    if playfield:
        source+=''' ldy #0
 ldx $F600,y
DrawPF
 sta WSYNC
 stx COLUPF
 lda $F700,y
 sta COLUBK
 lda $F000,y
 sta PF0
 lda $F100,y
 sta PF1
 lda $F200,y
 sta PF2
 nop
 nop
 nop
 lda $F300,y
 sta PF0
 lda $F400,y
 sta PF1
 lda $F500,y
 sta PF2
 iny
 cpy #192
 beq EndPF
 ldx $F600,y
 jmp DrawPF
EndPF
 sta WSYNC
 lda #0
 sta PF0
 sta PF1
 sta PF2
 lda #2
 sta VBLANK
 ldx #29
'''
    else:
        source+=''' ldx #31
Top
 sta WSYNC
 dex
 bne Top
 sta WSYNC
 ldy #127
 sty row
 REPEAT 26
 nop
 REPEND
 jmp (vector)
EndPicture
 lda #0
 sta GRP0
 sta GRP1
 sta GRP0
 sta WSYNC
 lda #2
 sta VBLANK
 inc phase
 lda phase
 cmp #3
 bcc PhaseOK
 lda #0
 sta phase
PhaseOK
 ldx #60
'''
    source+='''Overscan
 sta WSYNC
 dex
 bne Overscan
 jmp Frame
'''
    if not playfield:source+='VectorLo .byte <Draw0,<Draw1,<Draw2\nVectorHi .byte >Draw0,>Draw1,>Draw2\n'
    source+=' ORG $FFFA\n .word Reset,Reset,Reset\n END\n'
    return source

def binary(indices,codes,line_codes=(),playfield=False):
    name='raster40' if playfield else 'raster48'
    base=(DATA/(name+'.bin')).read_bytes()
    meta=json.loads((DATA/(name+'.json')).read_text())
    if len(base)!=4096 or hashlib.sha256(base).hexdigest()!=meta['sha256']:raise ValueError('Raster template integrity check failed')
    data=payload(indices,codes,line_codes,playfield)
    return data+base[len(data):]
