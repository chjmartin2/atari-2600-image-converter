"""Cycle-exact 128 x 200 BUS2 bitmap with a foreground color per scanline.

The sprite schedule follows cd-w/SpiceWare's 128bus_20170120. Unrolled
rows replace the counter/branch with two zero-page COLUP writes. One
extra RAM-load cycle balances the six-cycle write pair at the A/B boundary.
Only the HBLANK NUSIZ1 write moves one cycle earlier; visible writes and
sprite resets retain the original timing. Bank bridges replace delay slots.
"""
import hashlib,json,struct
import numpy as np
from .core import DATA,CODES
from .drivers import load,restore
from .bus_rom import byte_lines
from .bus128_rom import validate,STREAM_STRIPS,assembly as single_assembly

IMAGE_OFFSET=0x1000

def rows_for(codes,line_codes=()):
    if len(codes)!=4 or any(c not in CODES for c in codes):raise ValueError('Invalid NTSC colors')
    rows=tuple(tuple(r) for r in line_codes) if line_codes else ((codes[0],)*3+(codes[3],),)*200
    if len(rows)!=200 or any(len(r)!=4 or any(c not in CODES for c in r) for r in rows):
        raise ValueError('BUS color per line requires 200 valid NTSC palette rows')
    if any(r[0]!=r[1] or r[1]!=r[2] for r in rows) or len({r[3] for r in rows})!=1:
        raise ValueError('BUS color per line requires one foreground per row and a shared background')
    return rows

def image_bytes(indices,codes,line_codes=()):
    a=validate(indices,codes);rows=rows_for(codes,line_codes);out=bytearray()
    for phase in range(2):
        for y,row in enumerate(rows):
            out.extend([int(row[0],16)]*2)
            cols=[x+k for x in STREAM_STRIPS[(y+phase)%2] for k in range(8)]
            out.extend(np.packbits(a[y,cols]).tolist())
    return bytes(out)

def initializer():
    words=[];loads=[]
    def emit(v):words.append(v)
    def literal(reg,v):loads.append((len(words),reg,v));emit(0)
    emit(0xB410)
    literal(0,0x400006E0);emit(0x2100);emit(0x6001)
    literal(0,0x40000720);emit(0x2101);emit(0x0209);emit(0x6001)
    for reg in (0x06,0x07,0x1B,0x1C):
        literal(0,0x40000760+reg*4);emit(0x2100);emit(0x6001)
    literal(0,0x40000800);literal(1,IMAGE_OFFSET);literal(2,1000)
    loop=len(words)
    for w in (0x680C,0x6004,0x3104,0x3004,0x3A01):emit(w)
    emit(0xD100|((loop-len(words)-2)&255));emit(0xBC10);emit(0x4770)
    if len(words)%2:emit(0x46C0)
    pool=0x808+len(words)*2
    for n,(pos,reg,v) in enumerate(loads):
        words[pos]=0x4800|(reg<<8)|((pool+n*4-((0x808+pos*2+4)&~3))//4)
    return bytes.fromhex('01008fe210ff2fe1')+struct.pack('<'+'H'*len(words),*words)+b''.join(struct.pack('<I',v) for _,_,v in loads)

A=[' stx $04',' stx $05',' sta.w $1B',' sty $1C',' ldx $89',' sty $1B',' sty $1B',' stx $20',' sty $1B',' ldx #6',' sty $1C',' sta $10',' sty $1C',' sta $10',' stx $05',' sta $1B',' sty $1C',' sty $1B']
AE=[' ldx #3',' stx $21',' sta $2A',' sta $10']
AC=[' sty $06',' sty $07'] # 6 cycles; BP's RAM load restores the seventh.
BP=[' stx $05',' ldx $8C',' sta $1B',' sty $1C']
BT=[' sty $1B',' stx $20',' sty $1B',' ldx #$86',' sta $1B',' sta $10',' sty $1C',' sta $10',' sty $1C',' stx.w $05',' sty $1B',' sty $1C',' stx $04',' sty $1B',' stx $21']
BE=[' nop',' nop',' sta $10',' sta $2A']
BC=[' sty $06',' sty $07',' nop'] # 8 cycles, formerly DEC/BNE

def assembly(indices,codes,line_codes=()):
    rows=rows_for(codes,line_codes);data=image_bytes(indices,codes,rows)
    original=single_assembly(indices,codes)
    startup=original.split('Reset\n',1)[1].split('DrawA\n',1)[0]
    startup=startup[:startup.index('PhaseB\n sta $02')]
    startup=startup.replace(' jsr Detect',' lda #$83\n sta $8B\n lda #$B0\n sta $8C\n lda #0\n jsr Detect',1)
    startup=startup.replace(' lda #6\n sta $1014\n lda #$40',' lda #7\n sta $1014\n lda #$D0')
    startup=startup.replace('Foreground = *+1\n ldx #$'+codes[0]+'\n stx $06\n stx $07\n','')
    startup=startup.replace(' ldx #$'+codes[3]+'\n stx $09',' ldx #$'+rows[0][3]+'\n stx $09')
    startup=startup.replace(' bne PhaseB\n jmp PhaseA',' bne ChooseB\n jmp GateA\nChooseB\n jmp GateB')
    detect=original[original.index('Detect\n sta $02'):original.index(' ORG $7FFA')]
    ending=original[original.index('EndPicture\n ldx #0'):original.index('Detect\n sta $02')]
    # Exit paths arrive at different points of the original last-row boundary.
    # WSYNC below preserves the original frame count regardless of phase.
    out=['; 128x200 color per line / BUS2 / NTSC / two alternating fields',
         '; Sprite schedule: cd-w / SpiceWare, 128bus_20170120.',
         '; Per-row colors and cycle-neutral bank bridges: Atari 2600 Image Optimizer.',
         ' processor 6502',' SEG',' ORG $0000']+byte_lines(load('bus2'))
    out+=[' ORG $0800']+byte_lines(initializer())+[' ORG $1000']+byte_lines(data)
    phase_counts=((69,70,61),(70,70,60))
    for bank in range(2,8):
        phase=(bank-2)//3;chunk=(bank-2)%3
        start=0x200 if bank==7 else 0x40
        if bank==7:
            out+=[' ORG $7040',' RORG $F040','Reset']+startup.rstrip().splitlines()+['Delay12',' rts']+ending.rstrip().splitlines()+detect.rstrip().splitlines()
        out+=[f' ORG ${bank*4096+start:04X}',f' RORG ${0xF000+start:04X}',f'Chunk{bank}']
        if chunk==0:
            out+=(AE+AC if phase==0 else BE+BC)
        else:out+=[' sta $10',' sta $2A']+BC
        count=phase_counts[phase][chunk]
        normal=count-2 if chunk<2 else count
        first='B' if phase==0 and chunk==0 else 'A'
        for n in range(normal):
            kind=first if n%2==0 else ('A' if first=='B' else 'B')
            last=n==normal-1
            out+=[f'Row{bank}_{n}']
            if kind=='A':
                out+=A+AE
                if last and chunk==2:out+=[' jmp ExitA']
                else:out+=AC
            else:
                out+=BP+[' nop',' nop']+BT
                if last and chunk<2:out+=[' ldx $8B',' jmp $FE80']
                else:
                    out+=[' ldx #$83']+BE
                    out+=[' jmp ExitB'] if last and chunk==2 else BC
        out+=[f'ChunkEnd{bank}',f' IF * > $FE80',' ERR',' ENDIF']
        # Bridge rows A/B. The switch replaces the four-cycle delay in B.
        # The next bank holds the identical tail at the identical address.
        bridge=[' sta $10',' sta $2A']+BC+A+AE+AC+BP
        out+=[f' ORG ${bank*4096+0xE80:04X}',' RORG $FE80']+bridge+[f' bit ${0xFFF4+min(bank+1,7):04X}']+BT+[' ldx $8B',f' jmp Chunk{bank}']
        if bank in (4,7):
            out+=[f' ORG ${bank*4096+0xF30:04X}',' RORG $FF30']
            if bank==4:out+=['ExitA']
            else:out+=['ExitB']
            out+=[' bit $FFFB',' jmp EndPicture']
        if bank in (2,5,7):
            out+=[f' ORG ${bank*4096+0xF60:04X}',' RORG $FF60']
            if bank==7:out+=['GateA']
            out+=[' bit $FFF6',' jmp $FF70']
            if bank==7:out+=['GateB']
            out+=[' bit $FFF9',' jmp $FF70']
        if chunk==0:
            out+=[f' ORG ${bank*4096+0xF70:04X}',' RORG $FF70',f'Phase{phase}']
            if phase==0:
                out+=[' sta $02',' lda $89',' sta $20',' lda #0',' ldx #3',' stx $04']+[' jsr $FFF0']*3+[' .byte $04,$00']+[' nop']*5
            else:
                out+=[' sta $02',' lda #$B0',' sta $20',' lda #0',' ldx #$83']+[' jsr $FFF0']*4+[' .byte $04,$00']+[' nop']*3
            out+=[f' jmp Chunk{bank}',f' ORG ${bank*4096+0xFF0:04X}',' RORG $FFF0',' rts']
    out+=[' ORG $7FFA',' RORG $FFFA',' .word Reset,Reset,Reset',' END','']
    return '\n'.join(out)

def binary(indices,codes,line_codes=()):
    rows=rows_for(codes,line_codes);data=image_bytes(indices,codes,rows)
    b=bytearray((DATA/'bus128-line.bin').read_bytes());meta=json.loads((DATA/'bus128-line.json').read_text())
    if hashlib.sha256(b).hexdigest()!=meta['sha256']:raise ValueError('BUS row-color template integrity failure')
    b[IMAGE_OFFSET:IMAGE_OFFSET+len(data)]=data;b[meta['Background']]=int(rows[0][3],16)
    return bytes(restore(b,'bus2'))
