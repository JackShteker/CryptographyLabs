import os

from RSA import RSA
from OAEP import RSA_OAEP

BYTES_IN_KILOBYTE = 10 ** 3
BYTES_IN_MEGABYTE = 10 ** 6
BYTES_IN_GIGABYTE = 10 ** 9


def runMode(mode, msg):
    c = mode.encrypt(msg)
    m = mode.decrypt(c)
    assert m.hex() == msg.hex()


if __name__ == "__main__":
    inp = os.urandom(10 * BYTES_IN_MEGABYTE)
    # inp = os.urandom(BYTES_IN_KILOBYTE)
    rsa = RSA(64)
    oaep = RSA_OAEP()
    # runMode(rsa, inp)
    runMode(oaep, inp)
