"""Rebuild the self-contained Windows x64 matcher using installed MSVC tools."""
from pathlib import Path
import os,subprocess,sys,tempfile,hashlib,json


def main():
    root=Path(__file__).resolve().parents[1]
    source=root/'chrono/native/palette_match.c'
    output=root/'chrono/native/palette_match.dll'
    manifest=output.with_suffix('.json')
    if output.exists() and manifest.exists() and '--force' not in sys.argv:
        info=json.loads(manifest.read_text(encoding='utf-8'))
        if (info.get('source_sha256')==hashlib.sha256(source.read_bytes()).hexdigest()
                and info.get('dll_sha256')==hashlib.sha256(output.read_bytes()).hexdigest()):
            print('Native matcher is current.');return
    if sys.platform!='win32':
        raise SystemExit('This build script targets Windows x64; other systems use the NumPy matcher.')
    where=Path(os.environ.get('ProgramFiles(x86)',r'C:\Program Files (x86)'))/'Microsoft Visual Studio/Installer/vswhere.exe'
    install=subprocess.check_output([str(where),'-latest','-products','*','-requires',
        'Microsoft.VisualStudio.Component.VC.Tools.x86.x64','-property','installationPath'],text=True).strip()
    setup=Path(install)/'VC/Auxiliary/Build/vcvars64.bat'
    if not setup.is_file():raise SystemExit('Install Visual Studio C++ build tools to rebuild the matcher.')
    with tempfile.TemporaryDirectory(prefix='atari-palette-build-',ignore_cleanup_errors=True) as temp:
        temp=Path(temp);script=temp/'build.cmd';dll=temp/'palette_match.dll'
        script.write_text('\n'.join([
            '@echo off',f'call "{setup}" >nul','if errorlevel 1 exit /b 1',
            f'cl /nologo /O2 /LD /GS- /Zl "{source}" /Fo:"{temp / "palette_match.obj"}" /link /OUT:"{dll}" /IMPLIB:"{temp / "palette_match.lib"}" /NOENTRY /NODEFAULTLIB',
            'exit /b %errorlevel%','']),encoding='utf-8')
        subprocess.run(['cmd','/c',str(script)],cwd=root,check=True)
        output.write_bytes(dll.read_bytes())
    info={'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
          'dll_sha256':hashlib.sha256(output.read_bytes()).hexdigest(),'architecture':'Windows x64'}
    output.with_suffix('.json').write_text(json.dumps(info,indent=2)+'\n',encoding='utf-8')
    print('Built',output)


if __name__=='__main__':main()
