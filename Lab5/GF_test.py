import unittest
import GF


class TestGF(unittest.TestCase):

    def test_mod(self):
        a = 7
        print(bin(a))
        b = 5
        print(bin(b))
        m = GF.mod(a, b)
        print(bin(m))

    def test_mult(self):
        a = 0b111
        b = 0b11
        m = GF.mult(a, b, 0b100000000)
        print(bin(m))

    def test_div_mod(self):
        a = 15
        print(bin(a))
        b = 7
        print(bin(b))
        q, v = GF.div_mod(a, b)
        print(bin(q))
        print(bin(v))

    def test_inv(self):
        a = 0b11
        b = 1 << 233 | 1 << 9 | 1 << 4 | 1 << 1 | 1
        i = GF.inv(a, b)
        print(bin(i))
        print(bin(GF.mult(a, i ^ b, b)))
