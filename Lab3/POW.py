import os
from Kupyna import Kupyna
from SHA256 import SHA256
from timeit import default_timer as timer

BYTES_IN_KILOBYTE = 10 ** 3
BYTES_IN_MEGABYTE = 10 ** 6
BYTES_IN_GIGABYTE = 10 ** 9


def check10(hash):
    if hash[0] == 0 and hash[1] & 0b00111111 == hash[1]:
        return True
    return False


def check12(hash):
    if hash[0] == 0 and hash[1] & 0b00001111 == hash[1]:
        return True
    return False


def check16(hash):
    if hash[0] == 0 and hash[1] == 0:
        return True
    return False


def check20(hash):
    if hash[0] == 0 and hash[1] == 0 and hash[2] & 0b00001111 == hash[2]:
        return True
    return False


def runPow(hasher, msg: bytes, check_func):
    res_hash = hasher.hash(msg)
    counter = 0
    len_counter = 8
    max_counter = 2 ** (len_counter * 8) - 1
    while not check_func(res_hash):
        counter += 1
        cmsg = msg + counter.to_bytes(len_counter, "big")
        res_hash = hasher.hash(cmsg)
        if counter == max_counter:
            len_counter += 8
            max_counter = 2 ** (len_counter * 8) - 1
    return res_hash


def runKupyna(msg, check_func):
    k = Kupyna(256)
    return runPow(k, msg, check_func)


def runSHA256(msg, check_func):
    sha = SHA256()
    return runPow(sha, msg, check_func)


if __name__ == "__main__":
    # start = timer()
    # print(runSHA256(b'\x00\x01\x02\x03', check16).hex())
    # end = timer()
    # print("Run SHA256 in {:.2f} seconds".format(end-start))
    s = 0
    times = 10
    hasher = Kupyna(256)
    for i in range(times):
        msg = os.urandom(64)
        start = timer()
        h = runPow(hasher, msg, check16)
        end = timer()
        print(h.hex())
        print("Ran hash in {:.2f} seconds".format(end - start))
        s += end - start
    print("Average over {}: {:.2f} seconds".format(times, s / times))
