"""Hardware-constrained palettes and conversion for all output modes."""
from dataclasses import replace
import numpy as np
from .color import blend,distance,dim
from .core import (Settings,MODES,BUS128,BUS128LINE,PRESETS,CODES,TIA,prepare,target_palette,quantize,
                   hardware_palette,frame_pixels,optimize,optimize_legacy,SEARCHES,check_cancel,_score)

def normalize(s):
    if s.mode==MODES[1] and s.search!=SEARCHES[0]:s=replace(s,search=SEARCHES[0])
    if s.mapping != "Temporal blend":s=replace(s,mapping="Temporal blend")
    if s.mode==MODES[7]:return replace(s,line_codes=(),mapping='Temporal blend',preset='Full NTSC palette')
    if s.mode==MODES[0]:
        return replace(s,codes=PRESETS['RGB (original Chronocolour)'],line_codes=(),mapping='Temporal blend',preset='RGB (original Chronocolour)')
    if s.mode in (MODES[2],BUS128):
        return replace(s,codes=(s.codes[0],)*3+(s.codes[3],),line_codes=(),mapping='Temporal blend')
    return s

def render(indices,s):
    return blend(frame_pixels(indices,s.codes,s.line_codes,s.mode))

def convert_image(image,s,cancel=None):
    s=normalize(s)
    adjusted=prepare(image,s)
    if s.mode==MODES[4] and not s.line_codes:
        bg="00" if s.background=="Black" else "0E" if s.background=="White" else s.codes[3]
        row=(s.codes[0],)*3+(bg,)
        s=replace(s,codes=row,line_codes=(row,)*adjusted.height)
    if s.mode==MODES[3] and not s.line_codes:
        # Selecting the mode must not launch an image-specific palette search.
        # A legal starter table retains the current colors at either height.
        check_cancel(cancel)
        s=replace(s,line_codes=(tuple(s.codes),)*adjusted.height)
    if s.mode!=BUS128 and s.mode in (*MODES[3:7],*MODES[8:]) and not s.line_codes:
        s=search_palette(adjusted,s,cancel=cancel)
    from .temporal import canonicalize
    s=canonicalize(s)
    if s.mode in MODES[17:20]:
        from .extended import convert
        return adjusted,convert(adjusted,s,cancel),s
    if s.mode in (MODES[4],BUS128LINE):
        from .scanline_search import convert
        return adjusted,convert(adjusted,s,cancel),s
    indices=quantize(adjusted,target_palette(s),s.dither,s.strength,s.serpentine,cancel)
    # Duplicate palette entries must never accidentally produce temporal shades.
    if s.mode in (MODES[2],*MODES[4:7],*MODES[8:12]):indices=np.where(indices==7,7,0).astype(np.uint8)
    from .temporal import interleave
    indices,s=interleave(indices,s,cancel)
    return adjusted,indices,s

def backgrounds(s):
    return {'Black':[0],'Black or white':[0,112],'Any Atari color':list(range(128)),'Any color by line':list(range(128))}[s.background]

def best_pair(pixels,bgs):
    # All foregrounds x allowed backgrounds; distances computed just once.
    errors=distance(pixels[None,:,:],TIA[:,None,:])**2
    scores=np.minimum(errors[:,None,:],errors[bgs][None,:,:]).mean(axis=2)
    fg,bg=np.unravel_index(scores.argmin(),scores.shape)
    return int(fg),bgs[bg]

def search_palette(adjusted,s,progress=lambda p,t:None,cancel=None):
    s=normalize(s);check_cancel(cancel)
    if s.mode==MODES[4]:
        from .scanline_search import search
        return search(adjusted,s,progress,cancel)
    if s.mode==BUS128LINE:
        from .bus128_line import search
        return search(adjusted,s,progress,cancel)
    if s.mode==BUS128:
        from .bus128 import search
        return search(adjusted,s,progress,cancel)
    if s.mode in MODES[17:20]:
        from .extended import search
        return search(adjusted,s,progress,cancel)
    if s.mode==MODES[7]:
        progress(1,'BUS uses all 128 NTSC colors; no restricted palette to search')
        return s
    if s.mode==MODES[0]:return s
    pixels=np.asarray(adjusted,dtype=np.float32)
    if s.mode in MODES[12:17]:
        from .twoframe import search
        return search(adjusted,s,progress,cancel)
    if s.mode in MODES[8:]:return search_sprite_palette(pixels,s,progress,cancel)
    if s.mode==MODES[2]:
        from .two_color_match import search
        return search(adjusted,s,progress,cancel)
    if s.mode==MODES[6]:
        rows=[];bgs=backgrounds(s)
        for y,row in enumerate(pixels):
            check_cancel(cancel)
            left=best_pair(row[:19],bgs);right=best_pair(row[20:],bgs)
            rows.append(tuple(CODES[c] for c in (*left,*right)))
            if y%8==0:progress((y+1)/len(pixels),f'Fitting Playfield Plus halves: {y+1}/{len(pixels)}')
        return replace(s,line_codes=tuple(rows),codes=rows[len(rows)//2],mapping='Temporal blend',preset='Custom / optimized')
    if s.mode in MODES[3:]:
        rows=[];bgs=backgrounds(s)
        # Chronocolor can fit all four row colors; other sprite modes share BG.
        row_background=s.mode==MODES[3] and s.background=='Any color by line'
        bg=bgs[0]
        if s.mode!=MODES[5] and not row_background and len(bgs)>1:
            # Choose a legal shared background before fitting individual rows.
            global_codes,_=optimize_legacy(adjusted,replace(s,mode=MODES[1],line_codes=(),auto_input=False,search='Improved weighted'),progress,cancel)
            bg=CODES.index(global_codes[3])
        previous=np.array([CODES.index(c) for c in s.codes]);previous[3]=bg
        for y,row in enumerate(pixels):
            check_cancel(cancel)
            if s.mode in MODES[4:]:
                fg,k=best_pair(row,bgs if s.mode==MODES[5] else [bg])
                codes=(CODES[fg],)*3+(CODES[k],)
            else:
                weights=np.full(len(row),1/len(row));best=float('inf');winner=None
                nearest=distance(TIA[:,None,:],row[None,:,:]).argmin(axis=0)
                unique,counts=np.unique(nearest,return_counts=True)
                dominant=list(unique[np.argsort(counts)[-3:]])
                while len(dominant)<3:dominant.append(dominant[-1])
                for start in (previous,np.array([*dominant,dominant[-1] if row_background else bg])):
                    current=start.copy()
                    for sweep in range(3):
                        old=current.copy()
                        for axis in range(4 if row_background else 3):
                            check_cancel(cancel)
                            batch=np.tile(current,(128,1));batch[:,axis]=np.arange(128)
                            scores=_score(batch,row,weights)
                            current=batch[int(scores.argmin())]
                        if np.array_equal(old,current):break
                    score=float(_score([current],row,weights)[0])
                    if score<best:best,winner=score,current.copy()
                previous=winner;codes=tuple(CODES[c] for c in winner)
            rows.append(codes)
            if y%8==0 or y==len(pixels)-1:progress((y+1)/len(pixels),f'Fitting scanline colors: {y+1}/{len(pixels)}')
        return replace(s,line_codes=tuple(rows),codes=rows[len(rows)//2],mapping='Temporal blend',preset='Custom / optimized')
    codes,_=optimize(adjusted,replace(s,auto_input=False),progress,cancel)
    return replace(s,codes=codes,line_codes=(),preset='Custom / optimized',mapping='Temporal blend')

def search_sprite_palette(pixels,s,progress,cancel,duty=1.):
    """Exhaustive foreground choices with a legal shared background.

    MovieCart: ten cells per row, averaging the complementary black field.
    Streamed sprites: P0/P1 colors shared across their three copies per row.
    Plain sprites: one foreground for the complete row.
    """
    movie=s.mode==MODES[11];bgs=backgrounds(s);palette=dim(TIA,.5 if movie else duty)
    choices=[];row_scores=[]
    for y,row in enumerate(pixels):
        check_cancel(cancel)
        groups=[row[k:k+8] for k in range(0,80,8)] if movie else [row[(np.arange(48)//8)%2==k] for k in range(2)] if s.mode in MODES[9:11] else [row]
        winners=[];scores=[]
        for group in groups:
            errors=distance(palette[:,None,:],group[None,:,:])**2
            pair=np.minimum(errors[:,None,:],errors[bgs][None,:,:]).sum(axis=2)
            winners.append(pair.argmin(axis=0));scores.append(pair.min(axis=0))
        choices.append(winners);row_scores.append(np.sum(scores,axis=0))
        if y%8==0:progress((y+1)/len(pixels),f'Fitting {s.mode}: row {y+1}/{len(pixels)}')
    shared=int(np.sum(row_scores,axis=0).argmin());rows=[]
    for y,winners in enumerate(choices):
        bg=(bgs.index(0) if y==1 else int(np.argmin(row_scores[y]))) if movie else shared
        fg=[CODES[w[bg]] for w in winners]
        rows.append(tuple(fg+[CODES[bgs[bg]]]) if movie else (fg[0],fg[-1],fg[0],CODES[bgs[bg]]))
    if movie:rows[0]=rows[-1]=('00',)*11
    mid=rows[len(rows)//2];codes=(mid[0],mid[1],mid[2],mid[-1])
    return replace(s,line_codes=tuple(rows),codes=codes,mapping='Temporal blend',preset='Custom / optimized')
