"""Lossless website animation from a completed conversion, without GUI chrome."""
from pathlib import Path
from dataclasses import replace
import math
import os
import tempfile
import tkinter as tk
from tkinter import ttk,filedialog,messagebox
import numpy as np
from PIL import Image
from .core import dimensions,display_aspect,frame_count,frame_pixels

def preview_size(settings,long_edge=640):
    if long_edge not in (320,640,960):raise ValueError('Choose a supported export size')
    w,h={'Atari pixels 2:1':(3,4),'Display 4:3':(4,3),'BUS raster':(6,5),
         'Sprite raster':(1,2),'Wide raster':(1,1),'Movie raster':(5,6),
         'Raw pixels':dimensions(settings)}[display_aspect(settings)]
    return max(1,round(long_edge*w/max(w,h))),max(1,round(long_edge*h/max(w,h)))

def export_animation(path,indices,settings,rate=60,retention=.6,long_edge=640):
    """Write atomically; six phases make both 2/3-frame loops exact at 60 fps.

    Millisecond durations alternate as needed, rather than rounding every frame
    to 17 ms. A static mode exports one image; no artificial motion is invented.
    """
    from .animation import persistence_frames
    if rate not in (60,30,10,3):raise ValueError('Choose a supported frame rate')
    path=Path(path)
    if path.suffix.lower()!='.webp':raise ValueError('Save the animation with a .webp extension')
    settings.validate()
    raw=frame_pixels(indices,settings.codes,settings.line_codes,settings.mode)[:frame_count(settings.mode)]
    fields=persistence_frames(raw,retention)
    size=preview_size(settings,long_edge)
    pictures=[Image.fromarray(f).resize(size,Image.Resampling.NEAREST) for f in fields]
    count=math.lcm(len(pictures),3) if len(pictures)>1 else 1
    frames=[pictures[i%len(pictures)] for i in range(count)]
    edges=[round(i*1000/rate) for i in range(count+1)]
    durations=[edges[i+1]-edges[i] for i in range(count)]
    fd,temp=tempfile.mkstemp(prefix='.atari-preview-',suffix='.webp',dir=path.parent)
    os.close(fd)
    try:
        frames[0].save(temp,format='WEBP',save_all=True,append_images=frames[1:],
                       duration=durations,loop=0,lossless=True,method=4)
        os.replace(temp,path)
    finally:
        if os.path.exists(temp):os.unlink(temp)
    return {'size':size,'frames':len(pictures),'cycle_ms':sum(durations),'bytes':path.stat().st_size}

class AnimationExport(tk.Toplevel):
    def __init__(self,parent,indices,settings,stem='atari-preview',rate=60,retention=.6,on_saved=None):
        super().__init__(parent)
        self.title('Export animated preview for website')
        self.resizable(False,False);self.transient(parent)
        self.indices=np.array(indices,copy=True);self.settings=replace(settings);self.stem=stem;self.on_saved=on_saved
        self.rate=tk.IntVar(self,value=int(rate));self.retention=tk.DoubleVar(self,value=retention*100)
        self.edge=tk.IntVar(self,value=640);self.info=tk.StringVar(self)
        panel=ttk.Frame(self,padding=18);panel.pack(fill='both',expand=True)
        ttk.Label(panel,text='WEBSITE ANIMATION',style='Section.TLabel').pack(anchor='w')
        ttk.Label(panel,text='Looping, lossless WebP · picture only, without window controls.\nUses the completed conversion from when this dialog opened.',wraplength=430).pack(anchor='w',pady=(6,12))
        for label,var,values in [('Frames per second',self.rate,[60,30,10,3]),('Longest side (pixels)',self.edge,[320,640,960])]:
            row=ttk.Frame(panel);row.pack(fill='x',pady=4)
            ttk.Label(row,text=label).pack(side='left')
            box=ttk.Combobox(row,textvariable=var,values=values,state='readonly',width=8);box.pack(side='right')
            box.bind('<<ComboboxSelected>>',lambda e:self.refresh())
        ttk.Label(panel,text='Persistence (%) · 0 exports the raw alternating frames').pack(anchor='w',pady=(10,0))
        self.value_label=ttk.Label(panel);self.value_label.pack(anchor='e')
        ttk.Scale(panel,from_=0,to=80,variable=self.retention,command=lambda v:self.refresh()).pack(fill='x')
        ttk.Label(panel,textvariable=self.info,wraplength=430).pack(anchor='w',pady=10)
        ttk.Label(panel,text='60 fps is nominal NTSC pace. Browser refresh and CRT appearance will differ.\nStatic modes save a still WebP.',wraplength=430,style='Muted.TLabel').pack(anchor='w')
        buttons=ttk.Frame(panel);buttons.pack(fill='x',pady=(14,0))
        ttk.Button(buttons,text='Cancel',command=self.destroy).pack(side='right')
        self.save_button=ttk.Button(buttons,text='Save WebP…',command=self.save,style='Accent.TButton');self.save_button.pack(side='right',padx=8)
        self.refresh()

    def refresh(self):
        self.value_label.configure(text=f'{self.retention.get():.0f}%')
        w,h=preview_size(self.settings,self.edge.get())
        self.info.set(f'{w} × {h} pixels · '+(f'{self.rate.get()} fps · repeats continuously' if frame_count(self.settings.mode)>1 else 'static output'))

    def save(self):
        path=filedialog.asksaveasfilename(parent=self,title='Save website preview',initialfile=self.stem+'.webp',
                                          defaultextension='.webp',filetypes=[('WebP image / animation','*.webp')])
        if not path:return
        try:
            result=export_animation(path,self.indices,self.settings,self.rate.get(),self.retention.get()/100,self.edge.get())
        except Exception as ex:
            messagebox.showerror('Animation export failed',str(ex),parent=self);return
        if self.on_saved:self.on_saved(path,result)
        self.destroy()
