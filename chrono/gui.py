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
        def wheel(event):
            widget=self.winfo_containing(event.x_root,event.y_root)
            while widget is not None and widget is not self:widget=getattr(widget,'master',None)
            if widget is self and event.delta:
                canvas.yview_scroll(-1 if event.delta>0 else 1,'units')
                return 'break'
        self.bind_all('<MouseWheel>',wheel,add='+')

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

class Disclosure(ttk.Frame):
    def __init__(self,parent,title,opened=False):
        super().__init__(parent)
        self.pack(fill='x',pady=(2,6))
        self.title=title;self.opened=opened
        self.button=ttk.Button(self,command=self.toggle)
        self.button.pack(fill='x')
        self.inner=ttk.Frame(self,padding=(4,4))
        self.render()
    def toggle(self):
        self.opened=not self.opened;self.render()
    def render(self):
        self.button.configure(text=('▾  ' if self.opened else '▸  ')+self.title)
        if self.opened:self.inner.pack(fill='x')
        else:self.inner.pack_forget()

class Preview(ttk.Frame):
    def __init__(self,parent,title):
        super().__init__(parent)
        self.heading=ttk.Label(self,text=title,style="Section.TLabel"); self.heading.pack(anchor="w",pady=(0,8))
        self.toolbar=ttk.Frame(self);self.toolbar.pack(fill="x",pady=(0,6))
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
        bw,bh = {"Atari pixels 2:1":(384,512),"Display 4:3":(512,384),"BUS raster":(576,480),"Sprite raster":(288,576),"Wide raster":(1,1),"Movie raster":(480,576),"Raw pixels":self.image.size}[self.aspect]
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
        self.pending_action=None;self.active_action=None
        self.before_result=None;self.compare_before=tk.BooleanVar(value=False)
        self.result_current=False
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
        menu=tk.Menu(self)
        file_menu=tk.Menu(menu,tearoff=False)
        for title,command in [('Open image…',self.open_image),('Load settings…',self.load_settings),
                              ('Save settings…',self.save_settings),('Save preview…',self.save_preview),
                              ('Export animated preview…',self.export_animated_preview),
                              ('Save frame GIF…',self.save_gif),('Locate / change Stella…',self.locate_stella)]:
            file_menu.add_command(label=title,command=command)
        menu.add_cascade(label='File',menu=file_menu);self.configure(menu=menu)
        header=ttk.Frame(self,padding=(18,10));header.pack(fill='x')
        ttk.Label(header,text='ATARI 2600 IMAGE OPTIMIZER',style='Title.TLabel').pack(side='left')
        ttk.Button(header,text='Open image…',command=self.open_image,style='Accent.TButton').pack(side='right')
        ttk.Button(header,text='Reset all options',command=self.reset_all_options).pack(side='right',padx=8)
        self.file_label=ttk.Label(self,text='Built-in calibration image',style='Muted.TLabel',padding=(20,0));self.file_label.pack(anchor='w')
        self.status_label=ttk.Label(self,textvariable=self.status,padding=(18,6),style='Muted.TLabel',wraplength=1100)
        self.status_label.pack(side='bottom',fill='x')
        self.progress=ttk.Progressbar(self,maximum=100);self.progress.pack(side='bottom',fill='x',padx=18)
        footer=ttk.Frame(self,padding=(18,8));footer.pack(side='bottom',fill='x')
        self.export_button=ttk.Button(footer,text='Export ASM + BIN…',command=self.export,style='Accent.TButton');self.export_button.pack(side='right')
        ttk.Button(footer,text='Open in Stella',command=self.launch_stella).pack(side='right',padx=8)
        ttk.Button(footer,text='ATARI Rendering Preview',command=self.show_animated_preview).pack(side='right')
        self.compare_button=ttk.Checkbutton(footer,text='Compare: before optimization',variable=self.compare_before,command=self.show_result)
        self.compare_button.pack(side='left');self.compare_button.state(['disabled'])
        self.undo_button=ttk.Button(footer,text='Undo optimization',command=self.undo_optimization,state='disabled');self.undo_button.pack(side='left',padx=8)
        body=ttk.Panedwindow(self,orient='horizontal');body.pack(fill='both',expand=True,padx=18,pady=10)
        left=ttk.Frame(body,width=350);body.add(left,weight=0)
        self._combo(left,'Output mode · NTSC','mode',MODES,callback=self.mode_changed)
        self.mode_summary=tk.StringVar();ttk.Label(left,textvariable=self.mode_summary,style='Muted.TLabel',wraplength=325).pack(anchor='w',pady=(5,8))
        actions=ttk.Frame(left);actions.pack(side='bottom',fill='x',pady=(8,0))
        self._combo(actions,'Optimize','optimization_scope',['Image + colors','Image only','Colors only'],callback=self.scope_changed)
        self.scope_help=tk.StringVar();ttk.Label(actions,textvariable=self.scope_help,wraplength=325,style='Muted.TLabel').pack(fill='x',pady=5)
        buttons=ttk.Frame(actions);buttons.pack(fill='x')
        self.optimize_button=ttk.Button(buttons,text='Optimize',command=self.start_optimization,style='Accent.TButton');self.optimize_button.pack(side='left',fill='x',expand=True)
        ttk.Button(buttons,text='Cancel',command=self.cancel_conversion).pack(side='left',padx=(5,0))
        panel=ScrollControls(left);panel.pack(fill='both',expand=True)
        self.image_section=Disclosure(panel.inner,'Image preparation',True);adjust=self.image_section.inner
        self._combo(adjust,'Scaling','scale',['Fit','Fill / crop','Stretch'])
        ttk.Label(adjust,text='Crop zoom and drag are above/on the input. Stretch ignores aspect ratio.',wraplength=295,style='Muted.TLabel').pack(anchor='w',pady=5)
        self.vars['crop_x']=tk.DoubleVar(value=.5);self.vars['crop_y']=tk.DoubleVar(value=.5)
        self._combo(adjust,'Resampling','resample',list(FILTERS))
        for title,name in [('Brightness','brightness'),('Contrast','contrast'),('Saturation','saturation')]:self._slider(adjust,title,name,0,3)
        advanced=Disclosure(adjust,'Advanced image adjustments').inner
        self._combo(advanced,'Image geometry','aspect',['Atari pixels 2:1','Display 4:3','Raw pixels'])
        self._combo(advanced,'Rotate counterclockwise','rotate',[0,90,180,270],integer=True)
        self._check(advanced,'Mirror horizontally','mirror')
        for title,name,lo in [('Input gamma','gamma',.2),('Sharpness','sharpness',0),('Red gain','red',0),('Green gain','green',0),('Blue gain','blue',0)]:self._slider(advanced,title,name,lo,3)
        ttk.Button(adjust,text='Reset image adjustments',command=self.reset_adjustments).pack(fill='x',pady=6)
        self.palette_section=Disclosure(panel.inner,'Colors',True);palette=self.palette_section.inner
        self.palette_help=tk.StringVar();ttk.Label(palette,textvariable=self.palette_help,style='Muted.TLabel',wraplength=295).pack(fill='x')
        self._combo(palette,'Preset','preset',[*PRESETS,'Custom / optimized'],callback=self.preset_changed)
        for i in range(4):self.vars[f'code{i}']=tk.StringVar()
        self.edit_palette_button=ttk.Button(palette,text='Edit palette colors…',command=lambda:self.open_palette_picker(0));self.edit_palette_button.pack(fill='x',pady=5)
        self.row_controls=ttk.Frame(palette)
        ttk.Label(self.row_controls,text='Inspect row (read-only)').pack(side='left')
        self.inspect_row=tk.IntVar(value=64)
        self.row_spinner=ttk.Spinbox(self.row_controls,from_=0,to=127,textvariable=self.inspect_row,width=5,command=self.draw_swatches);self.row_spinner.pack(side='right')
        self.row_spinner.bind('<Return>',lambda e:self.draw_swatches());self.row_spinner.bind('<FocusOut>',lambda e:self.draw_swatches())
        dither=Disclosure(panel.inner,'Dithering').inner
        self._combo(dither,'Method','dither',DITHERS);self._slider(dither,'Strength','strength',0,1)
        self._check(dither,'Serpentine error diffusion','serpentine')
        ttk.Label(dither,text='None keeps flat areas clean. Ordered makes repeating patterns. Diffusion spreads error between pixels.',wraplength=295,style='Muted.TLabel').pack(fill='x')
        self.flicker_section=Disclosure(panel.inner,'Flicker handling')
        self.flicker_summary=tk.StringVar();ttk.Label(self.flicker_section.inner,textvariable=self.flicker_summary,wraplength=295,style='Muted.TLabel').pack(fill='x')
        self.flicker_check=self._check(self.flicker_section.inner,'Score temporal brightness','flicker_aware')
        self.balance_check=self._check(self.flicker_section.inner,'Balance frames where supported','balance_frames')
        advanced=Disclosure(panel.inner,'Advanced search').inner
        self._combo(advanced,'Search effort','search_effort',['Standard','Thorough'],callback=self.scope_changed)
        self.effort_help=tk.StringVar();ttk.Label(advanced,textvariable=self.effort_help,wraplength=295,style='Muted.TLabel').pack(fill='x',pady=4)
        self._combo(advanced,'Palette algorithm (custom Chronocolor)','search',['Improved weighted','Legacy exhaustive'])
        self._combo(advanced,'Search background','background',['Black','Black or white','Any Atari color'])
        self.diversity_check=self._check(advanced,'Prefer diversity (legacy search)','diversity')
        self._combo(advanced,'Quantization targets','mapping',['Temporal blend'])
        right=ttk.Frame(body);body.add(right,weight=1)
        controls=ttk.Frame(right);controls.pack(fill='x',pady=(0,8))
        self.zoom=tk.StringVar(value='Fit');self.view=tk.StringVar(value='Temporal blend');self.smooth=tk.BooleanVar(value=False)
        for label,var,values in [('View size',self.zoom,['Fit','50%','100%','200%','400%']),('Output',self.view,['Temporal blend','Quantization targets','Frame 1','Frame 2','Frame 3'])]:
            ttk.Label(controls,text=label).pack(side='left',padx=(0,5))
            box=ttk.Combobox(controls,textvariable=var,values=values,state='readonly',width=20 if label=='Output' else 7);box.pack(side='left',padx=(0,12));box.bind('<<ComboboxSelected>>',lambda e:self.show_result())
            if label=='Output':self.output_combo=box
        ttk.Checkbutton(controls,text='Smooth display',variable=self.smooth,command=self.show_result).pack(side='left')
        previews=ttk.Panedwindow(right,orient='horizontal');previews.pack(fill='both',expand=True)
        self.input_preview=Preview(previews,'INPUT');self.output_preview=Preview(previews,'ATARI OUTPUT')
        self.input_view=tk.StringVar(value='Adjusted input')
        box=ttk.Combobox(self.input_preview.toolbar,textvariable=self.input_view,values=['Adjusted input','Original input'],state='readonly',width=19);box.pack(fill='x');box.bind('<<ComboboxSelected>>',lambda e:self.show_result())
        self._slider(self.input_preview.toolbar,'Crop zoom','crop_zoom',1,8)
        crop_buttons=ttk.Frame(self.input_preview.toolbar);crop_buttons.pack(fill='x')
        ttk.Button(crop_buttons,text='Center',command=self.center_crop).pack(side='left')
        ttk.Button(crop_buttons,text='Reset crop',command=self.reset_crop).pack(side='left',padx=5)
        ttk.Label(self.input_preview.toolbar,text='Drag adjusted input to position crop. Shift-drag pans the view.',style='Muted.TLabel',wraplength=350).pack(fill='x',pady=3)
        self.input_preview.canvas.bind('<ButtonPress-1>',self.crop_press)
        self.input_preview.canvas.bind('<B1-Motion>',self.crop_motion)
        self.input_preview.canvas.bind('<ButtonRelease-1>',self.crop_release)
        self.output_notice=tk.StringVar(value='Light-corrected preview · estimated Atari colors. Check the cartridge in Stella.')
        ttk.Label(self.output_preview.toolbar,textvariable=self.output_notice,wraplength=350,style='Muted.TLabel').pack(fill='x')
        self.animation_export_button=ttk.Button(self.output_preview.toolbar,text='Export animated preview…',command=self.export_animated_preview)
        self.animation_export_button.pack(anchor='w',pady=8)
        self.output_preview.toolbar.pack_propagate(False)
        self.input_preview.toolbar.bind('<Configure>',lambda e:self.output_preview.toolbar.configure(height=e.height))
        previews.add(self.input_preview,weight=1);previews.add(self.output_preview,weight=1)
        self.swatches=tk.Canvas(right,height=96,bg=BG,highlightthickness=0);self.swatches.pack(fill='x',pady=6)
        self.swatches.bind('<Configure>',lambda e:self.draw_swatches());self.swatches.bind('<Button-1>',self.swatch_clicked)
        self.mode_info=tk.StringVar();ttk.Label(right,textvariable=self.mode_info,style='Muted.TLabel',wraplength=700).pack(anchor='w')

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
            label.configure(text=f"{v.get():.2f}"+('×' if name=='crop_zoom' else ''))
            if name=='crop_zoom' and not self.suspend:self.input_view.set('Adjusted input')
            self.changed()
        v.trace_add("write",update)
        ttk.Scale(parent,from_=low,to=high,variable=v).pack(fill="x")

    def _sync_vars(self,s):
        self.suspend = True
        for name,var in self.vars.items():
            var.set(s.codes[int(name[-1])] if name.startswith("code") else getattr(s,name))
        self.suspend = False
        self.mode_controls()

    def scope_changed(self):
        scope=self.vars['optimization_scope'].get()
        self.scope_help.set({'Image + colors':'Adjust the image and replace its palette. Crop stays fixed.',
                             'Image only':'Fit tone and RGB balance. Keep the current colors and crop.',
                             'Colors only':'Replace the palette. Keep image adjustments and crop.'}.get(scope,''))
        self.effort_help.set('Colors-only uses the selected mode’s palette search; effort applies to image fitting and joint search.' if scope=='Colors only' else 'Thorough adds image-fit sweeps and joint passes; custom Chronocolor also tries alternate starting palettes.')
        self.combos['search_effort'].configure(state='disabled' if scope=='Colors only' else 'readonly')
        if self.vars['mode'].get()==MODES[0]:
            self.scope_help.set('Set brightness only to 0.47. Keep contrast, input gamma, saturation, RGB balance and crop.')
            self.effort_help.set('Classic uses the fixed 0.47 brightness preset; search effort does not apply.')
            self.combos['search_effort'].configure(state='disabled')

    def mode_controls(self):
        mode=self.vars['mode'].get();count=frame_count(mode);w,h=dimensions(Settings(mode=mode))
        self.mode_summary.set(f'{w} × {h} · '+(f'{count} alternating frames · Flicker' if count>1 else 'Same picture every frame · Static'))
        self.export_button.configure(text='Export MovieCart…' if mode==MODES[11] else 'Export ASM + BIN…')
        self.flicker_check.configure(state='normal' if count>1 else 'disabled')
        balance=count>1 and mode not in (MODES[0],MODES[11],*MODES[18:20])
        self.balance_check.configure(state='normal' if balance else 'disabled')
        if count>1:
            if not self.flicker_section.winfo_manager():self.flicker_section.pack(fill='x',pady=(2,6),before=self.combos['search_effort'].master.master)
        else:self.flicker_section.pack_forget()
        automatic=self.vars['flicker_aware'].get() and (self.vars['balance_frames'].get() or not balance)
        self.flicker_section.title='Flicker handling · '+('Automatic' if automatic else 'Custom');self.flicker_section.render()
        self.flicker_summary.set('Temporal brightness scoring. '+('This format has fixed interleaving; no additional phase balancing.' if not balance else 'Balance legal phase assignments without changing the blended colors.')+' Preview persistence does not change scoring or export.')
        if mode==MODES[0]:
            self.flicker_section.title='Flicker handling · Fixed Classic RGB';self.flicker_section.render()
            self.flicker_summary.set('Classic optimization sets brightness to 0.47 and retains its scanline interleaving. Temporal scoring does not change this preset. Persistence is preview-only.')
        self.output_combo.configure(values=['Temporal blend','Quantization targets']+([f'Frame {k+1}' for k in range(count)] if count>1 else []))
        if self.view.get().startswith('Frame') and (count==1 or int(self.view.get()[-1])>count):self.view.set('Temporal blend')
        editable=mode in (MODES[1],MODES[2]);fixed=mode in (MODES[0],MODES[7])
        for name,enabled in [('search',mode==MODES[1]),('mapping',False),('preset',editable),('background',not fixed)]:
            self.combos[name].configure(state='readonly' if enabled else 'disabled')
        self.diversity_check.configure(state='normal' if mode==MODES[1] and self.vars['search'].get()=='Legacy exhaustive' else 'disabled')
        self.edit_palette_button.configure(state='normal' if editable else 'disabled')
        self.palette_help.set('Fixed original RGB components. Choose custom mode to edit.' if mode==MODES[0] else 'All 128 NTSC colors are available; no palette search.' if mode==MODES[7] else 'Edit the foreground and background. Your choices stay fixed until you explicitly optimize colors.' if mode==MODES[2] else 'Edit components or background below. Blended colors are read-only. A preset selects Image only.' if editable else 'Colors vary by row. Inspect them below; Optimize colors explicitly to replace them.')
        if not editable and not fixed:
            self.row_controls.pack(fill='x',pady=5);self.row_spinner.configure(to=h-1)
        else:self.row_controls.pack_forget()
        values=['Image only'] if fixed else ['Image + colors','Image only','Colors only']
        self.combos['optimization_scope'].configure(values=values)
        if self.vars['optimization_scope'].get() not in values:self.vars['optimization_scope'].set('Image only')
        self.scope_changed()

    def read_settings(self):
        data={name:var.get() for name,var in self.vars.items() if not name.startswith('code')}
        data['codes']=tuple(self.vars[f'code{i}'].get() for i in range(4))
        data['auto_input']=False
        # Image/crop/dither changes re-render the existing row palettes.
        # Only a new image, new mode, or explicit color search replaces them.
        if data['mode']==self.settings.mode:data['line_codes']=self.settings.line_codes
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

    def clear_comparison(self):
        self.before_result=None;self.compare_before.set(False)
        self.compare_button.state(['disabled']);self.undo_button.configure(state='disabled')

    def changed(self):
        if self.suspend:return
        interrupted=self.busy and self.active_action is not None
        if self.busy:self.cancel.set()
        self.pending_action=None
        self.clear_comparison();self.result_current=False
        self.input_preview.canvas.configure(cursor='fleur')
        self.revision+=1
        self.mode_controls()
        self.status.set('Optimization cancelled by an edit. Refreshing with current colors; click Optimize to search again.' if interrupted else 'Updating preview with current colors…')
        if self.after_preview:self.after_cancel(self.after_preview)
        self.after_preview=self.after(350,self.convert)

    def preset_changed(self):
        name=self.vars['preset'].get()
        if name in PRESETS:
            for i,c in enumerate(PRESETS[name]):self.vars[f'code{i}'].set(c)
            self.vars['mapping'].set('Temporal blend')
        self.vars['optimization_scope'].set('Image only');self.changed()

    def adjust_input_to_palette(self):
        self.vars['optimization_scope'].set('Image only');self.scope_changed();self.start_optimization()

    def start_optimization(self):
        self.mode_controls()
        self.pending_action=(self.vars['optimization_scope'].get(),self.vars['search_effort'].get())
        self.compare_before.set(False)
        if self.busy:
            self.cancel.set();self.revision+=1
        self.convert()

    def undo_optimization(self):
        if self.before_result is None or self.busy:return
        self.result=self.before_result;self.settings=self.result[2]
        self._sync_vars(self.settings);self.result_current=True;self.clear_comparison()
        self.show_result();self.status.set('Restored the image adjustments and colors from before optimization.')

    def reset_all_options(self):
        self.cancel_conversion()
        if self.animated_preview is not None:
            self.animated_preview.close();self.animated_preview=None
        if self.crop_preview_job:
            self.after_cancel(self.crop_preview_job);self.crop_preview_job=None
        self.crop_drag=None
        self.clear_comparison()
        self.settings=Settings()
        self._sync_vars(self.settings)
        self.zoom.set('Fit');self.smooth.set(False);self.view.set('Temporal blend')
        self.input_view.set('Adjusted input');self.inspect_row.set(64)
        self.last_export=None
        self.changed()

    def code_changed(self):
        self.vars["preset"].set("Custom / optimized"); self.vars["mapping"].set("Temporal blend"); self.vars["optimization_scope"].set("Image only"); self.changed()

    def reset_adjustments(self):
        self.suspend = True
        defaults = Settings()
        for name in ("brightness","contrast","saturation","gamma","sharpness","red","green","blue"):
            self.vars[name].set(getattr(defaults,name))
        self.suspend = False; self.changed()

    def reset_crop(self):
        self.suspend=True
        self.vars['crop_zoom'].set(1);self.vars['crop_x'].set(.5);self.vars['crop_y'].set(.5)
        self.suspend=False;self.crop_drag=None;self.changed()

    def center_crop(self):
        self.vars['crop_x'].set(.5);self.vars['crop_y'].set(.5)
        self.crop_drag=None;self.changed()

    def crop_press(self,event):
        canvas=self.input_preview.canvas;self.crop_drag=None
        canvas.scan_mark(event.x,event.y)
        if self.input_view.get()!='Adjusted input' or self.compare_before.get() or event.state & 1:return
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
        if self.vars['scale'].get()!=start.scale or self.vars['crop_zoom'].get()!=start.crop_zoom or self.source.size!=source_size or self.vars['rotate'].get()!=start.rotate or self.vars['mirror'].get()!=start.mirror or self.vars['aspect'].get()!=start.aspect:
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
        self.suspend=True;self.vars['crop_zoom'].set(1);self.vars['crop_x'].set(.5);self.vars['crop_y'].set(.5);self.suspend=False;self.crop_drag=None
        self.file_label.configure(text=f"{Path(path).name}  •  {im.width} × {im.height}")
        self.changed()

    def convert(self,search=False,global_search=False):
        # Keep programmatic palette-search callers working; the visible UI uses scope.
        if search:self.pending_action=('Image + colors' if global_search else 'Colors only','Thorough' if global_search else 'Standard')
        if self.after_preview:self.after_cancel(self.after_preview)
        self.after_preview=None
        if self.busy:
            self.after_preview=self.after(100,self.convert);return
        try:s=self.read_settings()
        except Exception as ex:self.status.set(str(ex));return
        action=self.pending_action;self.pending_action=None;self.active_action=action
        self.busy=True;self.cancel=threading.Event();cancel=self.cancel
        rev=self.revision;image=self.source.copy()
        self.optimize_button.configure(state='disabled');self.undo_button.configure(state='disabled');self.compare_button.state(['disabled'])
        self.progress['value']=0
        self.status.set(f'Optimizing {action[0].lower()}…' if action else 'Preparing preview'+(' and initializing this mode’s colors…' if s.mode in (*MODES[3:7],*MODES[8:]) and not s.line_codes else ' with current colors…'))
        def work():
            try:
                start=time.perf_counter();before=None
                progress=lambda p,t:self.messages.put(('progress',rev,p,t))
                if action:
                    before=convert_image(image,s,cancel);s2=before[2]
                    scope,effort=action;thorough=effort=='Thorough'
                    if scope=='Image + colors':s2=joint_optimize(image,s2,thorough,progress,cancel)
                    elif scope=='Colors only':s2=search_palette(prepare(image,s2),s2,progress,cancel)
                    else:s2=fit_controls(image,s2,global_fit=thorough,cancel=cancel)
                else:s2=s
                result=convert_image(image,s2,cancel)
                self.messages.put(('done',rev,result,before,action,time.perf_counter()-start))
            except Cancelled:self.messages.put(('cancelled',rev))
            except Exception as ex:self.messages.put(('error',rev,str(ex)))
        threading.Thread(target=work,daemon=True).start()

    def cancel_conversion(self):
        self.cancel.set();self.pending_action=None;self.revision+=1
        if self.after_preview:self.after_cancel(self.after_preview);self.after_preview=None
        self.status.set('Cancelled. The previous completed result is retained.')

    def optimization_summary(self,before,after):
        changes=[]
        for name in ('brightness','contrast','saturation','gamma','red','green','blue'):
            old,new=getattr(before,name),getattr(after,name)
            if abs(old-new)>.001:changes.append(f'{name.title()} {old:.2f} → {new:.2f}')
        if before.codes!=after.codes or before.line_codes!=after.line_codes:changes.append('colors updated')
        return '; '.join(changes) or 'Current settings retained — no better candidate found.'

    def _poll(self):
        try:
            while True:
                msg=self.messages.get_nowait();kind,rev=msg[:2]
                if kind=='progress':
                    if rev==self.revision:self.progress['value']=msg[2]*100;self.status.set(f'{msg[3]} — {msg[2]:.0%}')
                    continue
                self.busy=False;self.active_action=None;self.optimize_button.configure(state='normal')
                if self.before_result is not None:
                    self.undo_button.configure(state='normal');self.compare_button.state(['!disabled'])
                if rev!=self.revision:continue
                if kind=='done':
                    _,_,result,before,action,elapsed=msg
                    self.result=result;self.settings=result[2];self._sync_vars(self.settings);self.result_current=True
                    self.progress['value']=100
                    if action:
                        self.before_result=before;self.compare_button.state(['!disabled']);self.undo_button.configure(state='normal')
                        self.status.set(self.optimization_summary(before[2],result[2]))
                    else:self.status.set(f'Ready · {elapsed:.2f} s · current colors retained. Choose an optimization scope to search.')
                    self.show_result()
                elif kind=='cancelled':self.status.set('Cancelled. Previous completed result retained.')
                else:self.status.set('Conversion failed: '+msg[2])
        except queue.Empty:pass
        self.after(80,self._poll)

    def show_result(self):
        if self.result is None:return
        comparing=self.compare_before.get() and self.before_result is not None
        adjusted,indices,s = self.before_result if comparing else self.result
        self.output_preview.heading.configure(text='BEFORE OPTIMIZATION' if comparing else 'ATARI OUTPUT')
        self.output_notice.set('Comparison only — export uses the current result. Undo restores this version.' if comparing else 'Light-corrected preview · estimated Atari colors. Check the cartridge in Stella.')
        view = self.view.get()
        if view.startswith("Frame"): out = Image.fromarray(frame_pixels(indices,s.codes,s.line_codes,s.mode)[(int(view[-1])-1)%len(frame_pixels(indices,s.codes,s.line_codes,s.mode))])
        elif view=='Quantization targets':
            palette=target_palette(s)
            out=Image.fromarray(palette[np.arange(indices.shape[0])[:,None],np.arange(indices.shape[1])[None,:],indices] if palette.ndim==4 else palette[np.arange(len(indices))[:,None],indices] if palette.ndim==3 else palette[indices])
        else:out=Image.fromarray(render(indices,s))
        w,h=dimensions(s)
        temporal=s.mode in (MODES[0],MODES[1],MODES[3])
        self.mode_info.set(f'{mode_description(s.mode)} • {w} × {h} • '+(f'{frame_count(s.mode)} alternating frames' if frame_count(s.mode)>1 else 'same picture every frame')+f' • {cartridge_size(s.mode)//1024} KB {cartridge_type(s.mode)} ROM'+('\nScanline palettes: swatches show the selected row.' if s.line_codes else ''))
        original=self.input_view.get()=='Original input'
        for preview,im in ((self.input_preview,self.source if original else adjusted),(self.output_preview,out)):
            preview.image = im; preview.zoom = self.zoom.get(); preview.smooth = self.smooth.get(); preview.aspect = 'Raw pixels' if preview is self.input_preview and original else display_aspect(s); preview.draw()
        if s.mode==MODES[11]:self.mode_info.set('MovieCart — Flicker • 80 × 192 (190 content rows) • two alternating fields\n30-second silent .mvc stream • MovieCart hardware, not Harmony')
        if s.mode in MODES[8:11]:self.mode_info.set(self.mode_info.get()+'\nSix multiplexed sprite strips; narrow, centered raster • hardware untested')
        if s.mode==MODES[7]:self.mode_info.set(self.mode_info.get()+'\n128 colors available per sample • 9 color clocks wide • Stella verified; hardware untested')
        if s.mode==MODES[12] and s.balance_frames:
            shared=all(r[3]==r[7] for r in s.line_codes)
            self.mode_info.set(self.mode_info.get()+('\nAlternating A/B scanlines; the next frame reverses them.' if shared else '\nSaved palettes use different backgrounds. Choose Colors only → Optimize to enable row interleaving.'))
        if s.mode in MODES[17:20]:
            from .extended import NOTES
            self.mode_info.set(self.mode_info.get()+'\n'+NOTES[s.mode])
            if s.mode==MODES[17] and s.line_codes:
                positions=[int(v,16) for v in s.line_codes[0][4:]]
                self.mode_info.set(self.mode_info.get()+f' Windows at x={positions[0]} and {positions[1]}.')
        self.draw_swatches()

    def draw_swatches(self):
        if not hasattr(self,'swatches') or not self.result:return
        s=(self.before_result if self.compare_before.get() and self.before_result is not None else self.result)[2]
        self.swatches.delete('all');width=max(1,self.swatches.winfo_width())
        editable=s.mode in (MODES[1],MODES[2]) and not self.compare_before.get() and self.result_current
        self.swatches.configure(cursor='hand2' if editable else '')
        if s.mode==MODES[7]:
            self.swatches.create_text(0,8,text='FULL NTSC PALETTE · 128 colors · read-only',anchor='w',fill=MUTED,font=('Segoe UI',8))
            for hue in range(16):
                for lum in range(8):
                    hx='#'+''.join(f'{int(v):02x}' for v in TIA[CODES.index(f'{hue:X}{lum*2:X}')])
                    self.swatches.create_rectangle(hue*width/16+2,24+lum*7,(hue+1)*width/16-2,31+lum*7,fill=hx,outline='')
            return
        if s.line_codes:
            try:row=max(0,min(len(s.line_codes)-1,int(self.inspect_row.get())))
            except (ValueError,tk.TclError):row=len(s.line_codes)//2
            codes=s.line_codes[row][:4] if s.mode==MODES[17] else s.line_codes[row]
            title=f'ROW {row} COLORS · read-only · optimize colors to refit'
            labels=[f'Cell {k+1}' for k in range(10)]+['BG'] if s.mode==MODES[11] else ['A 1','A 2','A 3','A BG','B 1','B 2','B 3','B BG'] if len(codes)==8 else ['L FG','L BG','R FG','R BG'] if s.mode==MODES[6] else ['PF','Sprite 1','Sprite 2','BG'] if s.mode==MODES[17] else ['FG','FG','FG','BG'] if s.mode in MODES[18:20] else ['Comp. 1','Comp. 2','Comp. 3','BG']
            if s.mode in MODES[18:20]:codes=(codes[0],codes[3]);labels=['Foreground','Background']
            colors=[TIA[CODES.index(c)] for c in codes];tags=[None]*len(codes)
            labels=[label+'\n$'+code for label,code in zip(labels,codes)]
        elif s.mode==MODES[2]:
            title='TWO COLORS · click foreground or background to edit'
            colors=[TIA[CODES.index(s.codes[k])] for k in (0,3)]
            labels=['Foreground\n$'+s.codes[0],'Background\n$'+s.codes[3]];tags=['component0','component3']
        else:
            title='BLENDED OUTPUT · read-only                         COMPONENTS / BACKGROUND'+(' · locked RGB' if s.mode==MODES[0] else ' · click to edit')
            colors=list(target_palette(s))+list(TIA[[CODES.index(c) for c in s.codes]])
            labels=[str(i) for i in range(8)]+[f'Comp. {i+1}\n${s.codes[i]}' for i in range(3)]+['BG\n$'+s.codes[3]]
            tags=[None]*8+[f'component{i}' for i in range(4)]
        self.swatches.create_text(0,8,text=title,anchor='w',fill=MUTED,font=('Segoe UI',8))
        cell=width/len(colors)
        for i,(color,label,tag) in enumerate(zip(colors,labels,tags)):
            hx='#'+''.join(f'{int(v):02x}' for v in color);itemtags=(tag,) if tag and editable else ()
            self.swatches.create_rectangle(i*cell+2,25,(i+1)*cell-3,52,fill=hx,outline='#546272',tags=itemtags)
            self.swatches.create_text((i+.5)*cell,55,text=label,anchor='n',fill=TEXT,font=('Segoe UI',8),tags=itemtags)

    def swatch_clicked(self,event):
        if self.busy or not self.result_current or self.compare_before.get():return
        for item in self.swatches.find_overlapping(event.x,event.y,event.x,event.y):
            for tag in self.swatches.gettags(item):
                if tag.startswith('component'):
                    self.open_palette_picker(int(tag[-1]));return

    def open_palette_picker(self,component=None,output=None):
        if self.vars['mode'].get() in MODES[3:]:
            self.status.set('Scanline colors are read-only. Choose Colors only or Image + colors to refit all rows.');return
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
        if self.busy or self.result is None or not self.result_current:
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
        if self.result is None or self.busy or not self.result_current:raise ValueError("Conversion is not ready")
        _,indices,s = self.result; folder = Path(folder)
        folder.mkdir(parents=True,exist_ok=False)
        if s.mode!=MODES[11]:(folder/"image.asm").write_text(assembly(indices,s.codes,s.mode,s.line_codes),encoding="utf-8")
        (folder/("image.mvc" if s.mode==MODES[11] else "image.bin")).write_bytes(binary(indices,s.codes,s.mode,s.line_codes))
        s.save(folder/"settings.json")
        Image.fromarray(render(indices,s)).save(folder/"preview.png")
        (folder/'mode.txt').write_text(f'{s.mode}\nLogical resolution: {dimensions(s)}\n',encoding='utf-8')
        if s.mode in MODES[17:20]:
            from .extended import NOTES
            with (folder/'mode.txt').open('a',encoding='utf-8') as note:note.write(NOTES[s.mode]+'\n')
        (folder/"README.txt").write_text(f"Atari 2600 Image Optimizer — NTSC {cartridge_size(s.mode)//1024} KB {cartridge_type(s.mode)} Atari 2600 cartridge\nMode: {mode_description(s.mode)}\nLogical size: {dimensions(s)}\n\nChris Martin's Chrono2 converter. Original Chronocolour kernel and sprite technique: Andrew Davie, with acknowledgements to Eckhard Stohlberg and Thomas Jentzsch. New raster kernels developed for Atari 2600 Image Optimizer.\n\nimage.asm is self-contained DASM source. Rebuild: dasm image.asm -f3 -oimage.bin\nimage.bin is headerless, {cartridge_size(s.mode)//1024} KB {cartridge_type(s.mode)}. Open in Stella using NTSC.\nColor model: sRGB-referred NTSC palette, linear-light temporal blend, D65 CIEDE2000 matching. No automatic display gain.\npreview.png is an estimated display image, not a hardware capture.\nReal hardware/Harmony testing remains the user's validation step.\n",encoding="utf-8")
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
            try:self.settings=replace(Settings.load(path),auto_input=False);self._sync_vars(self.settings);self.changed()
            except Exception as ex:messagebox.showerror("Settings",str(ex))

    def save_preview(self):
        if not self.ready():return
        path = filedialog.asksaveasfilename(defaultextension=".png",filetypes=[("PNG image","*.png")])
        if path:
            comparing=self.compare_before.get()
            try:
                self.compare_before.set(False);self.show_result();self.output_preview.image.save(path)
            finally:
                self.compare_before.set(comparing);self.show_result()
            self.status.set("Saved the selected output view at its logical resolution.")

    def export_animated_preview(self):
        if not self.ready():return
        from .web_preview import AnimationExport
        _,indices,s=self.result
        stem=(self.source_path.stem if self.source_path else 'atari-preview')+'-animated'
        self.animation_export_dialog=AnimationExport(self,indices,s,stem=stem,
            on_saved=lambda path,result:self.status.set(f'Saved website preview: {path} ({result["bytes"]//1024} KB)'))

    def save_gif(self):
        if not self.ready():return
        path = filedialog.asksaveasfilename(defaultextension=".gif",filetypes=[("Animated GIF","*.gif")])
        if path:
            _,indices,s = self.result
            size = (512,384) if s.mode==MODES[17] else (384,384) if s.mode==MODES[18] else (288,576) if s.mode==MODES[19] else (480,576) if s.mode==MODES[11] else (288,576) if s.mode in (*MODES[8:11],*MODES[14:]) else (576,480) if s.mode==MODES[7] else (512,384) if s.mode in MODES[5:8] else {"Atari pixels 2:1":(384,512),"Display 4:3":(512,384),"Raw pixels":dimensions(s)}[s.aspect]
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
            messagebox.showerror('Could not open Stella',f'{ex}\n\nUse File → Locate / change Stella to select another installation.',parent=self)
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
