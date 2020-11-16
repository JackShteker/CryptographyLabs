import random


def miller_rabin(n, k=1000):
    if n == 1 or n % 2 == 0:
        return False
    if n == 2 or n == 3:
        return True

    m = (n - 1) // 2
    t = 1

    while m % 2 == 0:
        m = m // 2
        t += 1

    for _ in range(k):
        a = random.randint(2, n - 1)
        x = pow(a, m, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(t - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True
