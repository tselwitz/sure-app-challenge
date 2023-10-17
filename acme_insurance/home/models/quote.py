from django.db import models
from home.models.state import State
from home.models.base_coverage import Base_Coverage
from home.models.additional_costs import Additional_Costs
from uuid import uuid4
from home.utils.pretty_print import PrettyPrint


class Quote(PrettyPrint, models.Model):
    id = models.UUIDField(default=uuid4(), primary_key=True)

    name = models.CharField(max_length=100)
    has_pet = models.BooleanField(default=False)
    has_flood_coverage = models.BooleanField(default=False)

    # Foreign Keys
    coverage = models.ForeignKey(
        Base_Coverage, on_delete=models.CASCADE, related_name="coverage_obj"
    )
    coverage_state = models.ForeignKey(
        State, on_delete=models.CASCADE, related_name="coverage_state_obj"
    )
    additional_costs = models.ManyToManyField(Additional_Costs)

    # Calculated Fields
    subtotal = models.FloatField()
    taxes = models.FloatField()
    total_price = models.FloatField()
