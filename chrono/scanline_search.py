"""Dither-aware two-color rows; final conversion uses the exact search renderer."""
from dataclasses import replace
from concurrent.futures import ThreadPoolExecutor
import numpy as np
from .core import CODES,TIA,KERNELS,BUS128LINE,check_cancel,bayer
from .color import srgb_to_linear,linear_to_srgb,linear_to_lab,delta_e_2000

BACKGROUNDS=('Black','White','Any Atari color','Per line')
LIGHT=srgb_to_linear(TIA)
BUS_LIGHT=srgb_to_linear(linear_to_srgb((LIGHT[:,None,:]+LIGHT[None,:,:])*.5))
WEIGHT=np.array([.30,.59,.11])
ALL_PAIRS=np.column_stack(np.triu_indices(len(CODES)))
ALL_PAIRS.setflags(write=False)


def display_pairs(pairs,s):
    palettes=LIGHT[pairs].copy()
    if s.mode==BUS128LINE:
        palettes[:,0]=BUS_LIGHT[pairs[:,0],pairs[:,1]]
    return palettes


def smooth(a):
    p=np.pad(a,[(0,0)]*(a.ndim-2)+[(1,1),(0,0)],mode='edge')
    return (p[...,:-2,:]+2*p[...,1:-1,:]+p[...,2:,:])/4


def row_score(source,output,dithered):
    # Judge dither texture at viewing scale without rewarding loss of edges.
    point=np.mean((delta_e_2000(linear_to_lab(source),linear_to_lab(output))/100)**2,axis=-1)
    if not dithered:return point
    spatial=np.mean((delta_e_2000(linear_to_lab(smooth(source)),linear_to_lab(smooth(output)))/100)**2,axis=-1)
    lum=np.array([.2126,.7152,.0722])
    edge=np.mean((np.diff(smooth(source)@lum,axis=-1)-np.diff(smooth(output)@lum,axis=-1))**2,axis=-1)
    return .2*point+.8*spatial+.1*edge


def pair_screen(row,enabled):
    """Cheap shortlist of all legal pairs using their linear-light mixture range.

    This is only a shortlist, not an exhaustive dither optimum. All finalists
    go through the selected dither and inherited scanline error below.
    """
    bg=LIGHT[None,:,:];fg=LIGHT[:,None,:];direction=fg-bg
    norm=np.sum(direction*direction*WEIGHT,axis=2)
    score=np.zeros((128,128))
    for pixel in row:
        delta=pixel-bg
        if enabled:
            t=np.clip(np.sum(delta*direction*WEIGHT,axis=2)/np.maximum(norm,1e-20),0,1)
            error=delta-t[:,:,None]*direction
            score+=np.sum(error*error*WEIGHT,axis=2)
        else:
            score+=np.minimum(np.sum((pixel-LIGHT)**2*WEIGHT,axis=1)[:,None],
                              np.sum((pixel-LIGHT)**2*WEIGHT,axis=1)[None,:])
    return score/len(row)


def evaluate_row(row,incoming,pairs,s,y,cancel=None,previous=None):
    """Independent trial buffers; returns errors without committing any candidate."""
    check_cancel(cancel)
    w=len(row)
    diffuse=s.dither in KERNELS and s.strength>0
    ordered=s.dither.startswith('Ordered') and s.strength>0
    enabled=diffuse or ordered
    if ordered:matrix=bayer(int(s.dither.split()[1][0]))+.5
    palettes=display_pairs(pairs,s);labs=linear_to_lab(palettes);n=len(pairs)
    out=np.empty((n,w),np.uint8);future=np.zeros((n,2,w,3))
    if diffuse:
        bg=palettes[:,1,None,:];direction=palettes[:,0,None,:]-bg
        amount=np.clip(np.sum((row-bg)*direction,axis=2)/np.maximum(np.sum(direction*direction,axis=2),1e-20),0,1)
        work=bg+amount[:,:,None]*direction+incoming
        denom,kernel=KERNELS[s.dither]
        black=np.all(palettes==0,axis=2);original_black=np.all(row==0,axis=1)
        order=range(w-1,-1,-1) if s.serpentine and y%2 else range(w)
        for x in order:
            check_cancel(cancel)
            old=work[:,x].copy()
            dist=delta_e_2000(linear_to_lab(np.clip(old,0,1))[:,None,:],labs)
            chosen=dist.argmin(axis=1)
            protected=original_black[x]&black.any(axis=1)
            chosen=np.where(protected,black.argmax(axis=1),chosen)
            out[:,x]=chosen
            error=(old-palettes[np.arange(n),chosen])*s.strength/denom
            error[protected]=0
            for dx,dy,weight in kernel:
                xx=x+(-dx if s.serpentine and y%2 else dx)
                if 0<=xx<w:
                    if dy==0:work[:,xx]+=error*weight
                    else:future[:,dy-1,xx]+=error*weight
    else:
        distances=delta_e_2000(linear_to_lab(row)[None,:,None,:],labs[:,None,:,:])
        out=distances.argmin(axis=2).astype(np.uint8)
        if ordered:
            first=palettes[np.arange(n)[:,None],out];second=palettes[np.arange(n)[:,None],1-out]
            direction=second-first
            fraction=np.clip(np.sum((row-first)*direction,axis=2)/np.maximum(np.sum(direction*direction,axis=2),1e-20),0,1)
            threshold=matrix[y%len(matrix),np.arange(w)%len(matrix)]
            out=np.where(fraction*s.strength>threshold,1-out,out).astype(np.uint8)
    if s.mode==BUS128LINE:
        # BUS index zero is background; identical displayed colors stay off.
        out=np.where(np.all(palettes[:,0]==palettes[:,1],axis=1)[:,None],1,out).astype(np.uint8)
    colors=palettes[np.arange(n)[:,None],out]
    scores=row_score(row,colors,enabled)
    if previous is not None:
        previous_source,previous_output=previous
        scores=.2*scores+.8*row_score((row+previous_source)*.5,(colors+previous_output)*.5,enabled)
    return out,future,scores


def raster(source,s,choose,cancel=None,progress=lambda p,t:None):
    """Evaluate row candidates with identical incoming errors, commit winner only.

    Gamut projection, signed diffusion, pure black protection, ordered matrix
    phase and serpentine direction are shared by optimization and conversion.
    """
    source=np.asarray(source,dtype=np.float64);h,w=source.shape[:2]
    carry=np.zeros((h+2,w,3));indices=np.empty((h,w),np.uint8);rows=[];total=0.
    paired=s.mode==BUS128LINE and s.bus_pair_rows
    previous_output=None
    with ThreadPoolExecutor(max_workers=4,thread_name_prefix="scanline-pairs") as pool:
        for y in range(h):
            check_cancel(cancel)
            pairs=np.asarray(choose(y,source[y]+carry[y]),dtype=np.intp).reshape(-1,2)
            if paired and len(pairs)>1:
                valid=np.any(TIA[pairs[:,0]]!=TIA[pairs[:,1]],axis=1)
                if y%2:valid &= np.any(TIA[pairs[:,0]]!=TIA[CODES.index(rows[-1][0])],axis=1)
                pairs=pairs[valid]
                if not len(pairs):raise ValueError('No legal distinct foreground for paired BUS row')
            previous=(source[y-1],previous_output) if paired and y%2 else None
            def trial(bounds):
                lo,hi=bounds
                out,future,scores=evaluate_row(source[y],carry[y],pairs[lo:hi],s,y,cancel,previous)
                best=int(np.argmin(scores))
                return float(scores[best]),lo+best,out[best].copy(),future[best].copy()
            if len(pairs)>1024:
                bounds=np.linspace(0,len(pairs),5,dtype=int)
                candidates=list(pool.map(trial,zip(bounds[:-1],bounds[1:])))
                score,winner,out,future=min(candidates,key=lambda t:t[0])
            else:score,winner,out,future=trial((0,len(pairs)))
            total+=score
            fg,bg=map(int,pairs[winner]);rows.append((CODES[fg],)*3+(CODES[bg],))
            indices[y]=np.where(out==0,0,7)
            carry[y+1:y+3]+=future
            previous_output=display_pairs(pairs[winner:winner+1],s)[0,out]
            if y%8==0 or y==h-1:progress((y+1)/h,f'Testing scanline colors with {s.dither}: {y+1}/{h}'+(f' — all {len(pairs):,} pairs' if len(pairs)>1024 else ''))
    return indices,tuple(rows),total/h


def convert(adjusted,s,cancel=None):
    rows=s.line_codes or (s.codes,)*adjusted.height
    pairs=[(CODES.index(r[0]),CODES.index(r[3])) for r in rows]
    indices=raster(srgb_to_linear(adjusted),s,lambda y,row:[pairs[y]],cancel)[0]
    return (indices==0).astype(np.uint8) if s.mode==BUS128LINE else indices


def search(adjusted,s,progress=lambda p,t:None,cancel=None):
    source=srgb_to_linear(adjusted);h=len(source)
    enabled=s.dither!='None' and s.strength>0
    screens=[];point_screens=[]
    for y,row in enumerate(source):
        check_cancel(cancel);screens.append(pair_screen(row,enabled) if s.background=="Any Atari color" else None)
        distances=delta_e_2000(linear_to_lab(row)[None,:,:],linear_to_lab(LIGHT)[:,None,:])**2
        point_screens.append(np.minimum(distances[:,None,:],distances[None,:,:]).mean(axis=2))
        if y%8==0:progress(.25*(y+1)/h,f'Screening foreground/background pairs: {y+1}/{h}')
    white=CODES.index('0E');black=CODES.index('00')
    if s.background=='Black':backgrounds=[black]
    elif s.background=='White':backgrounds=[white]
    elif s.background=='Black or white':backgrounds=[black,white] # old saved projects
    elif s.background=='Per line':backgrounds=[None]
    else:
        scores=np.sum([a.min(axis=0) for a in screens],axis=0)
        backgrounds=list(np.argsort(scores)[:2])
        if s.line_codes and len({r[3] for r in s.line_codes})==1:
            current=CODES.index(s.line_codes[0][3])
            if current not in backgrounds:backgrounds.append(current)
    winner=None;best=float('inf')
    for run,bg in enumerate(backgrounds):
        def choose(y,incoming):
            if bg is None:return ALL_PAIRS
            pairs=[(int(f),int(bg)) for f in range(128)]
            # Keep the current legal table in the dither candidates.
            if s.line_codes:
                r=s.line_codes[y];pair=(CODES.index(r[0]),CODES.index(r[3]))
                if bg is None or pair[1]==bg:pairs.append(pair)
            return list(dict.fromkeys(pairs))
        # The old nearest-solid-color table is a full-raster baseline. Greedy
        # row choices can change later diffusion, so retain this whole candidate.
        baseline=[]
        for scores in point_screens:
            if bg is None:fg,b=np.unravel_index(scores.argmin(),scores.shape)
            else:fg,b=int(scores[:,bg].argmin()),int(bg)
            baseline.append((fg,b))
        _,rows,score=raster(source,s,lambda y,row:[baseline[y]],cancel)
        if score<best:best,winner=score,replace(s,line_codes=rows,codes=rows[h//2],preset='Custom / optimized',mapping='Temporal blend')
        ix,rows,score=raster(source,s,choose,cancel,lambda p,t:progress(.25+.7*(run+p)/len(backgrounds),t))
        if score<best:best,winner=score,replace(s,line_codes=rows,codes=rows[h//2],preset='Custom / optimized',mapping='Temporal blend')
    # Retain the entire existing legal raster if greedy choices lose globally.
    if s.line_codes:
        oldb={r[3] for r in s.line_codes}
        valid=(s.background=='Per line' or (len(oldb)==1 and (s.background=='Any Atari color' or oldb=={'00'} and s.background in ('Black','Black or white') or oldb=={'0E'} and s.background in ('White','Black or white'))))
        if valid:
            _,_,score=raster(source,s,lambda y,row:[(CODES.index(s.line_codes[y][0]),CODES.index(s.line_codes[y][3]))],cancel)
            if score<best:winner=s
    progress(1,'Scanline colors selected from the actual dithered output')
    return winner
