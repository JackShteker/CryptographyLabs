import unittest
from EC import Curve, Point
from GF import add
from ecc import EllipticCurve


class TestEC(unittest.TestCase):
    def test_mult(self):
        f = 1 << 163 | 1 << 7 | 1 << 6 | 1 << 3 | 1

        # print(f)
        cur = Curve(1, int("5FF6108462A2DC8210AB403925E638A19C1455D21", 16), f)
        P = Point(int("72D867F93A93AC27DF9FF01AFFE74885C8C540420", 16),
                  int("0224A9C3947852B97C5599D5F4AB81122ADC3FD9B", 16))
        d = int("183F60FDF7951FF47D67193F8D073790C1C9B5A3E", 16)
        print(cur.neg(cur.mul(d, P)))
        #
        # p1 = cur.mul2(P)183F60FDF7951FF47D67193F8D073790C1C9B5A3E
        # p2 = cur.add(P, p1)
        # print(p1)
        # print(p2)
        x = cur.mul(int("400000000000000000002BEC12BE2262D39BCF14D", 16), P)
        print(x)
