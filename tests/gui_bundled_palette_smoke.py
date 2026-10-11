"""Run the standard GUI checks with runtime palette generation forbidden."""
import runpy,sys
from pathlib import Path
from unittest.mock import patch
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from chrono import indexed_search as ix
from chrono.weighted_search import blend_cube
with patch.object(ix.Catalog,'__init__',side_effect=AssertionError('GUI attempted to generate palettes')):
    runpy.run_path(str(Path(__file__).with_name('gui_smoke.py')),run_name='__main__')
    catalog=ix.get_catalog()
    assert isinstance(catalog.rgb,np.memmap)
    assert not catalog.rgb.flags.writeable
    assert blend_cube(catalog) is catalog.blend_cube
    assert ix.get_catalog() is catalog
print('GUI used bundled read-only palettes throughout; no runtime generation')
