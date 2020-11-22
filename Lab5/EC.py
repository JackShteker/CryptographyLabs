from GF import add, mult, square, frac

class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __str__(self):
        return f"X: {self.x}\nY: {self.y}"

    def __eq__(self, other):
        assert type(other) == type(self)
        return self.x == other.x and self.y == other.y


Zero_point = Point(0, 0)
# Pol =


class Curve:
    def __init__(self, a, b, f):
        self.a = a
        self.b = b
        self.f = f

    def add(self, p: Point, q: Point):
        if p == Zero_point:
            return q
        if q == Zero_point:
             return p
        if q.x == p.x and q.y == add(p.x, p.y):
            return Zero_point

        t = frac(add(p.y, q.y), add(p.x, q.x), self.f)
        x_r = add(add(add(add(square(t, self.f), t), p.x), q.x), self.a)

        y_r = add(add(mult(t, add(p.x, x_r), self.f), x_r), p.y)

        return Point(x_r, y_r)

    def mul2(self, p: Point):
        if p.x == 0:
            return Zero_point

        x_r = add(square(p.x, self.f), frac(self.b, square(p.x, self.f), self.f))

        y_r = add(add(square(p.x, self.f), mult(add(p.x, frac(p.y, p.x, self.f)), x_r, self.f)), x_r)

        return Point(x_r, y_r)

    def mul(self, k: int, p: Point):
        q = Zero_point

        while k > 0:
            if k & 1 == 1:
                q = self.add(q, p)
            p = self.mul2(p)

            k >>= 1

        return q

