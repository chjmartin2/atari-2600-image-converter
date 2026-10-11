import json,tempfile,threading,unittest
from pathlib import Path
from unittest.mock import patch
from concurrent.futures import ThreadPoolExecutor
import numpy as np
from chrono import indexed_search as ix
from chrono import weighted_search as ws
from chrono import palette_store as store
from chrono.core import Cancelled,_mixtures,_mixtures_direct

class PaletteStoreTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.loaded=store.load_catalog()

    def test_every_array_matches_regeneration_exactly(self):
        generated=ix.Catalog();ws.blend_cube(generated)
        for name in store.DTYPES:
            with self.subTest(array=name):
                np.testing.assert_array_equal(getattr(self.loaded,name),getattr(generated,name))
                self.assertFalse(getattr(self.loaded,name).flags.writeable)
                self.assertIsInstance(getattr(self.loaded,name),np.memmap)
        points=np.array([[0.,0.,0.],[50.,25.,-30.],[90.,-10.,10.]])
        np.testing.assert_array_equal(self.loaded.index.query(points)[1],generated.index.query(points)[1])

    def test_all_backgrounds_and_component_combinations(self):
        # Every background, with deterministic samples of foreground triples.
        triples=self.loaded.triples[::193]
        cube=ws.blend_cube(self.loaded)
        for bg in range(128):
            ids=ws.palette_ids(self.loaded,triples,bg,cube)
            self.assertTrue((ids>=0).all())
            np.testing.assert_array_equal(self.loaded.rgb[ids],_mixtures_direct(np.column_stack((triples,np.full(len(triples),bg)))))

    def test_candidate_mixing_uses_lookup_and_preserves_direct_results(self):
        batch=np.random.default_rng(15).integers(0,128,(8000,4))
        expected=_mixtures_direct(batch)
        with patch('chrono.core._mixtures_direct',side_effect=AssertionError('runtime blending')):
            np.testing.assert_array_equal(_mixtures(batch),expected)

    def test_restricted_developer_catalog_keeps_direct_matching(self):
        catalog=ix.Catalog((0,7,20,60,64,112))
        codes=np.array([[20,60,64,112],[0,7,20,0]])
        with patch.object(ix,'get_catalog',return_value=catalog):
            np.testing.assert_array_equal(_mixtures(codes),_mixtures_direct(codes))

    def test_runtime_concurrent_load_never_regenerates(self):
        with patch.object(ix,'_catalog',None),patch.object(ix.Catalog,'__init__',side_effect=AssertionError('runtime generation')):
            with patch.object(store,'load_catalog',wraps=store.load_catalog) as load:
                with ThreadPoolExecutor(max_workers=4) as workers:
                    results=list(workers.map(lambda _:ix.get_catalog(),range(4)))
                self.assertEqual(load.call_count,1)
                self.assertTrue(all(c is results[0] for c in results))
                with patch.object(ws.itertools,'permutations',side_effect=AssertionError('runtime cube build')):
                    self.assertIs(ws.blend_cube(results[0]),results[0].blend_cube)

    def test_missing_corrupt_and_stale_resources_fail_without_generation(self):
        original=json.loads((store.DIRECTORY/'manifest.json').read_text())
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            with self.assertRaisesRegex(ValueError,'build_mixed_palettes'):store.load_catalog(directory=root)
            stale=dict(original,signature='stale')
            (root/'manifest.json').write_text(json.dumps(stale))
            with self.assertRaisesRegex(ValueError,'signature mismatch'):store.load_catalog(directory=root)
            (root/'manifest.json').write_text(json.dumps(original))
            (root/'triples.npy').write_bytes(b'corrupt')
            with self.assertRaisesRegex(ValueError,'checksum mismatch'):store.load_catalog(directory=root)

    def test_model_signature_changes_with_palette_and_cancel_works(self):
        before=store.signature()
        changed=store.TIA.copy();changed[0,0]+=1
        with patch.object(store,'TIA',changed):self.assertNotEqual(before,store.signature())
        with patch.object(store,'MODEL',store.MODEL+'-changed'):self.assertNotEqual(before,store.signature())
        event=threading.Event();event.set()
        with self.assertRaises(Cancelled):store.load_catalog(cancel=event)
        with self.assertRaises(Cancelled):ix.get_catalog(event)
