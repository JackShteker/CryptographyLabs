import os
import random
import time

from progressbar import progressbar

from RSA import RSA
from OAEP import RSA_OAEP
from miller_rabin import miller_rabin

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
    # rsa = RSA(64)
    # oaep = RSA_OAEP()
    # runMode(rsa, inp)
    # runMode(oaep, inp)
    t1 = time.time()
    for _ in progressbar(range(100)):
        miller_rabin(2074722246773485207821695222107608587480996474721117292752992589912196684750549658310084416732550077)
    t2 = time.time()

    print((t2 - t1) / 100)
