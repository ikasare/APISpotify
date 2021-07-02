import unittest
from spotifyapidatabase import gettingrequest


class TestFileName(unittest.TestCase):
    def test_gettingid(self):
        self.assertIsNotNone(gettingrequest())


if __name__ == '__main__':
    unittest.main()
