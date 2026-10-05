import tempfile,unittest
from pathlib import Path
from unittest.mock import patch
from chrono import drivers

class StandaloneTests(unittest.TestCase):
    def test_source_support_stays_with_existing_resources(self):
        with patch.object(drivers.sys,'frozen',False,create=True):
            self.assertEqual(drivers.support_directory(),drivers.DATA)

    def test_frozen_support_uses_persistent_user_cache(self):
        with tempfile.TemporaryDirectory() as temp:
            with patch.object(drivers.sys,'frozen',True,create=True),patch.dict('os.environ',{'LOCALAPPDATA':temp}):
                directory=Path(temp)/'RetroComputerist/Atari2600ImageOptimizer/drivers'
                self.assertEqual(drivers.support_directory(),directory)
                with self.assertRaisesRegex(ValueError,'Setup cartridge support'):
                    drivers.load('bus2')
                directory.mkdir(parents=True);(directory/'bus2-driver.bin').write_bytes(b'corrupt')
                with self.assertRaisesRegex(ValueError,'checksum mismatch'):
                    drivers.load('bus2')
