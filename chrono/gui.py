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
from .core import (Settings, PRESETS, FILTERS, DITHERS, CODES, TIA, prepare, load_image,
                   hardware_palette, target_palette, quantize, optimize, frame_pixels, Cancelled)
from .rom import assembly, binary

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
    d.text((16,444),"CHRONO2 / NTSC / 48 x 128",fill="white",stroke_width=1)
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
        bw,bh = {"Atari pixels 2:1":(384,512),"Display 4:3":(512,384),"Raw pixels":self.image.size}[self.aspect]
        if self.zoom == "Fit": scale = min(max(w-16,1)/bw,max(h-16,1)/bh)
        else: scale = float(self.zoom[:-1])/100
        dw,dh = max(1,round(bw*scale)),max(1,round(bh*scale))
        self.photo = ImageTk.PhotoImage(self.image.resize((dw,dh),Image.Resampling.BICUBIC if self.smooth else Image.Resampling.NEAREST))
        self.canvas.delete("all")
        self.canvas.create_image(max(w,dw)//2,max(h,dh)//2,image=self.photo)
        self.canvas.configure(scrollregion=(0,0,max(w,dw),max(h,dh)))

class App(tk.Tk):
    def __init__(self, initial=None):
        super().__init__()
        self.title(f"Chrono2 Studio {__version__} — Atari 2600 Image Converter")
        self.geometry("1320x850"); self.minsize(1000,700); self.configure(bg=BG)
        self.settings = Settings(); self.source = sample_image(); self.source_path = None
        self.result = None; self.busy = False; self.messages = queue.Queue(); self.cancel = threading.Event()
        self.revision = 0; self.after_preview = None; self.suspend = False; self.last_export = None
        self.vars = {}; self.status = tk.StringVar(value="Open an image or explore the built-in calibration image.")
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
        st.configure("Title.TLabel",foreground=TEXT,font=("Segoe UI Semibold",23))
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
        ttk.Label(header,text="CHRONO2",style="Title.TLabel").pack(side="left")
        ttk.Label(header,text="  STUDIO  /  ATARI 2600  /  NTSC",style="Section.TLabel").pack(side="left",padx=12)
        ttk.Button(header,text="Open image…",command=self.open_image,style="Accent.TButton").pack(side="right")
        self.file_label = ttk.Label(self,text="Built-in calibration image",style="Muted.TLabel",padding=(20,0)); self.file_label.pack(anchor="w")
        body = ttk.Panedwindow(self,orient="horizontal"); body.pack(fill="both",expand=True,padx=18,pady=12)
        left = ttk.Frame(body,width=360); body.add(left,weight=0)
        tabs = ttk.Notebook(left); tabs.pack(fill="both",expand=True)
        panels=[ScrollControls(tabs) for _ in range(3)]
        adjust,palette,dither=[panel.inner for panel in panels]
        for tab,name in zip(panels,("Image","Palette","Dither")): tabs.add(tab,text=name)
        self._combo(adjust,"Scale","scale",["Fit","Fill / crop","Stretch"])
        self._combo(adjust,"Resampling","resample",list(FILTERS))
        self._combo(adjust,"Image geometry","aspect",["Atari pixels 2:1","Display 4:3","Raw pixels"])
        self._combo(adjust,"Rotate counterclockwise","rotate",[0,90,180,270],integer=True)
        self._check(adjust,"Mirror horizontally","mirror")
        for title,name,low,high in [("Brightness","brightness",0,3),("Contrast","contrast",0,3),("Saturation","saturation",0,3),("Gamma","gamma",.2,3),("Sharpness","sharpness",0,3),("Red gain","red",0,3),("Green gain","green",0,3),("Blue gain","blue",0,3)]:
            self._slider(adjust,title,name,low,high)
        ttk.Button(adjust,text="Reset image adjustments",command=self.reset_adjustments).pack(fill="x",pady=8)
        self._combo(palette,"Preset","preset",[*PRESETS,"Custom / optimized"],callback=self.preset_changed)
        ttk.Label(palette,text="Three component colors + one background.\nAll presets use actual Atari color codes.",style="Muted.TLabel").pack(anchor="w",pady=8)
        for i,name in enumerate(("Component 1","Component 2","Component 3","Background")):
            self._combo(palette,name,f"code{i}",CODES,callback=self.code_changed)
        self._combo(palette,"Quantization targets","mapping",["Temporal blend","Legacy RGB targets"])
        self._combo(palette,"Palette search","search",["Improved weighted","Legacy exhaustive"])
        self._combo(palette,"Search background","background",["Black","Black or white","Any Atari color"])
        self._check(palette,"Prefer palette diversity (legacy search)","diversity")
        ttk.Label(palette,text="Legacy: exhaustive, 8 representative colors.\nImproved: weighted histogram, multi-start search.\nOptimize replaces the selected preset.",style="Muted.TLabel").pack(anchor="w",pady=10)
        self._combo(dither,"Dither method","dither",DITHERS)
        self._slider(dither,"Dither strength","strength",0,1)
        self._check(dither,"Serpentine error diffusion","serpentine")
        ttk.Label(dither,text="Ordered: stable repeating patterns.\nError diffusion: spreads color error to neighbors.\nNone: nearest palette color, clean flat areas.\n\nLegacy RGB targets reproduces the original\nideal RGB mapping. It can look much brighter\nthan the cartridge's temporal blend.\n\nPreview colors are estimates. CRT phosphors,\nemulator blending and capture timing affect\nthe real appearance.",style="Muted.TLabel",wraplength=305).pack(anchor="w",pady=14)
        actions = ttk.Frame(left); actions.pack(fill="x",pady=(10,0))
        ttk.Button(actions,text="Convert",command=self.convert).pack(side="left",expand=True,fill="x")
        ttk.Button(actions,text="Optimize palette",command=lambda:self.convert(True),style="Accent.TButton").pack(side="left",expand=True,fill="x",padx=4)
        ttk.Button(actions,text="Cancel",command=self.cancel.set).pack(side="left")
        right = ttk.Frame(body); body.add(right,weight=1)
        controls = ttk.Frame(right); controls.pack(fill="x",pady=(0,10))
        self.zoom = tk.StringVar(value="Fit"); self.view = tk.StringVar(value="Temporal blend"); self.smooth = tk.BooleanVar(value=False)
        for label,var,values in [("Zoom",self.zoom,["Fit","50%","100%","200%","400%"]),("Output",self.view,["Temporal blend","Quantization targets","Frame 1","Frame 2","Frame 3"])]:
            ttk.Label(controls,text=label).pack(side="left",padx=(0,5))
            box = ttk.Combobox(controls,textvariable=var,values=values,state="readonly",width=20 if label=="Output" else 7); box.pack(side="left",padx=(0,12)); box.bind("<<ComboboxSelected>>",lambda e:self.show_result())
        ttk.Checkbutton(controls,text="Smooth display",variable=self.smooth,command=self.show_result).pack(side="left")
        previews = ttk.Panedwindow(right,orient="horizontal"); previews.pack(fill="both",expand=True)
        self.input_preview = Preview(previews,"ADJUSTED INPUT"); self.output_preview = Preview(previews,"CARTRIDGE PREVIEW")
        previews.add(self.input_preview,weight=1); previews.add(self.output_preview,weight=1)
        self.swatches = tk.Canvas(right,height=58,bg=BG,highlightthickness=0); self.swatches.pack(fill="x",pady=10)
        ttk.Label(right,text="48 × 128 logical pixels • 3 interleaved frames • 4 KB cartridge\nAtari view uses the original 2:1 pixel geometry. Drag to pan when zoomed.",style="Muted.TLabel").pack(anchor="w")
        footer = ttk.Frame(self,padding=(18,8)); footer.pack(fill="x")
        for title,cmd in [("Save settings…",self.save_settings),("Load settings…",self.load_settings),("Export ASM + BIN…",self.export),("Save preview…",self.save_preview),("Frame GIF…",self.save_gif),("Open in Stella",self.launch_stella)]:
            ttk.Button(footer,text=title,command=cmd).pack(side="left",padx=(0,6))
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
        box = ttk.Combobox(parent,textvariable=var,values=values,state="readonly",width=31); box.pack(fill="x")
        box.bind("<<ComboboxSelected>>",lambda e:(callback() if callback else self.changed()))

    def _check(self,parent,title,name):
        v = tk.BooleanVar(); self.vars[name] = v
        ttk.Checkbutton(parent,text=title,variable=v,command=self.changed).pack(anchor="w",pady=5)

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

    def read_settings(self):
        data = {name:var.get() for name,var in self.vars.items() if not name.startswith("code")}
        data["codes"] = tuple(self.vars[f"code{i}"].get() for i in range(4))
        return Settings(**data).validate()

    def changed(self):
        if self.suspend:return
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

    def code_changed(self):
        self.vars["preset"].set("Custom / optimized"); self.vars["mapping"].set("Temporal blend"); self.changed()

    def reset_adjustments(self):
        self.suspend = True
        defaults = Settings()
        for name in ("scale","resample","aspect","rotate","mirror","brightness","contrast","saturation","gamma","sharpness","red","green","blue"):
            self.vars[name].set(getattr(defaults,name))
        self.suspend = False; self.changed()

    def open_image(self,path=None):
        path = path or filedialog.askopenfilename(title="Open image",filetypes=[("Images","*.png *.jpg *.jpeg *.bmp *.gif *.tif *.tiff *.webp"),("All files","*.*")])
        if not path:return
        try: im = load_image(path)
        except Exception as ex:messagebox.showerror("Cannot open image",str(ex));return
        self.source,self.source_path = im,Path(path)
        self.file_label.configure(text=f"{Path(path).name}  •  {im.width} × {im.height}")
        self.changed()

    def convert(self,search=False):
        self.after_preview = None
        if self.busy:
            if search:self.status.set("A conversion is running; cancel or wait before starting palette search.")
            else:self.after_preview = self.after(250,self.convert)
            return
        try:s = self.read_settings()
        except Exception as ex:self.status.set(str(ex));return
        self.busy = True; self.cancel.clear(); rev = self.revision; image = self.source.copy()
        self.status.set("Optimizing palette…" if search else "Converting…"); self.progress["value"] = 0
        def work():
            try:
                start = time.perf_counter(); adjusted = prepare(image,s)
                if search:
                    codes,score = optimize(adjusted,s,lambda p,t:self.messages.put(("progress",p,t)),self.cancel)
                    s2 = replace(s,codes=codes,preset="Custom / optimized",mapping="Temporal blend")
                else:s2 = s
                indices = quantize(adjusted,target_palette(s2),s2.dither,s2.strength,s2.serpentine,self.cancel)
                self.messages.put(("done",rev,adjusted,indices,s2,time.perf_counter()-start))
            except Cancelled:self.messages.put(("cancelled",))
            except Exception as ex:self.messages.put(("error",str(ex)))
        threading.Thread(target=work,daemon=True).start()

    def _poll(self):
        try:
            while True:
                msg = self.messages.get_nowait()
                if msg[0] == "progress":self.progress["value"] = msg[1]*100;self.status.set(f"{msg[2]} — {msg[1]:.0%}")
                elif msg[0] == "done":
                    self.busy = False
                    _,rev,adjusted,indices,s,elapsed = msg
                    if rev != self.revision:self.status.set("Discarded an outdated conversion; updating…");continue
                    self.settings = s; self._sync_vars(s); self.result = (adjusted,indices,s)
                    self.progress["value"] = 100; self.status.set(f"Ready • {elapsed:.2f} s • codes {' / '.join('$'+c for c in s.codes)} • ASM and BIN match this conversion")
                    self.show_result()
                elif msg[0] == "cancelled":self.busy = False;self.status.set("Cancelled. Previous completed result retained if settings are unchanged.")
                else:self.busy = False;self.status.set("Conversion failed: "+msg[1])
        except queue.Empty:pass
        self.after(80,self._poll)

    def show_result(self):
        if self.result is None:return
        adjusted,indices,s = self.result
        view = self.view.get()
        if view.startswith("Frame"): out = Image.fromarray(frame_pixels(indices,s.codes)[int(view[-1])-1])
        else:out = Image.fromarray((target_palette(s) if view == "Quantization targets" else hardware_palette(s.codes))[indices])
        for preview,im in ((self.input_preview,adjusted),(self.output_preview,out)):
            preview.image = im; preview.zoom = self.zoom.get(); preview.smooth = self.smooth.get(); preview.aspect = s.aspect; preview.draw()
        self.swatches.delete("all")
        for i,color in enumerate(hardware_palette(s.codes)):
            x = i*70; hx = "#"+"".join(f"{v:02x}" for v in color)
            self.swatches.create_rectangle(x,0,x+64,27,fill=hx,outline="#546272")
            self.swatches.create_text(x+32,43,text=str(i),fill=MUTED)

    def ready(self):
        if self.busy or self.result is None:
            messagebox.showinfo("Convert first","Wait for a completed conversion before exporting.");return False
        return True

    def export_to(self,folder):
        """Write one coherent bundle into a new folder, never mix stale outputs."""
        if self.result is None or self.busy:raise ValueError("Conversion is not ready")
        _,indices,s = self.result; folder = Path(folder)
        folder.mkdir(parents=True,exist_ok=False)
        (folder/"image.asm").write_text(assembly(indices,s.codes),encoding="utf-8")
        (folder/"image.bin").write_bytes(binary(indices,s.codes))
        s.save(folder/"settings.json")
        Image.fromarray(hardware_palette(s.codes)[indices]).save(folder/"preview.png")
        (folder/"README.txt").write_text("Chrono2 Studio — NTSC 4 KB Atari 2600 cartridge\n\nUses Andrew Davie's 2003 Interleaved Chronocolour kernel, with acknowledgements to Eckhard Stohlberg and Thomas Jentzsch. Python conversion follows Chris Martin's Chrono2 work.\n\nimage.asm is self-contained DASM source. Rebuild: dasm image.asm -f3 -oimage.bin\nimage.bin is headerless, standard 4 KB. Open in Stella using NTSC.\npreview.png is a 48x128 temporal-blend estimate, not a hardware capture.\nReal hardware/Harmony testing remains the user's validation step.\n",encoding="utf-8")
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
            try:self._sync_vars(Settings.load(path));self.changed()
            except Exception as ex:messagebox.showerror("Settings",str(ex))

    def save_preview(self):
        if not self.ready():return
        path = filedialog.asksaveasfilename(defaultextension=".png",filetypes=[("PNG image","*.png")])
        if path:
            self.show_result(); self.output_preview.image.save(path)
            self.status.set("Saved the selected output view at its logical 48 × 128 resolution.")

    def save_gif(self):
        if not self.ready():return
        path = filedialog.asksaveasfilename(defaultextension=".gif",filetypes=[("Animated GIF","*.gif")])
        if path:
            _,indices,s = self.result
            size = {"Atari pixels 2:1":(384,512),"Display 4:3":(512,384),"Raw pixels":(48,128)}[s.aspect]
            frames = [Image.fromarray(f).resize(size,Image.Resampling.NEAREST) for f in frame_pixels(indices,s.codes)]
            frames[0].save(path,save_all=True,append_images=frames[1:],duration=100,loop=0)
            self.status.set("Saved a slowed 3-frame illustration (100 ms/frame), not an NTSC timing simulation.")

    def launch_stella(self):
        if not self.ready():return
        exe = Path(os.environ.get("PROGRAMFILES",r"C:\Program Files"))/"Stella"/"Stella.exe"
        if not exe.exists():
            selected = filedialog.askopenfilename(title="Locate Stella.exe",filetypes=[("Stella executable","*.exe")])
            if not selected:return
            exe = Path(selected)
        folder = Path(tempfile.mkdtemp(prefix="chrono2-stella-")); rom = folder/"preview.bin"
        rom.write_bytes(binary(self.result[1],self.result[2].codes))
        subprocess.Popen([str(exe),"-format","NTSC","-type","4K",str(rom)])

    def close(self):
        self.cancel.set(); self.destroy()

def main():
    import sys
    App(sys.argv[1] if len(sys.argv)>1 else None).mainloop()
