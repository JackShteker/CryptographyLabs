import unittest
from OAEP import RSA_OAEP


class TestRSAFuncs(unittest.TestCase):

    def test_RSA(self):
        def run_RSA_OAEP(s):
            r = RSA_OAEP()
            c = r.encrypt(s)
            m = r.decrypt(c)
            assert s.hex() == m.hex()

        run_RSA_OAEP("abc".encode("utf-8"))
        run_RSA_OAEP("abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq".encode("utf-8"))


