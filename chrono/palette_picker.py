"""Pick valid NTSC register colors while showing their derived output mixture."""
import tkinter as tk
from tkinter import ttk
from .core import BITS, CODES, TIA, hardware_palette


def contributors(output):
    if output is None:return list(range(4))
    return [i for i,used in enumerate(BITS[output]) if used]+([3] if not BITS[output].all() else [])


class PalettePicker(tk.Toplevel):
    def __init__(self,parent,codes,callback,component=None,output=None,components=None):
        super().__init__(parent)
        self.title('Atari NTSC color picker');self.configure(bg='#10151c')
        self.transient(parent);self.resizable(False,False)
        self.codes=list(codes);self.callback=callback;self.output=output
        allowed=list(components) if components is not None else contributors(output)
        self.component=tk.IntVar(value=component if component is not None else allowed[0])
        body=ttk.Frame(self,padding=16);body.pack(fill='both',expand=True)
        text=(f'Output {output} is a blend. Choose a contributing color to edit.' if output is not None
              else 'Choose a component, then a color from the Atari NTSC palette.')
        ttk.Label(body,text=text).pack(anchor='w')
        ttk.Label(body,text='Changing a component updates every output color that uses it.').pack(anchor='w',pady=(3,10))
        row=ttk.Frame(body);row.pack(fill='x')
        for i in allowed:
            ttk.Radiobutton(row,text=f'Component {i+1}' if i<3 else 'Background',variable=self.component,
                            value=i,command=self.refresh).pack(side='left',padx=(0,14))
        self.preview=tk.Canvas(body,height=70,width=650,bg='#10151c',highlightthickness=0)
        self.preview.pack(fill='x',pady=10)
        grid=ttk.Frame(body);grid.pack()
        self.buttons={}
        for index,(code,rgb) in enumerate(zip(CODES,TIA)):
            hx='#'+''.join(f'{int(v):02x}' for v in rgb)
            fg='black' if float(rgb @ [.299,.587,.114])>140 else 'white'
            button=tk.Button(grid,text='$'+code,bg=hx,fg=fg,activebackground=hx,activeforeground=fg,
                             width=4,height=2,relief='flat',bd=2,command=lambda c=code:self.choose(c))
            button.grid(row=index//16,column=index%16,padx=1,pady=1)
            self.buttons[code]=button
        self.description=ttk.Label(body);self.description.pack(anchor='w',pady=10)
        actions=ttk.Frame(body);actions.pack(fill='x')
        ttk.Button(actions,text='Cancel',command=self.destroy).pack(side='right')
        ttk.Button(actions,text='Apply colors',command=self.apply).pack(side='right',padx=8)
        self.bind('<Escape>',lambda e:self.destroy())
        self.bind('<Return>',lambda e:self.apply())
        self.refresh();self.grab_set()

    def choose(self,code):
        if code not in CODES:raise ValueError('Choose a valid Atari color')
        self.codes[self.component.get()]=code;self.refresh()

    def refresh(self):
        self.preview.delete('all')
        for i,rgb in enumerate(hardware_palette(self.codes)):
            hx='#'+''.join(f'{int(v):02x}' for v in rgb)
            self.preview.create_rectangle(i*81+2,2,i*81+77,40,fill=hx,
                                          outline='#59d5e7' if i==self.output else '#546272',width=2)
            self.preview.create_text(i*81+40,55,text=str(i),fill='white')
        selected=self.codes[self.component.get()]
        for code,button in self.buttons.items():button.configure(relief='sunken' if code==selected else 'flat')
        name=f'Component {self.component.get()+1}' if self.component.get()<3 else 'Background'
        self.description.configure(text=f'{name}: ${selected}     •     128 hardware-valid NTSC colors')

    def apply(self):
        self.callback(tuple(self.codes));self.destroy()

    def destroy(self):
        super().destroy()
        # Release Tk variables here, on the UI thread, rather than letting a
        # conversion worker's cyclic garbage collection finalize a closed dialog.
        self.component=None
        self.buttons.clear()
        self.callback=None
