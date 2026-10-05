"""Measure VSYNC edge times in Stella, not just its rounded scanline counter."""
from pathlib import Path
import sys,subprocess,time,re,json
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from chrono.extended_rom import assembly
from chrono.extended import INTERLACE
run=(Path('test-output/interlace-sync')/str(time.time_ns())).resolve();run.mkdir(parents=True)
(run/'sync.asm').write_text(assembly(np.zeros((384,48),np.uint8),('00',)*4,INTERLACE))
r=subprocess.run([sys.argv[2],'sync.asm','-f3','-osync.bin','-ssync.sym'],cwd=run,capture_output=True)
assert r.returncode==0,r.stdout
symbols={name:int(addr,16) for name,addr in re.findall(r'^(SyncOn\d)\s+([0-9a-fA-F]+)',(run/'sync.sym').read_text(),re.M)}
commands=['frame #12']
for point,phase in enumerate((0,1,0,1)):
    addr=symbols['SyncOn'+str(phase)]
    commands += [f'stepWhile {{(pc != ${addr:04X}) || (_bank != #{phase})}}','step']
    commands += [f'ram ${0xD0+point*4:02X} _cyclesLo',f'ram ${0xD1+point*4:02X} (_cyclesLo/#256)',f'ram ${0xD2+point*4:02X} _sCycles',f'ram ${0xD3+point*4:02X} _bank']
commands+=['dump $d0 $df #1','saveSes']
(run/'autoexec.script').write_text('\n'.join(commands)+'\n')
with (run/'process.log').open('w') as log:
    proc=subprocess.Popen([sys.argv[1],'-basedir',str(run),'-userdir',str(run),'-debug','-fullscreen','0','-maxres','1400x1000','-format','NTSC','-type','F8',str(run/'sync.bin')],stdout=log,stderr=log)
    try:
        end=time.monotonic()+25
        while time.monotonic()<end and not list(run.glob('*.dump')):time.sleep(.2)
    finally:
        proc.terminate();proc.wait(timeout=5)
dump=next(run.glob('*.dump')).read_text();values=[int(v,16) for v in re.search(r'd0:\s*((?:[0-9a-f]{2}\s+){16})',dump.replace('-', ''),re.I)[1].split()]
times=[values[k]+256*values[k+1] for k in range(0,16,4)]
delta=[(b-a)%65536 for a,b in zip(times,times[1:])]
result={'cycles_between_VSYNC_edges':delta,'scanline_cycles_at_edge':values[2::4],'banks':values[3::4]}
print(run,result,flush=True)
assert delta==[19950]*3,result # 262.5 * 76 CPU cycles
assert values[2::4]==[3,41,3,41],result
(run/'result.json').write_text(json.dumps(result,indent=2))
