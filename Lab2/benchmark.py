import os

from AES_modes import AESmodes
from RC4 import RC4
from Salsa20 import Salsa

BYTES_IN_KILOBYTE = 10 ** 3
BYTES_IN_MEGABYTE = 10 ** 6
BYTES_IN_GIGABYTE = 10 ** 9


def runSalsa(msg, key):
    salsa = Salsa()
    nonce = b"\x00\x01\x02\x03\x04\x05\x06\x07"
    ciphertext = salsa.encrypt(msg, key, nonce)

    decrypted = salsa.decrypt(ciphertext, key, nonce)
    assert msg == decrypted


def runRC4(msg, key):
    rc4 = RC4(key)
    ciphertext = rc4.encrypt(msg)

    rc4 = RC4(key)
    decrypted = rc4.decrypt(ciphertext)
    assert msg == decrypted


def runMode(msg, key, mode):
    aes = AESmodes(4, "00 01 02 03 04 05 06 07 08 09 0a 0b 0c 0d 0e 0f")
    ciphertext = aes.encrypt(msg, key, mode)

    aes = AESmodes(4, "00 01 02 03 04 05 06 07 08 09 0a 0b 0c 0d 0e 0f")
    decrypted = aes.decrypt(ciphertext, key, mode)
    assert msg == decrypted, msg.hex() + "\n" + decrypted.hex()

if __name__ == "__main__":
    # inp = os.urandom(BYTES_IN_MEGABYTE  )
    inp = os.urandom(BYTES_IN_GIGABYTE  )
    print(str(type(inp)))
    AESkey = b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0A\x0B\x0C\x0D\x0E\x0F'
    RC4key = b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0A\x0B\x0C\x0D\x0E\x0F'
    salsaKey = b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0A\x0B\x0C\x0D\x0E\x0F'\
               b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0A\x0B\x0C\x0D\x0E\x0F'
    # runMode(inp, AESkey, "cbc")
    # runMode(inp, AESkey, "ecb")
    # runMode(inp, AESkey, "ofb")
    # runMode(inp, AESkey, "ctr")
    runMode(inp, AESkey, "cfb")
    # runSalsa(inp, salsaKey)
    # runRC4(inp, RC4key)