import math 

def sum(m, n):
    if n > 0:
        for i in range(n):
            m += 1
    else:
        for i in range(-n):
            m -= 1
    return m

def divide(m, n):
    result = 0
    negativeResult = False
    if n == 0:
        raise ZeroDivisionError
    else:
        negativeResult = m > 0 and n < 0 or m < 0 and n > 0
        n = abs(n)
        m = abs(m)

        while (m - n >= 0):
            m -= n
            result += 1

    return -result if negativeResult else result
