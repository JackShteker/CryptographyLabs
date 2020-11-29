def l(a: int):
    return a.bit_length()


def mod(a: int, b: int):
    if l(a) < l(b):
        return a
    if l(a) == l(b):
        return a if a < b else a ^ b

    d_l = l(a) - l(b)
    while d_l >= 0:
        d = b << d_l

        a ^= d

        d_l = l(a) - l(b)

    return a


def mult(a: int, b: int, f: int):
    r = 0
    while b > 0:
        if b & 1 == 1:
            r ^= a
            r = mod(r, f)
        a <<= 1
        b >>= 1
    return r

def pow(a:int, p:int, f:int) -> int:
    q = 1
    while p > 0:
        if p & 1 == 1:
            q = mult(q, a, f)
        a = mult(a, a, f)
        p >>= 1

    return q


def raw_mult(a: int, b: int):
    r = 0
    while b > 0:
        if b & 1 == 1:
            r ^= a
        a <<= 1
        b >>= 1
    return r


def square(a: int, f: int):
    return mult(a, a, f)


def add(a: int, b: int):
    return a ^ b

def inv(c: int, f: int):
    a = 1
    d = f
    u = 0
    v = c

    while v > 0:
        q, r = div_mod(d, v)
        w = add(a, raw_mult(u, q))
        a = u
        d = v
        u = w
        v = r

    q, r = div_mod(add(d, raw_mult(f, a)), c)
    # print(mult(q, c, f))
    # print(v)
    assert r == 0
    return q


def div_mod(a: int, b: int):
    assert l(a) >= l(b)
    # raise NotImplementedError
    r = 0

    d_l = l(a) - l(b)
    while d_l >= 0:
        d = b << d_l
        r |= 1 << d_l

        a ^= d

        d_l = l(a) - l(b)

    return r, a

def frac(a, b, f):
    return mult(a, inv(b, f), f)

def square(a, f):
    return mult(a, a, f)
