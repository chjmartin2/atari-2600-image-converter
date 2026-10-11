"""Indexed eight-color palettes with selected-dither beam refinement.

The blend catalog is shared across searches. All 128 backgrounds participate
in coordinate proposals when allowed; complete four-color palettes are never
enumerated. This is a deterministic heuristic, not an exhaustive optimum.
"""
from dataclasses import replace
from itertools import combinations_with_replacement
import threading
import numpy as np
from scipy.spatial import cKDTree
from .core import CODES, PRESETS, _mixtures, _mixtures_direct, check_cancel, quantize, hardware_palette
from .color import rgb_to_lab
from .exhaustive_black import histogram, complete_scores, DitherTarget

NAME = 'Indexed perceptual'
_catalog = None
_lock = threading.Lock()


def canonical(code):
    return tuple(sorted(map(int, code[:3]))) + (int(code[3]),)


def packed(rgb):
    a=np.asarray(rgb,dtype=np.uint32)
    return (a[...,0]<<16)+(a[...,1]<<8)+a[...,2]


class Catalog:
    def __init__(self, allowed=range(128), cancel=None):
        self.allowed=tuple(allowed)
        self.triples=np.asarray(list(combinations_with_replacement(self.allowed,3)),dtype=np.int16)
        self.black=CODES.index('00')
        palettes=np.empty((len(self.triples),8,3),np.uint8)
        for start in range(0,len(self.triples),4096):
            check_cancel(cancel);triples=self.triples[start:start+4096]
            palettes[start:start+len(triples)]=_mixtures_direct(np.column_stack((triples,np.full(len(triples),self.black))))
        check_cancel(cancel)
        self.rgb,inverse=np.unique(palettes.reshape(-1,3),axis=0,return_inverse=True)
        self.members=inverse.reshape(-1,8)
        self.lab=rgb_to_lab(self.rgb);self.keys=packed(self.rgb)
        self.index=cKDTree(self.lab)
        self.unique_members=np.sort(self.members,axis=1)
        self.unique_mask=np.ones(self.members.shape,bool)
        self.unique_mask[:,1:]=self.unique_members[:,1:]!=self.unique_members[:,:-1]
        check_cancel(cancel)

    def proposals(self,colors,weights,cancel=None):
        votes=np.zeros(len(self.rgb))
        for start in range(0,len(colors),256):
            check_cancel(cancel)
            d,near=self.index.query(colors[start:start+256],k=min(8,len(self.rgb)))
            if d.ndim==1:d=d[:,None];near=near[:,None]
            votes+=np.bincount(near.ravel(),weights=(weights[start:start+256,None]*np.exp(-d*d/100)).ravel(),minlength=len(self.rgb))
        rank=(votes[self.unique_members]*self.unique_mask).sum(axis=1)
        ids=np.argsort(-rank,kind='stable')[:256]
        return [tuple(map(int,self.triples[i]))+(self.black,) for i in ids]

    def labs(self,codes):
        # Reuse perceptual coordinates for identical blends across backgrounds.
        rgb=_mixtures(np.asarray(codes));keys=packed(rgb)
        ids=np.searchsorted(self.keys,keys);safe=np.minimum(ids,len(self.keys)-1)
        valid=(ids<len(self.keys)) & (self.keys[safe]==keys)
        labs=self.lab[safe].copy()
        # Restricted test catalogs and floating-point boundary cases remain exact.
        if not valid.all():labs[~valid]=rgb_to_lab(rgb[~valid])
        return labs


def get_catalog(cancel=None):
    global _catalog
    check_cancel(cancel)
    while not _lock.acquire(timeout=.05):check_cancel(cancel)
    try:
        check_cancel(cancel)
        if _catalog is None:
            from .palette_store import load_catalog
            built=load_catalog(cancel=cancel)
            check_cancel(cancel);_catalog=built
        return _catalog
    finally:_lock.release()


def neighbors(codes,allowed,backgrounds,cancel=None):
    result=set()
    for code in codes:
        check_cancel(cancel)
        for axis in range(4 if len(backgrounds)>1 else 3):
            for value in backgrounds if axis==3 else allowed:
                c=list(code);c[axis]=value;result.add(canonical(c))
    return sorted(result)


class Screening:
    def __init__(self,catalog,image,cancel):
        self.catalog=catalog;self.colors,self.weights=histogram(image)
        self.known={};self.cancel=cancel

    def score(self,codes):
        new=sorted(set(codes)-self.known.keys())
        for start in range(0,len(new),256):
            check_cancel(self.cancel);batch=new[start:start+256]
            scores=complete_scores(self.catalog.labs(batch),self.colors,self.weights,self.cancel)
            self.known.update(zip(batch,map(float,scores)))

    def top(self,count,backgrounds):
        return sorted((c for c in self.known if c[3] in backgrounds),key=lambda c:(self.known[c],c))[:count]


def search(image,s,progress=lambda p,t:None,cancel=None):
    check_cancel(cancel);progress(0,'Preparing reusable eight-color blend index')
    catalog=get_catalog(cancel)
    backgrounds={'Black':(CODES.index('00'),),'Black or white':(CODES.index('00'),CODES.index('0E')),
                 'Any Atari color':catalog.allowed}[s.background]
    progress(.04,'Finding compatible palettes from nearby blended colors')
    screen=Screening(catalog,image,cancel)
    seeds=catalog.proposals(screen.colors,screen.weights,cancel)
    references=[]
    for p in [s.codes,*PRESETS.values()]:
        code=tuple(CODES.index(c) for c in p)
        if any(c not in catalog.allowed for c in code[:3]):continue
        bg=code[3] if code[3] in backgrounds else backgrounds[0]
        references.append(code[:3]+(bg,))
        seeds.append(canonical(code[:3]+(catalog.black,)))
    # Black proposals provide a fast first estimate; optional backgrounds get
    # their own full 128-color coordinate proposals below.
    for iteration in range(3):
        screen.score(seeds)
        seeds=neighbors(screen.top(6,(catalog.black,)),catalog.allowed,(catalog.black,),cancel)
        progress(.08+.06*iteration,'Screening indexed foreground candidates')
    if len(backgrounds)>1:
        seeds=[c[:3]+(bg,) for c in screen.top(16,(catalog.black,)) for bg in backgrounds]
        seeds+=list(map(canonical,references))
        for iteration in range(3):
            screen.score(seeds)
            seeds=neighbors(screen.top(6,backgrounds),catalog.allowed,backgrounds,cancel)
            progress(.24+.06*iteration,f'Searching foregrounds and {len(backgrounds)} allowed shared backgrounds')
    screen.score(list(map(canonical,references)))
    check_cancel(cancel)
    thorough=s.search_effort=='Thorough'
    initial=64 if thorough else 32
    per_pass=32 if thorough else 16
    passes=3 if thorough else 2
    # Reserve one slot for the exact current palette/order when it is legal.
    # This guards against degrading it, including frame-order-sensitive scoring.
    current=tuple(CODES.index(c) for c in s.codes)
    legal_current=current[3] in backgrounds and all(c in catalog.allowed for c in current[:3])
    candidates=screen.top(initial,backgrounds)
    if legal_current and current not in candidates:candidates=candidates[:initial-1]+[current]
    target=DitherTarget(image);known={};budget=initial+passes*per_pass

    def evaluate(candidates):
        for code in candidates:
            check_cancel(cancel)
            if code in known:continue
            codes=tuple(CODES[c] for c in code);trial=replace(s,codes=codes,line_codes=())
            indices=quantize(image,hardware_palette(codes),s.dither,s.strength,s.serpentine,cancel)
            value=target.score(indices,trial)
            if not np.isfinite(value):raise ValueError('Non-finite eight-color palette score')
            known[code]=value
            progress(.42+.57*len(known)/budget,f'Comparing dithered palettes: {len(known)}/{budget}')

    evaluate(candidates)
    for iteration in range(passes):
        best=sorted(known,key=lambda c:(known[c],c))[:3]
        trials=neighbors(best,catalog.allowed,backgrounds,cancel)
        screen.score(trials)
        remaining=[c for c in trials if c not in known]
        remaining.sort(key=lambda c:(screen.known[c],c))
        evaluate(remaining[:per_pass])
    winner=min(known,key=lambda c:(known[c],c))
    check_cancel(cancel);progress(1,'Indexed palette search complete')
    return tuple(CODES[c] for c in winner),known[winner]
