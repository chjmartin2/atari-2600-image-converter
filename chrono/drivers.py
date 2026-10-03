"""Optional cartridge support, retrieved from upstream rather than redistributed."""
import hashlib,io,tarfile,urllib.request
from .core import DATA
SPECS={
 'bus2':('2d489398d221bd340e8ea7af129045c0147089a0b17785e6cea87a094cdb81d0',2048),
 'dpcplus':('bcbe33dc02ad5104f3a3a53a856a23c57f435344790843f4fb6e746193468d0c',3072),
 'cdfjplus':('9d1cf0fb16ed7ac7633c71a436066b2470a0bdb9b54323588793c2b1d2a95d0c',2048)}
TEMPLATES={'bus-raster':'bus2','sprites-dpc':'dpcplus','pair-dpc':'dpcplus','sprites-cdfj':'cdfjplus','pair-cdfj':'cdfjplus'}

def verify(name,data):
    digest,size=SPECS[name]
    if len(data)!=size or hashlib.sha256(data).hexdigest()!=digest:raise ValueError(name+' support checksum mismatch')
    return data

def load(name):
    path=DATA/(name+'-driver.bin')
    if not path.is_file():raise ValueError('Cartridge support missing. Run Setup cartridge support.cmd once with an Internet connection, then retry.')
    return verify(name,path.read_bytes())

def fetch(url):
    with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Atari2600ImageOptimizer/0.4.0'}),timeout=60) as r:
        data=r.read(32*1024*1024+1)
    if len(data)>32*1024*1024:raise ValueError('Upstream download exceeds size limit')
    return data

def download(name):
    if name=='dpcplus':
        data=fetch('https://raw.githubusercontent.com/batari-Basic/batari-Basic/efd6dcd319c31a5e37afb00d47c981105998d924/includes/DPCplus.arm')
    elif name=='cdfjplus':
        base='https://raw.githubusercontent.com/Aganarr/CDFJplus-template/4823c5842d8d6c902fee981e5790b80099afb247/'
        parts=[fetch(base+f'cdfjplus48_p{k}.bin') for k in range(1,5)]
        data=parts[0]+bytes([0xA9])+parts[1]+bytes([0xA9])+parts[2]+bytes([0])+parts[3]
    elif name=='bus2':
        archive=fetch('https://github.com/stella-emu/stella/releases/download/7.0/stella-7.0-src.tar.xz')
        with tarfile.open(fileobj=io.BytesIO(archive),mode='r:xz') as tar:
            matches=[m for m in tar.getmembers() if m.isfile() and m.name.rsplit('/',1)[-1]=='128bus_20170120.bin']
            if len(matches)!=1:raise ValueError('Cannot identify upstream BUS reference ROM')
            with tar.extractfile(matches[0]) as f:data=f.read(2048)
    else:raise ValueError('Unknown cartridge support')
    return verify(name,data)

def setup():
    for name in SPECS:
        try:load(name);print(name+': ready');continue
        except (OSError,ValueError):pass
        print('Downloading '+name+' support from its original source...')
        data=download(name);path=DATA/(name+'-driver.bin')
        temporary=path.with_suffix('.tmp');temporary.write_bytes(data);temporary.replace(path)
        print(name+': checksum verified')

def restore(template,name):
    driver=load(name);template[:len(driver)]=driver
    return template

def strip_template(stem,data):
    """Public templates reserve zero bytes for externally supplied drivers."""
    b=bytearray(data)
    if stem in TEMPLATES:b[:SPECS[TEMPLATES[stem]][1]]=bytes(SPECS[TEMPLATES[stem]][1])
    return bytes(b)
