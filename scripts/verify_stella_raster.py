"""Run installed Stella's debugger scripts, inspect saved TIA pixels and timing.

Uses an isolated configuration directory. No keyboard automation or user settings.
python scripts/verify_stella_raster.py path/to/Stella.exe
"""
from pathlib import Path
import subprocess,time,sys,re,json
import numpy as np
from PIL import Image
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from chrono.core import BITS,CODES,TIA,frame_pixels,Settings,MODES
from chrono.raster_rom import binary
from chrono.temporal import interleave

root=Path('test-output/stella-raster').resolve();root.mkdir(parents=True,exist_ok=True)
results=[]
for name,pf,temporal in (('static48',False,False),('temporal48',False,True),('playfield40',True,False),('playfield-plus',True,False)):
    plus=name=='playfield-plus'
    run=root/(name+'-'+str(time.time_ns()));run.mkdir()
    h,w=(192,40) if pf else (128,48)
    rng=np.random.default_rng(431)
    indices=rng.integers(0,8,(h,w),dtype=np.uint8)
    if not temporal:indices=np.where(indices<4,0,7).astype(np.uint8)
    indices[:,[0,-1]]=0;indices[[0,-1],:]=0
    rows=[]
    for y in range(h):
        fg=f'{y//16%15+1:X}8'
        bg=f'{(y//16+7)%15+1:X}2' if pf else '00'
        rows.append((fg,bg,f'{(y//16+4)%15+1:X}A',f'{(y//16+10)%15+1:X}4') if plus else ('48','C8','88','00') if temporal else (fg,fg,fg,bg))
    if temporal:
        indices,balanced=interleave(indices,Settings(mode=MODES[3],codes=rows[0],line_codes=tuple(rows)))
        rows=balanced.line_codes
    # A documented external palette makes the expected RGB values unambiguous.
    palette=bytes(TIA[[CODES.index(f'{i*2:02X}') for i in range(128)]].astype(np.uint8).ravel())
    (run/'stella.pal').write_bytes(palette+palette+bytes(24))
    rom=run/(name+'.bin')
    if plus:
        from chrono.playfield_plus import binary as plus_binary
        rom.write_bytes(plus_binary(indices,rows))
    else:rom.write_bytes(binary(indices,rows[0],rows,pf))
    (run/'autoexec.script').write_text('frame #12\nsaveSnap\nframe #1\nsaveSnap\nframe #1\nsaveSnap\nram $f0 _scanEnd\nram $f1 (_scanEnd/#256)\ndump $f0 $ff #1\n')
    with (run/'process.log').open('w') as log:
        proc=subprocess.Popen([sys.argv[1],'-basedir',str(run),'-userdir',str(run),'-snapsavedir',str(run),
            '-palette','user','-pal.gamma','0','-pal.brightness','0','-pal.contrast','0','-pal.saturation','0','-pal.hue','0','-debug','-fullscreen','0','-maxres','1400x1000','-format','NTSC','-type','F6' if plus else '4K',str(rom)],stdout=log,stderr=log)
        try:
            deadline=time.monotonic()+20
            while time.monotonic()<deadline:
                if list(run.glob('*.dump')) and len(list(run.glob('*.png')))>=3:break
                if proc.poll() is not None:break
                time.sleep(.2)
        finally:
            proc.terminate();proc.wait(timeout=5)
    dumps=list(run.glob('*.dump'));assert dumps,(name,'No debugger dump')
    values=re.search(r'f0:\s*([0-9a-f]{2})\s+([0-9a-f]{2})',dumps[0].read_text(),re.I)
    assert values,(name,'Missing timing bytes')
    lines=int(values[1],16)+256*int(values[2],16)
    assert lines==262,(name,'Incorrect frame length',lines)
    shots=list(run.glob('*.png'));assert len(shots)==3,(name,len(shots))
    masks=[];rgb_frames=[]
    for path in shots:
        a=np.asarray(Image.open(path).convert('RGB'))
        ys,xs=np.where(a.any(axis=2));x0,x1=xs.min(),xs.max()+1;y0,y1=ys.min(),ys.max()+1
        crop=a[y0:y1,x0:x1];scale=8 if pf else 2
        assert crop.shape==(h,w*scale,3),(name,'Unexpected image bounds',crop.shape)
        logical=crop[:,::scale]
        rgb_frames.append(crop)
        mask=np.concatenate([np.all(logical[:,:20]==logical[:,0:1],axis=2),np.all(logical[:,20:]==logical[:,-1:],axis=2)],axis=1) if plus else np.all(logical==logical[:,0:1],axis=2) if pf else logical.any(axis=2)
        masks.append(mask)
        if not temporal:np.testing.assert_array_equal(mask,indices==0,err_msg=name)
    if temporal:
        expected=[np.take_along_axis(BITS[indices],np.broadcast_to(((np.arange(h)+f)%3)[:,None,None],(h,w,1)),axis=2)[:,:,0].astype(bool) for f in range(3)]
        assert all(any(np.array_equal(mask,e) for e in expected) for mask in masks),'Temporal plane mismatch'
        assert len({m.tobytes() for m in masks})==3,'Temporal planes did not cycle'
    else:assert all(np.array_equal(masks[0],m) for m in masks),'Static output flickered'
    # Stella 7.0 applies this TV/PC gamma correction even with pal.gamma=0.
    # Source: stella-emu/stella 7.0 src/common/PaletteHandler.cxx adjustedPalette.
    expected_rgb=frame_pixels(indices,rows[0],rows,"Playfield Plus" if plus else None)
    expected_rgb=np.repeat(np.asarray(expected_rgb),scale,axis=2)
    expected_rgb=np.clip((np.asarray(expected_rgb,dtype=np.float32)/255)**np.float32(1.1333)*256+.5,0,255).astype(np.uint8)
    # Stella's hue/saturation round-trip can truncate a channel by up to two levels.
    assert all(any(np.abs(frame.astype(int)-e.astype(int)).max()<=2 for e in expected_rgb) for frame in rgb_frames),(name,'RGB colors mismatch')
    results.append({'mode':name,'scanlines':lines,'verified_frames':len(shots),'pixels_match':True,'colors_match':True,'directory':str(run)})
    print(name,': 262 lines; all three rendered pixel planes match',flush=True)
(root/'results.json').write_text(json.dumps(results,indent=2))
