"""Two-stage eight-color search: constrained dithered target, legal palette match.

The ideal-palette stage is a bounded spatial refinement, not a global optimum.
Colors-only matching scans every legal palette using a precomputed DE00 table.
Joint matching screens every legal palette with normalized RGB error, then
uses weighted DE00 on analytically toned targets for a bounded shortlist.
"""
from dataclasses import dataclass, replace
import itertools
import threading
import numpy as np
from PIL import Image
from .core import (CODES, MODES, PRESETS, Settings, check_cancel, quantize,
                   hardware_palette, prepare, target_palette, BITS, TIA)
from .color import rgb_to_lab, delta_e_2000, srgb_to_linear, linear_to_srgb, luminance
from .indexed_search import get_catalog
from .exhaustive_black import _smooth_light

import ctypes
from pathlib import Path
_NATIVE = None
try:
    _lib=ctypes.CDLL(str(Path(__file__).with_name('native')/'palette_match.dll'))
    _NATIVE=_lib.match_block
    ptr=ctypes.c_void_p
    _NATIVE.argtypes=[ptr,ctypes.c_int,ptr,ctypes.c_int,ptr,ptr,ptr,ptr,ptr,ctypes.c_int,ctypes.c_int,ctypes.c_float,ptr,ptr]
    _NATIVE.restype=None
except OSError:
    pass  # Portable NumPy implementation remains available.


def native_match(ids,rgb,table,ideal,bounds,tone,keep,cutoff,cost):
    ids=np.ascontiguousarray(ids,dtype=np.int32);rgb=np.ascontiguousarray(rgb,dtype=np.uint8)
    if table is None:table=np.zeros((1,),dtype=np.float32)
    q=np.ascontiguousarray(ideal.colors,dtype=np.float32)
    weights=np.ascontiguousarray(ideal.weights,dtype=np.float32)
    bounds=np.ascontiguousarray(bounds,dtype=np.float32)
    scores=np.empty(keep,np.float32);indices=np.empty(keep,np.int32)
    _NATIVE(ids.ctypes.data,len(ids),rgb.ctypes.data,len(rgb),table.ctypes.data,q.ctypes.data,
            weights.ctypes.data,bounds.ctypes.data,cost.ctypes.data,int(tone),keep,float(cutoff),scores.ctypes.data,indices.ctypes.data)
    valid=indices>=0
    return indices[valid],scores[valid]


NAME = 'Weighted eight-color'
_cube_lock = threading.Lock()


@dataclass
class Ideal:
    colors: np.ndarray
    weights: np.ndarray
    indices: np.ndarray
    score: float
    evaluations: int


def nearest_pool(lab, catalog):
    """Lab shortlist followed by DE00; choices always belong to the mixed pool."""
    lab=np.atleast_2d(lab)
    _,near=catalog.index.query(lab,k=min(24,len(catalog.rgb)))
    if near.ndim==1:near=near[:,None]
    err=delta_e_2000(lab[:,None,:],catalog.lab[near])
    return near[np.arange(len(lab)),err.argmin(axis=1)]


class SpatialTarget:
    def __init__(self,image):
        self.levels=[np.asarray(image,dtype=np.uint8)]
        light=srgb_to_linear(image)
        for _ in range(2):
            light=_smooth_light(light);self.levels.append(linear_to_srgb(light))

    def score(self,output):
        from .optimization import perceptual_score
        levels=[output];light=srgb_to_linear(output)
        for _ in range(2):
            light=_smooth_light(light);levels.append(linear_to_srgb(light))
        return sum(w*perceptual_score(a,b) for w,a,b in zip((.2,.5,.3),self.levels,levels))


def ideal_palette(image,s,catalog=None,progress=lambda p,t:None,cancel=None):
    catalog=get_catalog(cancel) if catalog is None else catalog
    image=np.asarray(image,dtype=np.uint8);check_cancel(cancel)
    colors,counts=np.unique(image.reshape(-1,3),axis=0,return_counts=True)
    lab=rgb_to_lab(colors);weights=counts/counts.sum()
    locked=s.background=='Black'
    black=int(nearest_pool([[0.,0.,0.]],catalog)[0])
    budget=16 if s.search_effort=='Thorough' else 8
    target=SpatialTarget(image);tested={}

    def normalize(ids):
        ids=list(dict.fromkeys(([black] if locked else [])+list(map(int,ids))))[:8]
        # Fill from colors the current set represents least accurately.
        while len(ids)<min(8,len(catalog.rgb)):
            d=((lab[:,None,:]-catalog.lab[ids][None,:,:])**2).sum(axis=2).min(axis=1)
            order=np.argsort(-(d*weights),kind='stable')
            extra=next((int(i) for i in nearest_pool(lab[order[:64]],catalog) if int(i) not in ids),None)
            if extra is None:break
            ids.append(extra)
        return tuple(ids+[ids[-1]]*(8-len(ids)))

    def evaluate(ids):
        check_cancel(cancel);ids=normalize(ids)
        if ids in tested or len(tested)>=budget:return
        palette=catalog.rgb[list(ids)]
        indices=quantize(image,palette,s.dither,s.strength,s.serpentine,cancel)
        tested[ids]=(target.score(palette[indices]),indices)
        progress(len(tested)/budget,f'Building ideal dithered palette: {len(tested)}/{budget}')

    # Independent deterministic seeds; no legal-palette relationship is imposed.
    median=Image.fromarray(image).quantize(colors=8,method=Image.Quantize.MEDIANCUT)
    raw=np.asarray(median.getpalette(),dtype=np.uint8).reshape(-1,3)[:8]
    evaluate(nearest_pool(rgb_to_lab(raw),catalog))
    for start in (int(weights.argmax()),int(np.argmax(lab[:,0]))):
        ids=[black] if locked else [int(nearest_pool(lab[start],catalog)[0])]
        ids=list(normalize(ids))
        for _ in range(10):
            check_cancel(cancel)
            labels=((lab[:,None,:]-catalog.lab[ids][None,:,:])**2).sum(axis=2).argmin(axis=1)
            new=list(ids)
            for j in range(1 if locked else 0,8):
                mask=labels==j
                if mask.any():new[j]=int(nearest_pool(np.average(lab[mask],axis=0,weights=weights[mask]),catalog)[0])
            new=list(normalize(new))
            if new==ids:break
            ids=new
        evaluate(ids)
    evaluate(nearest_pool(rgb_to_lab(hardware_palette(s.codes)),catalog))

    # Spatial least-squares proposals account for mixtures of neighboring pixels.
    # Every proposal is constrained back to the pool and evaluated with the user's
    # actual dither. Only a better rendered score becomes the next reference.
    for iteration in range(budget):
        if len(tested)>=budget:break
        best=min(tested,key=lambda ids:(tested[ids][0],ids));_,indices=tested[best]
        membership=np.eye(8)[indices];source=srgb_to_linear(image)
        matrix=np.zeros((8,8));rhs=np.zeros((8,3))
        for weight in (.2,.5,.3):
            a=membership.reshape(-1,8);b=source.reshape(-1,3)
            matrix+=weight*a.T@a;rhs+=weight*a.T@b
            membership=_smooth_light(membership);source=_smooth_light(source)
        solution=np.linalg.solve(matrix+np.eye(8)*1e-5,rhs+1e-5*srgb_to_linear(catalog.rgb[list(best)]))
        proposed=nearest_pool(rgb_to_lab(linear_to_srgb(solution)),catalog)
        if locked:proposed[0]=black
        before=len(tested);evaluate(proposed)
        # Coordinate alternatives avoid requiring all eight updates to help at once.
        for j in np.roll(np.arange(1 if locked else 0,8),iteration):
            candidate=list(best);candidate[j]=int(proposed[j]);evaluate(candidate)
        if len(tested)==before:break
    winner=min(tested,key=lambda ids:(tested[ids][0],ids));score,indices=tested[winner]
    colors=catalog.rgb[list(winner)].copy()
    weights=np.bincount(indices.ravel(),minlength=8).astype(float)/indices.size
    check_cancel(cancel);progress(1.,'Ideal eight-color image ready')
    return Ideal(colors,weights,indices,score,len(tested))


def blend_cube(catalog,cancel=None):
    while not _cube_lock.acquire(timeout=.05):check_cancel(cancel)
    try:
        if hasattr(catalog,'blend_cube'):return catalog.blend_cube
        cube=np.full((128,128,128),-1,dtype=np.int32)
        ids=catalog.members[:,0]
        for order in itertools.permutations(range(3)):
            check_cancel(cancel);cube[tuple(catalog.triples[:,i] for i in order)]=ids
        catalog.blend_cube=cube
        return cube
    finally:_cube_lock.release()


def palette_ids(catalog,triples,bg,cube):
    a,b,c=triples.T
    return np.column_stack((cube[a,b,c],cube[a,bg,bg],cube[b,bg,bg],cube[c,bg,bg],
                            cube[a,b,bg],cube[a,c,bg],cube[b,c,bg],np.full(len(a),cube[bg,bg,bg])))


def background_indices(s,catalog):
    return {'Black':(0,),'Black or white':(0,CODES.index('0E')),'Any Atari color':catalog.allowed}[s.background]


def weighted_bounds(colors,weights):
    limits=[]
    for axis in range(3):
        order=np.argsort(colors[:,axis],kind='stable');v=colors[order,axis];w=weights[order]
        cumulative=np.cumsum(w)/max(w.sum(),1e-12)
        limits.append([v[min(np.searchsorted(cumulative,q),len(v)-1)] for q in (.01,.99)])
    return np.asarray(limits,dtype=float).T


def tone_parameters(source_bounds,palettes):
    """CGA-style per-channel affine fit, with safe handling of flat channels."""
    lo=np.min(palettes,axis=-2).astype(float);hi=np.max(palettes,axis=-2).astype(float)
    black,white=np.asarray(source_bounds,dtype=float)
    flat=(white-black)<8.
    black=np.where(flat,0.,black);white=np.where(flat,255.,white)
    gain=np.clip((hi-lo)/np.maximum(white-black,1.),0,3.)
    offset=lo-black*gain
    return gain,offset


def toned_colors(colors,gain,offset):
    return np.clip(np.asarray(colors)*gain[...,None,:]+offset[...,None,:],0,255)


def fit_distortion(ideal,gain,offset):
    """Charge RGB/black-point distortion after removing a common exposure gain.

    Without this term, turning the entire ideal image red or blue can make a
    narrow palette look artificially accurate. Uniform dimming remains free.
    Weighted moments keep this independent of the source pixel count.
    """
    q=ideal.colors/255.;mean=ideal.weights@q;second=ideal.weights@(q*q)
    exposure=np.maximum(np.max(gain,axis=-1,keepdims=True),1e-6)
    slope=gain/exposure-1.;shift=offset/exposure/255.
    return np.sum((slope*slope*second+2*slope*shift*mean+shift*shift)*[.2126,.7152,.0722],axis=-1)


def joint_weighted_score(ideal,palettes,bounds,cost=None):
    gain,offset=tone_parameters(bounds,palettes)
    toned=toned_colors(ideal.colors,gain,offset)
    d=delta_e_2000(rgb_to_lab(toned)[..., :,None,:],rgb_to_lab(palettes)[...,None,:,:])**2
    # Scale error to the target's range; a dark palette is not an automatic win.
    lab=rgb_to_lab(palettes);span=np.ptp(lab,axis=-2)
    scale=np.maximum(np.sum(span*span,axis=-1),100.)
    score=np.sum(d.min(axis=-1)*ideal.weights,axis=-1)/scale
    score+=fit_distortion(ideal,gain,offset)
    if cost is not None:
        selected=d.argmin(axis=-1)
        score+=np.sum(np.take_along_axis(cost,selected,axis=1)*ideal.weights,axis=1)
    src_span=np.ptp(ideal.colors[ideal.weights>0],axis=0)
    lost=(np.ptp(palettes.astype(float),axis=-2)<2)&(src_span>8)
    score+=.25*np.mean(lost,axis=-1)
    return score


_LUMA=luminance(TIA)
_LUMA_DIFF=(_LUMA[:,None]-_LUMA[None,:])**2


def temporal_cost(triples,bg,tone,enabled):
    if not enabled:return np.zeros((len(triples),8),np.float32)
    a,b,c=np.asarray(triples).T;d=_LUMA_DIFF
    ab,ac,bc=d[a,b],d[a,c],d[b,c]
    ag,bg_,cg=d[a,bg],d[b,bg],d[c,bg]
    # Three-frame adjacent luminance error, from pairwise squared differences.
    cost=np.column_stack((ab+ac+bc,2*ag,2*bg_,2*cg,ab+ag+bg_,ac+ag+cg,bc+bg_+cg,np.zeros(len(a))))/3
    return np.ascontiguousarray(cost*(.025 if tone else 250.),dtype=np.float32)


def match_palette(ideal,s,catalog=None,tone=False,progress=lambda p,t:None,cancel=None):
    catalog=get_catalog(cancel) if catalog is None else catalog
    cube=blend_cube(catalog,cancel);backgrounds=background_indices(s,catalog)
    triples=catalog.triples;bounds=weighted_bounds(ideal.colors,ideal.weights)
    active=np.flatnonzero(ideal.weights>0);table=None
    if not tone:
        table=np.zeros((8,len(catalog.rgb)),dtype=np.float32)
        qlab=rgb_to_lab(ideal.colors[active])
        for start in range(0,len(catalog.rgb),8192):
            check_cancel(cancel)
            table[active,start:start+8192]=delta_e_2000(qlab[:,None,:],catalog.lab[None,start:start+8192,:])**2
    best=float('inf');winner=None;shortlist=[];total=len(triples)*len(backgrounds);done=0
    # Exhaustive weighted comparison only: no image rendering in this loop.
    for bg in backgrounds:
        for start in range(0,len(triples),16384):
            check_cancel(cancel);block=triples[start:start+16384];ids=palette_ids(catalog,block,bg,cube)
            cost=temporal_cost(block,bg,tone,s.flicker_aware)
            if _NATIVE is not None:
                cutoff=shortlist[-1][0] if tone and len(shortlist)==128 else best if not tone else float('inf')
                found,values=native_match(ids,catalog.rgb,table,ideal,bounds,tone,128 if tone else 1,cutoff,cost)
                if tone:
                    shortlist.extend((float(v),tuple(map(int,block[i]))+(int(bg),)) for i,v in zip(found,values))
                    shortlist=sorted(shortlist)[:128]
                elif len(found):
                    i=int(found[0]);best=float(values[0]);winner=tuple(map(int,block[i]))+(int(bg),)
                done+=len(block)
                progress(done/total,f'Matching weighted colors: {done:,}/{total:,} legal palettes')
                continue
            if not tone:
                scores=np.zeros(len(block))
                for k,i in enumerate(active):
                    distances=table[i,ids];selected=distances.argmin(axis=1)
                    scores+=ideal.weights[i]*(distances.min(axis=1)+cost[np.arange(len(block)),selected])
            else:
                p=catalog.rgb[ids].astype(np.float32)
                gain,offset=tone_parameters(bounds,p)
                # One batched matrix product compares all eight weighted colors.
                # Float32 screening is followed by float64 DE00 finalist scoring.
                normalized=((p-offset[:,None,:])/np.maximum(gain[:,None,:],1e-6)/255.).astype(np.float32)
                q=ideal.colors[active].astype(np.float32)/255.
                channel=np.array([.2126,.7152,.0722],dtype=np.float32)
                distances=(np.sum(normalized*normalized*channel,axis=2)[:,:,None]
                           +np.sum(q*q*channel,axis=1)[None,None,:]
                           -2*(normalized@(q*channel).T))
                scores=np.sum(np.maximum(distances.min(axis=1),0)*ideal.weights[active],axis=1)
                scores+=np.sum(np.take_along_axis(cost,distances.argmin(axis=1),axis=1)*ideal.weights[active],axis=1)
                lost=(gain<1e-6)&(np.ptp(ideal.colors[active],axis=0)>8)
                scores+=.25*np.mean(lost,axis=1)
                scores+=fit_distortion(ideal,gain,offset)
            index=int(scores.argmin())
            if not tone and scores[index]<best:
                best=float(scores[index]);winner=tuple(map(int,block[index]))+(int(bg),)
            if tone:
                keep=np.argsort(scores,kind='stable')[:128]
                shortlist.extend((float(scores[i]),tuple(map(int,block[i]))+(int(bg),)) for i in keep)
                shortlist=sorted(shortlist)[:128]
            done+=len(block)
            progress(done/total,f'Matching weighted colors: {done:,}/{total:,} legal palettes')
    if tone:
        codes=[c for _,c in shortlist]
        palettes=np.asarray([hardware_palette(tuple(CODES[i] for i in c)) for c in codes])
        cost=np.concatenate([temporal_cost(np.asarray([c[:3]]),c[3],True,s.flicker_aware) for c in codes])
        values=joint_weighted_score(ideal,palettes,bounds,cost)
        index=min(range(len(codes)),key=lambda i:(values[i],codes[i]));winner=codes[index];best=float(values[index])
    check_cancel(cancel)
    return tuple(CODES[i] for i in winner),best,bounds


def search(image,s,progress=lambda p,t:None,cancel=None):
    progress(0,'Loading bundled mixed-color catalog');catalog=get_catalog(cancel)
    ideal=ideal_palette(image,s,catalog,lambda p,t:progress(.05+.4*p,t),cancel)
    codes,score,_=match_palette(ideal,s,catalog,False,lambda p,t:progress(.45+.55*p,t),cancel)
    return codes,score


def neutral(s,keep_trim=False):
    return replace(s,brightness=1.,contrast=1.,gamma=1.,saturation=1.,red=1.,green=1.,blue=1.,
                   red_offset=0.,green_offset=0.,blue_offset=0.,brightness_trim=s.brightness_trim if keep_trim else 1.)


def apply_fit(s,bounds,palette,keep_trim=False):
    gain,offset=tone_parameters(bounds,np.asarray(palette).reshape(-1,3))
    # Brightness <= 1 avoids clipping before the RGB gains and fitted offsets.
    brightness=max(.001,min(1.,float(gain.max())))
    rgb=gain/brightness
    return replace(neutral(s,keep_trim),brightness=brightness,red=float(rgb[0]),green=float(rgb[1]),blue=float(rgb[2]),
                   red_offset=float(offset[0]),green_offset=float(offset[1]),blue_offset=float(offset[2]),auto_input=False)


def fit_input(image,s,cancel=None):
    check_cancel(cancel)
    baseline=neutral(s)
    pixels=np.asarray(prepare(image,baseline))
    bounds=np.percentile(pixels,(1,99),axis=(0,1))
    return apply_fit(s,bounds,target_palette(s),keep_trim=True)


def joint(image,s,progress=lambda p,t:None,cancel=None,iteration=lambda *args:None):
    from .modes import convert_image
    catalog=get_catalog(cancel);baseline=neutral(s)
    ideal=ideal_palette(prepare(image,baseline),baseline,catalog,lambda p,t:progress(.05+.4*p,t),cancel)
    codes,score,bounds=match_palette(ideal,baseline,catalog,True,lambda p,t:progress(.45+.54*p,t),cancel)
    winner=apply_fit(replace(s,codes=codes,line_codes=(),search=NAME),bounds,hardware_palette(codes))
    adjusted,indices,winner=convert_image(image,winner,cancel)
    iteration(adjusted,indices,winner,score)
    progress(1.,'Weighted palette and input fit complete')
    return winner
