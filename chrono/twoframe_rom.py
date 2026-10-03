"""True alternating-frame F8, DPC+ and CDFJ+ cartridge exporters."""
import re,json,hashlib,struct
import numpy as np
from .core import MODES,DATA
from .drivers import restore
from .twoframe import split
from .sprite_rom import assembly as sprite_assembly,payload
from .bus_rom import byte_lines

def name(mode):return 'pair128' if mode in MODES[12:14] else 'pair192' if mode==MODES[14] else 'pair-dpc' if mode==MODES[15] else 'pair-cdfj'

def parts(indices,codes,rows,mode):
    stream=mode in MODES[15:17];result=[]
    for a,r in split(indices,codes,rows,mode):
        if len(a)==128:
            # Shared 256-byte table stride, but the short kernel counts 128..1.
            padded=np.full((192,48),7,dtype=np.uint8);padded[64:]=a
            r=(r[0],)*64+r;a=padded
        result.append(payload(a,r[0],r,stream))
    return result

def _body(data,kind):
    s=sprite_assembly(np.zeros((192,48),dtype=np.uint8),('00',)*4,kind=kind)
    if kind=='4K':
        first=s.index(' ORG $F000\n');end=s.index(' ORG $F900\n')
        s=s[:first]+' ORG $F000\n'+'\n'.join(byte_lines(data))+'\n'+s[end:]
    return s

def _cdf_thumb():
    # The 6507 places phase in communication byte 0 before CALLFN. Read it before
    # copying graphics over that byte. This modifies only the source pointer.
    # Build from the same explicit Thumb instructions with relocated literals.
    words=[];loads=[]
    def emit(v):words.append(v)
    def lit(r,v):loads.append((len(words),r,v));emit(0)
    emit(0xB410);lit(0,0x40000800);emit(0x7801);emit(0x02C9) # ldrb r1,[r0]; lsl r1,#11
    lit(2,0x2000);emit(0x1889);lit(2,512) # add r1,r1,r2
    loop=len(words)
    for v in (0x680C,0x6004,0x3104,0x3004,0x3A01):emit(v)
    emit(0xD100|((loop-len(words)-2)&255))
    lit(0,0x40000098);lit(1,0x40000124);emit(0x2200);lit(3,0x01000000);lit(4,0x100)
    for k in range(8):emit(0x6002|(k<<6));emit(0x600C|(k<<6));emit(0x18D2)
    emit(0xBC10);emit(0x4770)
    if len(words)%2:emit(0x46C0)
    pool=0x1800+2*len(words)
    for n,(pos,r,v) in enumerate(loads):words[pos]=0x4800|(r<<8)|((pool+4*n-((0x1800+2*pos+4)&~3))//4)
    return struct.pack('<'+'H'*len(words),*words)+b''.join(struct.pack('<I',v) for _,_,v in loads)

def assembly(indices,codes,mode,rows):
    data=parts(indices,codes,rows,mode)
    if mode in MODES[12:15]:
        out=['; Atari 2600 Image Optimizer: two actual alternating NTSC frames / F8 / 8 KiB']
        for bank in range(2):
            s=_body(data[bank],'4K')
            if bank:s=s[s.index(' ORG $F000'):]
            if mode in MODES[12:14]:
                s=s.replace(' ldy #192',' ldy #128').replace(' ldx #27',' ldx #59')
                s=s.replace(' sta VBLANK\n sta WSYNC\n ldy',' sta VBLANK\n ldx #32\nTop\n sta WSYNC\n dex\n bne Top\n sta WSYNC\n ldy')
            s=s.replace(' jmp Frame',' jmp $FF80').replace(' ORG $FFFA',f' ORG $FF80\n bit ${0xFFF9 if bank==0 else 0xFFF8:04X}\n jmp Frame\n ORG $FFFA')
            for label in ('Draw','Reset','Clear','Frame','Blank','Over','EndPicture','Top'):
                s=re.sub(r'\b'+label+r'\b',label+str(bank),s)
            s=re.sub(r' ORG \$([A-F0-9]{4})',lambda m:f' ORG ${bank*4096+int(m[1],16)-0xF000:04X}\n RORG ${m[1]}',s)
            out.append(s.replace(' END\n',''))
        return '\n'.join(out)+ '\n END\n'
    kind='DPC+' if mode==MODES[15] else 'CDFJ+'
    s=_body(data[0],kind)
    s=s.replace(' jmp Frame',' lda phase\n eor #1\n sta phase\n jmp Frame')
    if kind=='DPC+':
        start=s.index(' lda #0\n sta $1050',s.index('\nFrame\n'));end=s.index(' ldx #36',start)
        init=[]
        for k in range(8):init+=[' lda #0',f' sta ${0x1050+k:04X}',' lda phase',' asl',' asl',' asl',f' ora #{k}',f' sta ${0x1068+k:04X}']
        init+=[' ldx phase',' lda $F700,x',' sta COLUBK']
        s=s[:start]+'\n'.join(init)+'\n'+s[end:]
        s=s.replace(' ldx #36',' ldx #35')
        s=s.replace(' ORG $6BFA',' ORG $6300\n RORG $F700\n'+ '\n'.join(byte_lines(bytes([data[0][-1],data[1][-1]])))+'\n ORG $6BFA')
        start=s.index(' ORG $6C00');end=s.index(' ORG $7FFF',start)
        s=s[:start]+' ORG $6C00\n RORG $0000\n'+'\n'.join(byte_lines(data[0][:2048]+data[1][:2048]))+'\n'+s[end:]
    else:
        s=s.replace(' lda #$FF\n sta $1FF3',' lda #0\n sta $1FF1\n sta $1FF1\n lda phase\n sta $1FF0\n lda #$FF\n sta $1FF3')
        s=s.replace(' lda $F700\n',' ldx phase\n lda $F700,x\n')
        start=s.index(' ORG $0F00');end=s.index(' ORG $17F0',start)
        s=s[:start]+' ORG $0F00\n RORG $F700\n'+'\n'.join(byte_lines(bytes([data[0][-1],data[1][-1]])))+'\n'+s[end:]
        start=s.index(' ORG $1800');end=s.index(' ORG $7FFF',start)
        s=s[:start]+' ORG $1800\n RORG $1800\n'+'\n'.join(byte_lines(_cdf_thumb()))+'\n ORG $2000\n'+'\n'.join(byte_lines(data[0][:2048]+data[1][:2048]))+'\n'+s[end:]
    return '; Atari 2600 Image Optimizer: two actual alternating frames\n'+s

def binary(indices,codes,mode,rows):
    data=parts(indices,codes,rows,mode);stem=name(mode)
    result=bytearray((DATA/(stem+'.bin')).read_bytes());meta=json.loads((DATA/(stem+'.json')).read_text())
    if hashlib.sha256(result).hexdigest()!=meta['sha256']:raise ValueError('Two-frame template integrity failure')
    if mode in MODES[12:15]:
        for f in range(2):result[f*4096:f*4096+2049]=data[f]
    else:
        offset=0x6C00 if mode==MODES[15] else 0x2000
        result[offset:offset+4096]=data[0][:2048]+data[1][:2048]
        bg=0x6300 if mode==MODES[15] else 0xF00
        result[bg:bg+2]=bytes([data[0][-1],data[1][-1]])
    if mode in MODES[15:]:restore(result,'dpcplus' if mode==MODES[15] else 'cdfjplus')
    return bytes(result)
