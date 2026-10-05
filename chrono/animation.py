"""Playback of the actual three interleaved component images, not their mean."""
import math
import time
import tkinter as tk
from tkinter import ttk
import numpy as np
from .color import srgb_to_linear,linear_to_srgb
from PIL import Image, ImageTk
from .core import frame_pixels, MODES, display_aspect, frame_count

RATES = {"NTSC pace (~60 fps)": 60.0, "Half speed (30 fps)": 30.0,
         "Slow motion (10 fps)": 10.0, "Inspect (3 fps)": 3.0}

class FrameClock:
    """Elapsed-time clock: late paints skip frames instead of slowing the movie."""
    def __init__(self, now, rate=60):
        self.epoch=now;self.position=0.;self.rate=rate;self.running=True

    def position_at(self,now):
        return self.position + (max(0,now-self.epoch)*self.rate if self.running else 0)

    def number(self,now):
        return math.floor(self.position_at(now)+1e-9)

    def set_rate(self,rate,now):
        if not math.isfinite(rate) or rate<=0:raise ValueError("Playback rate must be positive")
        self.position=self.position_at(now);self.epoch=now;self.rate=rate

    def toggle(self,now):
        self.position=self.position_at(now);self.epoch=now;self.running=not self.running

    def step(self,now):
        self.position=self.number(now)+1;self.epoch=now;self.running=False

def persistence_frames(frames,retention):
    """Optional periodic exponential trail; explicitly an illustrative approximation."""
    if not math.isfinite(retention) or not 0<=retention<=.8:
        raise ValueError("Persistence must be between 0 and 0.8")
    data=srgb_to_linear(frames)
    if data.ndim!=4 or data.shape[0] not in (1,2,3) or data.shape[-1]!=3:raise ValueError("Expected one, two or three RGB frames")
    a=retention
    return linear_to_srgb(sum(a**k*np.roll(data,k,axis=0) for k in range(len(data)))/sum(a**k for k in range(len(data))))

class AnimatedPreview(tk.Toplevel):
    def __init__(self,parent,indices,settings):
        super().__init__(parent)
        self.title("ATARI Rendering Preview")
        self.geometry("740x820");self.minsize(540,510);self.configure(bg="#10151c")
        self.job=None;self.resize_job=None;self.closed=False;self.photos=[]
        self.rate=tk.StringVar(value=next(iter(RATES)))
        self.persistence=tk.DoubleVar(value=.6)
        self.info=tk.StringVar()
        self.heading=ttk.Label(self,style="Section.TLabel",padding=(16,12));self.heading.pack(anchor="w")
        self.description=ttk.Label(self,style="Muted.TLabel",padding=(16,0));self.description.pack(anchor="w")
        controls=ttk.Frame(self,padding=(16,10));controls.pack(fill="x")
        self.play_button=ttk.Button(controls,text="Pause",command=self.toggle)
        self.play_button.pack(side="left")
        ttk.Button(controls,text="Next frame",command=self.step).pack(side="left",padx=6)
        box=ttk.Combobox(controls,textvariable=self.rate,values=list(RATES),state="readonly",width=23)
        box.pack(side="left");box.bind("<<ComboboxSelected>>",lambda e:self.change_rate())
        blend=ttk.Frame(self,padding=(16,0));blend.pack(fill="x")
        ttk.Label(blend,text="Persistence (preview only)").pack(side="left")
        self.blend_label=ttk.Label(blend,text="60%",width=5);self.blend_label.pack(side="right")
        ttk.Scale(blend,from_=0,to=.8,variable=self.persistence,command=self.change_persistence).pack(side="right",fill="x",expand=True,padx=10)
        ttk.Button(self,text='Export animated preview…',command=self.export_animation).pack(anchor='w',padx=16,pady=6)
        self.canvas=tk.Canvas(self,bg="#05070a",highlightthickness=0)
        # Reserve the lower explanatory rows before allocating the image area.
        ttk.Label(self,text="Nominal NTSC pace; desktop timing is not synchronized to your monitor.\nColors, flicker and CRT persistence will differ. Use Stella or hardware for validation.",style="Muted.TLabel",padding=(16,10)).pack(side="bottom",fill="x")
        ttk.Label(self,textvariable=self.info,style="Muted.TLabel",padding=(16,4)).pack(side="bottom",anchor="w")
        self.canvas.pack(fill="both",expand=True,padx=16,pady=10)
        self.canvas.bind("<Configure>",self.schedule_resize)
        self.bind("<space>",lambda e:self.toggle())
        self.bind("<Right>",lambda e:self.step())
        self.bind("<Escape>",lambda e:self.close())
        self.protocol("WM_DELETE_WINDOW",self.close)
        self.set_result(indices,settings)

    def set_result(self,indices,settings):
        self.export_indices=np.array(indices,copy=True);self.export_settings=settings
        static=frame_count(settings.mode)==1
        self.title("ATARI Rendering Preview — " + ("static output" if static else "two-field simulation" if frame_count(settings.mode)==2 else "three-frame simulation"))
        self.heading.configure(text="ATARI RENDERING PREVIEW")
        self.description.configure(text=("This mode repeats the same image on every frame." if static else "Plays the cartridge’s interleaved frames, not the static average.")+"\nSnapshot of the last completed conversion; reopen to load a newer result.")
        self.frames=frame_pixels(np.array(indices,copy=True),tuple(settings.codes),settings.line_codes,settings.mode)[:frame_count(settings.mode)]
        self.aspect=display_aspect(settings)
        now=time.perf_counter();self.clock=FrameClock(now,RATES[self.rate.get()])
        self.last_number=None;self.painted=0;self.skipped=0;self.measure_start=now;self.paint_rate=None
        self.play_button.configure(text="Pause")
        self.rebuild()
        if self.job is None:self.tick()

    def schedule_resize(self,event=None):
        if self.resize_job is not None:self.after_cancel(self.resize_job)
        self.resize_job=self.after(70,self.rebuild)

    def rebuild(self):
        if self.closed:return
        if self.resize_job is not None:self.after_cancel(self.resize_job);self.resize_job=None
        w,h=max(1,self.canvas.winfo_width()),max(1,self.canvas.winfo_height())
        bw,bh={"Atari pixels 2:1":(96,128),"Display 4:3":(4,3),"BUS raster":(6,5),"Sprite raster":(1,2),"Wide raster":(1,1),"Movie raster":(5,6),"Raw pixels":(self.frames[0].shape[1],self.frames[0].shape[0])}[self.aspect]
        scale=min(w/bw,h/bh);size=(max(1,round(bw*scale)),max(1,round(bh*scale)))
        frames=persistence_frames(self.frames,self.persistence.get())
        self.photos=[ImageTk.PhotoImage(Image.fromarray(frame).resize(size,Image.Resampling.NEAREST),master=self) for frame in frames]
        self.canvas.delete("all")
        self.item=self.canvas.create_image(w//2,h//2,image=self.photos[self.clock.number(time.perf_counter())%len(self.photos)])

    def change_persistence(self,value=None):
        value=self.persistence.get()
        self.blend_label.configure(text="Off" if value<.005 else f"{value:.0%}")
        self.schedule_resize()

    def change_rate(self):
        self.clock.set_rate(RATES[self.rate.get()],time.perf_counter())
        self.paint_rate=None;self.painted=0;self.measure_start=time.perf_counter()

    def toggle(self):
        self.clock.toggle(time.perf_counter())
        self.play_button.configure(text="Pause" if self.clock.running else "Play")
        self.paint_rate=None;self.painted=0;self.measure_start=time.perf_counter()

    def step(self):
        self.clock.step(time.perf_counter());self.play_button.configure(text="Play")
        self.paint()

    def paint(self):
        now=time.perf_counter();number=self.clock.number(now)
        if self.photos and number!=self.last_number:
            if self.last_number is not None:self.skipped+=max(0,number-self.last_number-1)
            self.canvas.itemconfigure(self.item,image=self.photos[number%len(self.photos)])
            self.last_number=number;self.painted+=1
        if self.clock.running and now-self.measure_start>=1:
            self.paint_rate=self.painted/(now-self.measure_start)
            self.measure_start=now;self.painted=0
        state="Playing" if self.clock.running else "Paused"
        rate=f" • {self.paint_rate:.0f} frame updates/s" if self.paint_rate is not None and self.clock.running else ""
        self.info.set(f"{state} • Frame {number%len(self.photos)+1} / {len(self.photos)} • {self.clock.rate:g} fps target{rate} • {self.skipped} skipped\nFrame updates measure software scheduling, not actual screen refresh.")

    def tick(self):
        self.job=None
        if self.closed:return
        self.paint()
        # The monotonic clock controls phase; polling only chooses when to paint.
        self.job=self.after(4 if self.clock.running else 50,self.tick)

    def export_animation(self):
        from .web_preview import AnimationExport
        self.export_dialog=AnimationExport(self,self.export_indices,self.export_settings,
            rate=RATES[self.rate.get()],retention=self.persistence.get())

    def close(self):
        self.closed=True
        for job in (self.job,self.resize_job):
            if job is not None:self.after_cancel(job)
        self.job=self.resize_job=None
        self.destroy()
        # Destroy Tcl-backed objects on the GUI thread, before worker-triggered GC.
        self.photos.clear()
        self.rate=self.persistence=self.info=None
