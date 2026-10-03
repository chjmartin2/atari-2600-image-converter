import unittest
from chrono.core import DATA
from chrono.drivers import SPECS,TEMPLATES,strip_template,load
class DriverPackagingTests(unittest.TestCase):
 def test_public_templates_exclude_driver_bytes(self):
  for stem,driver in TEMPLATES.items():
   b=(DATA/(stem+'.bin')).read_bytes();size=SPECS[driver][1]
   self.assertEqual(b[:size],bytes(size),stem)
 def test_stripping_preserves_remaining_kernel(self):
  for stem,driver in TEMPLATES.items():
   size=SPECS[driver][1];b=bytes([71])*32768;clean=strip_template(stem,b)
   self.assertEqual(clean[:size],bytes(size));self.assertEqual(clean[size:],b[size:])
