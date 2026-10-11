"""Single foreground/background with the BUS 128 kernel's fixed field coverage."""
from dataclasses import replace
import numpy as np
from .core import TIA,CODES,check_cancel
from .color import blend,distance
from .bus128_rom import STRIPS,validate

def palette(s):
    bg,fg=TIA[[CODES.index(s.codes[k]) for k in (3,0)]]
    return np.array([bg,blend([fg,bg])],dtype=np.uint8)

def coverage(phase):
    mask=np.zeros((200,128),bool)
    for parity in (0,1):
        for x in STRIPS[(parity+phase)%2]:mask[parity::2,x:x+8]=True
    return mask

def frames(indices,codes):
    a=validate(indices,codes)
    bg,fg=TIA[[CODES.index(codes[k]) for k in (3,0)]].astype(np.uint8)
    return [np.where((a.astype(bool)&coverage(f))[:,:,None],fg,bg) for f in range(2)]

def search(adjusted,s,progress=lambda p,t:None,cancel=None):
    from .modes import backgrounds
    flat=np.asarray(adjusted,dtype=np.float32).reshape(-1,3)
    _,inv,count=np.unique((flat//32).astype(int),axis=0,return_inverse=True,return_counts=True)
    colors=np.array([np.bincount(inv,weights=flat[:,c])/count for c in range(3)]).T
    weights=count/count.sum();bgs=backgrounds(s);best=(float('inf'),0,0)
    for n,bg in enumerate(bgs):
        check_cancel(cancel)
        mixed=blend(np.stack((TIA,np.broadcast_to(TIA[bg],TIA.shape))))
        fgerr=distance(mixed[:,None,:],colors[None,:,:])**2
        bgerr=distance(TIA[bg],colors)**2
        scores=np.minimum(fgerr,bgerr)@weights;fg=int(scores.argmin())
        if scores[fg]<best[0]:best=(float(scores[fg]),fg,bg)
        progress((n+1)/len(bgs),'Fitting one foreground color with the actual 50% pixel duty')
    return replace(s,codes=(CODES[best[1]],)*3+(CODES[best[2]],),line_codes=(),preset='Custom / optimized')
