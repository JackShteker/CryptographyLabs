import progressbar


def printBytes(s):
    for w in s:
        print(w.hex())
    print("")


def bytesToWordArray(b):
    return list(bytearray(b[i:i + 4]) for i in range(0, len(b), 4))

def bytesToString(b):
    b_hex = b.hex()
    return " ".join(b_hex[i:i+2] for i in range(0, len(b_hex), 2))

def bytesToStringDense(b):
    return b.hex()


def wordArrayToByteArray(w):
    return b''.join(w)


def strToByteArray(s):
    s_bytes = [int(b, 16) for b in s.split(" ")]

    return bytearray(s_bytes)

def strToByteArrayDense(s):
    s_bytes = [int(s[i:i + 2], 16) for i in progressbar.progressbar(range(0, len(s), 2))]

    return bytearray(s_bytes)


def strToWordArray(s):
    s_bytes = strToByteArray(s)
    assert len(s_bytes) == 16 or len(s_bytes) == 24 or len(s_bytes) == 32

    return [(s_bytes[i * 4:(i + 1) * 4]) for i in range(len(s_bytes) // 4)]


def strToWordArrayDense(s):
    s_bytes = strToByteArrayDense(s)
    assert len(s_bytes) == 16 or len(s_bytes) == 24 or len(s_bytes) == 32

    return [(s_bytes[i * 4:(i + 1) * 4]) for i in range(len(s_bytes) // 4)]


def wordArrayToStr(w):
    return "".join(col.hex() for col in w)
