"""Still frames in Rob Bairos's MovieCart stream format (MVC, not a ROM).

Format: lodefmode/moviecart firmware/frame.c, encoder/cpu/ColorizeTOP.cpp.
Each field streams five eight-pixel cells per scanline, alternating with the
other field's five cells. MovieCart hardware is required; this is not Harmony.
"""
import numpy as np
from .core import CODES, TIA

def validate(indices,rows):
    a=np.asarray(indices)
    if a.shape!=(192,80) or not np.issubdtype(a.dtype,np.integer) or np.any((a!=0)&(a!=7)):raise ValueError('MovieCart requires 80 x 192 foreground/background indices')
    if len(rows)!=192 or any(len(r)!=11 or any(c not in CODES for c in r) for r in rows):raise ValueError('MovieCart requires ten cell foreground colors and one background per row')
    if any(c!='00' for r in (rows[0],rows[-1]) for c in r) or rows[1][-1]!='00':raise ValueError('MovieCart needs black edge rows and a black background on the first content row')
    return a

def binary(indices,rows,seconds=30):
    a=validate(indices,rows)
    if not isinstance(seconds,int) or not 1<=seconds<=300:raise ValueError('MovieCart duration must be 1–300 seconds')
    fields=[]
    for phase in range(2):
        graph=[];colors=[]
        for raw_y in range(192):
            y=min(191,raw_y+phase)
            for cell in range(1-raw_y%2,10,2):
                graph.append(int((a[y,cell*8:cell*8+8]==0)@np.array([128,64,32,16,8,4,2,1])))
                colors.append(int(rows[y][cell],16) if 0<y<191 else 0)
        bg=bytes(int(r[10],16) for r in rows)
        fields.append(bytes(262)+bytes(graph)+bytes(60)+bytes(colors)+bg)
    out=bytearray()
    for n in range(seconds*60):
        header=b'MVC\0'+(n+2).to_bytes(3,'big')
        field=header+fields[n%2]
        out.extend(field+bytes(4096-len(field)))
    return bytes(out)

def frames(indices,rows):
    a=validate(indices,rows);result=[]
    colors=TIA[[[CODES.index(c) for c in r] for r in rows]].astype(np.uint8)
    yy,xx=np.indices(a.shape)
    for phase in range(2):
        on=(a==0)&((xx//8+yy+phase)%2==1)
        active=(xx//8+yy+phase)%2==1
        im=np.where(on[:,:,None],colors[yy,xx//8],colors[:,10,None,:])
        im=np.where(active[:,:,None],im,0);im[[0,-1]]=0
        result.append(im)
    return result
