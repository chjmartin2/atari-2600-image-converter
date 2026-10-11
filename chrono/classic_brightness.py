"""Brightness-only fitting against Classic's fixed simulated light range.

The palette, dither and other input controls are never searched. The reference
and output white remain fixed across all candidates; no fitted display gain.
"""
from dataclasses import replace
import numpy as np
from .color import luminance
from .core import (check_cancel, _geometry, _adjust_image, dimensions, FILTERS,
                   quantize, target_palette)


def _lightness(y):
    """D65 CIE L* from relative luminance, scaled to 0..1."""
    y = np.clip(y, 0., 1.)
    return np.where(y > (6/29)**3, 116*np.cbrt(y)-16, (29/3)**3*y)/100


def _smooth(y):
    # Binomial low-pass in linear light. No wraparound or black edge padding.
    p = np.pad(y, ((0, 0), (1, 1)), mode='edge')
    y = (p[:, :-2]+2*p[:, 1:-1]+p[:, 2:])/4
    p = np.pad(y, ((1, 1), (0, 0)), mode='edge')
    return (p[:-2]+2*p[1:-1]+p[2:])/4


def _levels(y):
    levels = [_lightness(y)]
    for _ in range(2):
        y = _smooth(y)
        levels.append(_lightness(y))
    return levels


class ClassicToneTarget:
    def __init__(self, reference, palette):
        self.reference = _levels(luminance(reference))
        # Hardware palette already contains the three-frame linear-light mix.
        # Use its ceiling, never the brightest pixel of a candidate image.
        self.white = float(luminance(palette).max())
        if self.white <= 0:
            raise ValueError('Classic palette must have a nonzero light range')

    def score(self, output):
        levels = _levels(luminance(output)/self.white)
        score = 0.
        for weight, ref, out in zip((.2, .5, .3), self.reference, levels):
            tone = float(np.mean((ref-out)**2))
            detail = clipped = 0.
            for axis in (0, 1):
                if ref.shape[axis] < 2:
                    continue
                dr, do = np.diff(ref, axis=axis), np.diff(out, axis=axis)
                detail += float(np.mean((dr-do)**2))
                a, b = (out[:-1], out[1:]) if axis == 0 else (out[:, :-1], out[:, 1:])
                collapsed = ((a > .98) & (b > .98)) | ((a < .02) & (b < .02))
                # Flat white/black source areas incur no extra clipping penalty.
                clipped += float(np.mean(np.where(collapsed, dr*dr, 0.)))
            score += weight*(tone+.5*detail+2.*clipped)
        return score


def fit_brightness(image, s, reference, cancel=None, progress=lambda p,t: None):
    check_cancel(cancel)
    palette = target_palette(s)
    target = ClassicToneTarget(reference, palette)
    geometry = _geometry(image, s)
    tested = {}
    current = round(float(s.brightness), 6)

    def evaluate(value):
        check_cancel(cancel)
        value = round(float(np.clip(value, 0, 3)), 6)
        if value not in tested:
            trial = replace(s, brightness=value)
            # Exactly the normal prepare/quantize path; cache geometry only.
            adjusted = _adjust_image(geometry, trial).resize(dimensions(s), FILTERS[s.resample])
            indices = quantize(adjusted, palette, s.dither, s.strength, s.serpentine, cancel)
            tested[value] = target.score(palette[indices])
        return value

    def ranked():
        # Stable ties avoid arbitrary changes on plateaus.
        return sorted(tested, key=lambda b: (tested[b], abs(b-.47), b))

    evaluate(current)
    if not np.any(reference):
        progress(1., 'Classic image is black; brightness retained')
        return s
    coarse = sorted(set([.05, .1, 1., 1.5, 2., 3., .47, .54, current]
                        + [round(v, 2) for v in np.arange(.15, .851, .05)]))
    for i, value in enumerate(coarse):
        evaluate(value)
        progress(.5*(i+1)/len(coarse), f'Classic brightness: testing {value:.3f}')
    # Quantized scores are not unimodal: refine several good coarse regions.
    seeds = ranked()[:3]
    fine = sorted(set(round(v, 6) for b in seeds for v in np.linspace(max(0,b-.05), min(3,b+.05), 11)))
    for i, value in enumerate(fine):
        evaluate(value)
        progress(.5+.35*(i+1)/len(fine), f'Classic brightness: refining {value:.3f}')
    seeds = ranked()[:2]
    final = sorted(set(round(v, 6) for b in seeds for v in np.linspace(max(0,b-.01), min(3,b+.01), 11)))
    for i, value in enumerate(final):
        evaluate(value)
        progress(.85+.15*(i+1)/len(final), f'Classic brightness: refining {value:.3f}')
    winner = ranked()[0]
    # Keep the caller's exact value on a tie; never degrade the current output.
    if tested[current] <= tested[winner]+1e-12:
        winner = float(s.brightness)
    progress(1., f'Classic brightness: {winner:.3f}')
    return replace(s, brightness=winner)
