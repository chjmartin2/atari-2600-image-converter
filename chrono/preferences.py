"""Machine-local preferences, separate from portable image/export settings."""
import json
import os
from pathlib import Path


def preferences_path():
    root=Path(os.environ.get('LOCALAPPDATA') or Path.home()/'AppData'/'Local')
    return root/'Chrono2 Studio'/'preferences.json'


def read_preferences():
    try:
        data=json.loads(preferences_path().read_text(encoding='utf-8'))
        return data if isinstance(data,dict) else {}
    except (OSError,ValueError):
        return {}


def stella_path():
    saved=read_preferences().get('stella_path')
    candidates=[]
    if isinstance(saved,str) and saved:candidates.append(Path(saved))
    for variable,fallback in (('PROGRAMFILES',r'C:\Program Files'),('PROGRAMFILES(X86)',r'C:\Program Files (x86)')):
        candidates.append(Path(os.environ.get(variable) or fallback)/'Stella'/'Stella.exe')
    return next((path for path in candidates if path.is_file() and path.name.lower()=='stella.exe'),None)


def save_stella_path(path):
    path=Path(path).resolve()
    if not path.is_file() or path.name.lower()!='stella.exe':
        raise ValueError('Select the Stella.exe application from your Stella installation.')
    destination=preferences_path();destination.parent.mkdir(parents=True,exist_ok=True)
    data=read_preferences();data['stella_path']=str(path)
    temporary=destination.with_suffix('.tmp')
    temporary.write_text(json.dumps(data,indent=2),encoding='utf-8')
    temporary.replace(destination)
    return path
