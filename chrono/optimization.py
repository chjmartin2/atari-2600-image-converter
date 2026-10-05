"""Alternating input/palette search with a fixed perceptual reference.

No candidate can redefine the reference to make a washed-out image score well.
The display estimate mixes linear light under an explicit sRGB assumption.
"""
from dataclasses import replace
import numpy as np
from PIL import Image
from .core import (MODES,PRESETS,FILTERS,dimensions,prepare,quantize,target_palette,
                   check_cancel,_geometry,_adjust_image,frame_count,frame_pixels)
from .modes import normalize,search_palette,render,convert_image

from .color import blend,rgb_to_lab,delta_e_2000,luminance

def perceptual_score(reference,output):
    ref=rgb_to_lab(reference);out=rgb_to_lab(output)
    # Same D65 white and absolute display scale for both sides. No fitted gain.
    color=float(np.mean((delta_e_2000(ref,out)/100)**2))
    ry=ref[...,0]/100;oy=out[...,0]/100
    edges=sum(float(np.mean((np.diff(ry,axis=k)-np.diff(oy,axis=k))**2))
              for k in (0,1) if ry.shape[k]>1)
    detail=max(0.,float(ry.std())*.8-float(oy.std()))**2
    return color+.55*edges+3*detail

def flicker_enabled(s):
    return s.flicker_aware and frame_count(s.mode)>1

def neutral_reference(image,s):
    # Fixed for the whole search: candidate controls cannot move the goalposts.
    if s.mode==MODES[0]:return prepare(image,replace(s,brightness=1.))
    return prepare(image,replace(s,brightness=1.,contrast=1.,gamma=1.,saturation=1.,
                                 red=1.,green=1.,blue=1.))

def flicker_score(reference,frames,mode):
    """DE00 fidelity plus a separate linear-luminance flicker cost.

    Actual field duty is already in blend(). No second dimming or exposure
    compensation belongs here. This is a display estimate, not CRT calibration.
    """
    fy=luminance(frames)
    temporal=float(np.mean((fy-np.roll(fy,1,axis=0))**2))
    from .temporal import imbalance
    return perceptual_score(reference,blend(frames))+.025*(temporal+4*imbalance(frames))

def conversion_score(reference,indices,s):
    if flicker_enabled(s):
        return flicker_score(reference,frame_pixels(indices,s.codes,s.line_codes,s.mode),s.mode)
    return perceptual_score(reference,render(indices,s))


def _preview_score(reference,adjusted,s):
    if s.mode in MODES[17:20]:
        from .extended import convert
        indices=convert(adjusted,replace(s,dither='None'))
    else:indices=quantize(adjusted,target_palette(s),'None')
    return conversion_score(reference,indices,s)


def fit_controls(image,s,reference=None,global_fit=False,cancel=None):
    """Fit visible input controls while holding every output color code fixed."""
    s=normalize(s)
    reference=neutral_reference(image,s) if reference is None else reference
    if s.mode==MODES[0]:return fit_classic_brightness(image,s,reference,global_fit,cancel)
    small=_geometry(image,s).resize(dimensions(s),FILTERS[s.resample])
    names=('brightness','contrast','gamma','saturation','red','green','blue')
    original=tuple(getattr(s,n) for n in names)
    tested={}
    def evaluate(values):
        check_cancel(cancel)
        key=tuple(round(float(v),4) for v in values)
        if key not in tested:
            trial=replace(s,**dict(zip(names,key)))
            tested[key]=_preview_score(reference,_adjust_image(small,trial),trial)
    evaluate(original);evaluate((1.,)*7)
    contrasts=(.35,.55,.75,1.,1.25,1.6,2.)
    for b in (.25,.4,.55,.7,.85,1.,1.2):
        for c in contrasts:evaluate((b,c,*original[2:]))
    best=min(tested,key=tested.get)
    for b in np.linspace(max(.1,best[0]-.12),min(1.5,best[0]+.12),3):
        for c in np.linspace(max(.15,best[1]-.2),min(3.,best[1]+.2),5):evaluate((b,c,*best[2:]))
    # Gamma, saturation and RGB balance are fitted for the one-shot and joint
    # input operations alike. Coordinate descent keeps the GUI responsive.
    for sweep in range(2 if global_fit else 1):
        for axis,values in ((2,(.65,.8,1.,1.2,1.5)),(3,(.65,.85,1.,1.2,1.45)),
                            (4,(.65,.8,1.,1.2,1.4)),(5,(.65,.8,1.,1.2,1.4)),(6,(.65,.8,1.,1.2,1.4))):
            best=min(tested,key=tested.get)
            for value in values:
                trial=list(best);trial[axis]=value;evaluate(trial)
    finalists=sorted(tested,key=tested.get)[:6]+[original]
    best_score=float('inf');winner=s
    for values in finalists:
        check_cancel(cancel)
        trial=replace(s,**dict(zip(names,values)))
        # Score the real full-resolution preparation and selected dithering,
        # not just the fast nearest-color search approximation.
        adjusted,indices,trial=convert_image(image,trial,cancel)
        score=conversion_score(reference,indices,trial)
        if score<best_score:best_score,winner=score,trial
    return winner


def fit_classic_brightness(image,s,reference,thorough=False,cancel=None):
    """Owner-selected Classic preset; never search or multiply current brightness."""
    check_cancel(cancel)
    return replace(s,brightness=.47)


def joint_optimize(image,s,global_search=False,progress=lambda p,t:None,cancel=None,iteration=lambda *args:None):
    """Alternate actual visible controls and actual palettes; retain the best state."""
    s=normalize(s)
    if s.mode==MODES[0]:
        progress(0,'Setting Classic RGB brightness to 0.47')
        result=fit_controls(image,s,global_fit=global_search,cancel=cancel)
        progress(1,f'Classic brightness: {result.brightness:.3f}')
        return result
    baseline=replace(s,brightness=1.,contrast=1.,gamma=1.,saturation=1.,red=1.,green=1.,blue=1.)
    reference=neutral_reference(image,s)
    starts=[s]
    if global_search and s.mode==MODES[1]:
        starts += [replace(baseline,codes=PRESETS[name],line_codes=(),mapping='Temporal blend')
                   for name in ('RGB (original Chronocolour)','Grayscale','Neon')]
    rounds=3 if not global_search else 4
    winner=None;best=float('inf');done=0
    for start in starts:
        current=start
        if current.mode in MODES[3:] and not current.line_codes:
            current=search_palette(prepare(image,current),current,progress,cancel)
        # Always keep the starting conversion as a candidate (no forced regression).
        adjusted,indices,current=convert_image(image,current,cancel)
        score=conversion_score(reference,indices,current)
        if score<best:best,winner=score,current
        for round_no in range(rounds):
            check_cancel(cancel)
            previous=current
            progress(done/(len(starts)*rounds),f'Joint optimization: pass {done+1}/{len(starts)*rounds}')
            current=fit_controls(image,current,reference,global_search,cancel)
            current=search_palette(prepare(image,current),current,
                lambda p,t:progress((done+p*.7)/(len(starts)*rounds),t),cancel)
            current=fit_controls(image,current,reference,global_search,cancel)
            adjusted,indices,current=convert_image(image,current,cancel)
            score=conversion_score(reference,indices,current)
            if score<best:best,winner=score,current
            # Show each completed pass. The final result restores the best pass.
            iteration(adjusted,indices,current,score)
            done+=1
            if current==previous:break
    progress(1,f'Best perceptual score: {best:.5f}')
    return winner
