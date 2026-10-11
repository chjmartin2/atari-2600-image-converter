"""Complete black-background gamut scan, followed by dither-aware selection.

All unordered foreground triples (including repeats) participate. Screening uses
frequency-weighted squared CIE76 over the lossless input histogram. Positive
partial sums can safely prune candidates above a known top-K bound. Finalists
are actually dithered and ranked with multiscale CIEDE2000 and optional flicker
cost. The final dithered result is not a globally exhaustive diffusion search.
"""
from dataclasses import replace
from itertools import combinations_with_replacement
import numpy as np
from .core import (CODES, PRESETS, check_cancel, _mixtures, quantize, hardware_palette,
                   frame_pixels)
from .color import rgb_to_lab, srgb_to_linear, linear_to_srgb, luminance

NAME = 'Exhaustive black background'
FINALISTS = 64


def build_catalog(color_indices=range(128), cancel=None, progress=lambda p,t:None):
    check_cancel(cancel)
    triples = np.asarray(list(combinations_with_replacement(color_indices, 3)), dtype=np.int16)
    palettes = np.empty((len(triples), 8, 3), dtype=np.uint8)
    black = CODES.index('00')
    for start in range(0, len(triples), 4096):
        check_cancel(cancel)
        block = triples[start:start+4096]
        palettes[start:start+len(block)] = _mixtures(np.column_stack((block, np.full(len(block), black))))
        progress((start+len(block))/len(triples), 'Building all black-background palettes')
    return triples, palettes


def histogram(image):
    colors, counts = np.unique(np.asarray(image, dtype=np.uint8).reshape(-1,3), axis=0, return_counts=True)
    order = np.argsort(-counts, kind='stable')
    return rgb_to_lab(colors[order]), counts[order].astype(np.float64)/counts.sum()


def errors(palettes_lab, colors):
    """Nearest squared CIE76, with bounded temporary storage and no Python pixels."""
    best = np.full((len(palettes_lab), len(colors)), np.inf)
    for entry in range(8):
        d = (palettes_lab[:,entry,0,None]-colors[None,:,0])**2
        d += (palettes_lab[:,entry,1,None]-colors[None,:,1])**2
        d += (palettes_lab[:,entry,2,None]-colors[None,:,2])**2
        np.minimum(best, d, out=best)
    return best


def complete_scores(palettes_lab, colors, weights, cancel=None):
    result = np.zeros(len(palettes_lab))
    for start in range(0, len(colors), 32):
        check_cancel(cancel)
        result += np.sum(errors(palettes_lab, colors[start:start+32])*weights[None,start:start+32], axis=1)
    return result


def screen(palettes, image, limit=FINALISTS, cancel=None, progress=lambda p,t:None, triples=None):
    """Exact top-K for the screening metric; pruning never samples input colors."""
    check_cancel(cancel)
    if not len(palettes):raise ValueError('No candidate palettes')
    limit = min(max(1, int(limit)), len(palettes))
    colors, weights = histogram(image)
    labs = rgb_to_lab(palettes)
    # Completed seed scores supply an upper bound, not a candidate restriction.
    seeds = np.unique(np.linspace(0,len(palettes)-1,min(len(palettes),max(512,limit)),dtype=int))
    seed_scores = complete_scores(labs[seeds], colors, weights, cancel)
    if triples is not None:
        # A short exact-metric coordinate walk tightens the pruning bound only.
        # Every catalog entry still participates in the exhaustive scan below.
        lookup=np.full((128,128,128),-1,dtype=np.int32)
        lookup[tuple(triples.T)]=np.arange(len(triples))
        known=dict(zip(seeds.tolist(),seed_scores.tolist()))
        best=min(known,key=known.get)
        for sweep in range(2):
            for axis in range(3):
                check_cancel(cancel)
                variants=np.tile(triples[best],(128,1));variants[:,axis]=np.arange(128)
                variants.sort(axis=1)
                ids=np.unique(lookup[tuple(variants.T)]);ids=ids[ids>=0]
                new=np.array([i for i in ids if int(i) not in known],dtype=int)
                if len(new):known.update(zip(new.tolist(),complete_scores(labs[new],colors,weights,cancel).tolist()))
                best=min(known,key=known.get)
                progress(0.,'Finding a bound for the complete palette scan')
        seed_scores=np.fromiter(known.values(),dtype=float)
    bound = np.partition(seed_scores,limit-1)[limit-1]
    scores = np.zeros(len(palettes))
    alive = np.arange(len(palettes))
    for start in range(0,len(colors),32):
        check_cancel(cancel)
        for chunk in range(0,len(alive),4096):
            check_cancel(cancel)
            ids = alive[chunk:chunk+4096]
            scores[ids] += np.sum(errors(labs[ids],colors[start:start+32])*weights[None,start:start+32],axis=1)
        # Tolerance protects candidates tied at a floating-point sum boundary.
        alive = alive[scores[alive] <= bound+1e-8]
        progress(min(1,(start+32)/len(colors)),
                 f'Exhaustive black: {len(palettes):,} candidates; {len(alive):,} still competitive')
    order = np.lexsort((alive,scores[alive]))[:limit]
    return alive[order], scores[alive[order]]


def _smooth_light(a):
    p=np.pad(a,((0,0),(1,1),(0,0)),mode='edge')
    a=(p[:,:-2]+2*p[:,1:-1]+p[:,2:])/4
    p=np.pad(a,((1,1),(0,0),(0,0)),mode='edge')
    return (p[:-2]+2*p[1:-1]+p[2:])/4


class DitherTarget:
    def __init__(self,image):
        a=srgb_to_linear(image)
        self.levels=[np.asarray(image,dtype=np.uint8)]
        for _ in range(2):
            a=_smooth_light(a);self.levels.append(linear_to_srgb(a))

    def score(self,indices,s):
        from .optimization import perceptual_score, flicker_enabled
        frames=frame_pixels(indices,s.codes,(),s.mode)
        output=hardware_palette(s.codes)[indices]
        a=srgb_to_linear(output);levels=[output]
        for _ in range(2):
            a=_smooth_light(a);levels.append(linear_to_srgb(a))
        score=sum(weight*perceptual_score(ref,out) for weight,ref,out in zip((.2,.5,.3),self.levels,levels))
        if flicker_enabled(s):
            from .temporal import imbalance
            y=luminance(frames)
            score+=.025*(float(np.mean((y-np.roll(y,1,axis=0))**2))+4*imbalance(frames))
        return score


def search(image,s,progress=lambda p,t:None,cancel=None):
    check_cancel(cancel)
    triples,palettes=build_catalog(cancel=cancel,progress=lambda p,t:progress(.04*p,t))
    ids,_=screen(palettes,image,cancel=cancel,progress=lambda p,t:progress(.04+.81*p,t),triples=triples)
    candidates=[tuple(CODES[int(v)] for v in triples[i])+('00',) for i in ids]
    # Always consider the existing foregrounds with black and useful preset seeds.
    candidates += [tuple(s.codes[:3])+('00',)] + [tuple(p[:3])+('00',) for p in PRESETS.values()]
    candidates=list(dict.fromkeys(candidates))
    target=DitherTarget(image);winner=None;best=float('inf')
    for number,codes in enumerate(candidates):
        check_cancel(cancel)
        trial=replace(s,codes=codes,line_codes=(),background='Black')
        indices=quantize(image,hardware_palette(codes),s.dither,s.strength,s.serpentine,cancel)
        score=target.score(indices,trial)
        if score<best:best,winner=score,codes
        progress(.85+.15*(number+1)/len(candidates),
                 f'Comparing dithered palettes: {number+1}/{len(candidates)}')
    return winner,best
