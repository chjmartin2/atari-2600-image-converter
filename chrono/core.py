"""Image preparation, hardware-valid temporal palettes, quantization and search."""
from dataclasses import dataclass, asdict
from pathlib import Path
import itertools
import json
import threading
import numpy as np
from PIL import Image, ImageEnhance, ImageOps, ImageFilter

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

@dataclass
class Settings:
    scale: str = "Fit"
    resample: str = "Lanczos"
    aspect: str = "Atari pixels 2:1"
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

    def validate(self):
        choices = {"scale": ["Fit", "Fill / crop", "Stretch"], "resample": FILTERS, "aspect": ["Atari pixels 2:1", "Display 4:3", "Raw pixels"], "dither": DITHERS, "mapping": ["Temporal blend", "Legacy RGB targets"], "search": ["Improved weighted", "Legacy exhaustive"], "background": ["Black", "Black or white", "Any Atari color"], "rotate": [0,90,180,270]}
        for name, allowed in choices.items():
            if getattr(self, name) not in allowed:
                raise ValueError(f"Invalid {name}: {getattr(self,name)}")
        for name in ("brightness","contrast","saturation","sharpness","red","green","blue"):
            if not 0 <= float(getattr(self, name)) <= 3:
                raise ValueError(f"{name} must be between 0 and 3")
        if not .2 <= float(self.gamma) <= 3 or not 0 <= float(self.strength) <= 1:
            raise ValueError("Gamma or dither strength is out of range")
        if len(self.codes) != 4 or any(c not in CODES for c in self.codes):
            raise ValueError("Choose four valid even NTSC color codes")
        if self.mapping == "Legacy RGB targets" and tuple(self.codes) != PRESETS["RGB (original Chronocolour)"]:
            raise ValueError("Legacy RGB targets requires the original RGB component colors")
        return self

    @classmethod
    def load(cls, path):
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        if data.get("schema") != 1:
            raise ValueError("Unsupported settings version")
        return cls(**data["settings"]).validate()

    def save(self, path):
        self.validate()
        Path(path).write_text(json.dumps({"schema":1,"settings":asdict(self)}, indent=2), encoding="utf-8")

def load_image(path):
    with Image.open(path) as im:
        im = ImageOps.exif_transpose(im).convert("RGBA")
        bg = Image.new("RGBA", im.size, (0,0,0,255))
        return Image.alpha_composite(bg, im).convert("RGB")

def prepare(image, settings):
    s = settings.validate()
    im = image.convert("RGB").rotate(s.rotate, expand=True)
    if s.mirror:
        im = ImageOps.mirror(im)
    # Work in display coordinates before reducing to 48 unusually wide pixels.
    target = {"Atari pixels 2:1": (384,512), "Display 4:3": (512,384), "Raw pixels": (48,128)}[s.aspect]
    if im.size == (48,128):
        target = (48,128)  # Historical inputs are already compressed logical pixels.
    filt = FILTERS[s.resample]
    if s.scale == "Fit":
        im = ImageOps.pad(im, target, method=filt, color="black")
    elif s.scale == "Fill / crop":
        im = ImageOps.fit(im, target, method=filt)
    else:
        im = im.resize(target, filt)
    for enhancer, factor in [(ImageEnhance.Brightness,s.brightness),(ImageEnhance.Contrast,s.contrast),(ImageEnhance.Color,s.saturation),(ImageEnhance.Sharpness,s.sharpness)]:
        im = enhancer(im).enhance(factor)
    a = np.asarray(im, dtype=np.float32) / 255
    a = np.clip(a * [s.red,s.green,s.blue], 0, 1) ** (1/s.gamma)
    return Image.fromarray(np.uint8(np.rint(a*255))).resize((48,128), filt)

def hardware_palette(codes):
    colors = TIA[[CODES.index(c) for c in codes]]
    return np.rint((BITS @ colors[:3] + (3-BITS.sum(axis=1))[:,None]*colors[3])/3).astype(np.uint8)

def target_palette(settings):
    if settings.mapping == "Legacy RGB targets":
        return BITS*255
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
    a = np.asarray(image, dtype=np.float32).copy()
    p = np.asarray(palette, dtype=np.float32)
    h,w = a.shape[:2]
    if method.startswith("Ordered"):
        n = int(method.split()[1][0]); matrix = bayer(n)
        distances = ((a[:,:,None,:]-p)**2).sum(axis=3)
        nearest = np.argsort(distances,axis=2,kind="stable")[:,:,:2]
        first,second = p[nearest[:,:,0]],p[nearest[:,:,1]]
        direction = second-first
        fraction = np.clip(((a-first)*direction).sum(axis=2)/np.maximum((direction*direction).sum(axis=2),1),0,1)
        threshold = np.tile(matrix+.5, ((h+n-1)//n,(w+n-1)//n))[:h,:w]
        return np.where(fraction*strength>threshold,nearest[:,:,1],nearest[:,:,0]).astype(np.uint8)
    if method not in KERNELS or strength == 0:
        check_cancel(cancel)
        return ((a[:,:,None,:]-p)**2).sum(axis=3).argmin(axis=2).astype(np.uint8)
    denom,kernel = KERNELS[method]
    out = np.empty((h,w), dtype=np.uint8)
    for y in range(h):
        check_cancel(cancel)
        reverse = serpentine and y%2
        for x in (range(w-1,-1,-1) if reverse else range(w)):
            old = np.clip(a[y,x], 0, 255)
            idx = int(((p-old)**2).sum(axis=1).argmin())
            out[y,x] = idx
            err = (old-p[idx])*strength/denom
            for dx,dy,weight in kernel:
                xx,yy = x+(-dx if reverse else dx),y+dy
                if 0 <= xx < w and yy < h:
                    a[yy,xx] += err*weight
    return out

def frame_pixels(indices, codes):
    """Three interleaved on/off frames before bottom-up ROM packing."""
    result = []
    colors = TIA[[CODES.index(c) for c in codes]].astype(np.uint8)
    for f in range(3):
        component = (np.arange(128)+f)%3
        on = np.take_along_axis(BITS[indices], np.broadcast_to(component[:,None,None],(128,48,1)),axis=2)[:,:,0]
        result.append(np.where(on[:,:,None], colors[component][:,None,:], colors[3]))
    return result

def representative_colors(image, count=8):
    pixels = np.asarray(image).reshape(-1,3)
    colors, first, counts = np.unique(pixels, axis=0, return_index=True, return_counts=True)
    order = np.argsort(first); colors,counts = colors[order].astype(np.float32),counts[order]
    chosen = [int(counts.argmax())]
    dist = np.full(len(colors), np.inf)
    for _ in range(min(count,len(colors))-1):
        c = colors[chosen[-1]]; delta = colors-c; rmean = (colors[:,0]+c[0])/2
        # Preserve the old representative-color distance, including its blue term.
        d = (2+rmean/256)*delta[:,0]**2+4*delta[:,1]**2+2+(255-rmean)/256*delta[:,2]**2
        dist = np.minimum(dist,d); dist[chosen] = -1
        chosen.append(int(dist.argmax()))
    return colors[chosen]

def _mixtures(batch):
    c = TIA[np.asarray(batch)]
    return np.rint((np.einsum("ij,bjk->bik",BITS.astype(np.float32),c[:,:3])+(3-BITS.sum(axis=1))[None,:,None]*c[:,3:4])/3).astype(np.float32)

def _score(batch, colors, weights=None, diversity=False):
    mix = _mixtures(batch)
    delta = mix[:,:,None,:]-colors[None,None,:,:]
    if weights is None:
        distances = np.sqrt((delta*delta).sum(axis=3))
        score = distances.min(axis=1).sum(axis=1)
        if diversity:
            picked = distances.argmin(axis=1)
            used = np.stack([(picked==i).any(axis=1) for i in range(8)],axis=1).sum(axis=1)
            score = score*1000/used
        return score
    return ((delta*delta)*[.299,.587,.114]).sum(axis=3).min(axis=1) @ weights

def optimize(image, settings, progress=lambda value,text: None, cancel=None):
    s = settings.validate()
    backgrounds = [0] if s.background == "Black" else [0,112]
    if s.search == "Legacy exhaustive":
        if s.background == "Any Atari color":
            raise ValueError("Legacy search supports black or black/white backgrounds; use Improved for any color")
        colors = representative_colors(image)
        best, winner = float("inf"), None
        # Preserve the FreeBASIC C-mode traversal, including its changing fstart.
        def candidates():
            estart=fstart=128
            for d in range(128,0,-1):
                for e in range(estart,0,-1):
                    for f in range(fstart,0,-1):
                        for bg in backgrounds:yield (d-1,e-1,f-1,bg)
                    fstart-=1
                    if fstart<=0:fstart=estart-1
                estart-=1
                if estart<=0:estart=128
        total=sum(1 for _ in candidates());done=0;iterator=candidates()
        while True:
            items=list(itertools.islice(iterator,512))
            if not items:break
            check_cancel(cancel)
            batch=np.array(items)
            scores=_score(batch,colors,diversity=s.diversity);i=int(scores.argmin())
            if scores[i]<best:best,winner=float(scores[i]),batch[i].copy()
            done+=len(batch);progress(done/total,"Legacy exhaustive palette search")
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
