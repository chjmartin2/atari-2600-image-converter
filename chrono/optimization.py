"""Mode-specific input fitting and joint palette optimization.

8 color mode delegates to the weighted eight-color pipeline. Other modes
retain their fixed-reference searches. Display mixing uses linear light under
an explicit sRGB assumption.
"""
from dataclasses import replace
import numpy as np
from PIL import Image
from .core import (MODES,BUS128LINE,PRESETS,FILTERS,dimensions,prepare,quantize,target_palette,
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
    # Keep brightness_trim: it defines the user's desired exposure, not a fitted control.
    if s.mode==MODES[0]:return prepare(image,replace(s,brightness=1.))
    return prepare(image,replace(s,brightness=1.,contrast=1.,gamma=1.,saturation=1.,
                                 red=1.,green=1.,blue=1.))

def spatial_score(reference,output,paired=False):
    if not paired:return perceptual_score(reference,output)
    from .bus128_pairs import pair_average
    return .8*perceptual_score(pair_average(reference),pair_average(output))+.2*perceptual_score(reference,output)


def flicker_score(reference,frames,mode,paired=False):
    """DE00 fidelity plus a separate linear-luminance flicker cost.

    Actual field duty is already in blend(). No second dimming or exposure
    compensation belongs here. This is a display estimate, not CRT calibration.
    """
    fy=luminance(frames)
    temporal=float(np.mean((fy-np.roll(fy,1,axis=0))**2))
    from .temporal import imbalance
    return spatial_score(reference,blend(frames),paired)+.025*(temporal+4*imbalance(frames))

def conversion_score(reference,indices,s):
    paired=s.mode==BUS128LINE and s.bus_pair_rows
    if flicker_enabled(s):
        return flicker_score(reference,frame_pixels(indices,s.codes,s.line_codes,s.mode),s.mode,paired)
    return spatial_score(reference,render(indices,s),paired)


def _preview_score(reference,adjusted,s):
    if s.mode in MODES[17:20]:
        from .extended import convert
        indices=convert(adjusted,replace(s,dither='None'))
    else:indices=quantize(adjusted,target_palette(s),'None')
    return conversion_score(reference,indices,s)


def fit_controls(image,s,reference=None,global_fit=False,cancel=None,progress=lambda p,t:None,free_trim=False):
    """Fit visible input controls while holding every output color code fixed."""
    s=normalize(s)
    if s.mode==MODES[2]:
        from .two_color_match import fit_input
        return fit_input(image,s,cancel,free_trim,reference)
    if s.mode==MODES[1]:
        from .weighted_search import fit_input
        return fit_input(image,s,cancel)
    reference=neutral_reference(image,replace(s,brightness_trim=1.) if free_trim else s) if reference is None else reference
    if free_trim and s.mode==MODES[0]:s=replace(s,brightness_trim=1.)
    if s.mode==MODES[0]:return fit_classic_brightness(image,s,reference,global_fit,cancel,progress)
    small=_geometry(image,s).resize(dimensions(s),FILTERS[s.resample])
    names=('brightness','contrast','gamma','saturation','red','green','blue') + (('brightness_trim',) if free_trim else ())
    original=tuple(getattr(s,n) for n in names)
    tested={}
    def evaluate(values):
        check_cancel(cancel)
        key=tuple(round(float(v),4) for v in values)
        if key not in tested:
            trial=replace(s,**dict(zip(names,key)))
            tested[key]=_preview_score(reference,_adjust_image(small,trial),trial)
    evaluate(original);evaluate((1.,)*len(names))
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
    if free_trim:
        # Joint search owns exposure; the incoming trim is only a candidate.
        for seed in sorted(tested,key=tested.get)[:3]:
            for value in (.25,.4,.55,.7,.85,1.,1.15,1.3,1.5):
                evaluate((*seed[:7],value))
        best=min(tested,key=tested.get)
        for value in np.linspace(max(.25,best[7]-.1),min(1.5,best[7]+.1),7):
            evaluate((*best[:7],value))
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


def fit_classic_brightness(image,s,reference,thorough=False,cancel=None,progress=lambda p,t:None):
    """Search brightness only against the fixed simulated Classic display range."""
    from .classic_brightness import fit_brightness
    return fit_brightness(image,s,reference,cancel,progress)


def joint_optimize(image,s,global_search=False,progress=lambda p,t:None,cancel=None,iteration=lambda *args:None):
    """Alternate actual visible controls and actual palettes; retain the best state."""
    s=normalize(s)
    if s.mode==MODES[2]:
        from .two_color_match import joint
        return joint(image,s,progress,cancel)
    if s.mode==MODES[1]:
        from .weighted_search import joint
        return joint(image,s,progress,cancel,iteration)
    if s.mode==MODES[0]:
        progress(0,'Fitting Classic brightness to its simulated display range')
        result=fit_controls(image,s,global_fit=global_search,cancel=cancel,progress=progress,free_trim=True)
        progress(1,f'Classic brightness: {result.brightness:.3f}')
        return result
    baseline=replace(s,brightness=1.,brightness_trim=1.,contrast=1.,gamma=1.,saturation=1.,red=1.,green=1.,blue=1.)
    reference=neutral_reference(image,baseline)
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
            current=fit_controls(image,current,reference,global_search,cancel,free_trim=True)
            current=search_palette(prepare(image,current),current,
                lambda p,t:progress((done+p*.7)/(len(starts)*rounds),t),cancel)
            current=fit_controls(image,current,reference,global_search,cancel,free_trim=True)
            adjusted,indices,current=convert_image(image,current,cancel)
            score=conversion_score(reference,indices,current)
            if score<best:best,winner=score,current
            # Show each completed pass. The final result restores the best pass.
            iteration(adjusted,indices,current,score)
            done+=1
            if current==previous:break
    progress(1,f'Best perceptual score: {best:.5f}')
    return winner
