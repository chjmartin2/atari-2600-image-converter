"""Tk desktop workbench. Conversion workers never call Tk."""
from dataclasses import asdict, replace
from pathlib import Path
import json
import os
import queue
import subprocess
import tempfile
import threading
import time
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import numpy as np
from PIL import Image, ImageTk, ImageDraw
from . import __version__
from .core import (Settings, PRESETS, FILTERS, DITHERS, CODES, TIA, MODES, dimensions, cartridge_type, cartridge_size, display_aspect, frame_count, mode_description, prepare, load_image,
                   hardware_palette, target_palette, quantize, optimize, optimize_input, frame_pixels, drag_crop_position, Cancelled)
from .palette_picker import PalettePicker
from .preferences import stella_path, save_stella_path
from .modes import normalize,search_palette,convert_image,render
from .optimization import joint_optimize,fit_controls
from .rom import assembly, binary
from .animation import AnimatedPreview

BG, PANEL, TEXT, MUTED, CYAN, PINK = "#10151c", "#1b2430", "#e1e8ef", "#98abba", "#59d5e7", "#ee7caf"

class ScrollControls(ttk.Frame):
    def __init__(self,parent):
        super().__init__(parent)
        canvas=tk.Canvas(self,bg=BG,highlightthickness=0,width=330)
        bar=ttk.Scrollbar(self,orient="vertical",command=canvas.yview)
        bar.pack(side="right",fill="y");canvas.pack(side="left",fill="both",expand=True)
        canvas.configure(yscrollcommand=bar.set)
        self.inner=ttk.Frame(canvas,padding=12)
        item=canvas.create_window((0,0),window=self.inner,anchor="nw")
        self.inner.bind("<Configure>",lambda e:canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind("<Configure>",lambda e:canvas.itemconfigure(item,width=e.width))

def sample_image():
    """Original calibration artwork; no third-party picture assets required."""
    im = Image.new("RGB",(640,480)); a = np.zeros((480,640,3),np.uint8)
    x = np.linspace(0,255,640); y = np.linspace(0,255,480)
    a[:,:,0] = x; a[:,:,1] = y[:,None]; a[:,:,2] = 255-x
    im = Image.fromarray(a); d = ImageDraw.Draw(im)
    for i,c in enumerate(("white","red","lime","blue","yellow","magenta","cyan","black")):
        d.rectangle((i*80,0,(i+1)*80-1,70),fill=c)
    d.ellipse((190,125,450,385),fill="#10151c",outline="white",width=6)
    d.polygon([(260,205),(395,255),(260,305)],fill="#59d5e7")
    d.text((16,444),"ATARI 2600 IMAGE OPTIMIZER / NTSC",fill="white",stroke_width=1)
    return im

class Preview(ttk.Frame):
    def __init__(self,parent,title):
        super().__init__(parent)
        ttk.Label(self,text=title,style="Section.TLabel").pack(anchor="w",pady=(0,8))
        self.canvas = tk.Canvas(self,bg="#080b0f",highlightthickness=0)
        self.canvas.pack(side="left",fill="both",expand=True)
        y = ttk.Scrollbar(self,orient="vertical",command=self.canvas.yview); y.pack(side="right",fill="y")
        x = ttk.Scrollbar(self,orient="horizontal",command=self.canvas.xview); x.pack(side="bottom",fill="x")
        self.canvas.configure(xscrollcommand=x.set,yscrollcommand=y.set)
        self.image = None; self.zoom = "Fit"; self.smooth = False; self.aspect = "Display 4:3"
        self.canvas.bind("<Configure>",lambda e:self.draw())
        self.canvas.bind("<ButtonPress-1>",lambda e:self.canvas.scan_mark(e.x,e.y))
        self.canvas.bind("<B1-Motion>",lambda e:self.canvas.scan_dragto(e.x,e.y,gain=1))
    def draw(self):
        if self.image is None:return
        w,h = self.canvas.winfo_width(),self.canvas.winfo_height()
        bw,bh = {"Atari pixels 2:1":(384,512),"Display 4:3":(512,384),"BUS raster":(576,480),"Sprite raster":(288,576),"Movie raster":(480,576),"Raw pixels":self.image.size}[self.aspect]
        if self.zoom == "Fit": scale = min(max(w-16,1)/bw,max(h-16,1)/bh)
        else: scale = float(self.zoom[:-1])/100
        dw,dh = max(1,round(bw*scale)),max(1,round(bh*scale))
        self.drawn_size=(dw,dh)
        self.image_bounds=((max(w,dw)-dw)/2,(max(h,dh)-dh)/2,(max(w,dw)+dw)/2,(max(h,dh)+dh)/2)
        self.photo = ImageTk.PhotoImage(self.image.resize((dw,dh),Image.Resampling.BICUBIC if self.smooth else Image.Resampling.NEAREST))
        self.canvas.delete("all")
        self.canvas.create_image(max(w,dw)//2,max(h,dh)//2,image=self.photo)
        self.canvas.configure(scrollregion=(0,0,max(w,dw),max(h,dh)))

class App(tk.Tk):
    def __init__(self, initial=None):
        super().__init__()
        self.title(f"Atari 2600 Image Optimizer {__version__}")
        self.geometry("1320x850"); self.minsize(1000,700); self.configure(bg=BG)
        self.settings = Settings(); self.source = sample_image(); self.source_path = None
        self.result = None; self.busy = False; self.messages = queue.Queue(); self.cancel = threading.Event()
        self.animated_preview = None
        self.pending_manual_fit = self.active_manual_fit = False
        self.pending_input_fit = False
        self.pending_palette_search = False
        self.active_input_fit = False
        self.active_palette_search = False
        self.pending_global = self.active_global = False
        self.crop_drag=None;self.crop_preview_job=None
        self.revision = 0; self.after_preview = None; self.suspend = False; self.last_export = None
        self.vars = {}; self.combos={}; self.status = tk.StringVar(value="Open an image or explore the built-in calibration image.")
        self._style(); self._layout(); self._sync_vars(self.settings)
        self.bind("<Control-o>",lambda e:self.open_image()); self.bind("<Control-s>",lambda e:self.export())
        self.protocol("WM_DELETE_WINDOW",self.close)
        self.after(80,self._poll)
        if initial:self.open_image(initial)
        else:self.convert()

    def _style(self):
        st = ttk.Style(self); st.theme_use("clam")
        st.configure(".",background=BG,foreground=TEXT,font=("Segoe UI",10))
        st.configure("TFrame",background=BG); st.configure("TLabel",background=BG)
        st.configure("Section.TLabel",foreground=CYAN,font=("Segoe UI Semibold",11))
        st.configure("Title.TLabel",foreground=TEXT,font=("Segoe UI Semibold",17))
        st.configure("Muted.TLabel",foreground=MUTED)
        st.configure("TButton",background=PANEL,padding=(12,7)); st.map("TButton",background=[("active","#324456")])
        st.configure("Accent.TButton",background="#185b69",foreground="white")
        st.configure("TCombobox",fieldbackground=PANEL,background=PANEL,foreground=TEXT,arrowcolor=CYAN)
        st.map("TCombobox",fieldbackground=[("readonly",PANEL)],foreground=[("readonly",TEXT)])
        st.configure("TEntry",fieldbackground=PANEL,foreground=TEXT)
        st.configure("TNotebook",background=BG,borderwidth=0)
        st.configure("TNotebook.Tab",background=PANEL,padding=(12,8))
        st.map("TNotebook.Tab",background=[("selected","#294655")],foreground=[("selected",CYAN)])
        st.configure("Horizontal.TProgressbar",background=CYAN,troughcolor=PANEL)
        st.configure("TScale",background=BG,troughcolor=PANEL)
        st.configure("TScrollbar",background="#344557",troughcolor=BG,arrowcolor=MUTED)
        self.option_add("*TCombobox*Listbox.background",PANEL); self.option_add("*TCombobox*Listbox.foreground",TEXT)

    def _layout(self):
        header = ttk.Frame(self,padding=(18,14)); header.pack(fill="x")
        ttk.Label(header,text="ATARI 2600 IMAGE OPTIMIZER",style="Title.TLabel").pack(side="left")
        ttk.Label(header,text="NTSC",style="Section.TLabel").pack(side="left",padx=12)
        ttk.Button(header,text="Open image…",command=self.open_image,style="Accent.TButton").pack(side="right")
        ttk.Button(header,text="Reset all options",command=self.reset_all_options).pack(side="right",padx=8)
        self.file_label = ttk.Label(self,text="Built-in calibration image",style="Muted.TLabel",padding=(20,0)); self.file_label.pack(anchor="w")
        body = ttk.Panedwindow(self,orient="horizontal"); body.pack(fill="both",expand=True,padx=18,pady=12)
        left = ttk.Frame(body,width=360); body.add(left,weight=0)
        tabs = ttk.Notebook(left); tabs.pack(fill="both",expand=True)
        panels=[ScrollControls(tabs) for _ in range(3)]
        adjust,palette,dither=[panel.inner for panel in panels]
        for tab,name in zip(panels,("Image","Palette","Dither")): tabs.add(tab,text=name)
        self._combo(adjust,'Output mode','mode',MODES,callback=self.mode_changed)
        self._combo(adjust,"Scale","scale",["Fit","Fill / crop","Stretch"])
        self.vars['crop_x']=tk.DoubleVar(value=.5);self.vars['crop_y']=tk.DoubleVar(value=.5)
        ttk.Label(adjust,text="Fill / crop: drag the input image to position it.\nShift-drag pans a zoomed preview.",style="Muted.TLabel").pack(anchor="w",pady=(5,0))
        ttk.Button(adjust,text="Center crop",command=self.center_crop).pack(fill="x",pady=(4,0))
        self._combo(adjust,"Resampling","resample",list(FILTERS))
        self._combo(adjust,"Image geometry","aspect",["Atari pixels 2:1","Display 4:3","Raw pixels"])
        self._combo(adjust,"Rotate counterclockwise","rotate",[0,90,180,270],integer=True)
        self._check(adjust,"Mirror horizontally","mirror")
        self._check(adjust,"Optimize input","auto_input",self.input_optimization_changed)
        self.flicker_check=self._check(adjust,"Flicker-aware optimization","flicker_aware")
        self.balance_check=self._check(adjust,"Balance flicker frames","balance_frames")
        ttk.Label(adjust,text="Fits tone and RGB balance for the current palette.\nPalette search alternates input and palette fits.\nUncheck to keep adjustments; check to refit.",style="Muted.TLabel").pack(anchor="w",pady=5)
        for title,name,low,high in [("Brightness","brightness",0,3),("Contrast","contrast",0,3),("Saturation","saturation",0,3),("Gamma","gamma",.2,3),("Sharpness","sharpness",0,3),("Red gain","red",0,3),("Green gain","green",0,3),("Blue gain","blue",0,3)]:
            self._slider(adjust,title,name,low,high)
        ttk.Button(adjust,text="Reset image adjustments",command=self.reset_adjustments).pack(fill="x",pady=8)
        self._combo(palette,"Preset","preset",[*PRESETS,"Custom / optimized"],callback=self.preset_changed)
        ttk.Label(palette,text="Three component colors + one background.\nAll presets use actual Atari color codes.",style="Muted.TLabel").pack(anchor="w",pady=8)
        for i in range(4):self.vars[f"code{i}"]=tk.StringVar()
        ttk.Button(palette,text="Edit palette colors…",command=lambda:self.open_palette_picker(0)).pack(fill="x")
        ttk.Label(palette,text="Click a color beneath the preview to open\nthe Atari color picker.",style="Muted.TLabel").pack(anchor="w",pady=5)
        self._combo(palette,"Quantization targets","mapping",["Temporal blend","Legacy RGB targets"])
        self._combo(palette,"Palette search","search",["Improved weighted","Legacy exhaustive"])
        self._combo(palette,"Search background","background",["Black","Black or white","Any Atari color"])
        self._check(palette,"Prefer palette diversity (legacy search)","diversity")
        ttk.Label(palette,text="Legacy: exhaustive, 8 representative colors.\nImproved: weighted histogram, multi-start search.\nOptimize replaces the selected preset.",style="Muted.TLabel").pack(anchor="w",pady=10)
        ttk.Button(palette,text="Locate / change Stella…",command=self.locate_stella).pack(fill="x",pady=8)
        self._combo(dither,"Dither method","dither",DITHERS)
        self._slider(dither,"Dither strength","strength",0,1)
        self._check(dither,"Serpentine error diffusion","serpentine")
        ttk.Label(dither,text="Ordered: stable repeating patterns.\nError diffusion: spreads color error to neighbors.\nNone: nearest palette color, clean flat areas.\n\nLegacy RGB targets reproduces the original\nideal RGB mapping. It can look much brighter\nthan the cartridge's temporal blend.\n\nPreview colors are estimates. CRT phosphors,\nemulator blending and capture timing affect\nthe real appearance.",style="Muted.TLabel",wraplength=305).pack(anchor="w",pady=14)
        actions = ttk.Frame(left); actions.pack(fill="x",pady=(10,0))
        ttk.Button(actions,text='Adjust input to palette',command=self.adjust_input_to_palette).pack(side='bottom',fill='x',pady=(6,0))
        ttk.Button(actions,text='Global optimize',command=lambda:self.convert(True,True),style='Accent.TButton').pack(side='bottom',fill='x',pady=(6,0))
        ttk.Button(actions,text="Convert",command=self.convert).pack(side="left",expand=True,fill="x")
        ttk.Button(actions,text="Optimize palette",command=lambda:self.convert(True),style="Accent.TButton").pack(side="left",expand=True,fill="x",padx=4)
        ttk.Button(actions,text="Cancel",command=self.cancel_conversion).pack(side="left")
        right = ttk.Frame(body); body.add(right,weight=1)
        controls = ttk.Frame(right); controls.pack(fill="x",pady=(0,10))
        self.zoom = tk.StringVar(value="Fit"); self.view = tk.StringVar(value="Temporal blend"); self.smooth = tk.BooleanVar(value=False)
        for label,var,values in [("Zoom",self.zoom,["Fit","50%","100%","200%","400%"]),("Output",self.view,["Temporal blend","Quantization targets","Frame 1","Frame 2","Frame 3"])]:
            ttk.Label(controls,text=label).pack(side="left",padx=(0,5))
            box = ttk.Combobox(controls,textvariable=var,values=values,state="readonly",width=20 if label=="Output" else 7); box.pack(side="left",padx=(0,12)); box.bind("<<ComboboxSelected>>",lambda e:self.show_result())
            if label=='Output':self.output_combo=box
        ttk.Checkbutton(controls,text="Smooth display",variable=self.smooth,command=self.show_result).pack(side="left")
        ttk.Button(right,text="ATARI Rendering Preview",command=self.show_animated_preview,style="Accent.TButton").pack(anchor="w",pady=(0,10))
        previews = ttk.Panedwindow(right,orient="horizontal"); previews.pack(fill="both",expand=True)
        self.input_preview = Preview(previews,"ADJUSTED INPUT"); self.output_preview = Preview(previews,"CARTRIDGE PREVIEW")
        self.input_preview.canvas.bind('<ButtonPress-1>',self.crop_press)
        self.input_preview.canvas.bind('<B1-Motion>',self.crop_motion)
        self.input_preview.canvas.bind('<ButtonRelease-1>',self.crop_release)
        previews.add(self.input_preview,weight=1); previews.add(self.output_preview,weight=1)
        self.swatches = tk.Canvas(right,height=96,bg=BG,highlightthickness=0,cursor="hand2"); self.swatches.pack(fill="x",pady=10)
        self.swatches.bind('<Configure>',lambda e:self.draw_swatches())
        self.swatches.bind('<Button-1>',self.swatch_clicked)
        self.mode_info=tk.StringVar(value='48 × 128 • custom temporal colors • 4 KB cartridge')
        ttk.Label(right,textvariable=self.mode_info,style="Muted.TLabel",wraplength=650).pack(anchor="w")
        footer = ttk.Frame(self,padding=(18,8)); footer.pack(fill="x")
        for title,cmd in [("Save settings…",self.save_settings),("Load settings…",self.load_settings),("Export ASM + BIN…",self.export),("Save preview…",self.save_preview),("Frame GIF…",self.save_gif),("Open in Stella",self.launch_stella)]:
            button=ttk.Button(footer,text=title,command=cmd);button.pack(side="left",padx=(0,6))
            if cmd==self.export:self.export_button=button
        self.progress = ttk.Progressbar(self,maximum=100); self.progress.pack(fill="x",padx=18)
        ttk.Label(self,textvariable=self.status,padding=(18,8),style="Muted.TLabel").pack(fill="x")
        # Reserve the export/status rows before the expandable work area, including at high DPI.
        body.pack_forget()
        body.pack(fill="both",expand=True,padx=18,pady=12,before=footer)
        footer.pack_configure(side="bottom")
        self.progress.pack_configure(side="bottom")
        for child in self.winfo_children():
            if isinstance(child,ttk.Label) and str(child.cget("textvariable"))==str(self.status):
                child.pack_configure(side="bottom")
        body.pack_forget();body.pack(fill="both",expand=True,padx=18,pady=12)

    def _combo(self,parent,title,name,values,callback=None,integer=False):
        ttk.Label(parent,text=title).pack(anchor="w",pady=(6,2))
        var = tk.IntVar() if integer else tk.StringVar(); self.vars[name] = var
        display=var
        if name=='mode':
            display=tk.StringVar();labels={mode_description(m):m for m in values}
            var.trace_add('write',lambda *args:display.set(mode_description(var.get())))
            values=list(labels)
        box = ttk.Combobox(parent,textvariable=display,values=values,state="readonly",width=31); box.pack(fill="x")
        self.combos[name]=box
        def selected(event):
            if name=='mode':var.set(labels[display.get()])
            callback() if callback else self.changed()
        box.bind("<<ComboboxSelected>>",selected)

    def _check(self,parent,title,name,callback=None):
        v = tk.BooleanVar(); self.vars[name] = v
        widget=ttk.Checkbutton(parent,text=title,variable=v,command=callback or self.changed)
        widget.pack(anchor="w",pady=5)
        return widget

    def _slider(self,parent,title,name,low,high):
        row = ttk.Frame(parent); row.pack(fill="x",pady=(7,0))
        ttk.Label(row,text=title).pack(side="left")
        v = tk.DoubleVar(value=1); self.vars[name] = v
        label = ttk.Label(row,width=5); label.pack(side="right")
        def update(*args):
            label.configure(text=f"{v.get():.2f}"); self.changed()
        v.trace_add("write",update)
        ttk.Scale(parent,from_=low,to=high,variable=v).pack(fill="x")

    def _sync_vars(self,s):
        self.suspend = True
        for name,var in self.vars.items():
            var.set(s.codes[int(name[-1])] if name.startswith("code") else getattr(s,name))
        self.suspend = False
        self.mode_controls()

    def mode_controls(self):
        mode=self.vars['mode'].get()
        self.export_button.configure(text='Export MovieCart…' if mode==MODES[11] else 'Export ASM + BIN…')
        count=frame_count(mode)
        self.flicker_check.configure(state='normal' if count>1 else 'disabled')
        self.balance_check.configure(state='normal' if count>1 else 'disabled')
        self.output_combo.configure(values=['Temporal blend','Quantization targets']+([f'Frame {k+1}' for k in range(count)] if count>1 else []))
        if self.view.get().startswith('Frame') and (count==1 or int(self.view.get()[-1])>count):self.view.set('Temporal blend')
        for name,enabled in (('search',mode==MODES[1]),('mapping',mode==MODES[1]),('preset',mode not in (MODES[0],*MODES[7:])),('background',mode not in (MODES[0],MODES[7]))):
            self.combos[name].configure(state='readonly' if enabled else 'disabled')

    def read_settings(self):
        data = {name:var.get() for name,var in self.vars.items() if not name.startswith("code")}
        data["codes"] = tuple(self.vars[f"code{i}"].get() for i in range(4))
        # Preserve saved/optimized line tables until an image or color control changes.
        if all(getattr(self.settings,k)==v for k,v in data.items() if k not in ('auto_input','flicker_aware','balance_frames','dither','strength','serpentine','search','background')):
            data['line_codes']=self.settings.line_codes
        return normalize(Settings(**data).validate())

    def mode_changed(self):
        self.settings=replace(self.settings,line_codes=())
        if self.vars['mode'].get() in MODES[5:]:self.vars['background'].set('Any Atari color')
        if self.vars['mode'].get()==MODES[0]:
            for i,c in enumerate(PRESETS['RGB (original Chronocolour)']):self.vars[f'code{i}'].set(c)
            self.vars['preset'].set('RGB (original Chronocolour)')
        self.vars['mapping'].set('Temporal blend')
        self.mode_controls()
        self.changed()

    def changed(self):
        if self.suspend:return
        if self.busy:
            # A preview refresh must not replace the requested optimization.
            # Restart it against the latest settings after the stale worker stops.
            self.pending_palette_search |= self.active_palette_search
            self.pending_global |= self.active_global
            self.pending_input_fit |= self.active_input_fit and self.vars['auto_input'].get()
            self.pending_manual_fit |= self.active_manual_fit
            self.cancel.set()
        self.input_preview.canvas.configure(cursor='fleur' if self.vars['scale'].get()=='Fill / crop' else '')
        self.revision += 1; self.result = None
        self.status.set("Settings changed — updating preview…")
        if self.after_preview:self.after_cancel(self.after_preview)
        self.after_preview = self.after(350,self.convert)

    def preset_changed(self):
        name = self.vars["preset"].get()
        if name in PRESETS:
            for i,c in enumerate(PRESETS[name]):self.vars[f"code{i}"].set(c)
            self.vars["mapping"].set("Temporal blend")
        self.changed()

    def input_optimization_changed(self):
        self.pending_input_fit = self.vars['auto_input'].get()
        self.changed()

    def adjust_input_to_palette(self):
        # Cancel any outstanding palette search; this action keeps the latest
        # completed palette fixed, including the full per-row color tables.
        self.cancel_conversion()
        self.pending_manual_fit=True
        self.changed()

    def reset_all_options(self):
        self.cancel_conversion()
        if self.animated_preview is not None:
            self.animated_preview.close();self.animated_preview=None
        if self.crop_preview_job:
            self.after_cancel(self.crop_preview_job);self.crop_preview_job=None
        self.crop_drag=None
        self.settings=Settings()
        self._sync_vars(self.settings)
        self.zoom.set('Fit');self.smooth.set(False);self.view.set('Temporal blend')
        self.last_export=None
        self.changed()

    def code_changed(self):
        self.vars["preset"].set("Custom / optimized"); self.vars["mapping"].set("Temporal blend"); self.changed()

    def reset_adjustments(self):
        self.suspend = True
        defaults = Settings()
        for name in ("scale","resample","aspect","crop_x","crop_y","rotate","mirror","brightness","contrast","saturation","gamma","sharpness","red","green","blue"):
            self.vars[name].set(getattr(defaults,name))
        self.suspend = False; self.changed()

    def center_crop(self):
        self.vars['crop_x'].set(.5);self.vars['crop_y'].set(.5)
        self.crop_drag=None;self.changed()

    def crop_press(self,event):
        canvas=self.input_preview.canvas;self.crop_drag=None
        canvas.scan_mark(event.x,event.y)
        if self.vars['scale'].get()!='Fill / crop' or event.state & 1:return
        if not hasattr(self.input_preview,'image_bounds'):return
        x,y=canvas.canvasx(event.x),canvas.canvasy(event.y)
        x0,y0,x1,y1=self.input_preview.image_bounds
        if not (x0<=x<=x1 and y0<=y<=y1):return
        try:s=self.read_settings()
        except Exception:return
        self.crop_drag=(event.x,event.y,s,self.input_preview.drawn_size,self.source.size)

    def crop_motion(self,event):
        if self.crop_drag is None:
            self.input_preview.canvas.scan_dragto(event.x,event.y,gain=1);return
        x,y,start,size,source_size=self.crop_drag
        # Reconfiguration during a drag must not apply offsets in an old coordinate space.
        if self.vars['scale'].get()!='Fill / crop' or self.source.size!=source_size or self.vars['rotate'].get()!=start.rotate or self.vars['mirror'].get()!=start.mirror or self.vars['aspect'].get()!=start.aspect:
            self.crop_drag=None;return
        cx,cy=drag_crop_position(source_size,start,(event.x-x,event.y-y),size)
        self.vars['crop_x'].set(cx);self.vars['crop_y'].set(cy)
        self.changed()
        if self.crop_preview_job is None:self.crop_preview_job=self.after(16,self.refresh_crop_input)

    def refresh_crop_input(self):
        self.crop_preview_job=None
        try:
            s=self.read_settings();self.input_preview.image=prepare(self.source,s)
            self.input_preview.aspect=display_aspect(s);self.input_preview.draw()
        except Exception as ex:self.status.set(str(ex))

    def crop_release(self,event):
        if self.crop_drag is None:return
        self.crop_drag=None
        if self.after_preview:self.after_cancel(self.after_preview);self.after_preview=None
        self.convert()

    def open_image(self,path=None):
        path = path or filedialog.askopenfilename(title="Open image",filetypes=[("Images","*.png *.jpg *.jpeg *.bmp *.gif *.tif *.tiff *.webp"),("All files","*.*")])
        if not path:return
        try: im = load_image(path)
        except Exception as ex:messagebox.showerror("Cannot open image",str(ex));return
        self.source,self.source_path = im,Path(path)
        self.settings=replace(self.settings,line_codes=())
        self.vars['crop_x'].set(.5);self.vars['crop_y'].set(.5);self.crop_drag=None
        self.file_label.configure(text=f"{Path(path).name}  •  {im.width} × {im.height}")
        self.changed()

    def convert(self,search=False,global_search=False):
        self.pending_palette_search |= search
        self.pending_global |= global_search
        if self.after_preview:self.after_cancel(self.after_preview)
        self.after_preview = None
        if self.busy:
            self.after_preview = self.after(250,self.convert)
            return
        try:
            s = self.read_settings()
            if self.pending_manual_fit and s.mode==self.settings.mode and s.codes==self.settings.codes:
                s=replace(s,line_codes=self.settings.line_codes)
        except Exception as ex:self.status.set(str(ex));return
        self.busy = True; self.cancel.clear(); rev = self.revision; image = self.source.copy()
        search = self.pending_palette_search
        global_search = self.pending_global
        self.pending_global = False
        self.pending_palette_search = False
        manual_fit=self.pending_manual_fit
        self.pending_manual_fit=False
        self.active_manual_fit=manual_fit
        fit_input = manual_fit or (self.pending_input_fit and s.auto_input)
        self.pending_input_fit = False
        self.active_palette_search = search
        self.active_global = global_search
        self.active_input_fit = fit_input
        self.status.set("Optimizing palette and input together…" if search and s.auto_input else "Optimizing palette…" if search else "Adjusting input to the selected palette…" if fit_input else "Converting…"); self.progress["value"] = 0
        def work():
            try:
                start = time.perf_counter()
                progress=lambda p,t:self.messages.put(('progress',p,t))
                if search and (s.auto_input or global_search):
                    s2=joint_optimize(image,s,global_search,progress,self.cancel,
                        lambda a,i,ss,score:self.messages.put(('candidate',rev,a,i,ss,score)))
                elif search:s2=search_palette(prepare(image,s),s,progress,self.cancel)
                else:s2=s
                if fit_input and not search:
                    if s2.mode in MODES[3:] and not s2.line_codes:
                        s2=search_palette(prepare(image,s2),s2,progress,self.cancel)
                    s2=fit_controls(image,s2,global_fit=manual_fit,cancel=self.cancel)
                adjusted,indices,s2=convert_image(image,s2,self.cancel)
                self.messages.put(("done",rev,adjusted,indices,s2,time.perf_counter()-start))
            except Cancelled:self.messages.put(("cancelled",))
            except Exception as ex:self.messages.put(("error",str(ex)))
        threading.Thread(target=work,daemon=True).start()

    def cancel_conversion(self):
        self.cancel.set()
        self.pending_manual_fit = self.active_manual_fit = False
        self.revision += 1
        self.pending_palette_search = self.pending_input_fit = False
        self.pending_global = self.active_global = False
        self.active_palette_search = self.active_input_fit = False
        if self.after_preview:self.after_cancel(self.after_preview);self.after_preview=None

    def _poll(self):
        try:
            while True:
                msg = self.messages.get_nowait()
                if msg[0] == "progress":self.progress["value"] = msg[1]*100;self.status.set(f"{msg[2]} — {msg[1]:.0%}")
                elif msg[0]=='candidate':
                    _,rev,adjusted,indices,s,score=msg
                    if rev==self.revision and not self.cancel.is_set():
                        self.settings=s;self._sync_vars(s);self.result=(adjusted,indices,s)
                        self.status.set(f'Joint optimization pass • perceptual score {score:.5f}')
                        self.show_result()
                elif msg[0] == "done":
                    self.busy = False
                    self.active_palette_search = self.active_input_fit = False
                    self.active_global = False
                    self.active_manual_fit = False
                    _,rev,adjusted,indices,s,elapsed = msg
                    if rev != self.revision:self.status.set("Discarded an outdated conversion; updating…");continue
                    self.settings = s; self._sync_vars(s); self.result = (adjusted,indices,s)
                    self.progress["value"] = 100; self.status.set(f"Ready • {elapsed:.2f} s • input optimization {'on' if s.auto_input else 'off'} • codes {' / '.join('$'+c for c in s.codes)}")
                    self.show_result()
                elif msg[0] == "cancelled":
                    self.busy = False
                    self.active_palette_search = self.active_input_fit = False
                    self.active_global = False
                    self.active_manual_fit = False
                    self.status.set("Settings changed — restarting requested operation…" if self.after_preview else "Cancelled. Previous completed result retained if settings are unchanged.")
                else:
                    self.busy = False
                    self.active_palette_search = self.active_input_fit = False
                    self.active_global = False
                    self.active_manual_fit = False
                    self.status.set("Conversion failed: "+msg[1])
        except queue.Empty:pass
        self.after(80,self._poll)

    def show_result(self):
        if self.result is None:return
        adjusted,indices,s = self.result
        view = self.view.get()
        if view.startswith("Frame"): out = Image.fromarray(frame_pixels(indices,s.codes,s.line_codes,s.mode)[(int(view[-1])-1)%len(frame_pixels(indices,s.codes,s.line_codes,s.mode))])
        elif view=='Quantization targets':
            palette=target_palette(s)
            out=Image.fromarray(palette[np.arange(indices.shape[0])[:,None],np.arange(indices.shape[1])[None,:],indices] if palette.ndim==4 else palette[np.arange(len(indices))[:,None],indices] if palette.ndim==3 else palette[indices])
        else:out=Image.fromarray(render(indices,s))
        w,h=dimensions(s)
        temporal=s.mode in (MODES[0],MODES[1],MODES[3])
        self.mode_info.set(f'{mode_description(s.mode)} • {w} × {h} • '+(f'{frame_count(s.mode)} alternating frames' if frame_count(s.mode)>1 else 'same picture every frame')+f' • {cartridge_size(s.mode)//1024} KB {cartridge_type(s.mode)} ROM'+('\nScanline palettes: swatches show the middle row.' if s.line_codes else ''))
        for preview,im in ((self.input_preview,adjusted),(self.output_preview,out)):
            preview.image = im; preview.zoom = self.zoom.get(); preview.smooth = self.smooth.get(); preview.aspect = display_aspect(s); preview.draw()
        if s.mode==MODES[11]:self.mode_info.set('MovieCart — Flicker • 80 × 192 (190 content rows) • two alternating fields\n30-second silent .mvc stream • MovieCart hardware, not Harmony')
        if s.mode in MODES[8:11]:self.mode_info.set(self.mode_info.get()+'\nSix multiplexed sprite strips; narrow, centered raster • hardware untested')
        if s.mode==MODES[7]:self.mode_info.set(self.mode_info.get()+'\n128 colors available per sample • 9 color clocks wide • Stella verified; hardware untested')
        self.draw_swatches()

    def draw_swatches(self):
        if not all(f'code{i}' in self.vars for i in range(4)):return
        codes=tuple(self.vars[f'code{i}'].get() for i in range(4))
        if any(c not in CODES for c in codes):return
        self.swatches.delete('all')
        width=max(1,self.swatches.winfo_width());cell=width/12
        if self.vars['mode'].get()==MODES[7]:
            self.swatches.create_text(0,8,text='FULL NTSC PALETTE — all 128 colors available; no component restrictions',anchor='w',fill=MUTED,font=('Segoe UI',8))
            for hue in range(16):
                for lum in range(8):
                    color=TIA[CODES.index(f'{hue:X}{lum*2:X}')]
                    hx='#'+''.join(f'{int(v):02x}' for v in color)
                    self.swatches.create_rectangle(hue*width/16+2,24+lum*7,(hue+1)*width/16-2,31+lum*7,fill=hx,outline='')
            return
        if self.vars['mode'].get() in MODES[8:]:
            s=self.read_settings();rows=s.line_codes
            colors=rows[len(rows)//2] if rows else ((s.codes[0],)*10+(s.codes[3],) if s.mode==MODES[11] else s.codes*2 if s.mode in MODES[12:] else s.codes)
            labels=[f'Cell {k+1}' for k in range(10)]+['BG'] if s.mode==MODES[11] else ['A P0','A P1','A P0','A BG','B P0','B P1','B P0','B BG'] if s.mode in MODES[12:] else ['P0','P1','P0','BG']
            cell=width/len(colors)
            self.swatches.create_text(0,8,text='SCANLINE COLORS — middle row; Optimize palette to refit',anchor='w',fill=MUTED,font=('Segoe UI',8))
            for k,(code,label) in enumerate(zip(colors,labels)):
                color=TIA[CODES.index(code)];hx='#'+''.join(f'{int(v):02x}' for v in color)
                self.swatches.create_rectangle(k*cell+2,25,(k+1)*cell-3,52,fill=hx,outline='#546272')
                self.swatches.create_text((k+.5)*cell,55,text=label+'\n$'+code,anchor='n',fill=TEXT,font=('Segoe UI',8))
            return
        self.swatches.create_text(0,8,text='OUTPUT COLORS — click to edit their components',anchor='w',fill=MUTED,font=('Segoe UI',8))
        self.swatches.create_text(cell*8,8,text='COMPONENTS / BACKGROUND',anchor='w',fill=MUTED,font=('Segoe UI',8))
        s=self.read_settings();palette=target_palette(s)
        if palette.ndim==4:
            row=palette[len(palette)//2];palette=np.array([row[0,0],row[0,7],row[20,0],row[20,7]]*2)
        elif palette.ndim==3:palette=palette[len(palette)//2]
        if s.mode in (MODES[2],*MODES[4:6]):palette=palette.copy();palette[:7]=palette[0]
        colors=list(palette)+list(TIA[[CODES.index(c) for c in codes]])
        for i,color in enumerate(colors):
            x=i*cell;tag=f'color{i}'
            hx='#'+''.join(f'{int(v):02x}' for v in color)
            self.swatches.create_rectangle(x+2,25,x+cell-3,52,fill=hx,outline='#546272',tags=(tag,))
            component_label='Component' if cell>=66 else 'Comp.'
            label=(str(i) if s.mode!=MODES[6] else ("L FG","L BG","R FG","R BG")[i%4]) if i<8 else f'{component_label}\n{i-7}' if i<11 else 'Back-\nground'
            if i>=8 and s.mode==MODES[6]:label=("L FG","L BG","R FG","R BG")[i-8]
            if i>=8:label+='\n$'+codes[i-8]
            self.swatches.create_text(x+cell/2,55,text=label,anchor='n',fill=TEXT,font=('Segoe UI',8),tags=(tag,))

    def swatch_clicked(self,event):
        if self.vars['mode'].get() in MODES[7:]:return
        for item in self.swatches.find_overlapping(event.x,event.y,event.x,event.y):
            for tag in self.swatches.gettags(item):
                if tag.startswith('color'):
                    index=int(tag[5:])
                    self.open_palette_picker(index-8 if index>=8 else None,index if index<8 else None)
                    return

    def open_palette_picker(self,component=None,output=None):
        if self.vars['mode'].get() in MODES[3:]:
            self.status.set('Scanline colors are fitted per row. These swatches show the middle row; use Optimize palette to refit all rows.');return
        if self.vars['mode'].get()==MODES[0]:
            self.status.set('Chronocolor classic locks the original RGB colors. Choose Chronocolor custom to edit them.');return
        codes=tuple(self.vars[f'code{i}'].get() for i in range(4))
        components=None
        if self.vars['mode'].get()==MODES[2]:
            component=3 if component==3 or output==7 else 0
            output=None;components=(0,3)
        def apply(codes):
            for i,code in enumerate(codes):self.vars[f'code{i}'].set(code)
            self.code_changed();self.draw_swatches()
        self.palette_picker=PalettePicker(self,codes,apply,component,output,components)
        return self.palette_picker

    def ready(self):
        if self.busy or self.result is None:
            messagebox.showinfo("Convert first","Wait for a completed conversion before previewing or exporting.");return False
        return True

    def show_animated_preview(self):
        if not self.ready():return
        _,indices,settings=self.result
        if self.animated_preview is not None and self.animated_preview.winfo_exists():
            self.animated_preview.set_result(indices,settings)
            self.animated_preview.lift()
        else:
            self.animated_preview=AnimatedPreview(self,indices,settings)

    def export_to(self,folder):
        """Write one coherent bundle into a new folder, never mix stale outputs."""
        if self.result is None or self.busy:raise ValueError("Conversion is not ready")
        _,indices,s = self.result; folder = Path(folder)
        folder.mkdir(parents=True,exist_ok=False)
        if s.mode!=MODES[11]:(folder/"image.asm").write_text(assembly(indices,s.codes,s.mode,s.line_codes),encoding="utf-8")
        (folder/("image.mvc" if s.mode==MODES[11] else "image.bin")).write_bytes(binary(indices,s.codes,s.mode,s.line_codes))
        s.save(folder/"settings.json")
        Image.fromarray(render(indices,s)).save(folder/"preview.png")
        (folder/'mode.txt').write_text(f'{s.mode}\nLogical resolution: {dimensions(s)}\n',encoding='utf-8')
        (folder/"README.txt").write_text(f"Atari 2600 Image Optimizer — NTSC {cartridge_size(s.mode)//1024} KB {cartridge_type(s.mode)} Atari 2600 cartridge\nMode: {mode_description(s.mode)}\nLogical size: {dimensions(s)}\n\nChris Martin's Chrono2 converter. Original Chronocolour kernel and sprite technique: Andrew Davie, with acknowledgements to Eckhard Stohlberg and Thomas Jentzsch. New raster kernels developed for Atari 2600 Image Optimizer.\n\nimage.asm is self-contained DASM source. Rebuild: dasm image.asm -f3 -oimage.bin\nimage.bin is headerless, {cartridge_size(s.mode)//1024} KB {cartridge_type(s.mode)}. Open in Stella using NTSC.\npreview.png is an estimated display image, not a hardware capture.\nReal hardware/Harmony testing remains the user's validation step.\n",encoding="utf-8")
        if s.mode==MODES[11]:
            (folder/"README.txt").write_text("MovieCart still frame — silent, 30 seconds, NTSC.\nOpen image.mvc with Stella 7 or later (MVC mapper), or copy to MovieCart media.\nThis is a stream, not a Harmony cartridge ROM; renaming it .bin will not work.\nTwo alternating fields provide 80 × 192 samples with 190 safe content rows.\npreview.png averages the fields; use ATARI Rendering Preview to inspect flicker.\nSettings and image-data.npz reproduce the stream with chrono.moviecart.binary.\nRob Bairos MovieCart format: https://github.com/lodefmode/moviecart\nReal hardware remains untested.\n",encoding="utf-8")
            np.savez_compressed(folder/"image-data.npz",indices=indices,line_codes=np.array(s.line_codes))
        if s.mode in MODES[8:]:
            doc=Path(__file__).resolve().parents[1]/"ADVANCED-MODES.md"
            if doc.exists():(folder/doc.name).write_bytes(doc.read_bytes())
        if s.mode==MODES[7]:
            with (folder/'README.txt').open('a',encoding='utf-8') as note:
                note.write('\nExperimental BUS2 color raster: 16 x 192 independent NTSC colors; 9 color clocks per sample. Use Stella mapper BUS. Includes a preserved third-party BUS driver from the Stella 7.0 reference archive. See BUS-RESEARCH.md for credits, unverified physical compatibility, and outstanding driver redistribution terms.\n')
            (folder/'BUS-RESEARCH.md').write_text((Path(__file__).resolve().parents[1]/'BUS-RESEARCH.md').read_text(encoding='utf-8'),encoding='utf-8')
        self.last_export = folder/"image.bin"
        return self.last_export

    def export(self):
        if not self.ready():return
        parent = filedialog.askdirectory(title="Choose the parent folder for a new export bundle")
        if not parent:return
        stem = self.source_path.stem if self.source_path else "calibration"
        folder = Path(parent)/f"{stem}-chrono2-{time.strftime('%Y%m%d-%H%M%S')}"
        try:self.export_to(folder)
        except Exception as ex:messagebox.showerror("Export failed",str(ex));return
        self.status.set(f"Exported ASM, BIN, settings and preview to {folder}")

    def save_settings(self):
        path = filedialog.asksaveasfilename(defaultextension=".json",filetypes=[("Conversion settings","*.json")])
        if path:
            try:self.read_settings().save(path)
            except Exception as ex:messagebox.showerror("Settings",str(ex))

    def load_settings(self):
        path = filedialog.askopenfilename(filetypes=[("Conversion settings","*.json")])
        if path:
            try:self.settings=Settings.load(path);self._sync_vars(self.settings);self.changed()
            except Exception as ex:messagebox.showerror("Settings",str(ex))

    def save_preview(self):
        if not self.ready():return
        path = filedialog.asksaveasfilename(defaultextension=".png",filetypes=[("PNG image","*.png")])
        if path:
            self.show_result(); self.output_preview.image.save(path)
            self.status.set("Saved the selected output view at its logical resolution.")

    def save_gif(self):
        if not self.ready():return
        path = filedialog.asksaveasfilename(defaultextension=".gif",filetypes=[("Animated GIF","*.gif")])
        if path:
            _,indices,s = self.result
            size = (480,576) if s.mode==MODES[11] else (288,576) if s.mode in (*MODES[8:11],*MODES[14:]) else (576,480) if s.mode==MODES[7] else (512,384) if s.mode in MODES[5:8] else {"Atari pixels 2:1":(384,512),"Display 4:3":(512,384),"Raw pixels":dimensions(s)}[s.aspect]
            frames = [Image.fromarray(f).resize(size,Image.Resampling.NEAREST) for f in frame_pixels(indices,s.codes,s.line_codes,s.mode)]
            frames[0].save(path,save_all=True,append_images=frames[1:],duration=100,loop=0)
            self.status.set("Saved a slowed field/frame illustration (100 ms/frame), not an NTSC timing simulation.")

    def locate_stella(self):
        previous=stella_path()
        initial=previous.parent if previous else Path(os.environ.get('PROGRAMFILES',r'C:\Program Files'))/'Stella'
        options={'initialdir':str(initial)} if initial.is_dir() else {}
        selected=filedialog.askopenfilename(parent=self,title='Locate Stella.exe — saved for future use',
                                            filetypes=[('Stella application','Stella.exe')],**options)
        if not selected:return None
        try:exe=save_stella_path(selected)
        except (OSError,ValueError) as ex:
            messagebox.showerror('Stella setup',str(ex),parent=self);return None
        self.status.set(f'Stella location saved: {exe}')
        return exe

    def launch_stella(self):
        if not self.ready():return
        exe=stella_path()
        if exe is None:
            if not messagebox.askyesno('Stella not found',
                'Stella was not found in its default installation folders or your saved location.\n\n'
                'If Stella is already installed, choose Yes to locate Stella.exe.\n'
                'Otherwise, you need to install Stella first, then try Open in Stella again.\n\n'
                'Locate Stella now?',parent=self):return
            exe=self.locate_stella()
        if exe is None:return
        try:
            folder = Path(tempfile.mkdtemp(prefix="chrono2-stella-"))
            s=self.result[2]
            rom = folder/("preview.mvc" if s.mode==MODES[11] else "preview.bin")
            rom.write_bytes(binary(self.result[1],s.codes,s.mode,s.line_codes))
            subprocess.Popen([str(exe),"-format","NTSC","-type",cartridge_type(s.mode),str(rom)])
        except OSError as ex:
            messagebox.showerror('Could not open Stella',f'{ex}\n\nUse Locate / change Stella in the Palette tab to select another installation.',parent=self)
            return
        self.status.set('Opened the current conversion in Stella (NTSC / '+cartridge_type(s.mode)+').')

    def close(self):
        if self.crop_preview_job is not None:self.after_cancel(self.crop_preview_job)
        if self.animated_preview is not None and self.animated_preview.winfo_exists():
            self.animated_preview.close()
        self.cancel.set(); self.destroy()

def main():
    import sys
    App(sys.argv[1] if len(sys.argv)>1 else None).mainloop()
