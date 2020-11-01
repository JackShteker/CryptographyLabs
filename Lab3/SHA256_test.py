import unittest
from SHA256 import SHA256


class TestSHA256Funcs(unittest.TestCase):
    def test_encrypt_decrypt(self):
        def runSHA256(msg, expected):
            sha = SHA256()
            res_hash = sha.hash(msg)

            assert res_hash == expected, res_hash

        runSHA256("abc".encode("utf-8"),
                  bytes.fromhex("ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"))

        runSHA256("abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq".encode("utf-8"),
                  bytes.fromhex("248D6A61D20638B8E5C026930C3E6039A33CE45964FF2167F6ECEDD419DB06C1"))
