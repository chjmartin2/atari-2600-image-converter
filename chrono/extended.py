"""Constrained spatial detail and field-interleaved image formats.

Hybrid rows contain four TIA colors followed by two hexadecimal sprite positions.
The two positions and sprite colors are shared across the image. Keeping them in
the saved row table makes every export reproducible without external state.
"""
from dataclasses import replace
import numpy as np
from PIL import Image
from .color import blend,dim,distance,rgb_to_lab,delta_e_2000
from .core import Settings,MODES,CODES,TIA,dimensions,quantize,check_cancel

HYBRID,WIDE,INTERLACE=MODES[17:20]
NOTES={
 HYBRID:'40 coarse playfield pixels + two 8-pixel detail windows; positions/colors fitted to the image. Hardware untested.',
 WIDE:'96 columns across two alternating fields; 48 are drawn per field. Fixed spatial interleaving; hardware untested.',
 INTERLACE:'384 image rows in two 192-row fields; half-line vertical sync. Experimental: CRT/display compatibility needs testing.'}

def rows_for(s):
    h=dimensions(s)[1]
    return s.line_codes or ((s.codes+('38','68')) if s.mode==HYBRID else (s.codes[0],)*3+(s.codes[3],),)*h

def validate_rows(s):
    rows=rows_for(s);hybrid=s.mode==HYBRID
    if len(rows)!=dimensions(s)[1] or any(len(r)!=(6 if hybrid else 4) or any(c not in CODES for c in r[:4]) for r in rows):
        raise ValueError('Invalid extended-mode row table')
    if hybrid:
        try:p0,p1=(int(v,16) for v in rows[0][4:])
        except (ValueError,TypeError):raise ValueError('Invalid sprite positions') from None
        if not (32<=p0<=144 and max(48,p0+8)<=p1<=152):raise ValueError('Sprite windows must not overlap and must fit the timed kernel')
        if any(r[1:3]!=rows[0][1:3] or r[4:]!=rows[0][4:] for r in rows):raise ValueError('Hybrid sprite colors and positions must be constant')
    elif any(r[0]!=r[1] or r[1]!=r[2] for r in rows):raise ValueError('One foreground color is allowed per row')
    if s.mode==INTERLACE and len({r[3] for r in rows})!=1:raise ValueError('Interlace requires a shared background')

def colors(s):return TIA[[[CODES.index(c) for c in r[:4]] for r in rows_for(s)]]

def palette(s):
    c=colors(s)
    if s.mode==HYBRID:return c[:,[3,0,1,2]].astype(np.uint8)
    p=c[:,[3,0]].copy()
    if s.mode==WIDE:p[:,1]=blend([p[:,1],p[:,0]])
    else:p=dim(p,.5)
    return np.rint(p).astype(np.uint8)

def convert(image,s,cancel=None):
    if s.mode!=HYBRID:return quantize(image,palette(s),s.dither,s.strength,s.serpentine,cancel)
    a=np.asarray(image,dtype=np.float32);p=palette(s)
    # Quantize each four-clock PF cell as one indivisible pixel. Sprites may then
    # cover individual clocks within their two windows; never invent illegal PF bits.
    coarse=blend(a.reshape(192,40,4,3),axis=2)
    pf=quantize(coarse,p[:,:2],s.dither,s.strength,s.serpentine,cancel)
    out=np.repeat(pf,4,axis=1);yy=np.arange(192)[:,None]
    for k,x in enumerate(int(v,16) for v in rows_for(s)[0][4:]):
        base=p[yy,out[:,x:x+8]]
        choices=np.stack((base,np.broadcast_to(p[:,k+2,None,:],base.shape)),axis=2)
        cover=quantize(a[:,x:x+8],choices,s.dither,s.strength,s.serpentine,cancel)
        out[:,x:x+8]=np.where(cover,k+2,out[:,x:x+8])
    return out.astype(np.uint8)

def validate_indices(a,s):
    validate_rows(s)
    if a.shape!=dimensions(s)[::-1] or not np.issubdtype(a.dtype,np.integer) or np.any(a<0) or np.any(a>(3 if s.mode==HYBRID else 1)):
        raise ValueError('Invalid extended-mode bitmap')
    if s.mode==HYBRID:
        for k,x in enumerate(int(v,16) for v in rows_for(s)[0][4:]):
            valid=np.zeros(a.shape,bool);valid[:,x:x+8]=True
            if np.any((a==k+2)&~valid):raise ValueError('Sprite pixels lie outside their window')
        cells=a.reshape(192,40,4)
        if np.any((cells==0).any(axis=2)&(cells==1).any(axis=2)):
            raise ValueError('Uncovered playfield pixels in each four-clock cell must agree')

def frames(indices,codes,rows,mode):
    s=Settings(mode=mode,codes=tuple(codes),line_codes=tuple(rows))
    a=np.asarray(indices);validate_indices(a,s);c=colors(s).astype(np.uint8)
    yy=np.arange(a.shape[0])[:,None]
    if mode==HYBRID:
        im=c[:,[3,0,1,2]][yy,a]
        return [im.copy() for _ in range(3)]
    im=c[:,[3,0]][yy,a]
    if mode==WIDE:
        mask=(np.arange(96)//16)%2
        return [np.where((mask==f)[None,:,None],im,c[:,3,None,:]).astype(np.uint8) for f in range(2)]
    return [np.where((np.arange(384)%2==f)[:,None,None],im,0).astype(np.uint8) for f in range(2)]

def search(adjusted,s,progress=lambda p,t:None,cancel=None):
    from .modes import backgrounds,best_pair,search_sprite_palette
    a=np.asarray(adjusted,dtype=np.float32);bgs=backgrounds(s)
    if s.mode==INTERLACE:
        # Each logical row is illuminated on alternate fields. One shared BG.
        r=search_sprite_palette(a,replace(s,mode=MODES[8]),progress,cancel,duty=.5)
        return replace(r,mode=INTERLACE)
    rows=[]
    if s.mode==HYBRID:
        coarse=blend(a.reshape(192,40,4,3),axis=2)
        for y,row in enumerate(coarse):
            check_cancel(cancel);fg,bg=best_pair(row,bgs)
            rows.append((CODES[fg],s.codes[1],s.codes[2],CODES[bg],'38','68'))
        trial=replace(s,line_codes=tuple(rows),codes=rows[96][:4])
        p=palette(trial);q=quantize(coarse,p[:,:2],'None')
        base=p[np.arange(192)[:,None],q];base=np.repeat(base,4,axis=1)
        error=distance(a,base)**2
        gain=np.empty((128,160),dtype=np.float64)
        for k,c in enumerate(TIA):
            check_cancel(cancel)
            gain[k]=np.maximum(0,error-distance(a,c)**2).sum(axis=0)
        sums=np.pad(np.cumsum(gain,axis=1),((0,0),(1,0)))
        windows=sums[:,8:]-sums[:,:-8];which=windows.argmax(axis=0);score=windows.max(axis=0)
        best=(-1,None)
        for p0 in range(32,145):
            for p1 in range(max(48,p0+8),153):
                value=score[p0]+score[p1]
                if value>best[0]:best=value,(p0,p1)
        p0,p1=best[1]
        rows=[(r[0],CODES[which[p0]],CODES[which[p1]],r[3],f'{p0:02X}',f'{p1:02X}') for r in rows]
    else:
        # Wide interleaving alternates FG with BG, not black: evaluate its actual
        # average, including the common background, for every legal color pair.
        bg=TIA[bgs];mix=blend(np.broadcast_arrays(TIA[:,None,:],bg[None,:,:]))
        # Many pairs have identical blends (including A/B versus B/A). Evaluate
        # each distinct mixture once, then restore every legal pair for ranking.
        # This preserves exhaustive results and limits DE00 temporary memory.
        unique,inverse=np.unique(mix.reshape(-1,3),axis=0,return_inverse=True)
        mix_lab=rgb_to_lab(unique);bg_lab=rgb_to_lab(bg)
        for y,row in enumerate(a):
            check_cancel(cancel)
            row_lab=rgb_to_lab(row)
            errors=np.empty((len(unique),len(row)))
            for k in range(0,len(unique),512):
                check_cancel(cancel)
                errors[k:k+512]=delta_e_2000(mix_lab[k:k+512,None,:],row_lab)**2
            fgerr=errors[inverse].reshape(128,len(bgs),len(row))
            bgerr=delta_e_2000(bg_lab[:,None,:],row_lab)**2
            scores=np.minimum(fgerr,bgerr[None,:,:]).mean(axis=2)
            fg,b=np.unravel_index(scores.argmin(),scores.shape)
            rows.append((CODES[fg],)*3+(CODES[bgs[b]],))
            if y%8==0:progress((y+1)/192,'Fitting spatially interleaved colors')
    progress(1,'Spatial palette fitted')
    return replace(s,line_codes=tuple(rows),codes=rows[len(rows)//2][:4],mapping='Temporal blend',preset='Custom / optimized')
