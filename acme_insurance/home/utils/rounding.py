from decimal import Decimal, ROUND_DOWN


def limit_decimal_places(value, places=2):
    """Limit the number of decimal places of a Decimal."""
    return value.quantize(Decimal("0." + "0" * places), rounding=ROUND_DOWN)
