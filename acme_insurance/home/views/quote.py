from home.models.quote import Quote
from home.utils.api_crud import API_CRUD
from home.models.base_coverage import Base_Coverage
from home.models.additional_costs import Additional_Costs
from home.models.state import State
from django.http import JsonResponse
import json


class Quote_View(API_CRUD):
    def __init__(self, *args, **kwargs):
        return super().__init__(Quote, *args, **kwargs)

    def calculate_price(
        coverage: float, pet_cost: float, flood_mult: float, tax_multiplier: float
    ):
        subtotal = (coverage + pet_cost) * flood_mult
        taxes = subtotal * (1 - tax_multiplier)
        total = subtotal * tax_multiplier
        return subtotal, taxes, total

    def post(self, request):
        body = request.body_json
        print(body)
        coverage = Base_Coverage.objects.filter(
            base_coverage_type=body["coverage"]
        ).first()
        additional_costs_ids = []
        if body["has_pet"] == True:
            pet_cost = Additional_Costs.objects.filter(description="Pet Fee").first()
            additional_costs_ids.append(pet_cost.id)
        else:
            pet_cost = 0
        state = State.objects.filter(name="State").first()
        if self.has_flood_coverage == True:
            # Get flood cost for their state
            flood_mult = state.flood_multiplier
        else:
            flood_mult = 1
        subtotal, taxes, total = self.calculate_price(
            coverage, pet_cost, flood_mult, state.tax_multiplier
        )
        quote, created = Quote.objects.create_or_update(
            name=body["name"],
            has_pet=body["has_pet"],
            has_flood_coverage=body["has_flood_coverage"],
            coverage=coverage.id,
            coverage_state=state.id,
            additional_costs=additional_costs_ids,
            subtotal=subtotal,
            taxes=taxes,
            total=total,
        )
        return JsonResponse(quote.get_dict(), safe=False)
