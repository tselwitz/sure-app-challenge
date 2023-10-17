from django.test import TestCase, RequestFactory
from home.views.quote import Quote_View
from home.models.quote import Quote
from home.models.base_coverage import Base_Coverage
from home.models.additional_costs import Additional_Costs
from home.models.state import State
import json


class QuoteViewTest(TestCase):
    def setUp(self):
        # Create necessary test data
        Base_Coverage.objects.create(base_coverage_type="Basic", price=20.0)
        Base_Coverage.objects.create(base_coverage_type="Premium", price=40.0)
        Additional_Costs.objects.create(description="Pet Fee", price=20.0)
        texas = State.objects.create(
            state="Texas", tax_multiplier=1.005, flood_multiplier=1.5
        )
        State.objects.create(
            state="California", tax_multiplier=1.01, flood_multiplier=1.02
        )
        State.objects.create(
            state="New York", tax_multiplier=1.02, flood_multiplier=1.1
        )
        # Set up request factory for mock requests
        self.factory = RequestFactory()

    def test_case_1(self):
        self.post_quote_test("Basic", "California", True, True, 40.8, 0.4, 41.2)

    def test_case_2(self):
        self.post_quote_test("Premium", "California", True, True, 61.20, 0.61, 61.81)

    def test_case_3(self):
        self.post_quote_test("Premium", "New York", True, False, 60, 1.20, 61.20)

    def test_case_4(self):
        self.post_quote_test("Basic", "Texas", False, True, 30, 0.15, 30.15)

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
        self.assertEqual(response_data["subtotal"], subtotal)
        self.assertEqual(response_data["taxes"], taxes)
        self.assertEqual(response_data["total_price"], total_price)
