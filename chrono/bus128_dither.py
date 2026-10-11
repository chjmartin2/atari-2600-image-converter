"""Full-raster dither-in-the-loop refinement for BUS row palettes."""
from dataclasses import replace
import numpy as np
from .core import BUS128LINE,CODES,TIA,check_cancel,quantize,target_palette
from .color import srgb_to_linear,linear_to_srgb

def random_rows(s,rng=None):
    """One foreground per row, no neighboring RGB duplicates; keep background."""
    if s.mode!=BUS128LINE:raise ValueError('Random row colors require BUS 128x200 Color per Line')
    s.validate()
    rng=np.random.default_rng() if rng is None else rng
    bg=s.line_codes[0][3] if s.line_codes else s.codes[3]
    seen={tuple(TIA[CODES.index(bg)])};choices=[]
    for code,rgb in zip(CODES,TIA):
        key=tuple(rgb)
        if key not in seen:choices.append(code);seen.add(key)
    rows=[];previous=None
    for _ in range(200):
        available=[c for c in choices if c!=previous]
        previous=str(rng.choice(available));rows.append((previous,)*3+(bg,))
    rows=tuple(rows)
    return replace(s,line_codes=rows,codes=rows[100],preset='Custom / random rows',optimization_scope='Image only').validate()

def refine(adjusted,s,initial,candidates,propose,progress,cancel):
    """Evaluate complete candidate tables through the exact final quantizer.

    Each render starts from the top of the image, so selected diffusion weights,
    cross-row error, palette gamut projection, black protection and serpentine
    direction all match final conversion. A bounded residual-feedback search
    proposes further palettes; only improvements on the unchanged image survive.
    """
    from .modes import render,backgrounds
    from .optimization import conversion_score
    if s.dither=='None' or s.strength==0:return initial
    tested=set();best=float('inf');winner=initial;output=None
    limit=4 if s.search_effort=='Thorough' else 2
    rounds=2 if s.search_effort=='Thorough' else 1
    completed=0;total=limit+rounds+1
    def evaluate(trial):
        nonlocal best,winner,output,completed
        check_cancel(cancel)
        key=trial.line_codes
        if key in tested:return
        tested.add(key);trial.validate()
        progress(.45+.5*min(completed/total,1),f'Testing row colors with {s.dither} — full image')
        indices=quantize(adjusted,target_palette(trial),s.dither,s.strength,s.serpentine,cancel)
        score=conversion_score(adjusted,indices,trial)
        if score<best:
            best,winner,output=score,trial,render(indices,trial)
        completed+=1
    evaluate(initial)
    for candidate in candidates:
        if len(tested)>=limit:break
        evaluate(candidate)
    # Preserve a valid current table when an explicit refit cannot beat it.
    if s.line_codes and CODES.index(s.line_codes[0][3]) in backgrounds(s):evaluate(s)
    source=srgb_to_linear(adjusted)
    for step in range(rounds):
        check_cancel(cancel)
        # Smoothed error guides a proposal only. Final scoring always uses the
        # original image and its full, unmodified dither path.
        residual=source-srgb_to_linear(output)
        smooth=np.repeat(residual.reshape(200,16,8,3).mean(axis=2),8,axis=1)
        if s.bus_pair_rows:smooth=np.repeat(smooth.reshape(100,2,128,3).mean(axis=1),2,axis=0)
        proposal_image=linear_to_srgb(source+.5*smooth)
        trial=propose(proposal_image,replace(winner,line_codes=()),
                      lambda p,t:progress(.8+.15*(step+p)/rounds,'Refining row colors from dithered output'),cancel)
        evaluate(trial)
    check_cancel(cancel);progress(1,'Row colors selected using the dithered output')
    return winner
