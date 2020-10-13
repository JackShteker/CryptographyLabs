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
        dw = eq_rev_key_expansion(key, self.N_k, self.N_r)

        if mode is not None:
            assert mode in self.encrypt_modes
            return self.decrypt_modes[mode](self, ciphertext, self.iv, dw)

        return self._decrypt_cbc(ciphertext, self.iv, dw)

    def _encrypt_ecb(self, plaintext, iv, expanded_key):
        plaintext = pad(plaintext, 16)

        blocks = []
        assert len(plaintext) % 16 == 0
        print("AES: Starting encrypting")
        time.sleep(0.1)
        for i in progressbar.progressbar(range(0, len(plaintext), 16)):
            plaintext_block = plaintext[i:i + 16]
            block = self._cipher(bytesToWordArray(plaintext_block), expanded_key)
            blocks.append(block)
        return b"".join(blocks)

    def _decrypt_ecb(self, ciphertext, iv, inv_expanded_key):
        blocks = []
        print("AES: Starting decrypting")
        time.sleep(0.1)
        for i in progressbar.progressbar(range(0, len(ciphertext), 16)):
            ciphertext_block = ciphertext[i:i + 16]
            blocks.append(wordArrayToByteArray(
                self._decipher(bytesToWordArray(ciphertext_block), inv_expanded_key)))

        return unpad(b''.join(blocks))

    encrypt_modes = {"ecb": _encrypt_ecb, "cbc": AES._encrypt_cbc}
    decrypt_modes = {"ecb": _decrypt_ecb, "cbc": AES._decrypt_cbc}




