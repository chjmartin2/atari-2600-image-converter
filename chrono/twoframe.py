"""Jointly fitted pairs of real, hardware-constrained image frames."""
from dataclasses import replace
import numpy as np
from .color import blend,distance
from .core import CODES,TIA,MODES,Settings,check_cancel

BASES={MODES[12]:MODES[2],MODES[13]:MODES[4],MODES[14]:MODES[8],MODES[15]:MODES[9],MODES[16]:MODES[10]}
PAIR=np.array([[0,0],[0,1],[1,0],[1,1]]) # 0 foreground, 1 background

def validate_rows(s):
    h=128 if s.mode in MODES[12:14] else 192
    rows=s.line_codes
    if rows and (len(rows)!=h or any(len(r)!=8 or any(c not in CODES for c in r) for r in rows)):raise ValueError('Two-frame modes need two four-color palettes per row')
    if rows:
        for f in (0,4):
            if len({r[f+3] for r in rows})!=1:raise ValueError('Each sprite frame needs its own constant background')
            if s.mode in MODES[12:15] and any(r[f]!=r[f+1] or r[f]!=r[f+2] for r in rows):raise ValueError('This mode uses one foreground per row in each frame')
        if s.mode==MODES[12]:
            # Interleaving exchanges the same two global palettes between rows.
            # Different backgrounds still require a uniform assignment per frame.
            first=tuple(rows[0]);allowed={first}
            if first[3]==first[7]:allowed.add(first[4:]+first[:4])
            if any(tuple(r) not in allowed for r in rows):
                raise ValueError('Two Color requires the same two palettes, optionally exchanged between rows with a shared background')

def palette(s):
    h=128 if s.mode in MODES[12:14] else 192
    rows=s.line_codes or (tuple(s.codes)*2,)*h
    colors=TIA[[[CODES.index(c) for c in r] for r in rows]]
    component=(np.arange(48)//8)%2 if s.mode in MODES[15:17] else np.zeros(48,dtype=int)
    first=np.stack((colors[:,component],np.broadcast_to(colors[:,3,None],(h,48,3))),axis=2)
    second=np.stack((colors[:,component+4],np.broadcast_to(colors[:,7,None],(h,48,3))),axis=2)
    return blend([first[:,:,PAIR[:,0]],second[:,:,PAIR[:,1]]])

def split(indices,codes,rows,mode):
    s=Settings(mode=mode,codes=tuple(codes),line_codes=tuple(rows));validate_rows(s)
    a=np.asarray(indices);h=128 if mode in MODES[12:14] else 192
    if a.shape!=(h,48) or not np.issubdtype(a.dtype,np.integer) or np.any(a<0) or np.any(a>3):raise ValueError('Invalid two-frame pixel indices')
    rows=rows or (tuple(codes)*2,)*h
    return [(np.where(PAIR[a,f],7,0).astype(np.uint8),tuple(tuple(r[f*4:f*4+4]) for r in rows)) for f in range(2)]

def frames(indices,codes,rows,mode):
    result=[]
    for a,r in split(indices,codes,rows,mode):
        colors=TIA[[[CODES.index(c) for c in row] for row in r]]
        component=(np.arange(48)//8)%2 if mode in MODES[15:17] else np.zeros(48,dtype=int)
        result.append(np.where((a==0)[:,:,None],colors[:,component],colors[:,3,None]).astype(np.uint8))
    return result

def _fit(pixels,start,bgs,cancel,axes=(0,1,2,3),shared_bg=False):
    """Coordinate search of four real colors; four legal pairwise mixtures."""
    state=np.array(start,dtype=int);pixels=np.asarray(pixels,dtype=np.float32)
    if shared_bg:state[3]=state[1]
    for sweep in range(3):
        old=state.copy()
        for axis in axes:
            if shared_bg and axis==3:continue
            check_cancel(cancel)
            allowed=bgs if axis in (1,3) else range(128)
            batch=np.tile(state,(len(allowed),1));batch[:,axis]=allowed
            if shared_bg:batch[:,3]=batch[:,1]
            c=TIA[batch];p=blend([c[:,[0,0,1,1]],c[:,[2,3,2,3]]])
            error=(distance(pixels[None,:,None,:],p[:,None,:,:])**2).min(axis=2).mean(axis=1)
            state=batch[int(error.argmin())]
        if np.array_equal(state,old):break
    return state

def search(adjusted,s,progress,cancel):
    from .modes import backgrounds
    pixels=np.asarray(adjusted,dtype=np.float32);flat=pixels.reshape(-1,3);bgs=backgrounds(s)
    # Deterministic stratified sample keeps full-image palette fitting bounded.
    sample=flat[np.linspace(0,len(flat)-1,min(384,len(flat)),dtype=int)]
    nearest=distance(TIA[:,None],sample[None]).argmin(axis=0)
    u,count=np.unique(nearest,return_counts=True);dominant=u[np.argsort(count)[-min(4,len(u)):]]
    winner=None;best=float('inf')
    for fg in (dominant[-1],dominant[0]):
        v=_fit(sample,[fg,bgs[0],dominant[len(dominant)//2],bgs[-1]],bgs,cancel,shared_bg=s.balance_frames)
        c=TIA[v];p=blend([c[[0,0,1,1]],c[[2,3,2,3]]])
        error=(distance(sample[:,None],p)**2).min(axis=1).mean()
        if error<best:best,winner=error,v
    rows=[]
    for y,row in enumerate(pixels):
        check_cancel(cancel)
        groups=[row[(np.arange(48)//8)%2==k] for k in range(2)] if s.mode in MODES[15:17] else [row]
        fits=[winner if s.mode==MODES[12] else _fit(g,winner,bgs,cancel,axes=(0,2)) for g in groups]
        a,b=fits[0],fits[-1]
        rows.append(tuple(CODES[k] for k in (a[0],b[0],a[0],a[1],a[2],b[2],a[2],a[3])))
        if y%8==0:progress((y+1)/len(pixels),f'Fitting two-frame palettes: {y+1}/{len(pixels)}')
    return replace(s,line_codes=tuple(rows),codes=rows[len(rows)//2][:4],mapping='Temporal blend',preset='Custom / optimized')
