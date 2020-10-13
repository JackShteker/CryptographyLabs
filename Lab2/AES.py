import time

import progressbar

from util import *
# from Crypto.Util.Padding import pad

s_box = (
    0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
    0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
    0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
    0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
    0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
    0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
    0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
    0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
    0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
    0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
    0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
    0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
    0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
    0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
    0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
    0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16,
)

inv_s_box = (
    0x52, 0x09, 0x6A, 0xD5, 0x30, 0x36, 0xA5, 0x38, 0xBF, 0x40, 0xA3, 0x9E, 0x81, 0xF3, 0xD7, 0xFB,
    0x7C, 0xE3, 0x39, 0x82, 0x9B, 0x2F, 0xFF, 0x87, 0x34, 0x8E, 0x43, 0x44, 0xC4, 0xDE, 0xE9, 0xCB,
    0x54, 0x7B, 0x94, 0x32, 0xA6, 0xC2, 0x23, 0x3D, 0xEE, 0x4C, 0x95, 0x0B, 0x42, 0xFA, 0xC3, 0x4E,
    0x08, 0x2E, 0xA1, 0x66, 0x28, 0xD9, 0x24, 0xB2, 0x76, 0x5B, 0xA2, 0x49, 0x6D, 0x8B, 0xD1, 0x25,
    0x72, 0xF8, 0xF6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xD4, 0xA4, 0x5C, 0xCC, 0x5D, 0x65, 0xB6, 0x92,
    0x6C, 0x70, 0x48, 0x50, 0xFD, 0xED, 0xB9, 0xDA, 0x5E, 0x15, 0x46, 0x57, 0xA7, 0x8D, 0x9D, 0x84,
    0x90, 0xD8, 0xAB, 0x00, 0x8C, 0xBC, 0xD3, 0x0A, 0xF7, 0xE4, 0x58, 0x05, 0xB8, 0xB3, 0x45, 0x06,
    0xD0, 0x2C, 0x1E, 0x8F, 0xCA, 0x3F, 0x0F, 0x02, 0xC1, 0xAF, 0xBD, 0x03, 0x01, 0x13, 0x8A, 0x6B,
    0x3A, 0x91, 0x11, 0x41, 0x4F, 0x67, 0xDC, 0xEA, 0x97, 0xF2, 0xCF, 0xCE, 0xF0, 0xB4, 0xE6, 0x73,
    0x96, 0xAC, 0x74, 0x22, 0xE7, 0xAD, 0x35, 0x85, 0xE2, 0xF9, 0x37, 0xE8, 0x1C, 0x75, 0xDF, 0x6E,
    0x47, 0xF1, 0x1A, 0x71, 0x1D, 0x29, 0xC5, 0x89, 0x6F, 0xB7, 0x62, 0x0E, 0xAA, 0x18, 0xBE, 0x1B,
    0xFC, 0x56, 0x3E, 0x4B, 0xC6, 0xD2, 0x79, 0x20, 0x9A, 0xDB, 0xC0, 0xFE, 0x78, 0xCD, 0x5A, 0xF4,
    0x1F, 0xDD, 0xA8, 0x33, 0x88, 0x07, 0xC7, 0x31, 0xB1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xEC, 0x5F,
    0x60, 0x51, 0x7F, 0xA9, 0x19, 0xB5, 0x4A, 0x0D, 0x2D, 0xE5, 0x7A, 0x9F, 0x93, 0xC9, 0x9C, 0xEF,
    0xA0, 0xE0, 0x3B, 0x4D, 0xAE, 0x2A, 0xF5, 0xB0, 0xC8, 0xEB, 0xBB, 0x3C, 0x83, 0x53, 0x99, 0x61,
    0x17, 0x2B, 0x04, 0x7E, 0xBA, 0x77, 0xD6, 0x26, 0xE1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0C, 0x7D,
)

r_con = (
    0x00, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36
)


# sub_bytes performs SubBytes() function in-place
def sub_bytes(s):
    for i in range(4):
        for j in range(4):
            s[i][j] = s_box[s[i][j]]


# inv_sub_bytes performs InvSubBytes() function in-place
def inv_sub_bytes(s):
    for i in range(4):
        for j in range(4):
            s[i][j] = inv_s_box[s[i][j]]


def shift_rows(s):
    s[0][1], s[1][1], s[2][1], s[3][1] = s[1][1], s[2][1], s[3][1], s[0][1]
    s[0][2], s[1][2], s[2][2], s[3][2] = s[2][2], s[3][2], s[0][2], s[1][2]
    s[0][3], s[1][3], s[2][3], s[3][3] = s[3][3], s[0][3], s[1][3], s[2][3]


def inv_shift_rows(s):
    s[0][1], s[1][1], s[2][1], s[3][1] = s[3][1], s[0][1], s[1][1], s[2][1]
    s[0][2], s[1][2], s[2][2], s[3][2] = s[2][2], s[3][2], s[0][2], s[1][2]
    s[0][3], s[1][3], s[2][3], s[3][3] = s[1][3], s[2][3], s[3][3], s[0][3]


def xtime(a):
    return (a << 1 ^ 0x1B) & 0xFF if a & 0x80 else a << 1


# times3 calculates a * 0x03
def times3(a):
    return xtime(a) ^ a


# mix_column multiplies polynomial a by polynomial [0x02, 0x01, 0x01, 0x03]
# a * 0x01 = a; a * 0x02 = xtime(a); a * 0x03 = times3(a) == xtime(a) ^ a
def mix_column(a):
    a[0], a[1], a[2], a[3] = xtime(a[0]) ^ times3(a[1]) ^ a[2] ^ a[3], \
                             a[0] ^ xtime(a[1]) ^ times3(a[2]) ^ a[3], \
                             a[0] ^ a[1] ^ xtime(a[2]) ^ times3(a[3]), \
                             times3(a[0]) ^ a[1] ^ a[2] ^ xtime(a[3])


# inv_mix_columns multiplies polynomial a by polynomial [0x0b, 0x0d, 0x09, 0x0e]
# or in matrix terms:
# 0E 0B 0D 09     a[0]
# 09 0E 0B 0D  *  a[1]
# 0D 09 0E 0B     a[2]
# 0B 0D 09 0E     a[3]
#
# 0E 0B 0D 09     02 03 01 01     05 00 04 00
# 09 0E 0B 0D  =  01 02 03 01  *  00 05 00 04
# 0D 09 0E 0B     01 01 02 03     04 00 05 00
# 0B 0D 09 0E     03 01 01 02     00 04 00 05
#
# a * 0x04 = xtime(xtime(a));  a * 0x05 = xtime(xtime(a)) ^ a
def inv_mix_columns(s):
    for i in range(4):
        u = xtime(xtime(s[i][0] ^ s[i][2]))
        v = xtime(xtime(s[i][1] ^ s[i][3]))
        s[i][0] ^= u
        s[i][1] ^= v
        s[i][2] ^= u
        s[i][3] ^= v

    mix_columns(s)


def mix_columns(s):
    for a in s:
        mix_column(a)


def add_round_key(s, k):
    for i in range(4):
        for j in range(4):
            s[i][j] ^= k[i][j]


# sub_word performs SubWord() function in-place
def sub_word(w):
    for i in range(4):
        w[i] = s_box[w[i]]


# rot_word performs RotWord() function in-place
def rot_word(w):
    temp = w[0]
    for i in range(3):
        w[i] = w[i + 1]
    w[3] = temp


def key_expansion(k, n_k, n_r):
    i = 0
    w = [bytes(4) for _ in range(4 * (n_r + 1))]

    while i < n_k:
        w[i] = k[i]
        i += 1

    while i < 4 * (n_r + 1):
        temp = list(w[i - 1][:])
        if i % n_k == 0:
            rot_word(temp)
            sub_word(temp)
            temp[0] = temp[0] ^ r_con[i // n_k]
        elif n_k > 6 and i % n_k == 4:
            sub_word(temp)
        temp = bytes(temp)
        w[i] = word_xor(w[i - n_k], temp)
        i += 1

    return w


def eq_rev_key_expansion(k, n_k, n_r):
    dw = key_expansion(k, n_k, n_r)
    for r in range(1, n_r):
        col = [list(c) for c in dw[r * 4:(r + 1) * 4]]
        inv_mix_columns(col)
        col = [bytes(c) for c in col]
        dw[r * 4:(r + 1) * 4] = col
    return dw


class AES:
    def __init__(self, n_k, iv):
        self.N_k = n_k
        if n_k == 4:
            self.N_r = 10
        elif n_k == 6:
            self.N_r = 12
        elif n_k == 8:
            self.N_r = 14
        else:
            raise Exception("Unexpected key length")

        if iv[2] == " ":
            iv = strToByteArray(iv)
        else:
            iv = strToByteArrayDense(iv)
        assert len(iv) == 16
        self.iv = iv

    def _cipher(self, inp, w):
        s = inp[:]
        add_round_key(s, w[:4])

        for r in range(1, self.N_r):
            sub_bytes(s)
            shift_rows(s)
            mix_columns(s)
            add_round_key(s, w[r * 4: (r + 1) * 4])

        sub_bytes(s)
        shift_rows(s)
        add_round_key(s, w[self.N_r * 4:(self.N_r + 1) * 4])
        s = wordArrayToByteArray(s)
        return s

    def _decipher(self, inp, dw):
        s = inp[:]

        add_round_key(s, dw[self.N_r * 4:(self.N_r + 1) * 4])

        for r in range(self.N_r - 1, 0, -1):
            inv_sub_bytes(s)
            inv_shift_rows(s)
            inv_mix_columns(s)
            add_round_key(s, dw[r * 4: (r + 1) * 4])

        inv_sub_bytes(s)
        inv_shift_rows(s)
        add_round_key(s, dw[0: 4])

        return s

    def _encrypt_cbc(self, plaintext, iv, expanded_key, inp_type=None):
        plaintext = pad(plaintext, 16)

        blocks = []
        previous = iv
        assert len(plaintext) % 16 == 0
        print("AES: Starting encrypting")
        time.sleep(0.1)
        for i in progressbar.progressbar(range(0, len(plaintext), 16)):
            plaintext_block = plaintext[i:i + 16]
            block = self._cipher(bytesToWordArray(word_xor(plaintext_block, previous)), expanded_key)
            blocks.append(block)
            previous = block
        if inp_type == "dense":
            return "".join(bytesToStringDense(block) for block in blocks)
        if inp_type == "bytes":
            return b''.join(blocks)
        return " ".join(bytesToString(block) for block in blocks)

    def _decrypt_cbc(self, ciphertext, iv, inv_expanded_key, inp_type=None):
        blocks = []
        previous = iv
        print("AES: Starting decrypting")
        time.sleep(0.1)
        for i in progressbar.progressbar(range(0, len(ciphertext), 16)):
            ciphertext_block = ciphertext[i:i + 16]
            blocks.append(word_xor(previous, wordArrayToByteArray(self._decipher(bytesToWordArray(ciphertext_block), inv_expanded_key))))
            previous = ciphertext_block

        if inp_type == "dense":
            return bytesToStringDense(unpad(b''.join(blocks)))
        if inp_type == "bytes":
            return unpad(b''.join(blocks))
        return bytesToString(unpad(b''.join(blocks)))

    def encrypt(self, plaintext, key, inp_type=None):
        if inp_type == "dense":
            key = strToWordArrayDense(key)
            plaintext = strToByteArrayDense(plaintext)
        elif inp_type == "bytes":
            key = strToWordArrayDense(key)
        else:
            key = strToWordArray(key)
            plaintext = strToByteArray(plaintext)
        w = key_expansion(key, self.N_k, self.N_r)
        return self._encrypt_cbc(plaintext, self.iv, w, inp_type)

    def decrypt(self, ciphertext, key, inp_type=None):
        if inp_type == "dense":
            key = strToWordArrayDense(key)
            ciphertext = strToByteArrayDense(ciphertext)
        elif inp_type == "bytes":
            key = strToWordArrayDense(key)
        else:
            key = strToWordArray(key)
            ciphertext = strToByteArray(ciphertext)
        dw = eq_rev_key_expansion(key, self.N_k, self.N_r)
        return self._decrypt_cbc(ciphertext, self.iv, dw, inp_type)


    # def cipher(self, ):
