import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from chrono.preferences import stella_path, save_stella_path


class StellaLocationTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name);self.config=self.root/'preferences.json'
        self.default=self.root/'programs'/'Stella'/'Stella.exe'
        self.other=self.root/'portable'/'Stella.exe'
        prefs=patch('chrono.preferences.preferences_path',return_value=self.config)
        prefs.start();self.addCleanup(prefs.stop)
        env=patch.dict('os.environ',{'PROGRAMFILES':str(self.root/'programs'),'PROGRAMFILES(X86)':str(self.root/'programs32')})
        env.start();self.addCleanup(env.stop)

    def create(self,path):
        path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(b'test placeholder')

    def test_default_installation_needs_no_configuration(self):
        self.assertIsNone(stella_path())
        self.create(self.default)
        self.assertEqual(stella_path(),self.default)
        self.assertFalse(self.config.exists())

    def test_custom_location_remembered_and_missing_custom_falls_back(self):
        self.create(self.default);self.create(self.other)
        save_stella_path(self.other)
        self.assertEqual(stella_path(),self.other.resolve())
        self.other.unlink()
        self.assertEqual(stella_path(),self.default)

    def test_bad_config_and_32_bit_default(self):
        self.config.write_text('{invalid')
        path=self.root/'programs32'/'Stella'/'Stella.exe';self.create(path)
        self.assertEqual(stella_path(),path)
        self.config.write_text(json.dumps({'stella_path':42}))
        self.assertEqual(stella_path(),path)

    def test_wrong_file_rejected_and_unrelated_preferences_retained(self):
        other=self.root/'other.exe';self.create(other)
        with self.assertRaises(ValueError):save_stella_path(other)
        self.config.write_text(json.dumps({'other_setting':True}))
        self.create(self.other);save_stella_path(self.other)
        self.assertTrue(json.loads(self.config.read_text())['other_setting'])


if __name__=='__main__':unittest.main()
