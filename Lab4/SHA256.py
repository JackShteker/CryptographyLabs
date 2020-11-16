from util import *


class SHA256:
    _K = [
        0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
        0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
        0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
        0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
        0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
        0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
        0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
        0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
    ]

    @staticmethod
    def _pad(msg):
        l = len(msg) * 8
        msg.append(0x80)
        while (len(msg) + 8) % 64 != 0:
            msg.append(0x00)

        msg += l.to_bytes(8, "big")

        assert len(msg) % 64 == 0
        return msg

    @staticmethod
    def hash(msg):
        msg = bytearray(msg)
        padded = SHA256._pad(msg)

        h0 = 0x6a09e667
        h1 = 0xbb67ae85
        h2 = 0x3c6ef372
        h3 = 0xa54ff53a
        h5 = 0x9b05688c
        h4 = 0x510e527f
        h6 = 0x1f83d9ab
        h7 = 0x5be0cd19

        for i in range(0, len(padded), 64):
            msg_block = padded[i: i + 64]
            message_schedule = []
            for t in range(0, 64):
                if t <= 15:
                    message_schedule.append(int.from_bytes(msg_block[t * 4:(t * 4) + 4], "big"))
                else:
                    term1 = SHA256._s1(message_schedule[t - 2])
                    term2 = message_schedule[t - 7]
                    term3 = SHA256._s0(message_schedule[t - 15])
                    term4 = message_schedule[t - 16]

                    schedule = ((term1 + term2 + term3 + term4) & word_mask)
                    message_schedule.append(schedule)

            assert len(message_schedule) == 64

            a = h0
            b = h1
            c = h2
            d = h3
            e = h4
            f = h5
            g = h6
            h = h7

            for t in range(64):
                t1 = ((h + SHA256._c1(e) + SHA256._ch(e, f, g) + SHA256._K[t] +
                       message_schedule[t]) & word_mask)
                t2 = (SHA256._c0(a) + SHA256._maj(a, b, c)) & word_mask

                h = g
                g = f
                f = e
                e = (d + t1) & word_mask
                d = c
                c = b
                b = a
                a = (t1 + t2) & word_mask

            h0 = (h0 + a) & word_mask
            h1 = (h1 + b) & word_mask
            h2 = (h2 + c) & word_mask
            h3 = (h3 + d) & word_mask
            h4 = (h4 + e) & word_mask
            h5 = (h5 + f) & word_mask
            h6 = (h6 + g) & word_mask
            h7 = (h7 + h) & word_mask

        return b''.join((h.to_bytes(4, "big") for h in (h0, h1, h2, h3, h4, h5, h6, h7)))

    @staticmethod
    def _s0(num: int):
        num = (SHA256._rotate_right(num, 7) ^
               SHA256._rotate_right(num, 18) ^
               (num >> 3))
        return num

    @staticmethod
    def _s1(num: int):
        num = (SHA256._rotate_right(num, 17) ^
               SHA256._rotate_right(num, 19) ^
               (num >> 10))
        return num & word_mask

    @staticmethod
    def _c0(num: int):
        num = (SHA256._rotate_right(num, 2) ^
               SHA256._rotate_right(num, 13) ^
               SHA256._rotate_right(num, 22))
        return num & word_mask

    @staticmethod
    def _c1(num: int):
        num = (SHA256._rotate_right(num, 6) ^
               SHA256._rotate_right(num, 11) ^
               SHA256._rotate_right(num, 25))
        return num & word_mask

    @staticmethod
    def _ch(x: int, y: int, z: int):
        return (x & y) ^ (~x & z)

    @staticmethod
    def _maj(x: int, y: int, z: int):
        return (x & y) ^ (x & z) ^ (y & z)

    @staticmethod
    def _rotate_right(num: int, shift: int, size: int = 32):
        return ((num >> shift) | (num << size - shift)) & word_mask
