import unittest
from RSA import RSA


class TestRSAFuncs(unittest.TestCase):
    def test_keygen(self):
        p_k, s_k = RSA._keygen(11, 17)

    def test_RSA(self):
        def run_RSA(s):
            r = RSA(16)
            c = r.encrypt(s)
            m = r.decrypt(c)
            assert s.hex() == m.hex()
        run_RSA("abc".encode("utf-8"))
        run_RSA(int(0x726485f293e19b95bc1d11dba85836).to_bytes(16, "little"))

    def test_blockRSA(self):
        def run_RSA_block(s):
            r = RSA(16)
            print(r._p)
            print(r._q)
            c = r.encrypt_block(s)
            print(c.hex())
            m = r.decrypt_block(c)
            assert s.hex() == m.hex()
        # run_RSA("abc".encode("utf-8"))
        run_RSA_block(int(0x42e655555).to_bytes(16, "little"))
