import os

from AES import AES

BYTES_IN_GIGABYTE = 10 ** 9

if __name__ == '__main__':
    print(BYTES_IN_GIGABYTE)
    inp = os.urandom(BYTES_IN_GIGABYTE)
    print(len(inp))

    aes = AES(4, "00 01 02 03 04 05 06 07 08 09 0a 0b 0c 0d 0e 0f")
    key = os.urandom(16).hex()

    ciphertext = aes.encrypt(inp, key, "bytes")

    deciphered = aes.decrypt(ciphertext, key, "bytes")
    assert deciphered == inp
