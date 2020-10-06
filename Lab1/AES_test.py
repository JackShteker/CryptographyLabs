import unittest

from AES import *
from util import *


class TestAESFuncs(unittest.TestCase):

    def test_strToWordArrayDense(self):
        assert strToWordArray("2b 7e 15 16 28 ae d2 a6 ab f7 15 88 09 cf 4f 3c") == strToWordArrayDense(
            "2b7e151628aed2a6abf7158809cf4f3c")

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
        aes = AES(4, "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00")
        inp = strToWordArray("32 43 f6 a8 88 5a 30 8d 31 31 98 a2 e0 37 07 34")
        key = strToWordArray("2b 7e 15 16 28 ae d2 a6 ab f7 15 88 09 cf 4f 3c")

        w = key_expansion(key, 4, 10)
        cipher = aes._cipher(inp, w)
        print(cipher)

        assert cipher.hex() == "3925841d02dc09fbdc118597196a0b32"

    def test__decipher(self):
        aes = AES(4, "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00")
        cipher = strToWordArrayDense("69c4e0d86a7b0430d8cdb78070b4c55a")
        key = strToWordArray("00 01 02 03 04 05 06 07 08 09 0a 0b 0c 0d 0e 0f")

        dw = eq_rev_key_expansion(key, 4, 10)

        msg = aes._decipher(cipher, dw)

        assert wordArrayToStr(msg) == "00112233445566778899aabbccddeeff"

    def test__AES(self):
        aes = AES(4, "00 01 02 03 04 05 06 07 08 09 0a 0b 0c 0d 0e 0f")
        key = "2b 7e 15 16 28 ae d2 a6 ab f7 15 88 09 cf 4f 3c"
        inp = "32 43 f6 a8 88 5a 30 8d 31 31 98 a2 e0 37 07 34"

        ciphertext = aes.encrypt(inp, key)

        deciphered = aes.decrypt(ciphertext, key)
        assert deciphered == inp

        # DENSE
        # 4 bytes key

        aes = AES(4, "00 01 02 03 04 05 06 07 08 09 0a 0b 0c 0d 0e 0f")
        key = "2b7e151628aed2a6abf7158809cf4f3c"
        inp = "3243f6a8885a308d313198a2e0370734"

        ciphertext = aes.encrypt(inp, key, "dense")

        deciphered = aes.decrypt(ciphertext, key, "dense")
        assert deciphered == inp

        # 6 bytes key

        aes = AES(6, "00 01 02 03 04 05 06 07 08 09 0a 0b 0c 0d 0e 0f")
        key = "2b7e151628aed2a6abf7158809cf4f3cabf7158809cf4f3c"
        inp = "3243f6a8885a308d313198a2e0370734"

        ciphertext = aes.encrypt(inp, key, "dense")

        deciphered = aes.decrypt(ciphertext, key, "dense")
        assert deciphered == inp

        # 8 bytes key

        aes = AES(8, "00 01 02 03 04 05 06 07 08 09 0a 0b 0c 0d 0e 0f")
        key = "2b7e151628aed2a6abf7158809cf4f3c2b7e151628aed2a6abf7158809cf4f3c"
        inp = "3243f6a8885a308d313198a2e0370734"

        ciphertext = aes.encrypt(inp, key, "dense")

        deciphered = aes.decrypt(ciphertext, key, "dense")
        assert deciphered == inp

if __name__ == '__main__':
    unittest.main()
