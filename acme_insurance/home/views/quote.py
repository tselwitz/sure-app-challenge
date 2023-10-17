from typing import Any
from django import http
from django.http import HttpResponse, HttpRequest
from home.models.quote import Quote
from home.utils.api_crud import API_CRUD
from home.models.base_coverage import Base_Coverage
from home.models.additional_costs import Additional_Costs
from home.models.state import State

from home.utils.round_price import truncate_decimal
from django.http import JsonResponse, HttpResponseBadRequest
from functools import reduce
from uuid import uuid4
from decimal import Decimal


class Quote_View(API_CRUD):
    def __init__(self, *args, **kwargs):
        return super().__init__(Quote, *args, **kwargs)

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if request.method == "GET" and request.path.split("/")[-2] == "rater":
            return self.rater(request, *args, **kwargs)
        return super().dispatch(request, *args, **kwargs)

    def calculate_price(
        self,
        coverage: float,
        add_costs: list,
        mult_costs: list,
        tax_multiplier: float,
    ):
        coverage = Decimal(str(coverage))
        tax_multiplier = Decimal(str(tax_multiplier))
        add_costs = [Decimal(str(i)) for i in add_costs]
        mult_costs = [Decimal(str(i)) for i in mult_costs]

        subtotal = (coverage + sum(add_costs)) * reduce(lambda x, y: x * y, mult_costs)
        taxes = subtotal * tax_multiplier
        total = subtotal + (subtotal * tax_multiplier)
        return (
            float(subtotal),
            truncate_decimal(float(taxes)),
            truncate_decimal(float(total)),
        )

    def post(self, request):
        body = request.body_json
        if "coverage" not in body.keys():
            return HttpResponseBadRequest(
                "Invalid JSON request body: missing coverage", status=400
            )
        coverage = Base_Coverage.objects.filter(
            base_coverage_type=body["coverage"]
        ).first()

        # Costs which must be added to the total
        add_costs = [0]
        # Costs which be multiplied into the total. Excludes tax
        mult_costs = [1]
        if "has_pet" not in body.keys():
            body["has_pet"] = False
        if body["has_pet"] == True:
            pet_cost = Additional_Costs.objects.filter(description="Pet Fee").first()
            add_costs.append(pet_cost.price)
        if "state" not in body.keys():
            return HttpResponseBadRequest(
                "Invalid JSON request body: missing state", status=400
            )
        state = State.objects.filter(state=body["state"]).first()

        if "has_flood_coverage" not in body.keys():
            body["has_flood_coverage"] = False
        if body["has_flood_coverage"] == True:
            # Get flood cost for their state
            mult_costs.append(state.flood_multiplier)

        subtotal, taxes, total = self.calculate_price(
            coverage.price, add_costs, mult_costs, state.tax_multiplier
        )
        try:
            quote, created = Quote.objects.update_or_create(
                id=body["id"] if "id" in body.keys() else None,
                defaults={
                    "id": body["id"] if "id" in body.keys() else uuid4(),
                    "name": body["name"] if "name" in body.keys() else "",
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
        except (AttributeError, KeyError):
            return JsonResponse("Invalid JSON request body", status=400)
        return JsonResponse(
            quote.pretty_print(),
            safe=False,
        )

    def rater(self, request, *args, **kwargs):
        if "id" not in request.GET:
            return HttpResponseBadRequest(
                "Invalid query params. Requires 'id'", status=400
            )
        id = request.GET.get("id")
        quote = Quote.objects.filter(id=id).first()
        return JsonResponse(quote.rater_view(), safe=False)
