import unittest
from Signature import Signature

class TestSignature(unittest.TestCase):
    def test_rand_int(self):
        s = Signature()
        for i in range(10):
            r = s.rand_int()
            print(r.bit_length())

    def test_to_from_sign(self):
        r = 100
        s = 911
        sig = Signature()
        D = sig.to_signature(r, s)
        r1, s1 = sig.from_signature(D)
        assert r == r1
        assert s == s1

    def test_sign_verify(self):
        T = b"\x01\x02\x03\x04"
        sig = Signature()
        _, D = sig.sign(T)
        assert sig.verify(T, D)