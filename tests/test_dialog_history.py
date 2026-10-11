import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from chrono.preferences import dialog_directory, remember_directory, read_preferences, save_stella_path


class DialogHistoryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.prefs = self.root/'preferences.json'
        self.patch = patch('chrono.preferences.preferences_path', return_value=self.prefs)
        self.patch.start()
        self.addCleanup(self.patch.stop)

    def test_independent_persistent_histories(self):
        opened = self.root/'inputs'; opened.mkdir()
        saved = self.root/'outputs'; saved.mkdir()
        self.assertTrue(remember_directory('open', opened))
        self.assertEqual(dialog_directory('save')['initialdir'], str(Path.home()))
        self.assertTrue(remember_directory('save', saved))
        self.assertEqual(dialog_directory('open')['initialdir'], str(opened.resolve()))
        self.assertEqual(dialog_directory('save')['initialdir'], str(saved.resolve()))
        # Disk data, rather than a session cache, supplies the next app's defaults.
        data = json.loads(self.prefs.read_text())
        self.assertEqual(data['last_open_directory'], str(opened.resolve()))
        data['last_save_directory'] = str(opened.resolve())
        self.prefs.write_text(json.dumps(data))
        self.assertEqual(dialog_directory('save')['initialdir'], str(opened.resolve()))

    def test_missing_invalid_and_corrupt_paths_fall_back(self):
        for value in (str(self.root/'missing'), 12, '', '\0'):
            self.prefs.write_text(json.dumps({'last_open_directory': value}))
            self.assertEqual(dialog_directory('open')['initialdir'], str(Path.home()))
        self.prefs.write_text('broken json')
        self.assertEqual(dialog_directory('save')['initialdir'], str(Path.home()))

    def test_missing_directory_does_not_replace_history(self):
        remember_directory('save', self.root)
        self.assertFalse(remember_directory('save', self.root/'missing'))
        self.assertEqual(dialog_directory('save')['initialdir'], str(self.root.resolve()))

    def test_preserves_stella_and_other_preferences(self):
        stella = self.root/'Stella.exe'; stella.touch()
        self.prefs.write_text(json.dumps({'other': True}))
        save_stella_path(stella)
        remember_directory('open', self.root)
        remember_directory('save', self.root)
        save_stella_path(stella)
        data = read_preferences()
        self.assertTrue(data['other'])
        self.assertEqual(data['stella_path'], str(stella.resolve()))
        self.assertIn('last_open_directory', data)
        self.assertIn('last_save_directory', data)

    def test_preference_write_failure_is_nonfatal(self):
        with patch('pathlib.Path.write_text', side_effect=PermissionError('read only')):
            self.assertFalse(remember_directory('open', self.root))


if __name__ == '__main__':
    unittest.main()
