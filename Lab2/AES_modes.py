import time

from AES import AES, key_expansion, eq_rev_key_expansion
from util import *

class AESmodes(AES):
    def encrypt(self, plaintext, key, mode=None):
        key = bytesToWordArray(key)
        w = key_expansion(key, self.N_k, self.N_r)
        if mode is not None:
            assert mode in self.encrypt_modes
            return self.encrypt_modes[mode](self, plaintext, self.iv, w)

        return self._encrypt_cbc(plaintext, self.iv, w)

    def decrypt(self, ciphertext, key, mode=None):
        key = bytesToWordArray(key)
        if mode is not None and mode in ["ofb", "ctr", "cfb"]:
            dw = key_expansion(key, self.N_k, self.N_r)
        else:
            dw = eq_rev_key_expansion(key, self.N_k, self.N_r)

        if mode is not None:
            assert mode in self.encrypt_modes
            return self.decrypt_modes[mode](self, ciphertext, self.iv, dw)

        return self._decrypt_cbc(ciphertext, self.iv, dw)

    def _encrypt_ecb(self, plaintext, iv, expanded_key):
        plaintext = pad(plaintext, 16)

        blocks = []
        assert len(plaintext) % 16 == 0
        print("AES: Starting encryption")
        time.sleep(0.1)
        for i in progressbar.progressbar(range(0, len(plaintext), 16)):
        # for i in range(0, len(plaintext), 16):
            plaintext_block = plaintext[i:i + 16]
            block = self._cipher(bytesToWordArray(plaintext_block), expanded_key)
            blocks.append(block)
        return b"".join(blocks)

    def _decrypt_ecb(self, ciphertext, iv, inv_expanded_key):
        blocks = []
        print("AES: Starting decryption")
        time.sleep(0.1)
        # for i in range(0, len(ciphertext), 16):
        for i in progressbar.progressbar(range(0, len(ciphertext), 16)):
            ciphertext_block = ciphertext[i:i + 16]
            blocks.append(wordArrayToByteArray(
                self._decipher(bytesToWordArray(ciphertext_block), inv_expanded_key)))

        return unpad(b''.join(blocks))

    def _encrypt_cfb(self, plaintext, iv, expanded_key, s=6):
        blocks = []
        print("AES: Starting encryption")
        time.sleep(0.1)
        iv = bytearray(iv)
        for i in progressbar.progressbar(range(0, len(plaintext), s)):
        # for i in range(0, len(plaintext), s):
            plaintext_block = plaintext[i:i + s]
            y = self._cipher(bytesToWordArray(iv), expanded_key)
            c = word_xor(plaintext_block, y[:s])
            iv[:16-s], iv[-s:] = iv[s:], c
            blocks.append(c)
        return b"".join(blocks)

    def _decrypt_cfb(self, ciphertext, iv, expanded_key, s=6):
        blocks = []
        print("AES: Starting encryption")
        time.sleep(0.1)
        iv = bytearray(iv)
        for i in progressbar.progressbar(range(0, len(ciphertext), s)):
        # for i in range(0, len(ciphertext), s):
            ciphertext_block = ciphertext[i:i + s]
            y = self._cipher(bytesToWordArray(iv), expanded_key)
            iv[:16 - s], iv[-s:] = iv[s:], ciphertext_block
            blocks.append(word_xor(ciphertext_block, y[:s]))
        return b"".join(blocks)

    def _encrypt_ofb(self, plaintext, iv, expanded_key):
        blocks = []
        print("AES: Starting encryption")
        time.sleep(0.1)
        for i in progressbar.progressbar(range(0, len(plaintext), 16)):
        # for i in range(0, len(plaintext), 16):
            plaintext_block = plaintext[i:i + 16]
            iv = self._cipher(bytesToWordArray(iv), expanded_key)
            blocks.append(word_xor(plaintext_block, iv))
        return b"".join(blocks)

    def _decrypt_ofb(self, ciphertext, iv, expanded_key):
        blocks = []
        print("AES: Starting decryption")
        time.sleep(0.1)
        for i in progressbar.progressbar(range(0, len(ciphertext), 16)):
        # for i in range(0, len(ciphertext), 16):
            ciphertext_block = ciphertext[i:i + 16]
            iv = self._cipher(bytesToWordArray(iv), expanded_key)
            blocks.append(word_xor(ciphertext_block, iv))
        return b"".join(blocks)

    def _encrypt_ctr(self, plaintext, iv, expanded_key):
        blocks = []
        print("AES: Starting encryption")
        time.sleep(0.1)
        offset = int.from_bytes(iv, "little")
        for i in progressbar.progressbar(range(0, len(plaintext), 16)):
        # for i in range(0, len(plaintext), 16):
            plaintext_block = plaintext[i:i + 16]
            n = offset + (i // 16) % two_in_128
            y = self._cipher(bytesToWordArray(n.to_bytes(16, "little", signed=False)), expanded_key)
            blocks.append(word_xor(plaintext_block, y))
        return b"".join(blocks)

    def _decrypt_ctr(self, ciphertext, iv, expanded_key):
        blocks = []
        print("AES: Starting decryption")
        time.sleep(0.1)
        offset = int.from_bytes(iv, "little")
        for i in progressbar.progressbar(range(0, len(ciphertext), 16)):
        # for i in range(0, len(ciphertext), 16):
            ciphertext_block = ciphertext[i:i + 16]
            n = offset + (i // 16) % two_in_128
            y = self._cipher(bytesToWordArray(n.to_bytes(16, "little", signed=False)), expanded_key)
            blocks.append(word_xor(ciphertext_block, y))
        return b"".join(blocks)

    encrypt_modes = {"ecb": _encrypt_ecb,
                     "cbc": AES._encrypt_cbc,
                     "cfb": _encrypt_cfb,
                     "ofb": _encrypt_ofb,
                     "ctr": _encrypt_ctr,}
    decrypt_modes = {"ecb": _decrypt_ecb,
                     "cbc": AES._decrypt_cbc,
                     "cfb": _decrypt_cfb,
                     "ofb": _decrypt_ofb,
                     "ctr": _decrypt_ctr}




