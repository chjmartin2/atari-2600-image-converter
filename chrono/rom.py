"""Unmodified legacy NTSC kernel; ROM patching verified against DASM assembly."""
import hashlib
import json
import re
from pathlib import Path
import numpy as np
from .core import DATA, BITS, CODES, MODES, BUS128, BUS128LINE

def bank_bytes(indices):
    indices = np.asarray(indices)
    if indices.shape != (128,48) or not np.issubdtype(indices.dtype,np.integer) or np.any(indices < 0) or np.any(indices > 7):
        raise ValueError("The cartridge requires 48×128 indices in the range 0–7")
    out = bytearray()
    for f in range(3):
        for strip in range(6):
            for y in range(127,-1,-1):
                bits = BITS[indices[y,strip*8:strip*8+8],(y+f)%3]
                out.append(int(bits @ np.array([128,64,32,16,8,4,2,1])))
    for start in (12,6,0): out.extend([24,0,*range(start,start+6)])
    return bytes(out)

def assembly(indices, codes, mode='8 color mode', line_codes=()):
    if mode==MODES[3] and len({r[3] for r in line_codes})>1:
        from .chrono_line_rom import assembly as per_line
        return per_line(indices,codes,line_codes)
    if mode==MODES[4]:
        from .scanline_rom import assembly as scanline
        return scanline(indices,codes,line_codes)
    if mode in MODES[1:4] and np.asarray(indices).shape==(192,48):
        from .tall_rom import assembly as tall
        return tall(indices,codes,mode,line_codes)
    if mode==BUS128LINE:
        from .bus128_line_rom import assembly as row_color
        return row_color(indices,codes,line_codes)
    if mode==BUS128:
        from .bus128_rom import assembly as bus128
        if line_codes:raise ValueError('BUS single color does not use scanline palettes')
        return bus128(indices,codes)
    if mode in MODES[17:20]:
        from .extended_rom import assembly as extended
        return extended(indices,codes,mode,line_codes)
    if mode in MODES[12:17]:
        from .twoframe_rom import assembly as pair
        return pair(indices,codes,mode,line_codes)
    if mode=='MovieCart frame':raise ValueError('MovieCart exports a streamed .mvc file, not 6507 assembly')
    if mode in ('Multiplexed sprites','DPC+ sprites','CDFJ+ sprites'):
        from .sprite_rom import assembly as sprite
        return sprite(indices,codes,line_codes,{'Multiplexed sprites':'4K','DPC+ sprites':'DPC+','CDFJ+ sprites':'CDFJ+'}[mode])
    if mode==MODES[7]:
        from .bus_rom import assembly as bus
        return bus(indices)
    if mode=='Playfield Plus':
        from .playfield_plus import assembly as plus
        return plus(indices,line_codes or (codes,)*192)
    if mode in ('8 color per line mode','Scanline color','No flicker — playfield'):
        from .raster_rom import assembly as raster
        return raster(indices,codes,line_codes,mode=='No flicker — playfield')
    if len(codes) != 4 or any(c not in CODES for c in codes): raise ValueError("Invalid NTSC codes")
    data = bank_bytes(indices)
    lines = ["; Generated image data: three frames, six strips, 128 rows bottom-up"]
    for i in range(0,2304,16): lines.append(" .byte " + ",".join(f"${b:02X}" for b in data[i:i+16]))
    for n,label in enumerate(("BLUE_png_0","GREEN_png_1","RED_png_2")):
        lines += [f"FRAME_{label}", " .byte " + ",".join(str(b) for b in data[2304+n*8:2312+n*8])]
    source = (DATA/"kernel.asm").read_text()
    source = re.sub(r'^\s*include\s+"Bank00.asm".*$', "\n".join(lines),source,flags=re.I|re.M)
    source = re.sub(r'^\s*include\s+"Bank_Frametable.asm".*$',lambda m:(DATA/"frametable.asm").read_text(),source,flags=re.I|re.M)
    for name,code in zip(("NTSC_RED","NTSC_GREEN","NTSC_BLUE","BGCOL"),codes):
        source = re.sub(rf'^{name}\s*=.*$',f"{name} = ${code}",source,flags=re.M)
    return "; Atari 2600 Image Optimizer. NTSC / 4KB. Retain the acknowledgements below.\n"+source

def binary(indices,codes,mode='8 color mode',line_codes=()):
    if mode==MODES[3] and len({r[3] for r in line_codes})>1:
        from .chrono_line_rom import binary as per_line
        return per_line(indices,codes,line_codes)
    if mode==MODES[4]:
        from .scanline_rom import binary as scanline
        return scanline(indices,codes,line_codes)
    if mode in MODES[1:4] and np.asarray(indices).shape==(192,48):
        from .tall_rom import binary as tall
        return tall(indices,codes,mode,line_codes)
    if mode==BUS128LINE:
        from .bus128_line_rom import binary as row_color
        return row_color(indices,codes,line_codes)
    if mode==BUS128:
        from .bus128_rom import binary as bus128
        if line_codes:raise ValueError('BUS single color does not use scanline palettes')
        return bus128(indices,codes)
    if mode in MODES[17:20]:
        from .extended_rom import binary as extended
        return extended(indices,codes,mode,line_codes)
    if mode in MODES[12:17]:
        from .twoframe_rom import binary as pair
        return pair(indices,codes,mode,line_codes)
    if mode=='MovieCart frame':
        from .moviecart import binary as movie
        return movie(indices,line_codes)
    if mode in ('Multiplexed sprites','DPC+ sprites','CDFJ+ sprites'):
        from .sprite_rom import binary as sprite
        return sprite(indices,codes,line_codes,{'Multiplexed sprites':'4K','DPC+ sprites':'DPC+','CDFJ+ sprites':'CDFJ+'}[mode])
    if mode==MODES[7]:
        from .bus_rom import binary as bus
        return bus(indices)
    if mode=='Playfield Plus':
        from .playfield_plus import binary as plus
        return plus(indices,line_codes or (codes,)*192)
    if mode in ('8 color per line mode','Scanline color','No flicker — playfield'):
        from .raster_rom import binary as raster
        return raster(indices,codes,line_codes,mode=='No flicker — playfield')
    if len(codes) != 4 or any(c not in CODES for c in codes): raise ValueError("Invalid NTSC codes")
    meta = json.loads((DATA/"kernel-patches.json").read_text())
    template = (DATA/"kernel.bin").read_bytes()
    if hashlib.sha256(template).hexdigest() != meta["sha256"]:
        raise ValueError("The bundled ROM template failed its integrity check")
    result = bytearray(template)
    result[:2328] = bank_bytes(indices)
    for code,positions in zip(codes,meta["colorOffsets"]):
        for pos in positions: result[pos] = int(code,16)
    if len(result) != 4096: raise ValueError("Invalid cartridge size")
    return bytes(result)
