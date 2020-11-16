import math
import random

import progressbar

from miller_rabin import miller_rabin
from util import pad, unpad


class RSA:
    def __init__(self, block_size: int):
        bitlen = ((block_size + 1) * 8) // 2
        p, q = RSA._large_prime(bitlen), RSA._large_prime(bitlen)
        pub, priv = RSA._keygen(p, q)

        self._n, self._e = pub
        _, self._d = priv

        self._d_p = self._d % (p - 1)
        self._d_q = self._d % (q - 1)
        self._block_size = block_size
        self.oblock_size = block_size + 4
        self._inv_q = RSA._inverse(q, p)
        self._p = p
        self._q = q

    @staticmethod
    def _large_prime(bits: int):
        times = int(1000 * (math.log(bits, 2) + 1))
        for _ in range(times):
            n = random.randrange(2 ** (bits - 1), 2 ** bits)
            if miller_rabin(n):
                return n
        raise Exception(f'failed to generate prime number of {bits} bit length in {times} tries')

    @staticmethod
    def _inverse(a, n):
        t = 0
        newt = 1
        r = n
        newr = a

        while not newr == 0:
            quotient = r // newr
            t, newt = newt, t - quotient * newt
            r, newr = newr, r - quotient * newr

        if t < 0:
            t = t + n
        return t

    @staticmethod
    def _gcd(a, b):
        while b != 0:
            a, b = b, a % b
        return a

    @staticmethod
    def _keygen(p, q):
        n = p * q
        phi = (p - 1) * (q - 1)

        e = random.randint(2, phi - 1)
        while not RSA._gcd(phi, e) == 1:
            e = random.randint(2, phi - 1)

        d = RSA._inverse(e, phi)
        return (n, e), (n, d)

    def encrypt_block(self, block: bytes):
        m = int.from_bytes(block, "little")
        assert m < self._n

        c = int(pow(m, self._e, self._n))

        return c.to_bytes(self.oblock_size, "little")

    def decrypt_block(self, block: bytes):
        c = int.from_bytes(block, "little")

        m1 = pow(c, self._d_p, self._p)
        m2 = pow(c, self._d_q, self._q)

        h = (self._inv_q * (m1 - m2)) % self._p
        m = (m2 + h * self._q) % self._n

        return m.to_bytes(self._block_size, "little")

    def encrypt(self, m: bytes):
        plaintext = pad(m, self._block_size)

        assert len(plaintext) % self._block_size == 0
        blocks = []
        for i in progressbar.progressbar(range(0, len(plaintext), self._block_size)):
            plaintext_block = plaintext[i:i + self._block_size]
            block = self.encrypt_block(plaintext_block)
            blocks.append(block)

        return b"".join(blocks)

    def decrypt(self, c: bytes):
        blocks = []
        for i in progressbar.progressbar(range(0, len(c), self.oblock_size)):
            ciphertext_block = c[i:i + self.oblock_size]
            block = self.decrypt_block(ciphertext_block)
            blocks.append(block)

        return unpad(b"".join(blocks))
