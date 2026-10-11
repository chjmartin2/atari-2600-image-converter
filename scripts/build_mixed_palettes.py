"""Generate portable mixed-color tables at build time, never during mode selection."""
from pathlib import Path
import argparse,hashlib,json,os,sys,tempfile,time
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from chrono.indexed_search import Catalog
from chrono.weighted_search import blend_cube
from chrono.palette_store import DIRECTORY,DTYPES,FORMAT,signature,checksum,load_catalog


def build(directory=DIRECTORY,check=False):
    directory=Path(directory)
    try:
        catalog=load_catalog(directory=directory)
    except ValueError:
        if check:raise
    else:
        print('Mixed palettes are current: '+str(directory))
        return
    started=time.perf_counter()
    catalog=Catalog();blend_cube(catalog)
    directory.mkdir(parents=True,exist_ok=True)
    # Publish the manifest last. A failed build is detected instead of silently
    # using a partly updated table or rebuilding it inside the application.
    manifest={'format':FORMAT,'signature':signature(),'colors':len(catalog.rgb),'arrays':{}}
    with tempfile.TemporaryDirectory(prefix='.palette-build-',dir=directory.parent) as tmp:
        stage=Path(tmp)
        assert stage.resolve().is_relative_to(directory.parent.resolve())
        for name,dtype in DTYPES.items():
            a=np.asarray(getattr(catalog,name),dtype=dtype)
            path=stage/(name+'.npy');np.save(path,a,allow_pickle=False)
            manifest['arrays'][name]={'sha256':checksum(path),'shape':list(a.shape),'dtype':a.dtype.str}
        (stage/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
        for name in DTYPES:os.replace(stage/(name+'.npy'),directory/(name+'.npy'))
        os.replace(stage/'manifest.json',directory/'manifest.json')
    print(f'Built {len(catalog.rgb):,} mixed colors and 357,760 canonical foreground triples in {time.perf_counter()-started:.3f}s')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true',help='Validate only; do not regenerate')
    parser.add_argument('--output',type=Path,default=DIRECTORY)
    args=parser.parse_args();build(args.output,args.check)
