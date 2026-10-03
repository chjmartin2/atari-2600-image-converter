"""Experimental BUS2 color raster: 16 x 192 independent NTSC color samples.

Each STY COLUBK receives a byte from the cartridge stream in three CPU cycles.
Samples occupy 9 color clocks, x=7..150. This is not a 160-pixel bitmap.
The preserved 2 KiB BUS2 driver comes from Stella's 128bus_20170120 test ROM.
See BUS-RESEARCH.md for provenance and hardware/redistribution limitations.
"""
import hashlib,json,struct
import numpy as np
from .core import DATA,CODES
from .drivers import load,restore

NAME='Bus stuffing (experimental)'
DRIVER_HASH='2d489398d221bd340e8ea7af129045c0147089a0b17785e6cea87a094cdb81d0'
IMAGE_OFFSET=0x4000

def image_bytes(indices):
    a=np.asarray(indices)
    if a.shape!=(192,16) or not np.issubdtype(a.dtype,np.integer) or np.any(a<0) or np.any(a>=128):
        raise ValueError('BUS requires 16 x 192 NTSC palette indices (0–127)')
    return np.array([int(c,16) for c in CODES],dtype=np.uint8)[a].tobytes()

def thumb_initializer():
    """Small, reproducible ARM7TDMI Thumb initializer; no cross compiler needed.

    Called once before video starts. Preserves r4; LR returns to the BUS driver.
    Sets stream 0 pointer/increment and COLUBK mapping, copies the image to RAM.
    Literal loads/branches are calculated, not dependent on compiler versions.
    """
    words=[];loads=[]
    def emit(word):words.append(word)
    def literal(reg,value):loads.append((len(words),reg,value));emit(0)
    emit(0xB410) # push {r4}
    literal(0,0x400006E0);emit(0x2100);emit(0x6001) # DS0PTR = 0
    literal(0,0x40000720);emit(0x2101);emit(0x0209);emit(0x6001) # DS0INC = 0x100
    literal(0,0x40000784);emit(0x2100);emit(0x6001) # COLUBK map = stream 0
    literal(0,0x40000800);literal(1,IMAGE_OFFSET);literal(2,768)
    loop=len(words)
    emit(0x680C);emit(0x6004) # ldr r4,[r1]; str r4,[r0]
    emit(0x3104);emit(0x3004);emit(0x3A01)
    emit(0xD100|((loop-len(words)-2)&255)) # bne loop
    emit(0xBC10);emit(0x4770) # pop {r4}; bx lr
    if len(words)%2:emit(0x46C0)
    pool=0x808+len(words)*2
    for n,(position,reg,value) in enumerate(loads):
        pc=(0x808+position*2+4)&~3
        words[position]=0x4800|(reg<<8)|((pool+n*4-pc)//4)
    # ARM entry switches to Thumb; this is an ARM instruction sequence, not data.
    return bytes.fromhex('01008fe210ff2fe1')+struct.pack('<'+'H'*len(words),*words)+b''.join(struct.pack('<I',v) for _,_,v in loads)

def byte_lines(data):
    return [' .byte '+','.join(f'${b:02X}' for b in data[n:n+16]) for n in range(0,len(data),16)]

def assembly(indices,codes=None,line_codes=()):
    data=image_bytes(indices)
    driver=load('bus2')
    if hashlib.sha256(driver).hexdigest()!=DRIVER_HASH:raise ValueError('BUS2 driver integrity check failed')
    out=['; Atari 2600 Image Optimizer / experimental BUS2 / 32 KiB / NTSC',
         '; 16 independent colors per line, 9 color clocks per sample, 192 lines.',
         '; BUS driver preserved from 128bus_20170120.bin in Stella 7.0 tests.',
         '; Local experimental use; see BUS-RESEARCH.md before redistribution.',
         ' processor 6502',' SEG',' ORG $0000']+byte_lines(driver)
    out+=[' ORG $0800']+byte_lines(thumb_initializer())
    for bank in range(3):
        out += [f' ORG ${(bank+1)*4096+0x40:04X}',' RORG $F040']
        for y in range(64):
            out += [f'; Raster row {bank*64+y}: STY completions at 25,28,...70; clear at 73.']
            if y==0 and bank:
                # Cross-bank continuation arrives seven cycles into this line.
                out += [' bit $80']+[' nop']*6
            else:out += [' sta $02']+[' nop']*11
            out += [' sty $09']*16+[' sta $09']
        out += [f' jmp ${0xFF00+bank*6:04X}',
                f' ORG ${(bank+1)*4096+0xF00:04X}',' RORG $FF00',
                ' bit $FFF6',' jmp $F040',' bit $FFF7',' jmp $F040',
                ' bit $FFFB',' jmp $F200',' bit $FFF5',' jmp $F040']
    out += [' ORG $4000',' RORG $4000','ImageData']+byte_lines(data)
    out += [' ORG $7040',' RORG $F040','Start',' sei',' cld',' ldx #$FF',' txs',
            ' lda #0','Clear',' sta 0,x',' dex',' bne Clear',
            ' lda #$FF',' sta $101A', # One-time ARM copy and stream initialization.
            ' lda #0',' sta $1019',' ldy #$FF',
            'Frame',' lda #2',' sta $01',' sta $00',' sta $02',' sta $02',' sta $02',
            ' lda #0',' sta $00',' sta $1014',' sta $1014',
            ' ldx #37','Blank',' sta $02',' dex',' bne Blank',
            ' sta $01',' jmp $FF12',
            ' ORG $7200',' RORG $F200','Overscan',
            # Continuation arrives c7 after the 192nd row; this is overscan line 1.
            ' lda #2',' sta $01',' lda #0',' ldx #29','Over',' sta $02',' dex',' bne Over',' jmp Frame',
            ' ORG $7F00',' RORG $FF00',
            ' bit $FFF6',' jmp $F040',' bit $FFF7',' jmp $F040',
            ' bit $FFFB',' jmp $F200',' bit $FFF5',' jmp $F040',
            ' ORG $7FFA',' RORG $FFFA',' .word Start,Start,Start',' END','']
    return '\n'.join(out)

def binary(indices,codes=None,line_codes=()):
    data=image_bytes(indices)
    result=bytearray((DATA/'bus-raster.bin').read_bytes())
    meta=json.loads((DATA/'bus-raster.json').read_text(encoding='utf-8'))
    if len(result)!=32768 or hashlib.sha256(result).hexdigest()!=meta['sha256']:
        raise ValueError('BUS template integrity check failed')
    result[IMAGE_OFFSET:IMAGE_OFFSET+len(data)]=data
    return bytes(restore(result,'bus2'))
