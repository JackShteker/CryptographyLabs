import unittest

from Kalyna import Kalyna
from util import strToWordArrayDense


class TestKalynaFuncs(unittest.TestCase):
    def test__add_mod_64(self):
        inp1 = bytes((0, 1, 1, 1, 1, 1, 1, 200))
        inp1 = Kalyna._bytes_to_state(inp1)

        inp2 = bytes((1, 0, 0, 0, 0, 0, 0, 200))
        inp2 = Kalyna._bytes_to_state(inp2)

        Kalyna._add_mod_64(inp1, inp2)
        assert inp1[0] == bytearray(b'\x01\x01\x01\x01\x01\x01\x01\x90')

    def test__sub_bytes(self):
        state = strToWordArrayDense("050102030405060708090A0B0C0D0E0F", 8)
        Kalyna._sub_bytes(state)
        assert state == strToWordArrayDense("75BB9A4D6BCB452A713ADFB31790511F", 8)

    def test__shift_rows(self):
        state = strToWordArrayDense("75BB9A4D6BCB452A713ADFB31790511F", 8)
        Kalyna._shift_rows(state, 2)
        assert state == strToWordArrayDense("75BB9A4D1790511F713ADFB36BCB452A", 8)

    def test__linear_transfrom(self):
        state = strToWordArrayDense("75BB9A4D1790511F713ADFB36BCB452A", 8)
        Kalyna._mix_cols(state)
        assert state == strToWordArrayDense("62C97C6E6ABF4133ED5131D624C7C182", 8)

    def test__inv_sub_bytes(self):
        state = strToWordArrayDense("AFF9B83FB5CB2EADB66A08CECDB4966C", 8)
        Kalyna._inv_sub_bytes(state)
        assert state == strToWordArrayDense("17AF69BA9A0547EB259BC23A8813BDB0", 8)

    def test__inv_shift_rows(self):
        state = strToWordArrayDense("AFF9B83FCDB4966CB66A08CEB5CB2EAD", 8)
        Kalyna._inv_shift_rows(state, 2)
        assert state == strToWordArrayDense("AFF9B83FB5CB2EADB66A08CECDB4966C", 8)

    def test__inv_linear_transfrom(self):
        state = strToWordArrayDense("DA4AF5B72FCEB2793F72622CDA894498", 8)
        Kalyna._inv_mix_cols(state)
        assert state == strToWordArrayDense("AFF9B83FCDB4966CB66A08CEB5CB2EAD", 8)

    def test__shift_cols_left(self):
        inp1 = bytes((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15))
        inp1 = Kalyna._bytes_to_mutable_state(inp1)
        Kalyna._shift_cols_left(inp1)

        assert inp1 == Kalyna._bytes_to_mutable_state(
            bytes((0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30)))

    def test__rotate_key_right(self):
        inp = [bytearray(b'\x01\x01\x01\x01\x01\x01\x01\x01'), bytearray(b'\x02\x02\x02\x02\x02\x02\x02\x02'),
               bytearray(b'\x03\x03\x03\x03\x03\x03\x03\x03')]
        Kalyna._rotate_key_right(inp)
        assert inp == [bytearray(b'\x03\x03\x03\x03\x03\x03\x03\x03'), bytearray(b'\x01\x01\x01\x01\x01\x01\x01\x01'),
                       bytearray(b'\x02\x02\x02\x02\x02\x02\x02\x02')]

    def test_rotate_left(self):
        inp = b'\x16\x50\x5e\x6b\x9b\x3a\xb1\xe6\x86\x5b\x77\xdc\xe0\x82\xa0\xf4'
        expected_out = b'\xe6\x86\x5b\x77\xdc\xe0\x82\xa0\xf4\x16\x50\x5e\x6b\x9b\x3a\xb1'
        state = Kalyna._bytes_to_mutable_state(inp)
        out_state = Kalyna._bytes_to_mutable_state(expected_out)
        Kalyna._rotate_left(state, 2)
        assert state == out_state

    def test_round_key_expand(self):
        kal = Kalyna(128, 128)

        kt = kal._key_expand_kt(b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0A\x0B\x0C\x0D\x0E\x0F')

        assert Kalyna._state_to_bytes(kt) == b'\x86\x2F\x1F\x65\x3B\x77\x5B\xA1\xD0\x5C\xBC\x2F\x38\xE2\xD8\x7D'

    def test_key_expansion(self):
        kal = Kalyna(128, 128)

        expected_keys = [
            b'\x16\x50\x5e\x6b\x9b\x3a\xb1\xe6\x86\x5b\x77\xdc\xe0\x82\xa0\xf4',
            b'\xE6\x86\x5B\x77\xDC\xE0\x82\xA0\xF4\x16\x50\x5E\x6B\x9B\x3A\xB1',
            b'\x7E\x70\x87\x6E\xAE\x49\x84\x76\x8A\xAA\xA0\x0A\x7C\x93\xEC\x42',
            b'\x76\x8A\xAA\xA0\x0A\x7C\x93\xEC\x42\x7E\x70\x87\x6E\xAE\x49\x84',
            b'\x45\xCE\xD4\xC5\x1E\x91\x40\xF5\x3E\x72\x76\x82\x0F\x0B\xD9\xFE',
            b'\xF5\x3E\x72\x76\x82\x0F\x0B\xD9\xFE\x45\xCE\xD4\xC5\x1E\x91\x40',
            b'\x8C\x77\xEE\x22\x79\x00\xC4\x62\x51\x5F\x66\x32\x05\x60\xC4\xB1',
            b'\x62\x51\x5F\x66\x32\x05\x60\xC4\xB1\x8C\x77\xEE\x22\x79\x00\xC4',
            b'\x0A\x98\x72\xE2\x5C\xD2\xB0\xB8\xAA\x87\x9A\x20\x86\xA6\x6D\xD8',
            b'\xB8\xAA\x87\x9A\x20\x86\xA6\x6D\xD8\x0A\x98\x72\xE2\x5C\xD2\xB0',
            b'\x57\x26\xB1\xA8\x94\xDB\xC4\x18\xF6\x0B\xF3\xD5\xE8\xD7\x48\x61'
        ]

        round_keys = kal._key_expansion(b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0A\x0B\x0C\x0D\x0E\x0F')
        assert len(expected_keys) == len(round_keys)

        for key_index in range(len(expected_keys)):
            key = kal._state_to_bytes(round_keys[key_index])
            assert expected_keys[key_index] == key

    def test__cipher(self):
        inp = b'\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1A\x1B\x1C\x1D\x1E\x1F'
        expected = b'\x81\xBF\x1C\x7D\x77\x9B\xAC\x20\xE1\xC9\xEA\x39\xB4\xD2\xAD\x06'
        key = b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0A\x0B\x0C\x0D\x0E\x0F'

        kal = Kalyna(128, 128)
        res = kal._cipher(inp, kal._key_expansion(key))
        assert res == expected

    def test__decipher(self):
        inp = b'\x81\xBF\x1C\x7D\x77\x9B\xAC\x20\xE1\xC9\xEA\x39\xB4\xD2\xAD\x06'
        expected = b'\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1A\x1B\x1C\x1D\x1E\x1F'
        key = b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0A\x0B\x0C\x0D\x0E\x0F'

        kal = Kalyna(128, 128)
        res = kal._decipher(inp, kal._key_expansion(key))
        assert res == expected

    # without dividing into blocks
    def test_cypher_decypher(self):
        def runKalyna(msg: bytes, key: bytes):
            kal = Kalyna(len(msg) * 8, len(key) * 8)
            expanded_key = kal._key_expansion(key)

            ciphertext = kal._cipher(msg, expanded_key)
            decrypted = kal._decipher(ciphertext, expanded_key)
            assert msg == decrypted

        # 128 128
        runKalyna(b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0A\x0B\x0C\x0D\x0E\x0F',
                  b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0A\x0B\x0C\x0D\x0E\x0F')

        # 128 256
        runKalyna(b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0A\x0B\x0C\x0D\x0E\x0F',
                  b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0A\x0B\x0C\x0D\x0E\x0F\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0A\x0B\x0C\x0D\x0E\x0F')

        # 512 512
        runKalyna(int(
            "404142434445464748494A4B4C4D4E4F505152535455565758595A5B5C5D5E5F606162636465666768696A6B6C6D6E6F707172737475767778797A7B7C7D7E7F",
            16).to_bytes(64, "big"),
                  int(
                      "000102030405060708090A0B0C0D0E0F101112131415161718191A1B1C1D1E1F202122232425262728292A2B2C2D2E2F303132333435363738393A3B3C3D3E3F",
                      16).to_bytes(64, "big"))

    def test_encrypt_decrypt(self):
        def runKalyna(msg, key):
            kal = Kalyna(128, 128)
            ciphertext = kal.encrypt(msg, key)
            decrypted = kal.decrypt(ciphertext, key)
            assert msg == decrypted

        runKalyna("test_string".encode("utf-8"),
                  b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0A\x0B\x0C\x0D\x0E\x0F')

        runKalyna("much_much_much_much_much_longer_test_string".encode("utf-8"),
                  b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0A\x0B\x0C\x0D\x0E\x0F')

    def test_inv_sub_bytes(self):
        kal = Kalyna(128, 128)
        inp = b'\x9A\x2B\x1E\xAC\x76\xEE\x89\x1B\x91\x4A\xCF\x17\x7C\x98\xDD\x3D'
        expected = b'\x26\x61\x70\x7E\xAF\x4F\xC7\xFD\x9E\x74\x91\xF7\xFC\x9F\xBE\x13'

        state = Kalyna._bytes_to_mutable_state(inp)
        kal._inv_sub_bytes(state)

        assert state == Kalyna._bytes_to_mutable_state(expected)
