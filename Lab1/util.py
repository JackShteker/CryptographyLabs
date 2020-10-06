import progressbar


def printBytes(s):
    for w in s:
        print(w.hex())
    print("")


def bytesToWordArray(b, rows=4):
    return list(bytearray(b[i:i + rows]) for i in range(0, len(b), rows))


def bytesToString(b):
    b_hex = b.hex()
    return " ".join(b_hex[i:i + 2] for i in range(0, len(b_hex), 2))


def bytesToStringDense(b):
    return b.hex()


def wordArrayToByteArray(w):
    return b''.join(w)


def strToByteArray(s):
    s_bytes = [int(b, 16) for b in s.split(" ")]

    return bytearray(s_bytes)


def strToByteArrayDense(s):
    s_bytes = [int(s[i:i + 2], 16) for i in range(0, len(s), 2)]

    return bytearray(s_bytes)


def strToWordArray(s):
    s_bytes = strToByteArray(s)
    assert len(s_bytes) == 16 or len(s_bytes) == 24 or len(s_bytes) == 32

    return [(s_bytes[i * 4:(i + 1) * 4]) for i in range(len(s_bytes) // 4)]


def strToWordArrayDense(s, rows=4):
    s_bytes = strToByteArrayDense(s)
    assert len(s_bytes) == 16 or len(s_bytes) == 24 or len(s_bytes) == 32

    return [(s_bytes[i * rows:(i + 1) * rows]) for i in range(len(s_bytes) // rows)]


def wordArrayToStr(w):
    return "".join(col.hex() for col in w)


def pad(data_to_pad, block_size):
    padding_len = block_size - len(data_to_pad) % block_size

    p = bytearray([padding_len]) * padding_len
    return data_to_pad + p


def unpad(data_to_unpad):
    padding_len = data_to_unpad[-1]
    return data_to_unpad[:-padding_len]


def word_xor(w1, w2):
    return bytes(b1 ^ b2 for (b1, b2) in zip(w1, w2))
