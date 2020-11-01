import unittest
from Kupyna import Kupyna


class TestKupynaFuncs(unittest.TestCase):
    def test_encrypt_decrypt_256(self):
        def runKupyna(msg, expected):
            k = Kupyna(256)
            res_hash = k.hash(msg)

            assert res_hash == expected, res_hash

        runKupyna(bytes.fromhex("000102030405060708090A0B0C0D0E0F101112131415161718191A1B1C1D1E1F"
                                "202122232425262728292A2B2C2D2E2F303132333435363738393A3B3C3D3E3F"),
                  bytes.fromhex("08F4EE6F1BE6903B324C4E27990CB24EF69DD58DBE84813EE0A52F6631239875"))

        runKupyna(bytes.fromhex("000102030405060708090A0B0C0D0E0F101112131415161718191A1B1C1D1E1F"
                                "202122232425262728292A2B2C2D2E2F303132333435363738393A3B3C3D3E3F"
                                "404142434445464748494A4B4C4D4E4F505152535455565758595A5B5C5D5E5F"
                                "606162636465666768696A6B6C6D6E6F707172737475767778797A7B7C7D7E7F"),
                  bytes.fromhex("0A9474E645A7D25E255E9E89FFF42EC7EB31349007059284F0B182E452BDA882"))

    def test_encrypt_decrypt_512(self):
        def runKupyna(msg, expected):
            k = Kupyna(512)
            res_hash = k.hash(msg)

            assert res_hash == expected, res_hash

        runKupyna(bytes.fromhex("000102030405060708090A0B0C0D0E0F101112131415161718191A1B1C1D1E1F"
                                "202122232425262728292A2B2C2D2E2F303132333435363738393A3B3C3D3E3F"),
                  bytes.fromhex("3813E2109118CDFB5A6D5E72F7208DCCC80A2DFB3AFDFB02F46992B5EDBE536B"
                                "3560DD1D7E29C6F53978AF58B444E37BA685C0DD910533BA5D78EFFFC13DE62A"))

        runKupyna(bytes.fromhex("000102030405060708090A0B0C0D0E0F101112131415161718191A1B1C1D1E1F"
                                "202122232425262728292A2B2C2D2E2F303132333435363738393A3B3C3D3E3F"
                                "404142434445464748494A4B4C4D4E4F505152535455565758595A5B5C5D5E5F"
                                "606162636465666768696A6B6C6D6E6F707172737475767778797A7B7C7D7E7F"),
                  bytes.fromhex("76ED1AC28B1D0143013FFA87213B4090B356441263C13E03FA060A8CADA32B97"
                                "9635657F256B15D5FCA4A174DE029F0B1B4387C878FCC1C00E8705D783FD7FFE"))


    def test_t1(self):
        k = Kupyna(256)
        b = bytes.fromhex(
            "000102030405060708090A0B0C0D0E0F101112131415161718191A1B1C1D1E1F202122232425262728292A2B2C2D2" +
            "E2F303132333435363738393A3B3C3D3E3F")
        s = Kupyna._bytes_to_mutable_state(b)
        k._t1(s)
        b_s = k._state_to_bytes(s)
        assert b_s.hex() == "20a066016c8daa5aa2aca450d21f2796fbdc2e0cc452af0aaf67e27a0755cb32718c2c7909201" + \
                            "d3e7a3f256234c80b70d51ae3936db26cf56e1f1ba8a0a7e1c0"

    def test_t2(self):
        k = Kupyna(256)
        b = bytes.fromhex(
            "000102030405060708090A0B0C0D0E0F101112131415161718191A1B1C1D1E1F202122232425262728292A2B2C2D2E" +
            "2F303132333435363738393A3B3C3D3E3F")
        s = Kupyna._bytes_to_mutable_state(b)
        k._t2(s)
        b_s = k._state_to_bytes(s)
        assert b_s.hex() == "2d6f3a8e12f162aec3f76e0402575068671824ef72fea1cd7d71fd4d8e6a27a10c2ba7ebf31c27" + \
                            "7f91dd384731025a8df3013049279cf47251b2434f2632f00a"

    def test_xor_states(self):
        s1 = [bytearray((1, 2, 3)), bytearray((4, 5, 6)), bytearray((7, 8, 9))]
        s2 = [bytearray((1, 2, 3)), bytearray((4, 5, 6)), bytearray((7, 8, 9))]
        s = Kupyna._xor_states(s1, s2)
        assert Kupyna._state_to_bytes(s).hex() == "000000000000000000"

        s1 = [bytearray((1, 2, 3)), bytearray((0, 0, 0)), bytearray((7, 8, 9))]
        s2 = [bytearray((1, 2, 3)), bytearray((4, 5, 6)), bytearray((7, 8, 9))]
        s = Kupyna._xor_states(s1, s2)
        assert Kupyna._state_to_bytes(s).hex() == "000000040506000000"
