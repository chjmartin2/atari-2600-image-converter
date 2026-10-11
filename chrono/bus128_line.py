"""Per-row foreground fitting for the fixed 50%-duty BUS bitmap kernel."""
from dataclasses import replace
import numpy as np
from .core import CODES,TIA,check_cancel
from .color import blend,distance
from .bus128 import coverage
from .bus128_rom import validate
from .bus128_line_rom import rows_for

def palette(s):
    rows=rows_for(s.codes,s.line_codes)
    colors=TIA[[[CODES.index(r[k]) for k in (3,0)] for r in rows]]
    colors[:,1]=blend([colors[:,1],colors[:,0]])
    return np.rint(colors).astype(np.uint8)

def frames(indices,codes,line_codes=()):
    a=validate(indices,codes);rows=rows_for(codes,line_codes)
    colors=TIA[[[CODES.index(r[k]) for k in (3,0)] for r in rows]].astype(np.uint8)
    bg,fg=colors[:,0,None,:],colors[:,1,None,:]
    return [np.where((a.astype(bool)&coverage(f))[:,:,None],fg,bg) for f in range(2)]

def propose(adjusted,s,progress=lambda p,t:None,cancel=None,candidates=None):
    """Search every allowed background and every foreground independently per row.

    Weighted 32-level RGB histogram centroids bound perceptual-distance cost;
    row-specific counts retain each scanline's distribution. Background is shared.
    Both palette matching and previews use the actual half-duty temporal blend.
    """
    if s.bus_pair_rows:
        from .bus128_pairs import propose as paired_search
        return paired_search(adjusted,s,progress,cancel,candidates)
    from .modes import backgrounds
    check_cancel(cancel)
    pixels=np.asarray(adjusted,dtype=np.float32)
    if pixels.shape!=(200,128,3):raise ValueError('Expected a 128 x 200 RGB image')
    flat=pixels.reshape(-1,3)
    _,inv,count=np.unique((flat//32).astype(int),axis=0,return_inverse=True,return_counts=True)
    colors=np.array([np.bincount(inv,weights=flat[:,c])/count for c in range(3)]).T
    weights=np.zeros((len(count),200))
    np.add.at(weights,(inv,np.repeat(np.arange(200),128)),1/128)
    best=float('inf');winner=None;bgs=backgrounds(s);ranked=[]
    for n,bg in enumerate(bgs):
        check_cancel(cancel)
        mixed=blend(np.stack((TIA,np.broadcast_to(TIA[bg],TIA.shape))))
        fgerr=distance(mixed[:,None,:],colors[None,:,:])**2
        bgerr=distance(TIA[bg],colors)**2
        scores=np.minimum(fgerr,bgerr)@weights
        choices=scores.argmin(axis=0);score=float(scores[choices,np.arange(200)].mean())
        rows=tuple((CODES[f],)*3+(CODES[bg],) for f in choices)
        ranked.append((score,rows))
        order=np.argsort(scores,axis=0)
        alternate=tuple((CODES[f],)*3+(CODES[bg],) for f in order[1])
        ranked.append((float(scores[order[1],np.arange(200)].mean()),alternate))
        if score<best:best=score;winner=rows
        progress((n+1)/len(bgs),'Fitting 200 row colors and one shared background')
    if candidates is not None:
        candidates.extend(replace(s,line_codes=rows,codes=rows[100],preset='Custom / optimized') for _,rows in sorted(ranked,key=lambda v:v[0])[:8])
    return replace(s,line_codes=winner,codes=winner[100],preset='Custom / optimized')

def search(adjusted,s,progress=lambda p,t:None,cancel=None):
    """Use the shared scanline dither engine, with BUS half-duty colors.

    Every legal foreground is evaluated per row for each tested shared
    background. Background proposals remain whole-image candidates; the BUS
    kernel still requires a single background for all 200 rows.
    """
    if s.background=="Per line":raise ValueError("BUS Color per Line requires a shared background")
    from .scanline_search import raster
    from .color import srgb_to_linear
    from .modes import backgrounds
    from .bus128_pairs import distinct_rows
    candidates=[]
    initial=propose(adjusted,s,lambda p,t:progress(p*.15,t),cancel,candidates)
    source=srgb_to_linear(adjusted)
    allowed=backgrounds(s)
    # Same bounded shared-background strategy as Scanline Color. All foregrounds
    # are tested through actual dithering, never short-listed by the proposal.
    bgs=allowed if len(allowed)<=2 else list(dict.fromkeys(CODES.index(v.line_codes[0][3]) for v in [initial,*candidates]))[:2]
    if s.line_codes and CODES.index(s.line_codes[0][3]) in allowed:
        bg=CODES.index(s.line_codes[0][3])
        if bg not in bgs:bgs.append(bg)
    winner=None;best=float('inf')
    def retain(rows,score,settings=s):
        nonlocal winner,best
        if score<best:
            best=score;winner=replace(settings,line_codes=rows,codes=rows[100],preset='Custom / paired rows' if s.bus_pair_rows else 'Custom / optimized')
    # Baseline is evaluated with the SAME final dithering as the exhaustive rows.
    seeds=[initial]
    if s.line_codes and CODES.index(s.line_codes[0][3]) in allowed and (not s.bus_pair_rows or distinct_rows(s.line_codes)):seeds.append(s)
    for seed in seeds:
        _,rows,score=raster(source,s,lambda y,row:[(CODES.index(seed.line_codes[y][0]),CODES.index(seed.line_codes[y][3]))],cancel)
        retain(rows,score)
    for n,bg in enumerate(bgs):
        pairs=np.column_stack((np.arange(128),np.full(128,bg)))
        _,rows,score=raster(source,s,lambda y,row:pairs,cancel,
            lambda p,t:progress(.15+.8*(n+p)/len(bgs),'BUS '+t+' — every legal foreground'))
        retain(rows,score)
    winner.validate();progress(1,'BUS row colors selected with scanline dither-aware search')
    return winner
