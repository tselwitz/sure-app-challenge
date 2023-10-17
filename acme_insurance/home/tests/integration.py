from django.test import TestCase
from home.models.base_coverage import Base_Coverage
from home.models.additional_costs import Additional_Costs
from home.models.quote import Quote
from home.models.state import State


class IntegrationTest(TestCase):
    def setUp(self) -> None:
        State(
            **{"state": "California", "tax_multiplier": 1.01, "flood_multiplier": 1.02}
        ).save()
        State(
            **{"state": "Texas", "tax_multiplier": 1.005, "flood_multiplier": 1.5}
        ).save()
        State(
            **{"state": "New York", "tax_multiplier": 1.02, "flood_multiplier": 1.1}
        ).save()

        Additional_Costs(**{"description": "Pet Fee", "price": 20.0}).save()

        Base_Coverage(**{"base_coverage_type": "Basic", "price": 10.0}).save()
        Base_Coverage(**{"base_coverage_type": "Premium", "price": 20.0}).save()
