from django.test import TestCase, RequestFactory
from home.views.quote import Quote_View
from home.models.quote import Quote
from home.models.base_coverage import Base_Coverage
from home.models.additional_costs import Additional_Costs
from home.models.state import State
import json
from decimal import Decimal
from home.utils.rounding import limit_decimal_places


class QuoteViewTest(TestCase):
    def setUp(self):
        # Create necessary test data
        Base_Coverage.objects.create(base_coverage_type="Basic", price=20.0)
        Base_Coverage.objects.create(base_coverage_type="Premium", price=40.0)
        Additional_Costs.objects.create(description="Pet Fee", price=20.0)
        State.objects.create(state="Texas", tax_multiplier=0.005, flood_multiplier=1.5)
        State.objects.create(
            state="California", tax_multiplier=0.01, flood_multiplier=1.02
        )
        State.objects.create(
            state="New York", tax_multiplier=0.02, flood_multiplier=1.1
        )
        # Set up request factory for mock requests
        self.factory = RequestFactory()

    def test_case_1(self):
        self.post_quote_test("Basic", "California", True, True, 40.8, 0.4, 41.2)

    def test_case_2(self):
        self.post_quote_test("Premium", "California", True, True, 61.20, 0.61, 61.81)

    def test_case_3(self):
        self.post_quote_test("Premium", "New York", True, False, 60.0, 1.20, 61.20)

    def test_case_4(self):
        self.post_quote_test("Basic", "Texas", False, True, 30.0, 0.15, 30.15)

    def post_quote_test(
        self, coverage, state, pet, flood, subtotal, taxes, total_price
    ):
        body = {
            "id": "12345678-1234-5678-1234-567812345678",
            "name": "Test User",
            "coverage": coverage,
            "state": state,
            "has_pet": pet,
            "has_flood_coverage": flood,
        }

        request = self.factory.post(
            "/home/quote/", json.dumps(body), content_type="application/json"
        )
        request.body_json = body
        response = Quote_View().post(request)

        # Assert that the Quote was created properly
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertEqual(
            Decimal(response_data["subtotal"]),
            limit_decimal_places(Decimal(str(subtotal))),
        )
        self.assertEqual(
            Decimal(response_data["taxes"]), limit_decimal_places(Decimal(str(taxes)))
        )
        self.assertEqual(
            Decimal(response_data["total_price"]),
            limit_decimal_places(Decimal(str(total_price))),
        )
