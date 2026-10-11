"""Small, deterministic two-cluster match for the static Two Color mode.

Population-weighted Lab centroids, snapped to legal NTSC colors. This is a fast
approximation, not an exhaustive or dither-scored palette search. Dithering and
CIEDE2000 pixel matching still run normally for the final output.
"""
from dataclasses import replace
import numpy as np
from .core import TIA,CODES,MODES,prepare,check_cancel
from .color import rgb_to_lab

_ATARI_LAB=rgb_to_lab(TIA)


def search(image,s,progress=lambda p,t:None,cancel=None):
    check_cancel(cancel)
    if s.mode!=MODES[2]:raise ValueError('Fast two-color matching is for Two Color Static')
    # At most 512 weighted cells; every image pixel contributes to the means.
    pixels=np.asarray(image,dtype=float).reshape(-1,3)
    keys=np.minimum(pixels.astype(int)//32,7)
    ids=keys[:,0]*64+keys[:,1]*8+keys[:,2]
    counts=np.bincount(ids,minlength=512);used=counts>0
    colors=np.stack([np.bincount(ids,weights=pixels[:,k],minlength=512)[used]/counts[used] for k in range(3)],axis=1)
    weights=counts[used]/counts.sum();lab=rgb_to_lab(colors)
    errors=((lab[:,None,:]-_ATARI_LAB[None,:,:])**2).sum(axis=2)
    mean=np.sum(lab*weights[:,None],axis=0)
    far=int(np.argmax(((lab-mean)**2).sum(axis=1)*weights))
    other=int(np.argmax(((lab-lab[far])**2).sum(axis=1)*weights))
    seeds=((lab.argmin(axis=0)[0],lab.argmax(axis=0)[0]),(far,other))
    fixed={'Black':(0,),'Black or white':(0,CODES.index('0E')),'Any Atari color':(None,)}[s.background]
    best=None;trials=len(fixed)*3;done=0
    for bg in fixed:
        starts=[(int(errors[a].argmin()),int(errors[b].argmin())) for a,b in seeds]
        starts.append((CODES.index(s.codes[0]),CODES.index(s.codes[3])))
        for first,second in starts:
            pair=[first,second if bg is None else bg]
            for _ in range(8):
                check_cancel(cancel)
                before=tuple(pair)
                assigned=errors[:,pair].argmin(axis=1)
                for k in range(2 if bg is None else 1):
                    mask=assigned==k
                    if mask.any():
                        centroid=np.average(lab[mask],axis=0,weights=weights[mask])
                        scores=((_ATARI_LAB-centroid)**2).sum(axis=1)
                    else:
                        worst=int(np.argmax(errors[:,pair].min(axis=1)*weights))
                        scores=errors[worst].copy()
                    # Different visible colors, even when Atari codes alias black.
                    scores[np.all(TIA==TIA[pair[1-k]],axis=1)]=np.inf
                    pair[k]=int(scores.argmin())
                score=float(np.sum(errors[:,pair].min(axis=1)*weights))
                candidate=(score,*pair)
                if best is None or candidate<best:best=candidate
                if tuple(pair)==before:break
            done+=1;progress(done/trials,'Matching two representative colors')
    _,fg,bg=best
    return replace(s,codes=(CODES[fg],)*3+(CODES[bg],),line_codes=(),preset='Custom / optimized')


def fit_input(image,s,cancel=None,free_trim=False,reference=None):
    # Direct percentile-to-palette RGB fit; no repeated rendering or grid search.
    from .weighted_search import fit_input as direct_fit
    check_cancel(cancel)
    from .modes import convert_image
    from .optimization import neutral_reference,conversion_score
    base=replace(s,brightness_trim=1.) if free_trim else s
    fitted=direct_fit(image,base,cancel)
    reference=neutral_reference(image,base) if reference is None else reference
    # Compare only the direct fit and current controls, using actual dithering.
    # This protects detail without reopening the old multi-axis search.
    best=None;winner=base
    for candidate in (base,fitted):
        check_cancel(cancel)
        _,indices,candidate=convert_image(image,candidate,cancel)
        score=conversion_score(reference,indices,candidate)
        if best is None or score<best:best=score;winner=candidate
    return winner


def joint(image,s,progress=lambda p,t:None,cancel=None):
    from .weighted_search import neutral
    baseline=neutral(s)
    palette=search(prepare(image,baseline),baseline,lambda p,t:progress(p*.8,t),cancel)
    result=fit_input(image,palette,cancel,free_trim=True)
    check_cancel(cancel);progress(1.,'Two-color match and direct input fit complete')
    return result
