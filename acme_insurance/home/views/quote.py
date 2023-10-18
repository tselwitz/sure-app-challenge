from typing import Any
from django.http import HttpResponse, HttpRequest
from home.utils.view_helpers import (
    calculate_price,
    get_required_field,
    has_add_cost,
    has_mult_cost,
)
from home.models.quote import Quote
from home.utils.api_crud import API_CRUD
from home.models.base_coverage import Base_Coverage
from home.models.state import State
from django.http import JsonResponse
from uuid import uuid4


class Quote_View(API_CRUD):
    def __init__(self, *args, **kwargs):
        return super().__init__(Quote, *args, **kwargs)

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if request.method == "GET" and request.path.split("/")[-2] == "rater":
            return self.rater(request, *args, **kwargs)
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        body = request.body_json
        try:
            coverage = get_required_field(
                body, "coverage", Base_Coverage, "base_coverage_type"
            )
            state = get_required_field(body, "state", State, "state")
        except AttributeError as err:
            return JsonResponse({"error": repr(err)}, status=400)
        # Costs which must be added to the total
        add_cost_ids = []
        add_costs = [0]
        # Costs which be multiplied into the total. Excludes tax
        mult_costs = [1]

        add_costs, add_cost_ids = has_add_cost(
            "Pet Fee", "has_pet", body, add_costs, add_cost_ids
        )
        mult_costs = has_mult_cost(
            "has_flood_coverage", body, mult_costs, state.flood_multiplier
        )
        subtotal, taxes, total = calculate_price(
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
            for id in add_cost_ids:
                quote.additional_costs.add(id)
        except (AttributeError, KeyError) as err:
            return JsonResponse({"error": repr(err)}, status=400)
        return JsonResponse(
            quote.pretty_print(),
            safe=False,
        )

    def rater(self, request, *args, **kwargs):
        params = {i: request.GET.get(i) for i in request.GET}
        quote = Quote.objects.filter(**params).all()
        if quote != None:
            return JsonResponse([i.rater_view() for i in quote], safe=False)
        else:
            return JsonResponse([], safe=False)
