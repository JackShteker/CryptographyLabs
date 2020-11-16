import math
import os
import random
import progressbar

from RSA import RSA
from SHA256 import SHA256
from util import word_xor, pad, unpad


class RSA_OAEP:
    def __init__(self, n=128):
        self._n = n
        self._k0 = 4
        self._k1 = 4
        self._block_size = self._n - self._k0 - self._k1

        self.hash = SHA256()
        self.rsa = RSA(self._n)

    def _pad(self, m):
        return b"".join((m, int(0).to_bytes(self._k1, "little")))

    def _G(self, r):
        return self.hash.hash(r)[:self._n - self._k0]

    def _H(self, m_pad):
        return self.hash.hash(m_pad)[:self._k0]

    def _encrypt_block(self, m: bytes):
        assert len(m) == self._block_size

        pad_m = self._pad(m)

        r = os.urandom(self._k0)
        r_hash = self._G(r)
        X = word_xor(r_hash, pad_m)

        X_hash = self._H(X)
        Y = word_xor(r, X_hash)


        XY = b"".join((X, Y))
        return self.rsa.encrypt_block(XY)

    def _decrypt_block(self, c: bytes):
        # assert len(c) == self._n

        XY = self.rsa.decrypt_block(c)
        X, Y = XY[:(self._n - self._k0)], XY[(self._n - self._k0):]

        X_hash = self._H(X)
        r = word_xor(Y, X_hash)

        r_hash = self._G(r)
        pad_m = word_xor(X, r_hash)

        return pad_m[:self._block_size]

    def encrypt(self, m):
        plaintext = pad(m, self._block_size)
        # plaintext = m

        assert len(plaintext) % self._block_size == 0
        blocks = []
        for i in progressbar.progressbar(range(0, len(plaintext), self._block_size)):
            plaintext_block = plaintext[i:i + self._block_size]
            block = self._encrypt_block(plaintext_block)
            blocks.append(block)

        return b"".join(blocks)

    def decrypt(self, c: bytes):
        blocks = []
        for i in progressbar.progressbar(range(0, len(c), self.rsa.oblock_size)):
            ciphertext_block = c[i:i + self.rsa.oblock_size]
            block = self._decrypt_block(ciphertext_block)
            blocks.append(block)

        return unpad(b"".join(blocks))
        # return b"".join(blocks)




