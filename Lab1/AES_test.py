import unittest

from AES import *


def strToWordArray(s):
    s_bytes = [int(b, 16) for b in s.split(" ")]
    assert len(s_bytes) == 16 or len(s_bytes) == 24 or len(s_bytes) == 32

    return [bytearray(s_bytes[i * 4:(i + 1) * 4]) for i in range(len(s_bytes) // 4)]


class TestAESFuncs(unittest.TestCase):

    def test_key_expansion_4(self):
        key = strToWordArray("2b 7e 15 16 28 ae d2 a6 ab f7 15 88 09 cf 4f 3c")
        w = key_expansion(key, 4, 10)

        #
        assert len(w) == 44

        # verify fist 4 columns (same as key)
        assert w[0].hex() == "2b7e1516"
        assert w[1].hex() == "28aed2a6"
        assert w[2].hex() == "abf71588"
        assert w[3].hex() == "09cf4f3c"

        # verify last 4 columns
        assert w[-4].hex() == "d014f9a8"
        assert w[-3].hex() == "c9ee2589"
        assert w[-2].hex() == "e13f0cc8"
        assert w[-1].hex() == "b6630ca6"

    def test_key_expansion_6(self):
        key = strToWordArray("8e 73 b0 f7 da 0e 64 52 c8 10 f3 2b 80 90 79 e5 62 f8 ea d2 52 2c 6b 7b")
        w = key_expansion(key, 6, 12)

        assert len(w) == 52

        # verify last 6 columns
        assert w[-6].hex() == "282d166a"
        assert w[-5].hex() == "bc3ce7b5"
        assert w[-4].hex() == "e98ba06f"
        assert w[-3].hex() == "448c773c"
        assert w[-2].hex() == "8ecc7204"
        assert w[-1].hex() == "01002202"

    def test_key_expansion_8(self):
        key = strToWordArray(
            "60 3d eb 10 15 ca 71 be 2b 73 ae f0 85 7d 77 81 1f 35 2c 07 3b 61 08 d7 2d 98 10 a3 09 14 df f4")
        w = key_expansion(key, 8, 14)

        assert len(w) == 60

        # verify last 8 columns
        assert w[-8].hex() == "cafaaae3"
        assert w[-7].hex() == "e4d59b34"
        assert w[-6].hex() == "9adf6ace"
        assert w[-5].hex() == "bd10190d"
        assert w[-4].hex() == "fe4890d1"
        assert w[-3].hex() == "e6188d0b"
        assert w[-2].hex() == "046df344"
        assert w[-1].hex() == "706c631e"

    def test__cipher(self):
        aes = AES(4)
        inp = strToWordArray("32 43 f6 a8 88 5a 30 8d 31 31 98 a2 e0 37 07 34")
        key = strToWordArray("2b 7e 15 16 28 ae d2 a6 ab f7 15 88 09 cf 4f 3c")

        w = key_expansion(key, 4, 10)
        cipher = aes._cipher(inp, w)

        assert cipher[0].hex() == "3925841d"
        assert cipher[1].hex() == "02dc09fb"
        assert cipher[2].hex() == "dc118597"
        assert cipher[3].hex() == "196a0b32"


if __name__ == '__main__':
    unittest.main()
