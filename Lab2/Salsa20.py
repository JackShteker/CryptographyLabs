from copy import copy

from util import *
from progressbar import progressbar


class Salsa:
    def __init__(self):
        self.block = 0
        self.s = []

    @staticmethod
    def _init_state(key, nonce, block):
        return [0x61707865, word(key[:4]), word(key[4:8]), word(key[8:12]),
                word(key[12:16]), 0x3320646e, word(nonce[:4]), word(nonce[4:]),
                word(block[:4]), word(block[4:]), 0x79622d32, word(key[16:20]),
                word(key[20:24]), word(key[24:28]), word(key[28:]), 0x6b206574]

    def encrypt(self, plaintext, key, nonce):
        self.block = 0
        assert len(key) == 32
        assert len(nonce) == 8
        blocks = []
        for i in progressbar(range(0, len(plaintext), 64)):
            plaintext_block = plaintext[i:i + 64]
            self.s = Salsa._init_state(key, nonce, self.block.to_bytes(8, "little"))
            orig_s = copy(self.s)
            self.rounds()
            stream_block = Salsa.add_states(self.s, orig_s)
            block = word_xor(plaintext_block, Salsa.state_to_bytes(stream_block))
            blocks.append(block)
            self.block = (self.block + 1) % two_in_64
        return b"".join(blocks)

    def decrypt(self, ciphertext, key, nonce):
        self.block = 0
        assert len(key) == 32
        assert len(nonce) == 8
        blocks = []
        for i in progressbar(range(0, len(ciphertext), 64)):
            ciphertext_block = ciphertext[i:i + 64]
            self.s = Salsa._init_state(key, nonce, self.block.to_bytes(8, "little"))
            orig_s = copy(self.s)
            self.rounds()
            stream_block = Salsa.add_states(self.s, orig_s)
            block = word_xor(ciphertext_block, Salsa.state_to_bytes(stream_block))
            blocks.append(block)
            self.block = (self.block + 1) % two_in_64
        return b"".join(blocks)

    @staticmethod
    def state_to_bytes(s):
        return b"".join((w.to_bytes(4, "little") for w in s))

    @staticmethod
    def add_states(s1, s2):
        return [(w1 + w2) & word_mask for w1, w2 in zip(s1, s2)]

    def rounds(self):
        for i in range(20):
            self._round(i % 2 == 1)

    def _qr(self, a, b, c, d):
        self.s[b] = self.s[b] ^ Salsa._rotate((self.s[a] + self.s[d]) & word_mask, 7)
        self.s[c] = self.s[c] ^ Salsa._rotate((self.s[b] + self.s[a]) & word_mask, 9)
        self.s[d] = self.s[d] ^ Salsa._rotate((self.s[c] + self.s[b]) & word_mask, 13)
        self.s[a] = self.s[a] ^ Salsa._rotate((self.s[d] + self.s[c]) & word_mask, 18)

        self.s = [self.s[0], self.s[4], self.s[8], self.s[12],
                  self.s[1], self.s[5], self.s[9], self.s[13],
                  self.s[2], self.s[6], self.s[10], self.s[14],
                  self.s[3], self.s[7], self.s[11], self.s[15]]

    def _round(self, odd: bool):
        if odd:
            self._qr(0, 4, 8, 12)
            self._qr(5, 9, 13, 1)
            self._qr(10, 14, 2, 6)
            self._qr(15, 3, 7, 11)
        else:
            self._qr(0, 1, 2, 3)
            self._qr(5, 6, 7, 4)
            self._qr(10, 11, 8, 9)
            self._qr(15, 12, 13, 14)

    @staticmethod
    def _rotate(w, r):
        return ((w << r) & word_mask) | (w >> (32 - r))
