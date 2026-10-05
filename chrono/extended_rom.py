"""Unrolled F4 hybrid/wide kernels and an F8 half-line interlace kernel.

No assembler is needed by the application. Audited binary templates are patched
only at generated immediate operands/data slots; DASM parity tests cover exports.
"""
import re,json,hashlib
import numpy as np
from .core import DATA,Settings
from .extended import HYBRID,WIDE,INTERLACE,rows_for,validate_indices
from .twoframe_rom import _body
from .sprite_rom import payload

def stem(mode):return {HYBRID:'hybrid',WIDE:'wide96',INTERLACE:'interlace'}[mode]

def values(indices,codes,mode,rows):
    s=Settings(mode=mode,codes=tuple(codes),line_codes=tuple(rows));a=np.asarray(indices)
    validate_indices(a,s);rows=rows_for(s)
    if mode==INTERLACE:
        return [payload(np.where(a[f::2],0,7).astype(np.uint8),rows[f][:4],tuple(rows[f::2])) for f in range(2)]
    result={}
    if mode==HYBRID:
        p0,p1=(int(v,16) for v in rows[0][4:])
        pf=(a.reshape(192,40,4)==1).any(axis=2)
        strips=[]
        for half in range(2):
            p=pf[:,half*20:(half+1)*20]
            for lo,hi,weights in ((0,4,[16,32,64,128]),(4,12,[128,64,32,16,8,4,2,1]),(12,20,[1,2,4,8,16,32,64,128])):
                strips.append(p[:,lo:hi]@np.array(weights))
        for y,r in enumerate(rows):
            sprite=[int((a[y,x:x+8]==k+2)@np.array([128,64,32,16,8,4,2,1])) for k,x in enumerate((p0,p1))]
            result[y//64,y%64]=[int(r[3],16),int(r[0],16),*[int(t[y]) for t in strips[:3]],*sprite,*[int(t[y]) for t in strips[3:]]]
        result[7,0]=[p0,p1,int(rows[0][1],16),int(rows[0][2],16)]
    else:
        for f in range(2):
            cols=np.where((np.arange(96)//16)%2==f)[0]
            packed=np.packbits(a[:,cols],axis=1)
            for y,r in enumerate(rows):result[f*3+y//64,y%64]=[int(r[3],16),int(r[0],16),int(r[0],16),*packed[y].tolist()]
    return result

def f4_assembly(data,mode):
    wide=mode==WIDE
    out=['; Atari 2600 Image Optimizer: '+mode+'; NTSC / 32K F4',
         '; Each visible row is unrolled. No data-dependent branches in the raster.',
         ' processor 6502',' SEG']
    def operand(bank,item,value):
        out.extend([f'P_{bank}_{item} = *+1',f' lda #${value:02X}'])
    for bank in range(8):
        out += [f' ORG ${bank*4096:04X}',' RORG $F000']
        if bank<(6 if wide else 3):
            for y in range(64):
                v=data[bank,y];out+=[' sta $02']
                registers=(9,6,7,27,28,27,28,27,28) if wide else (9,8,13,14,15,27,28,13,14,15)
                for n,reg in enumerate(registers):
                    # PF right half write at c45; wide second copy at c40/45.
                    if (wide and n==5) or (not wide and n==7):
                        cycles=(15 if bank>=3 else 10) if wide else 5
                        if cycles%2:out+=[' bit $80'];cycles-=3
                        out+=[' nop']*(cycles//2)
                    operand(bank,y*len(v)+n,v[n]);out += [f' sta ${reg:02X}']
            out += [f' jmp ${0xFF00+6*bank:04X}']
        elif bank==7:
            out += ['Init',' sei',' cld',' ldx #$FF',' txs',' lda #0','Clear',' sta 0,x',' dex',' bne Clear',
                    f' lda #{6 if wide else 0}',' sta $04',' sta $05']
            if not wide:
                # Fixed positions only need setting at reset. Far-right positions
                # can consume a second line; keep this outside counted frames.
                operand(7,0,data[7,0][0]);out+=[' ldx #0',' jsr Position']
                operand(7,1,data[7,0][1]);out+=[' ldx #1',' jsr Position']
                out+=[' sta $02',' sta $2A']
                for n,reg in ((2,6),(3,7)):operand(7,n,data[7,0][n]);out+=[f' sta ${reg:02X}']
            out+=['Frame',' lda #2',' sta $01',' sta $00',' sta $02',' sta $02',' sta $02',' lda #0',' sta $00']
            if wide:
                out+=[' lda $82',' asl',' asl',' asl',' asl',' clc',' adc #32',' ldx #0',' jsr Position',
                      ' lda $82',' asl',' asl',' asl',' asl',' clc',' adc #40',' ldx #1',' jsr Position']
                out+=[' sta $02',' sta $2A']
            out+=[' ldx #34' if wide else ' ldx #37','Blank',' sta $02',' dex',' bne Blank',' lda #0',' sta $01']
            if wide:out+=[' lda $82',' bne StartB']
            out+=[' jmp $FF24']
            if wide:out+=['StartB',' jmp $FF2A']
            out += [f' ORG ${bank*4096+0x180:04X}',' RORG $F180','Position',' sec',' sbc #3',' sta $02',' sec','Coarse',' sbc #15',' bcs Coarse',' eor #7',' asl',' asl',' asl',' asl',' sta $20,x',' sta $10,x',' rts',
                    f' ORG ${bank*4096+0x200:04X}',' RORG $F200','Overscan',' sta $02',' lda #2',' sta $01',
                    ' lda #0',' sta $0D',' sta $0E',' sta $0F',' sta $1B',' sta $1C',' sta $09']
            if wide:out+=[' lda $82',' eor #1',' sta $82']
            out+=[' ldx #29','Over',' sta $02',' dex',' bne Over',' jmp Frame']
        out += [f' ORG ${bank*4096+0xF00:04X}',' RORG $FF00']
        for target,address in ((1,0xF000),(2,0xF000),(7,0xF200),(4,0xF000),(5,0xF000),(7,0xF200),(0,0xF000),(3,0xF000),(7,0xF000)):
            out += [f' lda ${0xFFF4+target:04X}',f' jmp ${address:04X}']
        out += [f' ORG ${bank*4096+0xFFA:04X}',' RORG $FFFA',' .word $FF30,$FF30,$FF30']
    return '\n'.join(out+[' END',''])

def interlace_assembly(data):
    out=['; Experimental true interlace: 48 x 384 / F8 / NTSC 525-line field pair.',
         '; Half-line VSYNC offset: Billy Eno / Glenn Saunders proof-of-concept.',
         '; https://www.biglist.com/lists/stella/archives/200208/msg00110.html']
    for bank in range(2):
        s=_body(data[bank],'4K')
        if bank:s=s[s.index(' ORG $F000'):]
        # Align both edges to either CPU cycle 3 or 41: exactly half a scanline.
        # Alternating 262 / 263 horizontal periods makes the sync edges 262.5 apart.
        sync=['Frame',' lda #2',' sta VBLANK',' sta WSYNC']
        if bank:sync+=[' nop']*19
        sync+=['SyncOn',' sta VSYNC',' sta WSYNC',' sta WSYNC',' lda #0',' sta WSYNC']
        if bank:sync+=[' nop']*19
        sync+=['SyncOff',' sta VSYNC']
        begin=s.index('Frame\n');end=s.index(' lda $F800',begin)
        s=s[:begin]+'\n'.join(sync)+'\n'+s[end:]
        # The explicit WSYNC before SyncOn adds one line vs the original kernel.
        s=s.replace(' ldx #27',f' ldx #{26 if bank==0 else 27}')
        s=s.replace(' jmp Frame',' jmp $FF80').replace(' ORG $FFFA',f' ORG $FF80\n bit ${0xFFF9 if bank==0 else 0xFFF8:04X}\n jmp Frame\n ORG $FFFA')
        for label in ('Draw','Reset','Clear','Frame','Blank','Over','EndPicture','SyncOn','SyncOff'):
            s=re.sub(r'\b'+label+r'\b',label+str(bank),s)
        s=re.sub(r' ORG \$([A-F0-9]{4})',lambda m:f' ORG ${bank*4096+int(m[1],16)-0xF000:04X}\n RORG ${m[1]}',s)
        out.append(s.replace(' END\n',''))
    return '\n'.join(out)+'\n END\n'

def assembly(indices,codes,mode,rows=()):
    data=values(indices,codes,mode,rows)
    return interlace_assembly(data) if mode==INTERLACE else f4_assembly(data,mode)

def binary(indices,codes,mode,rows=()):
    data=values(indices,codes,mode,rows);name=stem(mode)
    result=bytearray((DATA/(name+'.bin')).read_bytes());meta=json.loads((DATA/(name+'.json')).read_text())
    if hashlib.sha256(result).hexdigest()!=meta['sha256']:raise ValueError('Extended kernel template integrity failure')
    if mode==INTERLACE:
        for bank in range(2):result[bank*4096:bank*4096+2049]=data[bank]
    else:
        for bank in range(8):
            if bank==7:
                vals=data.get((7,0),[])
            else:vals=[v for y in range(64) for v in data.get((bank,y),[])]
            for item,value in enumerate(vals):result[meta['offsets'][f'P_{bank}_{item}']]=value
    return bytes(result)
