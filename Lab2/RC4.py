from progressbar import progressbar


class RC4:
    def __init__(self, key):
        self.S = self.initialize_S(key)
        self.i = 0
        self.j = 0

    @staticmethod
    def initialize_S(key):
        S = bytearray(range(256))
        j = 0

        for i in range(256):
            j = (j + S[i] + key[i % len(key)]) % 256
            S[i], S[j] = S[j], S[i]

        return S

    def generate_next(self):
        self.i = (self.i + 1) % 256
        self.j = (self.j + self.S[self.i]) % 256
        self.S[self.i], self.S[self.j] = self.S[self.j], self.S[self.i]

        return self.S[(self.S[self.i] + self.S[self.j]) % 256]

    def encrypt(self, plaintext: bytes) -> bytes:
        return bytes((b ^ self.generate_next() for b in progressbar(plaintext)))

    def decrypt(self, plaintext: bytes) -> bytes:
        return bytes((b ^ self.generate_next() for b in progressbar(plaintext)))