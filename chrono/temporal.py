"""Redistribute legal temporal phases; never change cartridge timing."""
from dataclasses import replace
from itertools import permutations
import numpy as np
from .color import luminance,srgb_to_linear
from .core import MODES,BITS,frame_pixels,frame_count,check_cancel

def imbalance(frames):
    y=luminance(frames)
    centered=y-y.mean(axis=0)
    # Whole-frame flashing plus local two-line/eight-pixel bands.
    global_error=np.mean(centered.mean(axis=(1,2))**2)
    h,w=y.shape[1:];hh=h//2*2;ww=w//8*8
    blocks=centered[:,:hh,:ww].reshape(len(y),hh//2,2,ww//8,8).mean(axis=(2,4))
    return float(global_error+np.mean(blocks**2))


def canonicalize(s):
    """Stable palette order before dithering makes save/reload reproducible."""
    if s.mode==MODES[12] and s.line_codes and all(r[3]==r[7] for r in s.line_codes):
        # Normalize phase even when balancing is turned off, so the toggle also
        # removes an earlier row assignment before requantizing the source.
        r=tuple(s.line_codes[0]);r=min(r,r[4:]+r[:4])
        return replace(s,line_codes=(r,)*len(s.line_codes),codes=r[:4])
    if s.mode in MODES[17:20] or not s.balance_frames or not s.line_codes:return s
    rows=[]
    for r in s.line_codes:
        r=tuple(r)
        if s.mode==MODES[3]:r=tuple(sorted(r[:3]))+(r[3],)
        elif s.mode in MODES[13:17] and r[3]==r[7]:
            r=tuple(v for group in sorted((r[:4],r[4:])) for v in group)
        rows.append(r)
    return replace(s,line_codes=tuple(rows),codes=tuple(rows[len(rows)//2][:4]))


def interleave(indices,s,cancel=None):
    if not s.balance_frames or frame_count(s.mode)==1:return indices,s
    if s.mode==MODES[12]:
        base=(s.codes[0],)*3+(s.codes[3],)
        rows=s.line_codes or (base*2,)*128
        if all(r[3]==r[7] for r in rows):
            # A/B/A/B scanlines in one frame, B/A/B/A in the other. Exchange
            # both palette and bit assignment: each pixel's exact RGB sum stays.
            result=indices.copy();interlaced=[]
            swap=np.array([0,2,1,3],dtype=np.uint8)
            for y,row in enumerate(rows):
                check_cancel(cancel)
                r=tuple(row);base=min(r,r[4:]+r[:4])
                desired=base[4:]+base[:4] if y%2 else base
                if r!=desired:result[y]=swap[result[y]]
                interlaced.append(desired)
            trial=replace(s,line_codes=tuple(interlaced),codes=interlaced[0][:4])
            # With identical palettes, half-intensity pixels can also exchange
            # phase horizontally. Keep a balanced pattern if it already exists.
            if all(r[:4]==r[4:] for r in interlaced):
                original=frame_pixels(result,trial.codes,trial.line_codes,trial.mode)
                yy,xx=np.indices(result.shape);mask=(result==1)|(result==2)
                for shift in (0,1):
                    candidate=result.copy();candidate[mask]=1+((xx+yy+shift)%2)[mask]
                    f=frame_pixels(candidate,trial.codes,trial.line_codes,trial.mode)
                    if imbalance(f)<imbalance(original)-1e-8:return candidate,trial
            return result,trial
    original=np.asarray(frame_pixels(indices,s.codes,s.line_codes,s.mode))
    result=indices.copy();rows=list(s.line_codes)
    row_swaps=s.mode in MODES[13:17] and rows and all(r[3]==r[7] for r in rows)
    row_perms=s.mode==MODES[3] and rows
    if row_swaps or row_perms:
        count=len(original);load=np.zeros((count,6))
        for y in range(len(result)):
            check_cancel(cancel)
            options=[]
            for perm in permutations(range(count)):
                f=luminance(original[list(perm),y])
                delta=f.reshape(count,6,8).mean(axis=2);delta-=delta.mean(axis=0)
                # Balance cumulative light across columns as well as whole rows.
                score=float(np.mean((load+delta)**2)+np.mean((load+delta).mean(axis=1)**2))
                if row_swaps:
                    r=tuple(rows[y][4:]+rows[y][:4]) if perm[0] else tuple(rows[y])
                    index=np.array([0,2,1,3],dtype=np.uint8)[indices[y]] if perm[0] else indices[y]
                else:
                    # Physical frame f uses component (y+f)%3.
                    cp=tuple((y+perm[(k-y)%3])%3 for k in range(3))
                    r=tuple(rows[y][k] for k in cp)+(rows[y][3],)
                    mapping=np.array([np.flatnonzero(np.all(BITS==b[list(cp)],axis=1))[0] for b in BITS],dtype=np.uint8)
                    index=mapping[indices[y]]
                options.append((score,r,index,delta))
            _,r,index,delta=min(options,key=lambda v:(round(v[0],8),v[1]))
            rows[y]=r;result[y]=index;load+=delta
        trial=replace(s,line_codes=tuple(rows),codes=tuple(rows[len(rows)//2][:4]))
        frames=np.asarray(frame_pixels(result,trial.codes,trial.line_codes,trial.mode))
        # Exact means are mandatory for row rearrangement. Keep the old result if
        # local band balance did not improve; no brightness-only degradation.
        if np.array_equal(frames.sum(axis=0),original.sum(axis=0)) and imbalance(frames)<imbalance(original)-1e-8:
            return result,trial
    # Pair states 01 and 10 have precisely the same average when both frames use
    # identical colors. Checkerboard their assignment to avoid full-field pulses.
    if s.mode in MODES[12:17]:
        from .core import CODES,TIA
        rows=s.line_codes or (tuple(s.codes)*2,)*len(indices)
        c=srgb_to_linear(TIA[[[CODES.index(v) for v in r] for r in rows]])
        k=(np.arange(48)//8)%2 if s.mode in MODES[15:17] else np.zeros(48,dtype=int)
        equivalent=np.all(np.isclose(c[:,k]+c[:,7,None],c[:,k+4]+c[:,3,None],rtol=0,atol=1e-12),axis=2)
        y,x=np.indices(indices.shape);mask=equivalent & ((indices==1)|(indices==2))
        for shift in (0,1):
            trial=indices.copy();trial[mask]=1+((x+y+shift)%2)[mask]
            frames=frame_pixels(trial,s.codes,s.line_codes,s.mode)
            if imbalance(frames)<imbalance(original)-1e-8:return trial,s
    # Classic already rotates component phase by scanline; MovieCart's alternating
    # cells are hardwired. Do not invent illegal phase swaps for these formats.
    return indices,s
