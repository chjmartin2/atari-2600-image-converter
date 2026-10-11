"""128 x 200 BUS2 bitmap, based on cd-w / SpiceWare's 128bus_20170120 kernel.

The original alternating, cycle-exact sprite schedule is retained. This module
supplies a new fixed-image ARM initializer and two image streams, not the demo
application. Driver is fetched separately by chrono.drivers; never redistributed.
"""
import hashlib,json,struct
import numpy as np
from .core import DATA,CODES
from .drivers import load,restore
from .bus_rom import byte_lines

IMAGE_OFFSET=0x4000
STRIPS=((0,16,32,48,64,88,96,120),(8,24,40,56,72,80,104,112))
STREAM_STRIPS=((32,0,16,48,64,88,96,120),(40,8,24,80,56,72,104,112))

def validate(indices,codes):
    a=np.asarray(indices)
    if a.shape!=(200,128) or not np.issubdtype(a.dtype,np.integer) or np.any(a<0) or np.any(a>1):
        raise ValueError('BUS 128 requires a 128 x 200 bitmap with indices 0 or 1')
    if len(codes)!=4 or any(c not in CODES for c in codes):raise ValueError('Invalid NTSC colors')
    return a

def image_bytes(indices,codes):
    a=validate(indices,codes)
    # Writes are chronological, but sprites appear in this non-linear order.
    # Verified with random bitmaps in Stella for both phases and all 200 rows.
    result=[]
    for phase in range(2):
        for y in range(200):
            cols=np.array([x+k for x in STREAM_STRIPS[(y+phase)%2] for k in range(8)])
            result.extend(np.packbits(a[y,cols]).tolist())
    return bytes(result)

def initializer():
    words=[];loads=[]
    def emit(v):words.append(v)
    def literal(reg,value):loads.append((len(words),reg,value));emit(0)
    emit(0xB410)
    literal(0,0x400006E0);emit(0x2100);emit(0x6001)
    literal(0,0x40000720);emit(0x2101);emit(0x0209);emit(0x6001)
    for reg in (0x1B,0x1C):
        literal(0,0x40000760+reg*4);emit(0x2100);emit(0x6001)
    literal(0,0x40000800);literal(1,IMAGE_OFFSET);literal(2,800)
    loop=len(words)
    emit(0x680C);emit(0x6004);emit(0x3104);emit(0x3004);emit(0x3A01)
    emit(0xD100|((loop-len(words)-2)&255));emit(0xBC10);emit(0x4770)
    if len(words)%2:emit(0x46C0)
    pool=0x808+len(words)*2
    for n,(pos,reg,value) in enumerate(loads):
        words[pos]=0x4800|(reg<<8)|((pool+n*4-((0x808+pos*2+4)&~3))//4)
    return bytes.fromhex('01008fe210ff2fe1')+struct.pack('<'+'H'*len(words),*words)+b''.join(struct.pack('<I',v) for _,_,v in loads)

def assembly(indices,codes):
    data=image_bytes(indices,codes)
    out=['; 128 x 200 BUS2 single-color bitmap / NTSC / alternating spatial fields',
         '; Sprite timing: cd-w and SpiceWare, 128bus_20170120.',
         '; https://forums.atariage.com/topic/258191-bus-stuffing-demos/',
         '; Fixed-image stream packing and initialization: Atari 2600 Image Optimizer.',
         ' processor 6502',' SEG',' ORG $0000']+byte_lines(load('bus2'))
    out+=[' ORG $0800']+byte_lines(initializer())
    out+=[' ORG $4000']+byte_lines(data)
    out+=[' ORG $7040',' RORG $F040','Reset',' sei',' cld',' ldx #0',' txa',' tay',
          'Clear',' dex',' txs',' pha',' bne Clear',' jsr Detect',
          ' lda #$FF',' sta $101A',' lda #0',' sta $1019',
          'Frame',' lda #2',' sta $02',' sta $00',' sta $01',' ldy #44',' sty $0296',
          ' sta $02',' sta $02',' lda #0',' sta $02',' sta $00',
          ' lda $85',' beq PointerA',' lda #6',' sta $1014',' lda #$40',' sta $1014',' jmp Colors',
          'PointerA',' lda #0',' sta $1014',' sta $1014',
          'Colors','Foreground = *+1',f' ldx #${codes[0]}',' stx $06',' stx $07',
          'Background = *+1',f' ldx #${codes[3]}',' stx $09',
          ' sta $02']
    out+=[' nop']*18
    out+=[' sta $11',' ldx #$E0',' stx $21',' .byte $04,$00',' nop',' nop',' sta $14',
          ' ldx #$20',' stx $24',' sta $02',' sta $2A']+[' nop']*12
    out+=[' sta $2B',' lda #$B0',' sta $20',' ldx #201',' stx $88',' ldx #0',' stx $1019',' ldy #$FF',
          'WaitBlank',' sta $02',' lda $0294',' bpl WaitBlank',' stx $01',' lda $85',' and #1',' bne PhaseB',' jmp PhaseA',
          'PhaseB',' sta $02',' lda #$B0',' sta $20',' lda #0',' ldx #$83',
          ' jsr Delay12',' jsr Delay12',' jsr Delay12',' jsr Delay12',' .byte $04,$00',' nop',' nop',' nop',' jmp EntryB',
          'PhaseA',' sta $02',' lda $89',' sta $20',' lda #0',' ldx #3',' stx $04',
          ' jsr Delay12',' jsr Delay12',' jsr Delay12',' .byte $04,$00']+[' nop']*5
    out+=[' jmp EntryA','Delay12',' rts',' ORG $7200',' RORG $F200',
          'DrawA',' stx $04',' stx $05',' sta.w $1B',' sty $1C',' ldx $89',
          ' sty $1B',' sty $1B',' stx $20',' sty $1B',' ldx #6',' sty $1C',
          ' sta $10',' sty $1C',' sta $10',' stx $05',' sta $1B',' sty $1C',' sty $1B',
          'EntryA',' ldx #3',' stx $21',' sta $2A',' sta $10',' dec $88',' beq EndPicture',
          ' stx $05',' ldx #$B0',' sta $1B',' sty $1C',' nop',' nop',' sty $1B',' stx $20',
          ' sty $1B',' ldx #$86',' sta $1B',' sta $10',' sty $1C',' sta $10',' sty $1C',
          ' stx.w $05',' sty $1B',' sty $1C',' stx $04',' sty $1B',' stx $21',' ldx #$83',
          'EntryB',' nop',' nop',' sta $10',' sta $2A',' dec $88',' bne DrawA',
          'EndPicture',' ldx #0',' stx $1B',' stx $1C',' stx $1F',
          ' lda #2',' sta $02',' sta $01',' lda $85',' eor #1',' sta $85',
          ' ldx #20','Overscan',' sta $02',' dex',' bne Overscan',' jmp Frame',
          'Detect',' sta $02',' lda #$C3',' sta $20',' sta $04',' lda #$33',' sta $0E',' lda #$FF',' sta $1B',
          ' jsr Delay12',' jsr Delay12',' jsr Delay12',' jsr Delay12',' nop',' nop',
          ' sta $2A',' sta $10',' sta $2C',' sta $02',' ldy #$B0',' bit $32',' bmi Detected',' ldy #$C0',
          'Detected',' sty $89',' ldy #0',' sty $20',' sty $04',' sty $0E',' sty $1B',' rts',
          ' ORG $7FFA',' RORG $FFFA',' .word Reset,Reset,Reset',' END','']
    return '\n'.join(out)

def binary(indices,codes):
    data=image_bytes(indices,codes)
    b=bytearray((DATA/'bus128.bin').read_bytes());meta=json.loads((DATA/'bus128.json').read_text())
    if hashlib.sha256(b).hexdigest()!=meta['sha256']:raise ValueError('BUS 128 template integrity failure')
    b[IMAGE_OFFSET:IMAGE_OFFSET+len(data)]=data
    for label,value in [('Foreground',codes[0]),('Background',codes[3])]:b[meta[label]]=int(value,16)
    return bytes(restore(b,'bus2'))
