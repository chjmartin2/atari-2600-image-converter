"""Joint foreground selection for non-overlapping BUS scanline pairs.

This module proposes baseline color tables from independently quantized rows.
Final search and conversion use scanline_search with horizontal and cross-row
diffusion, half-duty colors, and a distinct foreground on each paired row.
"""
from dataclasses import replace
import numpy as np
from .core import CODES,TIA,check_cancel
from .color import blend,distance,srgb_to_linear,linear_to_srgb

def pair_average(pixels):
    a=np.asarray(pixels)
    if a.shape[0]%2:raise ValueError('Paired rows require an even image height')
    return blend(a.reshape(a.shape[0]//2,2,*a.shape[1:]),axis=1)

def distinct_rows(rows):
    for y in range(0,len(rows),2):
        a,b,bg=(TIA[CODES.index(c)] for c in (rows[y][0],rows[y+1][0],rows[y][3]))
        if np.array_equal(a,b) or np.array_equal(a,bg) or np.array_equal(b,bg):return False
    return True

def _fit_pair(pixels,mixed,bg,row_scores,cancel,alternates=None):
    check_cancel(cancel)
    target=pair_average(pixels)[0]
    errors=distance(mixed[:,None,None,:],pixels[None,:,:,:])**2
    bgerr=distance(bg,pixels)**2
    on=errors<bgerr[None,:,:]
    row_error=np.minimum(errors,bgerr).mean(axis=2)
    # Include leading row fits, leading averaged-row fits and one best color
    # from every TIA hue family so similar adjacent rows can gain useful variety.
    avg_errors=np.minimum(distance(mixed[:,None,:],target[None,:,:])**2,distance(bg,target)**2).mean(axis=1)
    pooled=row_scores.mean(axis=1)
    candidates=list(np.argsort(row_error[:,0])[:4])+list(np.argsort(row_error[:,1])[:4])+list(np.argsort(avg_errors)[:4])
    for hue in range(16):
        ix=[i for i,c in enumerate(CODES) if int(c[0],16)==hue]
        candidates.append(ix[int(np.argmin(pooled[ix]))])
    unique=[];seen={tuple(bg)}
    for i in candidates:
        rgb=tuple(TIA[i])
        if rgb not in seen:unique.append(i);seen.add(rgb)
    ix=np.array(unique,dtype=int)
    # Every legal palette has many non-background colors; the hue shortlist
    # also guarantees at least two different physical RGB colors.
    if len(ix)<2:raise ValueError('No distinct foreground pair available')
    foreground=mixed[ix]
    upper=np.where(on[ix,0,:,None],foreground[:,None,:],bg)
    lower=np.where(on[ix,1,:,None],foreground[:,None,:],bg)
    combined=linear_to_srgb((srgb_to_linear(upper)[:,None]+srgb_to_linear(lower)[None,:])*.5)
    combined_error=(distance(combined,target[None,None,:,:])**2).mean(axis=2)
    individual=(row_error[ix,0,None]+row_error[ix,1][None,:])*.5
    scores=.8*combined_error+.2*individual
    np.fill_diagonal(scores,np.inf)
    a,b=np.unravel_index(scores.argmin(),scores.shape)
    if alternates is not None:
        # Second ordered pair gives the full dither loop another legal table.
        order=np.argsort(scores,axis=None)
        for k in order[1:]:
            c,d=np.unravel_index(int(k),scores.shape)
            if np.isfinite(scores[c,d]):
                alternates.append((int(ix[c]),int(ix[d]),float(scores[c,d])));break
    return int(ix[a]),int(ix[b]),float(scores[a,b])

def propose(adjusted,s,progress=lambda p,t:None,cancel=None,candidates=None):
    from .modes import backgrounds
    check_cancel(cancel)
    pixels=np.asarray(adjusted,dtype=np.float32)
    if pixels.shape!=(200,128,3):raise ValueError('Expected a 128 x 200 RGB image')
    flat=pixels.reshape(-1,3)
    _,inv,count=np.unique((flat//32).astype(int),axis=0,return_inverse=True,return_counts=True)
    colors=np.array([np.bincount(inv,weights=flat[:,c])/count for c in range(3)]).T
    weights=np.zeros((len(count),200))
    np.add.at(weights,(inv,np.repeat(np.arange(200),128)),1/128)
    bgs=backgrounds(s);ranked=[]
    for n,bg in enumerate(bgs):
        check_cancel(cancel)
        mixed=blend(np.stack((TIA,np.broadcast_to(TIA[bg],TIA.shape))))
        errors=np.minimum(distance(mixed[:,None,:],colors[None,:,:])**2,distance(TIA[bg],colors)**2)
        scores=errors@weights
        ranked.append((float(scores.min(axis=0).mean()),bg,mixed,scores))
        progress(.15*(n+1)/len(bgs),'Shortlisting shared backgrounds for paired rows')
    # All allowed backgrounds are screened. Expensive pair fitting uses the
    # four best global candidates; this is a bounded heuristic, not exhaustive.
    ranked=sorted(ranked,key=lambda v:(v[0],v[1]))[:4]
    best=float('inf');winner=None;tables=[]
    for n,(_,bg,mixed,row_scores) in enumerate(ranked):
        rows=[];total=0.;other=[];other_total=0.
        for y in range(0,200,2):
            alternatives=[]
            a,b,score=_fit_pair(pixels[y:y+2],mixed,TIA[bg],row_scores[:,y:y+2],cancel,alternatives)
            c,d,value=alternatives[0]
            other.extend(((CODES[c],)*3+(CODES[bg],),(CODES[d],)*3+(CODES[bg],)))
            other_total+=value
            rows.extend(((CODES[a],)*3+(CODES[bg],),(CODES[b],)*3+(CODES[bg],)))
            total+=score
            if y%4==0:progress(.15+.85*(n+(y+2)/200)/len(ranked),f'Fitting distinct row pairs: {y//2+1}/100')
        tables.extend(((total,tuple(rows)),(other_total,tuple(other))))
        if total<best:best=total;winner=tuple(rows)
    check_cancel(cancel);progress(1,'Paired rows: two distinct foregrounds per pair')
    if candidates is not None:
        candidates.extend(replace(s,line_codes=rows,codes=rows[100],preset='Custom / paired rows') for _,rows in sorted(tables,key=lambda v:v[0])[:8])
    return replace(s,line_codes=winner,codes=winner[100],preset='Custom / paired rows')

def search(adjusted,s,progress=lambda p,t:None,cancel=None):
    from .bus128_line import search as fitted_search
    return fitted_search(adjusted,replace(s,bus_pair_rows=True),progress,cancel)
