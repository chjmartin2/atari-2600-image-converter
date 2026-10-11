"""Read-only, versioned mixed-color resources. Never generate at UI runtime."""
import hashlib
import json
from pathlib import Path
import numpy as np
from scipy.spatial import cKDTree
from .core import DATA,TIA,BITS,CODES,check_cancel
from .color import MODEL

FORMAT=1  # Bump with lookup layout or blend-generation algorithm changes.
DIRECTORY=DATA/'mixed-palettes'
DTYPES={'triples':'<i2','rgb':'|u1','members':'<i4','lab':'<f8','keys':'<u4',
        'unique_members':'<i4','unique_mask':'|b1','blend_cube':'<i4'}


def signature():
    value=hashlib.sha256()
    value.update(f'{FORMAT}:{MODEL}'.encode('utf-8'))
    value.update(np.asarray(TIA,dtype='<f4').tobytes())
    value.update(np.asarray(BITS,dtype='u1').tobytes())
    value.update(','.join(CODES).encode('ascii'))
    return value.hexdigest()


def checksum(path,cancel=None):
    digest=hashlib.sha256()
    with Path(path).open('rb') as stream:
        while block:=stream.read(1024*1024):
            check_cancel(cancel);digest.update(block)
    return digest.hexdigest()


def load_catalog(cancel=None,directory=None):
    from .indexed_search import Catalog
    directory=DIRECTORY if directory is None else Path(directory)
    check_cancel(cancel)
    arrays={}
    try:
        manifest=json.loads((directory/'manifest.json').read_text(encoding='utf-8'))
        if manifest['format']!=FORMAT or manifest['signature']!=signature():
            raise ValueError('color-model signature mismatch')
        count=int(manifest['colors'])
        shapes={'triples':(357760,3),'rgb':(count,3),'members':(357760,8),
                'lab':(count,3),'keys':(count,),'unique_members':(357760,8),
                'unique_mask':(357760,8),'blend_cube':(128,128,128)}
        for name,dtype in DTYPES.items():
            check_cancel(cancel);path=directory/(name+'.npy')
            if checksum(path,cancel)!=manifest['arrays'][name]['sha256']:
                raise ValueError(name+' checksum mismatch')
            a=np.load(path,mmap_mode='r',allow_pickle=False);arrays[name]=a
            if a.shape!=shapes[name] or a.dtype.str!=dtype:
                raise ValueError(name+' layout mismatch')
        result=Catalog.__new__(Catalog)
        result.allowed=tuple(range(128));result.black=CODES.index('00')
        for name,a in arrays.items():setattr(result,name,a)
        # This small in-memory search index is independent of image and mode.
        # Rebuilding it avoids Python/SciPy-version-dependent pickle files.
        result.index=cKDTree(result.lab)
        check_cancel(cancel)
        return result
    except BaseException as ex:
        for array in arrays.values():array._mmap.close()
        if isinstance(ex,(OSError,ValueError,KeyError,TypeError)):
            raise ValueError('Bundled mixed Atari palette data is missing, damaged, or out of date. '
                             'Update/reinstall the application; source builds should run '
                             'python scripts/build_mixed_palettes.py. '+str(ex)) from ex
        raise
