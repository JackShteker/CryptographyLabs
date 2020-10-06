import unittest

from AES import *
from util import *


class TestUtilFuncs(unittest.TestCase):
    def test_bytesToWordArray(self):
        w = bytesToWordArray(bytearray(b"\x00\x00\x00\x00\x07\x80\x00\x03"))
        assert w[0].hex() == "00000000"
        assert w[1].hex() == "07800003"

    def test_strToByteArray(self):
        b = strToByteArray("00 00 00 00 07 80 00 03")
        print(b)



if __name__ == '__main__':
    unittest.main()
