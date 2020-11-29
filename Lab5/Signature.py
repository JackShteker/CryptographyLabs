from EC import Curve, Point, Zero_point
from GF import *
import random
from SHA256 import SHA256

class Signature:
    def __init__(self):
        self.f = 1 << 233 | 1 << 9 | 1 << 4 | 1 << 1 | 1
        self.m = 233
        self.n = 0x1000000000000000000000000000013E974E72F8A6922031D2603CFE0D7
        print(f"L(n):{self.n.bit_length()}")
        self.ln = self.n.bit_length()
        ld = (2 * self.ln)
        self.ld = ld + (16 - ld % 16)
        assert self.ld % 16 == 0 and self.ld >= 2 * self.ln
        self.curve = Curve(1, 0x06973B15095675534C7CF7E64A21BD54EF5DD3B8A0326AA936ECE454D2C, self.f)

        while True:
            self.d = self.rand_int()
            if self.d > 0:
                break

        self.P = self.base_point()
        self.Q = self.curve.neg(self.curve.mul(self.d, self.P))
        self.hash = SHA256()
        self.m_mask = 1 << self.m - 1
        self.n_mask = 1 << (self.ln - 1) - 1
        self.fe, self.e = self.pre_signature()

    def sign(self, T: bytes):
        h = self.hashed_field(T)
        y = mult(h, self.fe, self.f)
        r = self.field_to_int(y)
        assert r != 0
        s = (self.e + self.d * r) % self.n
        assert s != 0
        D = self.to_signature(r, s)

        return T, D

    def verify(self, T: bytes, D: str) -> bool:
        h = self.hashed_field(T)
        r, s = self.from_signature(D)
        R = self.curve.add(self.curve.mul(s, self.P), self.curve.mul(r, self.Q))
        y = mult(h, R.x, self.f)
        rt = self.field_to_int(y)
        return r == rt

    def to_signature(self, r: int, s:int) -> str:
        l = self.ld // 2
        d1 = bin(r)[-1:1:-1] + '0' * (l - r.bit_length())
        d2 = bin(s)[-1:1:-1] + '0' * (l - s.bit_length())
        return d1 + d2

    def from_signature(self, D:str) -> (int, int):
        l = self.ld // 2
        r = int(D[l - 1:: -1].lstrip('0'), 2)
        s = int(D[-1: l-1: -1].lstrip('0'), 2)
        return r, s

    def field_to_int(self, n):
        return n & self.n_mask


    def pre_signature(self) -> (int, int):
        while True:
            e = self.rand_int()
            R = self.curve.mul(e, self.P)
            if R.x != 0:
                break

        return R.x, e



    def hashed_field(self, T: bytes) -> int:
        h = self.hash.hash(T)[:self.m // 8 + 1]
        n = int.from_bytes(h, "little") & self.m_mask
        return n if n != 0 else 1


    def base_point(self):
        while True:
            p = self.rand_point()
            r = self.curve.mul(self.n, p)
            if r == Zero_point:
                break
        return p


    def rand_int(self) -> int:
        r = random.getrandbits(self.ln - 1)
        return r

    def rand_field(self) -> int:
        return random.getrandbits(self.m)

    def rand_point(self) -> Point:
        while True:
            u = self.rand_field()
            w1 = mult(mult(u, u, self.f), u, self.f)
            w2 = mult(self.curve.a, mult(u, u, self.f), self.f)
            w = add(add(w1, w2), self.curve.b)
            k, z = self.solve_eq(u, w)
            if k > 0:
                break

        return Point(u, z)

    def trace(self, x:int ) -> int:
        t = x
        for i in range(1, self.m):
            t = add(square(t, self.f), x)

        return t

    def half_trace(self, x:int) -> int:
        t = x
        for i in range(1, (self.m - 1) // 2 + 1):
            t = add(square(square(t, self.f), self.f), x)

        return t

    def solve_eq(self, u:int, w:int) -> (int, int):
        if u == 0:
            return 1, pow(w, 2 ** (self.m - 1), self.f)
        if w == 0:
            return 2, 0

        v = frac(w, mult(u, u, self.f), self.f)
        t = self.trace(v)

        if t == 1:
            return 0, 0

        t = self.half_trace(v)
        return 2, mult(t, u, self.f)