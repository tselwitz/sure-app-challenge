from home.models.quote import Quote
from home.utils.api_crud import API_CRUD
from home.models.base_coverage import Base_Coverage
from home.models.additional_costs import Additional_Costs
from home.models.state import State
from home.utils.round_price import round_price
from django.http import JsonResponse
from functools import reduce
from uuid import uuid4


class Quote_View(API_CRUD):
    def __init__(self, *args, **kwargs):
        return super().__init__(Quote, *args, **kwargs)

    def calculate_price(
        self,
        coverage: float,
        add_costs: list,
        mult_costs: list,
        tax_multiplier: float,
    ):
        mult_costs = [i for i in mult_costs]
        add_costs = [i for i in add_costs]
        coverage = coverage
        tax_multiplier = tax_multiplier

        subtotal = (coverage + sum(add_costs)) * reduce(lambda x, y: x * y, mult_costs)
        taxes = subtotal * (tax_multiplier - 1)
        total = subtotal * tax_multiplier
        return round_price(subtotal), round_price(taxes), round_price(total)

    def post(self, request):
        body = request.body_json
        coverage = Base_Coverage.objects.filter(
            base_coverage_type=body["coverage"]
        ).first()

        # Costs which must be added to the total
        add_costs = [0]
        # Costs which be multiplied into the total. Excludes tax
        mult_costs = [1]
        if body["has_pet"] == True:
            pet_cost = Additional_Costs.objects.filter(description="Pet Fee").first()
            add_costs.append(pet_cost.price)

        state = State.objects.filter(state=body["state"]).first()

        if body["has_flood_coverage"] == True:
            # Get flood cost for their state
            mult_costs.append(state.flood_multiplier)

        subtotal, taxes, total = self.calculate_price(
            coverage.price, add_costs, mult_costs, state.tax_multiplier
        )
        quote, created = Quote.objects.update_or_create(
            id=body["id"],
            defaults={
                "id": uuid4(),
                "name": body["name"],
                "has_pet": body["has_pet"],
                "has_flood_coverage": body["has_flood_coverage"],
                "subtotal": subtotal,
                "taxes": taxes,
                "total_price": total,
                "coverage_id": coverage.id,
                "coverage_state_id": state.id,
            },
        )
        if body["has_pet"] == True:
            quote.additional_costs.add(pet_cost.id)
        return JsonResponse(
            quote.pretty_print(),
            safe=False,
        )
