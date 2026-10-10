"""Build an audited Windows x64 folder bundle. Run with PyInstaller installed."""
from pathlib import Path
import subprocess,sys,shutil,importlib.metadata
root=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(root))
from chrono.drivers import TEMPLATES,SPECS
from chrono import __version__
output=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else root/'private/windows-build'
output.mkdir(parents=True,exist_ok=True)
name='Atari-2600-Image-Optimizer'
args=[sys.executable,'-m','PyInstaller','--noconfirm','--windowed','--onedir','--noupx',
      '--name',name,'--distpath',str(output/'dist'),'--workpath',str(output/'work'),'--specpath',str(output)]
args+=['--icon',str(root/'chrono/resources/branding/app.ico'),
       '--add-data',str(root/'chrono/resources/branding')+':chrono/resources/branding']
for path in sorted((root/'chrono/resources').iterdir()):
    if path.suffix not in ('.asm','.bin','.json'):continue
    if path.name.endswith('-driver.bin') or (path.suffix=='.asm' and path.stem in TEMPLATES):continue
    if path.suffix=='.bin' and path.stem in TEMPLATES:
        assert not any(path.read_bytes()[:SPECS[TEMPLATES[path.stem]][1]]),'Driver-bearing public template: '+path.name
    args+=['--add-data',str(path)+':chrono/resources']
for name_ in ('ADVANCED-MODES.md','BUS-RESEARCH.md'):
    args+=['--add-data',str(root/name_)+':.']
args+=[str(root/'run.py')]
subprocess.run(args,cwd=root,check=True)
bundle=output/'dist'/name
licenses=bundle/'third-party-licenses';licenses.mkdir(exist_ok=True)
for package in ('numpy','pillow','pyinstaller'):
    distribution=importlib.metadata.distribution(package)
    for item in distribution.files or ():
        if 'license' in str(item).lower() and distribution.locate_file(item).is_file():
            target=licenses/package/str(item).replace('../','')
            target.parent.mkdir(parents=True,exist_ok=True)
            shutil.copy2(distribution.locate_file(item),target)
python_license=Path(sys.base_prefix)/'LICENSE.txt'
if python_license.exists():shutil.copy2(python_license,licenses/'Python-LICENSE.txt')
for doc in ('README.md','RELEASE-NOTES.md','CREDITS.md','ADVANCED-MODES.md','BUS-RESEARCH.md'):
    shutil.copy2(root/doc,bundle/doc)
(bundle/'Setup cartridge support.cmd').write_text('@echo off\ncd /d "%~dp0"\nstart "" "Atari-2600-Image-Optimizer.exe" --setup-cartridge-support\n')
(bundle/'START-HERE.txt').write_text('Atari 2600 Image Optimizer '+__version__+' — Windows x64\n\nExtract the entire ZIP, then open Atari-2600-Image-Optimizer.exe.\nKeep the _internal folder beside the EXE. Python is included.\n\nBUS, DPC+ and CDFJ+ exports need optional cartridge support.\nRun Setup cartridge support.cmd and click Download cartridge support once.\nThe original upstream files are checksum-verified and stored under LocalAppData.\nOther modes and image previews work without that download. Stella is installed separately.\n\nThis build is unsigned. See RELEASE-NOTES.md for changes and validation limits.\n',encoding='utf-8')
print('Standalone folder:',bundle)
