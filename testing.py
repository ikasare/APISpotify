import unittest
from spotifyapidatabase import gettingrequest


class TestFileName(unittest.TestCase):
    def test_gettingid(self):
      self.assertEqual(gettingrequest().status_code, 200)

if __name__ == '__main__':
    unittest.main()