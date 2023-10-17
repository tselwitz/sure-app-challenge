from math import floor


def round_price(x, prec=2, base=0.001):
    return round(base * round(x / base), prec)


def floor_price(x, base=0.01):
    return floor(x / base) * base
