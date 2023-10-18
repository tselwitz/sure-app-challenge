from home.models.additional_costs import Additional_Costs
from home.utils.round_price import limit_decimal_places
from decimal import Decimal
from functools import reduce


def calculate_price(
    coverage,
    add_costs,
    mult_costs,
    tax_multiplier,
):
    coverage = Decimal(str(coverage))
    tax_multiplier = Decimal(str(tax_multiplier))
    add_costs = [Decimal(str(i)) for i in add_costs]
    mult_costs = [Decimal(str(i)) for i in mult_costs]

    subtotal = (coverage + sum(add_costs)) * reduce(lambda x, y: x * y, mult_costs)
    taxes = subtotal * tax_multiplier
    total = subtotal + taxes
    return (
        limit_decimal_places(subtotal),
        limit_decimal_places(taxes),
        limit_decimal_places(total),
    )


def has_add_cost(descriptor, param, body, add_costs, add_cost_ids):
    if param not in body.keys():
        body[param] = False
    if body[param] == True:
        add_cost = Additional_Costs.objects.filter(description=descriptor).first()
        add_costs.append(add_cost.price)
        add_cost_ids.append(add_cost.id)
    return add_costs, add_cost_ids


def has_mult_cost(param, body, mult_costs, mult_cost):
    if param not in body.keys():
        body[param] = False
    if body[param] == True:
        mult_costs.append(mult_cost)
    return mult_costs


def get_required_field(body, name, baseClass, baseClassField):
    if name not in body.keys():
        raise AttributeError(f"Invalid JSON request body: missing {name}")
    return baseClass.objects.filter(**{baseClassField: body[name]}).first()
