import unittest
from miller_rabin import miller_rabin


class TestMiller(unittest.TestCase):
    def test_miller_rabin(self):
        assert not miller_rabin(1000000)
        assert miller_rabin(115249)
        assert not miller_rabin(115251)
        assert miller_rabin(22953686867719691230002707821868552601124472329079)
        assert not miller_rabin(22953686867719691230002707821868552601124472329081)
