"""Shared display model: sRGB-referred palette, D65 Lab and CIEDE2000.

The bundled NTSC RGB values are treated as display-referred sRGB, not measured
CRT voltages. Decode once before mixing emitted light; encode once for display.
No automatic exposure gain or additional CRT power curve is applied.
"""
import math
import numpy as np

MODEL = 'srgb-linear-light-d65-ciede2000-v1'
XYZ = np.array([[.4124564,.3575761,.1804375],
                [.2126729,.7151522,.0721750],
                [.0193339,.1191920,.9503041]])
WHITE = np.array([.95047,1.,1.08883])

def srgb_to_linear(rgb):
    v=np.clip(np.asarray(rgb,dtype=np.float64)/255,0,1)
    return np.where(v<=.04045,v/12.92,((v+.055)/1.055)**2.4)

def linear_to_srgb(light,quantized=True):
    v=np.clip(np.asarray(light,dtype=np.float64),0,1)
    rgb=255*np.where(v<=.0031308,12.92*v,1.055*v**(1/2.4)-.055)
    return np.rint(rgb).astype(np.uint8) if quantized else rgb

def blend(rgb,axis=0,weights=None):
    return linear_to_srgb(np.average(srgb_to_linear(rgb),axis=axis,weights=weights))

def dim(rgb,duty):
    return linear_to_srgb(srgb_to_linear(rgb)*duty)

def linear_to_lab(light):
    xyz=np.asarray(light)@XYZ.T/WHITE
    f=np.where(xyz>(6/29)**3,np.cbrt(xyz),xyz/(3*(6/29)**2)+4/29)
    return np.stack((116*f[...,1]-16,500*(f[...,0]-f[...,1]),200*(f[...,1]-f[...,2])),axis=-1)

def rgb_to_lab(rgb):
    return linear_to_lab(srgb_to_linear(rgb))

def luminance(rgb):
    return srgb_to_linear(rgb)@XYZ[1]

def delta_e_2000(first,second):
    """Broadcasting implementation of CIEDE2000, kL=kC=kH=1.

    Equations: Sharma, Wu & Dalal (2005); independently implemented here.
    Float64 and explicit zero-chroma / 180-degree branches are intentional.
    """
    x,y=np.asarray(first,dtype=np.float64),np.asarray(second,dtype=np.float64)
    l1,a1,b1=np.moveaxis(x,-1,0);l2,a2,b2=np.moveaxis(y,-1,0)
    c1=np.hypot(a1,b1);c2=np.hypot(a2,b2);cm=(c1+c2)/2
    g=.5*(1-np.sqrt(cm**7/(cm**7+25**7)))
    ap1=(1+g)*a1;ap2=(1+g)*a2
    cp1=np.hypot(ap1,b1);cp2=np.hypot(ap2,b2)
    h1=np.mod(np.degrees(np.arctan2(b1,ap1)),360)
    h2=np.mod(np.degrees(np.arctan2(b2,ap2)),360)
    zero=cp1*cp2==0;dh=h2-h1
    dh=np.where(zero,0,np.where(dh>180,dh-360,np.where(dh < -180,dh+360,dh)))
    dl=l2-l1;dc=cp2-cp1;dh=2*np.sqrt(cp1*cp2)*np.sin(np.radians(dh/2))
    lm=(l1+l2)/2;cp=(cp1+cp2)/2
    hm=np.where(zero,h1+h2,np.where(np.abs(h1-h2)<=180,(h1+h2)/2,
                np.where(h1+h2<360,(h1+h2+360)/2,(h1+h2-360)/2)))
    t=1-.17*np.cos(np.radians(hm-30))+.24*np.cos(np.radians(2*hm))+.32*np.cos(np.radians(3*hm+6))-.20*np.cos(np.radians(4*hm-63))
    sl=1+.015*(lm-50)**2/np.sqrt(20+(lm-50)**2)
    sc=1+.045*cp;sh=1+.015*cp*t
    rt=-2*np.sqrt(cp**7/(cp**7+25**7))*np.sin(np.radians(60*np.exp(-((hm-275)/25)**2)))
    v=dl/sl;w=dc/sc;z=dh/sh
    return np.sqrt(np.maximum(0,v*v+w*w+z*z+rt*w*z))

def distance(first,second):
    return delta_e_2000(rgb_to_lab(first),rgb_to_lab(second))

def diffusion_target(light,palette,cancel=None):
    """Bound source light to mixtures that this local palette can actually make.

    Frank-Wolfe convex projection, in linear RGB. Every intermediate point is a
    valid mixture, so even the bounded iteration limit cannot introduce an
    impossible target. This is gamut clipping before diffusion, not selection of
    an output index; nearest output colors still use CIEDE2000.
    """
    from .core import check_cancel
    target=np.clip(light,palette.min(axis=-2),palette.max(axis=-2))
    index=np.sum((target[...,None,:]-palette)**2,axis=-1).argmin(axis=-1)
    current=np.take_along_axis(palette,index[...,None,None],axis=-2)[...,0,:].copy()
    for _ in range(64):
        check_cancel(cancel)
        residual=current-target
        index=np.sum(palette*residual[...,None,:],axis=-1).argmin(axis=-1)
        vertex=np.take_along_axis(palette,index[...,None,None],axis=-2)[...,0,:]
        direction=vertex-current
        gap=-np.sum(residual*direction,axis=-1)
        if float(gap.max())<1e-10:break
        amount=np.clip(gap/np.maximum(np.sum(direction**2,axis=-1),1e-20),0,1)
        current+=amount[...,None]*direction
    return current

def nearest_linear(light,palette_lab):
    """Scalar diffusion hot path; exact same DE00 equations, without array setup."""
    r,g,b=(float(v) for v in light)
    xyz=((.4124564*r+.3575761*g+.1804375*b)/.95047,
         .2126729*r+.7151522*g+.0721750*b,
         (.0193339*r+.1191920*g+.9503041*b)/1.08883)
    f=[v**(1/3) if v>(6/29)**3 else v/(3*(6/29)**2)+4/29 for v in xyz]
    l1,a1,b1=116*f[1]-16,500*(f[0]-f[1]),200*(f[1]-f[2])
    c1=math.hypot(a1,b1);best=float('inf');winner=0
    for i,(l2,a2,b2) in enumerate(palette_lab):
        c2=math.hypot(a2,b2);cm=(c1+c2)/2
        g=.5*(1-math.sqrt(cm**7/(cm**7+25**7)))
        ap1=(1+g)*a1;ap2=(1+g)*a2
        cp1=math.hypot(ap1,b1);cp2=math.hypot(ap2,b2)
        h1=math.degrees(math.atan2(b1,ap1))%360;h2=math.degrees(math.atan2(b2,ap2))%360
        zero=cp1*cp2==0;dh=h2-h1
        dh=0 if zero else dh-360 if dh>180 else dh+360 if dh < -180 else dh
        dl=l2-l1;dc=cp2-cp1;dh=2*math.sqrt(cp1*cp2)*math.sin(math.radians(dh/2))
        lm=(l1+l2)/2;cp=(cp1+cp2)/2
        hm=h1+h2 if zero else (h1+h2)/2 if abs(h1-h2)<=180 else (h1+h2+360)/2 if h1+h2<360 else (h1+h2-360)/2
        t=1-.17*math.cos(math.radians(hm-30))+.24*math.cos(math.radians(2*hm))+.32*math.cos(math.radians(3*hm+6))-.20*math.cos(math.radians(4*hm-63))
        sl=1+.015*(lm-50)**2/math.sqrt(20+(lm-50)**2)
        sc=1+.045*cp;sh=1+.015*cp*t
        rt=-2*math.sqrt(cp**7/(cp**7+25**7))*math.sin(math.radians(60*math.exp(-((hm-275)/25)**2)))
        v,w,z=dl/sl,dc/sc,dh/sh;score=v*v+w*w+z*z+rt*w*z
        if score<best:best,winner=score,i
    return winner
