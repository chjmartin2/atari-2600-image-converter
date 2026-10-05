"""Image preparation, hardware-valid temporal palettes, quantization and search."""
from dataclasses import dataclass, asdict, replace
from pathlib import Path
import itertools
import json
import threading
import time
import numpy as np
from PIL import Image, ImageEnhance, ImageOps, ImageFilter
from .color import (MODEL,srgb_to_linear,linear_to_srgb,rgb_to_lab,linear_to_lab,
                    delta_e_2000,distance,dim,nearest_linear,diffusion_target)

DATA = Path(__file__).parent / "resources"
RECORDS = json.loads((DATA / "ntsc.json").read_text())
TIA = np.array([r["rgb"] for r in RECORDS], dtype=np.float32)
CODES = [r["code"] for r in RECORDS]
BITS = np.array([[1,1,1],[1,0,0],[0,1,0],[0,0,1],[1,1,0],[1,0,1],[0,1,1],[0,0,0]], dtype=np.uint8)
FILTERS = {s: getattr(Image.Resampling, s.upper()) for s in ("Nearest", "Box", "Bilinear", "Hamming", "Bicubic", "Lanczos")}
PRESETS = {
    "RGB (original Chronocolour)": ("42", "C6", "74", "00"),
    "Grayscale": ("0E", "08", "04", "00"),
    "Sepia": ("2E", "28", "14", "00"),
    "Neon": ("4E", "AE", "6E", "00"),
    "Pink": ("4E", "5A", "64", "00"),
    "Blue": ("8E", "88", "74", "00"),
    "CGA (magenta / cyan / black)": ("5C", "AC", "00", "00"),
}
KERNELS = {
    "Floyd–Steinberg": (16, [(1,0,7),(-1,1,3),(0,1,5),(1,1,1)]),
    "Atkinson": (8, [(1,0,1),(2,0,1),(-1,1,1),(0,1,1),(1,1,1),(0,2,1)]),
    "Jarvis–Judice–Ninke": (48, [(1,0,7),(2,0,5),(-2,1,3),(-1,1,5),(0,1,7),(1,1,5),(2,1,3),(-2,2,1),(-1,2,3),(0,2,5),(1,2,3),(2,2,1)]),
    "Stucki": (42, [(1,0,8),(2,0,4),(-2,1,2),(-1,1,4),(0,1,8),(1,1,4),(2,1,2),(-2,2,1),(-1,2,2),(0,2,4),(1,2,2),(2,2,1)]),
    "Sierra": (32, [(1,0,5),(2,0,3),(-2,1,2),(-1,1,4),(0,1,5),(1,1,4),(2,1,2),(-1,2,2),(0,2,3),(1,2,2)]),
    "Burkes": (32, [(1,0,8),(2,0,4),(-2,1,2),(-1,1,4),(0,1,8),(1,1,4),(2,1,2)]),
}
DITHERS = ["None", "Ordered 2×2", "Ordered 4×4", "Ordered 8×8", *KERNELS]
MODES = ['Chronocolor classic','Chronocolor custom','Two Color','Chronocolor per line','Scanline color','No flicker — playfield','Playfield Plus','Bus stuffing (experimental)', 'Multiplexed sprites', 'DPC+ sprites', 'CDFJ+ sprites', 'MovieCart frame', 'Two Color (2 frames)', 'Scanline color (2 frames)', 'Multiplexed sprites (2 frames)', 'DPC+ sprites (2 frames)', 'CDFJ+ sprites (2 frames)', 'Hybrid playfield + sprites', '96-pixel interleaved bitmap', 'Television interlace (experimental)']

def frame_count(mode):
    return 2 if mode in (*MODES[11:17],*MODES[18:20]) else 3 if mode in (MODES[0],MODES[1],MODES[3]) else 1

def mode_description(mode):
    return mode + (' — Flicker' if frame_count(mode)>1 else ' — Static')


def dimensions(s):
    if s.mode in MODES[17:20]:return {MODES[17]:(160,192),MODES[18]:(96,192),MODES[19]:(48,384)}[s.mode]
    if s.mode in MODES[12:17]:return (48,128) if s.mode in MODES[12:14] else (48,192)
    if s.mode==MODES[7]:return (16,192)
    if s.mode==MODES[11]:return (80,192)
    if s.mode in MODES[8:11]:return (48,192)
    return (40,192) if s.mode in MODES[5:] else (48,128)

def cartridge_type(mode):
    if mode in MODES[17:20]:return "F8" if mode==MODES[19] else "F4"
    if mode in MODES[12:17]:return "F8" if mode in MODES[12:15] else "DPC+" if mode==MODES[15] else "CDF"
    if mode in MODES[9:]:return {MODES[9]:'DPC+',MODES[10]:'CDF',MODES[11]:'MVC'}[mode]
    return 'BUS' if mode==MODES[7] else 'F6' if mode==MODES[6] else '4K'

def cartridge_size(mode):
    return {'F4':32768,'F8':8192,'BUS':32768,'F6':16384,'4K':4096,'DPC+':32768,'CDF':32768,'MVC':30*60*4096}[cartridge_type(mode)]

def display_aspect(s):
    if s.mode in MODES[17:20]:return "Raw pixels" if s.aspect=="Raw pixels" else {MODES[17]:"Display 4:3",MODES[18]:"Wide raster",MODES[19]:"Sprite raster"}[s.mode]
    if s.mode in MODES[12:14]:return s.aspect
    if s.mode in MODES[14:17]:return "Raw pixels" if s.aspect=="Raw pixels" else "Sprite raster"
    if s.mode in MODES[8:]:return 'Raw pixels' if s.aspect=='Raw pixels' else 'Movie raster' if s.mode==MODES[11] else 'Sprite raster'
    return 'BUS raster' if s.mode==MODES[7] else 'Display 4:3' if s.mode in MODES[5:] else s.aspect

@dataclass
class Settings:
    mode: str = 'Chronocolor custom'
    line_codes: tuple = ()
    scale: str = "Fill / crop"
    resample: str = "Lanczos"
    aspect: str = "Atari pixels 2:1"
    crop_x: float = .5
    crop_y: float = .5
    crop_zoom: float = 1.0
    brightness: float = 1.0
    contrast: float = 1.0
    saturation: float = 1.0
    gamma: float = 1.0
    sharpness: float = 1.0
    red: float = 1.0
    green: float = 1.0
    blue: float = 1.0
    rotate: int = 0
    mirror: bool = False
    dither: str = "Floyd–Steinberg"
    strength: float = 1.0
    serpentine: bool = False
    preset: str = "RGB (original Chronocolour)"
    codes: tuple = ("42", "C6", "74", "00")
    mapping: str = "Temporal blend"
    search: str = "Improved weighted"
    background: str = "Black"
    diversity: bool = False
    auto_input: bool = False
    flicker_aware: bool = True
    balance_frames: bool = True
    optimization_scope: str = 'Image + colors'
    search_effort: str = 'Standard'

    def validate(self):
        if self.mode not in MODES:raise ValueError('Unknown output mode')
        if self.optimization_scope not in ('Image + colors','Image only','Colors only'):
            raise ValueError('Unknown optimization scope')
        if self.search_effort not in ('Standard','Thorough'):
            raise ValueError('Unknown search effort')
        if self.mode in MODES[17:20]:
            from .extended import validate_rows
            validate_rows(self)
            replace(self,mode=MODES[1],line_codes=()).validate()
            return self
        if self.mode in MODES[12:17]:
            from .twoframe import validate_rows,BASES
            validate_rows(self)
            replace(self,mode=BASES[self.mode],line_codes=()).validate()
            return self
        if self.line_codes and (len(self.line_codes)!=dimensions(self)[1] or any(len(row)!=(11 if self.mode==MODES[11] else 4) or any(c not in CODES for c in row) for row in self.line_codes)):
            raise ValueError('Invalid scanline palette data')
        if self.line_codes:
            if self.mode==MODES[11] and (any(c!='00' for r in (self.line_codes[0],self.line_codes[-1]) for c in r) or self.line_codes[1][-1]!='00'):
                raise ValueError('MovieCart requires black boundary rows and the first content-row background')
            if self.mode not in (*MODES[3:7],*MODES[8:]):raise ValueError('This mode does not use scanline palettes')
            if self.mode in (*MODES[3:5],*MODES[8:11]) and len({row[3] for row in self.line_codes})!=1:raise ValueError('The sprite kernel requires a constant background')
            if self.mode in (*MODES[4:6],MODES[8]) and any(row[0]!=row[1] or row[1]!=row[2] for row in self.line_codes):raise ValueError('Static scanlines require one foreground color')
        choices = {"scale": ["Fit", "Fill / crop", "Stretch"], "resample": FILTERS, "aspect": ["Atari pixels 2:1", "Display 4:3", "Raw pixels"], "dither": DITHERS, "mapping": ["Temporal blend", "Legacy RGB targets"], "search": ["Improved weighted", "Legacy exhaustive"], "background": ["Black", "Black or white", "Any Atari color"], "rotate": [0,90,180,270]}
        for name, allowed in choices.items():
            if getattr(self, name) not in allowed:
                raise ValueError(f"Invalid {name}: {getattr(self,name)}")
        for name in ("brightness","contrast","saturation","sharpness","red","green","blue"):
            if not 0 <= float(getattr(self, name)) <= 3:
                raise ValueError(f"{name} must be between 0 and 3")
        if not .2 <= float(self.gamma) <= 3 or not 0 <= float(self.strength) <= 1:
            raise ValueError("Gamma or dither strength is out of range")
        if not 0 <= float(self.crop_x) <= 1 or not 0 <= float(self.crop_y) <= 1:
            raise ValueError("Crop position must be between 0 and 1")
        if not 1 <= float(self.crop_zoom) <= 8:
            raise ValueError("Input crop zoom must be between 1 and 8")
        if not isinstance(self.auto_input,bool):raise ValueError("Optimize input must be on or off")
        if not isinstance(self.balance_frames,bool):raise ValueError("Frame balancing must be on or off")
        if not isinstance(self.flicker_aware,bool):raise ValueError("Flicker-aware optimization must be on or off")
        if len(self.codes) != 4 or any(c not in CODES for c in self.codes):
            raise ValueError("Choose four valid even NTSC color codes")
        return self

    @classmethod
    def load(cls, path):
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        if data.get("schema") != 1:
            raise ValueError("Unsupported settings version")
        values=data['settings']
        values['mapping']='Temporal blend'
        if 'codes' in values:values['codes']=tuple(values['codes'])
        if 'line_codes' in values:values['line_codes']=tuple(tuple(row) for row in values['line_codes'])
        return cls(**values).validate()

    def save(self, path):
        self.validate()
        Path(path).write_text(json.dumps({"schema":1,"color_model":MODEL,"settings":asdict(self)}, indent=2), encoding="utf-8")

def load_image(path):
    with Image.open(path) as im:
        im = ImageOps.exif_transpose(im).convert("RGBA")
        bg = Image.new("RGBA", im.size, (0,0,0,255))
        return Image.alpha_composite(bg, im).convert("RGB")

def prepare(image, settings, apply_auto=True):
    """Render stored controls. auto_input is an optimization policy, not a filter.

    apply_auto remains accepted for compatibility with earlier callers.
    """
    s = settings.validate()
    return _adjust_image(_geometry(image,s),s).resize(dimensions(s),FILTERS[s.resample])

def geometry_target(size,s):
    if s.mode in MODES[17:20]:
        return dimensions(s) if s.aspect=="Raw pixels" else {MODES[17]:(512,384),MODES[18]:(384,384),MODES[19]:(192,384)}[s.mode]
    if s.mode in MODES[12:17]:
        from .twoframe import BASES
        return geometry_target(size,replace(s,mode=BASES[s.mode],line_codes=()))
    if s.mode in MODES[8:]:
        w,h=dimensions(s);return (w,h) if s.aspect=='Raw pixels' else (w*2,h)
    if s.mode==MODES[7]:return (16,192) if s.aspect=='Raw pixels' else (576,480)
    if s.mode in MODES[5:]:
        return {'Atari pixels 2:1':(512,384),'Display 4:3':(512,384),'Raw pixels':(40,192)}[s.aspect]
    if size == (48,128):return (48,128)
    return {"Atari pixels 2:1": (384,512), "Display 4:3": (512,384), "Raw pixels": (48,128)}[s.aspect]

def crop_bounds(size,s):
    """Source-space selection after rotation/mirroring; Stretch never locks aspect."""
    sw,sh=size
    vw,vh=float(sw),float(sh)
    if s.scale=='Fill / crop':
        tw,th=geometry_target(size,s)
        scale=max(tw/sw,th/sh)
        vw,vh=tw/scale,th/scale
    vw/=s.crop_zoom;vh/=s.crop_zoom
    left=(sw-vw)*s.crop_x;top=(sh-vh)*s.crop_y
    return left,top,left+vw,top+vh


def drag_crop_position(source_size,s,delta,display_size):
    """Move the picture with the pointer; crop offsets refer to rotated/mirrored space."""
    sw,sh=source_size
    if s.rotate in (90,270):sw,sh=sh,sw
    tw,th=geometry_target((sw,sh),s)
    left,top,right,bottom=crop_bounds((sw,sh),s)
    visible=(right-left,bottom-top);excess=(sw-visible[0],sh-visible[1])
    if s.scale=='Fit':
        fit=min(tw/visible[0],th/visible[1])
        display_size=(display_size[0]*visible[0]*fit/tw,display_size[1]*visible[1]*fit/th)
    result=[]
    for pos,motion,span,extra,display in zip((s.crop_x,s.crop_y),delta,visible,excess,display_size):
        result.append(float(np.clip(pos-motion*span/(max(display,1)*extra),0,1)) if extra>1e-8 else pos)
    return tuple(result)

def _geometry(image,s):
    im = image.convert("RGB").rotate(s.rotate, expand=True)
    if s.mirror:
        im = ImageOps.mirror(im)
    # Work in display coordinates before reducing to 48 unusually wide pixels.
    target = geometry_target(im.size,s)
    filt = FILTERS[s.resample]
    bounds=crop_bounds(im.size,s)
    if s.scale == "Fit":
        if s.crop_zoom!=1:
            # Keep a single source crop, then letterbox its original aspect ratio.
            size=(max(1,round(im.width/s.crop_zoom)),max(1,round(im.height/s.crop_zoom)))
            im=im.resize(size,filt,box=bounds)
        im = ImageOps.pad(im, target, method=filt, color="black")
    elif s.scale == "Fill / crop":
        im = im.resize(target,filt,box=bounds)
    else:
        im = im.resize(target, filt,box=bounds)
    return im

def _adjust_image(im,s):
    for enhancer, factor in [(ImageEnhance.Brightness,s.brightness),(ImageEnhance.Contrast,s.contrast),(ImageEnhance.Color,s.saturation),(ImageEnhance.Sharpness,s.sharpness)]:
        im = enhancer(im).enhance(factor)
    a = np.asarray(im, dtype=np.float32) / 255
    a = np.clip(a * [s.red,s.green,s.blue], 0, 1) ** (1/s.gamma)
    return Image.fromarray(np.uint8(np.rint(a*255)))

def optimize_input(image,settings,progress=lambda value,text:None,cancel=None):
    """Compatibility entry point for the shared visible-control optimizer."""
    from .optimization import fit_controls
    progress(0,'Matching input to the current palette with CIEDE2000')
    result=fit_controls(image,settings,cancel=cancel)
    progress(1,'Input matching complete')
    return result


def hardware_palette(codes):
    colors = srgb_to_linear(TIA[[CODES.index(c) for c in codes]])
    return linear_to_srgb((BITS @ colors[:3] + (3-BITS.sum(axis=1))[:,None]*colors[3])/3)

def target_palette(settings):
    if settings.mode in MODES[17:20]:
        from .extended import palette
        return palette(settings)
    if settings.mode in MODES[12:17]:
        from .twoframe import palette
        return palette(settings)
    if settings.mode in MODES[8:]:
        w,h=dimensions(settings);movie=settings.mode==MODES[11]
        fallback=((settings.codes[0],)*10+(settings.codes[3],),)*h if movie else (settings.codes,)*h
        rows=settings.line_codes or fallback
        colors=TIA[[[CODES.index(c) for c in r] for r in rows]]
        fg=colors[:,np.arange(w)//8] if movie else colors[:,(np.arange(w)//8)%2] if settings.mode in MODES[9:11] else np.repeat(colors[:,0,None,:],w,axis=1)
        bg=np.broadcast_to(colors[:,-1,None,:],fg.shape)
        p=np.empty((h,w,8,3),dtype=np.float32);p[:,:,:7]=fg[:,:,None,:];p[:,:,7]=bg
        if movie:p=dim(p,.5);p[[0,-1]]=0
        return np.rint(p).astype(np.uint8)
    if settings.mode==MODES[7]:return TIA.astype(np.uint8)
    if settings.mode==MODES[6]:
        rows=settings.line_codes or (settings.codes,)*192
        colors=TIA[[[CODES.index(c) for c in row] for row in rows]].astype(np.uint8)
        p=np.empty((192,40,8,3),dtype=np.uint8)
        p[:,:20,:7]=colors[:,0,None,None,:];p[:,:20,7]=colors[:,1,None,:]
        p[:,20:,:7]=colors[:,2,None,None,:];p[:,19:,7]=colors[:,3,None,:]
        return p
    if settings.mode==MODES[0]:return hardware_palette(PRESETS['RGB (original Chronocolour)'])
    if settings.line_codes:
        p=np.array([hardware_palette(row) for row in settings.line_codes])
        if settings.mode in MODES[4:]:p[:,:7]=p[:,:1]
        return p
    if settings.mode==MODES[2]:
        p=hardware_palette((settings.codes[0],)*3+(settings.codes[3],))
        p[:7]=p[0]
        return p
    return hardware_palette(settings.codes)

class Cancelled(Exception):
    pass

def check_cancel(cancel):
    if cancel is not None and cancel.is_set():
        raise Cancelled()

def bayer(n):
    a = np.array([[0,2],[3,1]], dtype=np.float32)
    while a.shape[0] < n:
        a = np.block([[4*a,4*a+2],[4*a+3,4*a+1]])
    return (a+.5)/(n*n)-.5

def quantize(image, palette, method="None", strength=1, serpentine=False, cancel=None):
    a = srgb_to_linear(image)
    p = srgb_to_linear(palette)
    h,w = a.shape[:2]
    lab=linear_to_lab(p)
    if p.ndim==2:
        p=np.broadcast_to(p,(h,*p.shape));lab=np.broadcast_to(lab,(h,*lab.shape))
    if p.shape[0]!=h:raise ValueError('Palette height must match the image')
    if p.ndim==3:
        p=np.broadcast_to(p[:,None,:,:],(h,w,*p.shape[1:]));lab=np.broadcast_to(lab[:,None,:,:],(h,w,*lab.shape[1:]))
    if p.shape[:2]!=(h,w):raise ValueError('Palette dimensions must match the image')
    if method.startswith("Ordered"):
        n = int(method.split()[1][0]); matrix = bayer(n)
        distances = delta_e_2000(linear_to_lab(a)[:,:,None,:],lab)
        first_index=distances.argmin(axis=2)
        yy,xx=np.indices((h,w))
        first=p[yy,xx,first_index]
        # Repeated entries in two-color palettes must not hide the second color.
        distinct=np.any(p!=first[:,:,None,:],axis=3)
        second_index=np.where(distinct,distances,np.inf).argmin(axis=2)
        second=p[yy,xx,second_index]
        direction = second-first
        fraction = np.clip(((a-first)*direction).sum(axis=2)/np.maximum((direction*direction).sum(axis=2),1e-12),0,1)
        threshold = np.tile(matrix+.5, ((h+n-1)//n,(w+n-1)//n))[:h,:w]
        return np.where(fraction*strength>threshold,second_index,first_index).astype(np.uint8)
    if method not in KERNELS or strength == 0:
        check_cancel(cancel)
        return delta_e_2000(linear_to_lab(a)[:,:,None,:],lab).argmin(axis=2).astype(np.uint8)
    # Exact source black is an absorbing boundary when the local palette can
    # reproduce it. Never let neighboring residuals paint into a black border.
    black_entries=np.all(p==0,axis=3)
    keep_black=np.all(a==0,axis=2)&black_entries.any(axis=2)
    black_index=black_entries.argmax(axis=2)
    # Discard source light outside the mixtures available at this pixel, before
    # accumulating error. It cannot be recovered by flooding neighboring pixels.
    a=diffusion_target(a,p,cancel)
    denom,kernel = KERNELS[method]
    out = np.empty((h,w), dtype=np.uint8)
    # Collapse duplicate palette entries once; diffusion visits only distinct colors.
    cache={}
    for y in range(h):
        check_cancel(cancel)
        row_palettes=[]
        for x in range(w):
            key=lab[y,x].tobytes()
            if key not in cache:
                _,ix=np.unique(lab[y,x],axis=0,return_index=True);ix=np.sort(ix)
                cache[key]=(ix,lab[y,x,ix].tolist())
            row_palettes.append(cache[key])
        reverse = serpentine and y%2
        for x in (range(w-1,-1,-1) if reverse else range(w)):
            if keep_black[y,x]:
                out[y,x]=black_index[y,x]
                continue
            # Keep signed accumulated error. Clipping it before subtracting the
            # chosen color discards negative residuals and biases diffusion bright.
            old = a[y,x].copy()
            ix,entries=row_palettes[x]
            idx = int(ix[nearest_linear(np.clip(old,0,1),entries)])
            out[y,x] = idx
            err = (old-p[y,x,idx])*strength/denom
            for dx,dy,weight in kernel:
                xx,yy = x+(-dx if reverse else dx),y+dy
                if 0 <= xx < w and yy < h:
                    a[yy,xx] += err*weight
    return out

def frame_pixels(indices, codes, line_codes=(), mode=None):
    """Three interleaved on/off frames before bottom-up ROM packing."""
    if mode in MODES[17:20]:
        from .extended import frames
        return frames(indices,codes,line_codes,mode)
    if mode in MODES[12:17]:
        from .twoframe import frames
        return frames(indices,codes,line_codes,mode)
    if mode==MODES[11]:
        from .moviecart import frames
        return frames(indices,line_codes)
    if mode in MODES[8:11]:
        p=target_palette(Settings(mode=mode,codes=tuple(codes),line_codes=tuple(line_codes)))
        yy,xx=np.indices(indices.shape);im=p[yy,xx,indices]
        return [im.copy() for _ in range(3)]
    if mode==MODES[7]:
        from .bus_rom import image_bytes
        image_bytes(indices) # Validate the full-color index range and geometry.
        return [TIA[indices].astype(np.uint8) for _ in range(3)]
    if mode==MODES[6]:
        p=target_palette(Settings(mode=mode,codes=tuple(codes),line_codes=tuple(line_codes)))
        yy,xx=np.indices(indices.shape);im=p[yy,xx,indices]
        return [im.copy() for _ in range(3)]
    result = []
    h,w=indices.shape
    colors = TIA[[[CODES.index(c) for c in row] for row in line_codes]].astype(np.uint8) if line_codes else np.broadcast_to(TIA[[CODES.index(c) for c in codes]].astype(np.uint8),(h,4,3))
    for f in range(3):
        component = (np.arange(h)+f)%3
        on = np.take_along_axis(BITS[indices], np.broadcast_to(component[:,None,None],(h,w,1)),axis=2)[:,:,0]
        result.append(np.where(on[:,:,None], colors[np.arange(h),component][:,None,:], colors[:,3,None,:]))
    return result

def representative_colors(image, count=8):
    pixels = np.asarray(image).reshape(-1,3)
    colors, first, counts = np.unique(pixels, axis=0, return_index=True, return_counts=True)
    order = np.argsort(first); colors,counts = colors[order].astype(np.float32),counts[order]
    chosen = [int(counts.argmax())]
    dist = np.full(len(colors), np.inf)
    for _ in range(min(count,len(colors))-1):
        d = distance(colors,colors[chosen[-1]])
        dist = np.minimum(dist,d); dist[chosen] = -1
        chosen.append(int(dist.argmax()))
    return colors[chosen]

def _mixtures(batch):
    c = srgb_to_linear(TIA[np.asarray(batch)])
    return linear_to_srgb((np.einsum("ij,bjk->bik",BITS.astype(np.float32),c[:,:3])+(3-BITS.sum(axis=1))[None,:,None]*c[:,3:4])/3)

def _score(batch, colors, weights=None, diversity=False):
    mix = _mixtures(batch)
    # A fixed source reference prevents palette-dependent darkening from hiding
    # error. Input controls are fitted explicitly by the joint optimizer.
    distances = distance(mix[:,:,None,:],colors[None,None,:,:])
    nearest=distances.min(axis=1)
    if weights is None:
        score=nearest.sum(axis=1)
        if diversity:
            picked=distances.argmin(axis=1)
            used=np.stack([(picked==i).any(axis=1) for i in range(8)],axis=1).sum(axis=1)
            score=score*1000/used
        return score
    return (nearest**2) @ weights


def _legacy_component_ranges():
    """Compact traversal description: (component 1, component 2, fstart)."""
    ranges=[];estart=fstart=128
    for d in range(128,0,-1):
        for e in range(estart,0,-1):
            ranges.append((d-1,e-1,fstart))
            fstart-=1
            if fstart<=0:fstart=estart-1
        estart-=1
        if estart<=0:estart=128
    return ranges

def optimize(image, settings, progress=lambda value,text: None, cancel=None):
    """Search the prepared image using the common fixed-reference DE00 objective."""
    s = settings.validate()
    backgrounds = {"Black":[0],"Black or white":[0,112],"Any Atari color":list(range(128))}[s.background]
    check_cancel(cancel)
    if s.search == "Legacy exhaustive":
        colors = representative_colors(image)
        best, winner = float("inf"), None
        # Preserve the FreeBASIC C-mode traversal, including its changing fstart.
        ranges=_legacy_component_ranges()
        def candidates():
            for d,e,fstart in ranges:
                for f in range(fstart-1,-1,-1):
                    for bg in backgrounds:yield (d,e,f,bg)
        # Count ranges, not tens of millions of candidate tuples, before starting.
        total=sum(fstart for _,_,fstart in ranges)*len(backgrounds)
        done=0;iterator=candidates();last_progress=time.monotonic()
        progress(0,f"Legacy exhaustive search — {len(backgrounds)} background colors")
        while True:
            check_cancel(cancel)
            items=list(itertools.islice(iterator,1024))
            if not items:break
            check_cancel(cancel)
            batch=np.array(items)
            scores=_score(batch,colors,diversity=s.diversity);i=int(scores.argmin())
            if scores[i]<best:best,winner=float(scores[i]),batch[i].copy()
            done+=len(batch)
            if best==0:
                progress(1,"Exact palette match found")
                break
            now=time.monotonic()
            if now-last_progress>=.1 or done==total:
                progress(done/total,f"Legacy exhaustive search — {len(backgrounds)} background colors")
                last_progress=now
    else:
        # Histogram weighting preserves frequent colors; quantization bounds work.
        pixels = np.asarray(image).reshape(-1,3)
        keys = (pixels//16).astype(np.int32)
        _,inv,counts = np.unique(keys,axis=0,return_inverse=True,return_counts=True)
        colors = np.array([np.bincount(inv,weights=pixels[:,i])/counts for i in range(3)]).T
        top = np.argsort(counts)[-96:]; colors,weights = colors[top], counts[top].astype(float)
        weights /= weights.sum()
        starts = [[CODES.index(c) for c in s.codes]] + [[CODES.index(c) for c in p] for p in PRESETS.values()]
        best,winner = float("inf"),None
        for startno,start in enumerate(starts):
            current = np.array(start)
            if s.background != "Any Atari color": current[3] = backgrounds[0]
            for sweep in range(6):
                previous = current.copy()
                for axis in range(4):
                    check_cancel(cancel)
                    allowed = range(128) if axis < 3 or s.background == "Any Atari color" else backgrounds
                    batch = np.tile(current,(len(allowed),1)); batch[:,axis] = list(allowed)
                    scores = _score(batch,colors,weights); current = batch[int(scores.argmin())].copy()
                if np.array_equal(previous,current): break
            score = float(_score([current],colors,weights)[0])
            if score < best: best,winner = score,current.copy()
            progress((startno+1)/len(starts), "Improved weighted palette search")
    return tuple(CODES[int(i)] for i in winner), best
