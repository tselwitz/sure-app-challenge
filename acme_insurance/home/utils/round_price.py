import math


def round_price(x, prec=2, base=0.01):
    return round(base * round(x / base), prec)
