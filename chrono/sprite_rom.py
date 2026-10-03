"""48 x 192 single-frame sprite kernels, with optional cartridge data streams.

Six interleaved eight-pixel copies of P0/P1, based on Andrew Davie's technique.
The DPC+ variant uses eight authentic fast-fetch streams, not banked plain ROM.
"""
import hashlib, json, struct
import numpy as np
from .core import DATA, CODES
from .drivers import load,restore
from .raster_rom import REGISTERS
from .bus_rom import byte_lines

def cdf_initializer():
    """Thumb code at $1800: refresh display RAM and eight stream pointers.

    CDFJ+ pointers are 16.16 fixed point; increments are 8.8. Preserve r4.
    Called during timed vertical blank. ARM code does no TIA register writes.
    """
    words=[];loads=[]
    def emit(v):words.append(v)
    def literal(r,v):loads.append((len(words),r,v));emit(0)
    emit(0xB410)
    literal(0,0x40000800);literal(1,0x2000);literal(2,512)
    loop=len(words)
    for v in (0x680C,0x6004,0x3104,0x3004,0x3A01):emit(v)
    emit(0xD100|((loop-len(words)-2)&255))
    literal(0,0x40000098);literal(1,0x40000124)
    emit(0x2200);literal(3,0x01000000);literal(4,0x100)
    for k in range(8):
        emit(0x6002|(k<<6));emit(0x600C|(k<<6));emit(0x18D2)
    emit(0xBC10);emit(0x4770)
    if len(words)%2:emit(0x46C0)
    pool=0x1800+len(words)*2
    for n,(pos,r,v) in enumerate(loads):words[pos]=0x4800|(r<<8)|((pool+n*4-((0x1800+pos*2+4)&~3))//4)
    return struct.pack('<'+'H'*len(words),*words)+b''.join(struct.pack('<I',v) for _,_,v in loads)

def payload(indices,codes,rows=(),stream=False):
    a=np.asarray(indices)
    if a.shape!=(192,48) or not np.issubdtype(a.dtype,np.integer) or np.any((a!=0)&(a!=7)):
        raise ValueError('Sprite raster requires 48 x 192 binary foreground/background indices')
    rows=rows or (codes,)*192
    if len(rows)!=192 or any(len(r)!=4 or any(c not in CODES for c in r) for r in rows):raise ValueError('Invalid sprite colors')
    if len({r[3] for r in rows})!=1:raise ValueError('Sprite raster requires a constant background')
    if not stream and any(r[0]!=r[1] or r[0]!=r[2] for r in rows):raise ValueError('Plain sprite raster has one foreground per line')
    data=bytearray(2049)
    for y in range(192):
        dest=y if stream else 192-y
        for strip in range(6):
            data[strip*256+dest]=int((a[y,strip*8:strip*8+8]==0)@np.array([128,64,32,16,8,4,2,1]))
        for k in range(2):data[(6+k)*256+dest]=int(rows[y][k if stream else 0],16)
    data[2048]=int(rows[0][3],16)
    return bytes(data)

def assembly(indices,codes,rows=(),kind='4K'):
    stream=kind!='4K';data=payload(indices,codes,rows,stream)
    out=['; Atari 2600 Image Optimizer: six multiplexed sprite strips, 48 x 192 NTSC.',
         '; Sprite technique: Andrew Davie / Eckhard Stohlberg / Thomas Jentzsch.',
         REGISTERS.split(' SEG')[0],' SEG']
    if kind=='DPC+':
        driver=load('dpcplus')
        if hashlib.md5(driver).hexdigest()!='5f80b5a5adbe483addc3f6e6f1b472f8':raise ValueError('DPC+ driver integrity failure')
        out+=[' ORG $0000']+byte_lines(driver)+[' ORG $5E00',' RORG $F200']
    elif kind=='CDFJ+':
        driver=load('cdfjplus')
        meta=json.loads((DATA/'cdfjplus-driver.json').read_text())
        if hashlib.sha256(driver).hexdigest()!=meta['sha256']:raise ValueError('CDFJ+ driver integrity failure')
        out+=[' ORG $0000']+byte_lines(driver)+[' ORG $0A00',' RORG $F200']
    else:out+=[' ORG $F000']+byte_lines(data)+[' ORG $F900']
    out+=['Draw',' ldy row']
    if stream:out+=[' lda #14',' sta COLUP0',' lda #15',' sta COLUP1']
    else:out+=[' lda $F600,y',' sta COLUP0',' sta COLUP1']
    for k,reg in ((0,'GRP0'),(1,'GRP1'),(2,'GRP0')):
        out += [f' lda #{8+k}' if stream else f' lda ${0xF000+256*k:04X},y',f' sta {reg}']
    if stream:out+=[' lda #13',' sta temp',' lda #12',' tax',' lda #11',' ldy temp']+[' nop']*7
    else:out+=[' lda $F500,y',' sta temp',' .byte $BF',' .word $F400',' lda $F300,y',' ldy temp',' nop',' nop']
    out+=[' sta GRP1',' stx GRP0',' sty GRP1',' sta GRP0',' dec row',' bne Draw',' jmp EndPicture']
    out+=[' ORG $0C00' if kind=='CDFJ+' else ' ORG $6000',' RORG $F400'] if stream else [' ORG $FA00']
    out+=['Reset',' sei',' cld',' ldx #$FF',' txs',' lda #0','Clear',' sta 0,x',' dex',' bne Clear']
    if stream:out+=[' lda #1',' sta $1058']
    out+=[' sta WSYNC',' lda #3',' sta NUSIZ0',' sta NUSIZ1',' lda #$80',' sta HMP0',
          ' lda #$90',' sta HMP1',' lda #1',' sta VDELP0',' sta VDELP1',' bit row',' bit row',' nop',
          ' sta RESP0',' sta RESP1',' sta WSYNC',' sta HMOVE',
          'Frame',' lda #2',' sta VBLANK',' sta VSYNC',' sta WSYNC',' sta WSYNC',' sta WSYNC',' lda #0',' sta VSYNC']
    if kind=='CDFJ+':
        out+=[' lda #45',' sta $0296',' lda #$FF',' sta $1FF3',
              ' lda $F700',' sta COLUBK','WaitARM',' lda $0284',' bne WaitARM']
    elif stream:
        for k in range(8):out += [' lda #0',f' sta ${0x1050+k:04X}',f' lda #{k}',f' sta ${0x1068+k:04X}']
        # Stream 0 temporarily reads the saved global background, then resets.
        out+=[' lda #8',' sta $1068',' lda $1008',' sta COLUBK',' lda #0',' sta $1050',' sta $1068']
    else:out+=[' lda $F800',' sta COLUBK']
    # Stream setup consumes more than one line: sync before counted blank interval.
    if kind!='CDFJ+':out+=[' ldx #36' if stream else ' ldx #37','Blank',' sta WSYNC',' dex',' bne Blank']
    out+=[' lda #0',' sta VBLANK',' sta WSYNC',' ldy #192',' sty row']
    if stream:out+=[' stx $1058'] # X is zero: enable fast fetch. No low immediates until disabled.
    out+=[' nop']*(25 if stream else 27)
    out+=[' jmp Draw','EndPicture']
    if stream:out+=[' ldx #1',' stx $1058']
    out+=[' lda #0',' sta GRP0',' sta GRP1',' sta GRP0',' sta WSYNC',' lda #2',' sta VBLANK',' ldx #27',
          'Over',' sta WSYNC',' dex',' bne Over',' jmp Frame']
    if kind=='CDFJ+':
        out+=[' ORG $0F00',' RORG $F700',f' .byte ${data[2048]:02X}',
              ' ORG $17F0',' RORG $FFF0',' .byte 0,0,0,0',' .long $40001FDC,$00001801',' .word Reset,Reset',
              ' ORG $1800',' RORG $1800']+byte_lines(cdf_initializer())+[' ORG $2000']+byte_lines(data)+[' ORG $7FFF',' .byte 0']
    elif stream:
        out+=[' ORG $6BFA',' RORG $FFFA',' .word Reset,Reset,Reset',' ORG $6C00',' RORG $0000']+byte_lines(data)+[' ORG $7FFF',' .byte 0']
    else:out+=[' ORG $FFFA',' .word Reset,Reset,Reset']
    if kind=='CDFJ+':
        # Only LDA immediates in Draw are stream operands. X/Y fast fetch is disabled.
        start=out.index('Draw');end=out.index('Reset')
        for n in range(start,end):
            if out[n].startswith(' lda #'):out[n]=' lda #'+str(int(out[n][6:])-8)
        out=[v.replace('$1058','$1FF2') for v in out]
        # X was the blank loop counter in DPC+; explicitly zero it here.
        pos=out.index(' stx $1FF2');out.insert(pos,' ldx #0')
        # This adds two cycles, so remove one setup NOP.
        pos=out.index(' jmp Draw');out.pop(pos-1)
    return '\n'.join(out+[' END',''])

def binary(indices,codes,rows=(),kind='4K'):
    name='sprites-cdfj' if kind=='CDFJ+' else 'sprites-dpc' if kind=='DPC+' else 'sprites48'
    result=bytearray((DATA/(name+'.bin')).read_bytes())
    meta=json.loads((DATA/(name+'.json')).read_text())
    if hashlib.sha256(result).hexdigest()!=meta['sha256']:raise ValueError('Sprite template integrity failure')
    data=payload(indices,codes,rows,kind!='4K');start=0x2000 if kind=='CDFJ+' else 0x6C00 if kind=='DPC+' else 0
    result[start:start+len(data)]=data
    if kind=='CDFJ+':result[0xF00]=data[2048]
    if kind!='4K':restore(result,'cdfjplus' if kind=='CDFJ+' else 'dpcplus')
    return bytes(result)
