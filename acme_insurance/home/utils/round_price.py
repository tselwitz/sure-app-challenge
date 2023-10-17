from math import trunc


def truncate_decimal(x, places=2):
    return trunc(x * (10**places)) / 10**places
