from django.test import TestCase
from home.models.quote import Quote
from home.models.state import State
from home.models.base_coverage import Base_Coverage
from home.models.additional_costs import Additional_Costs


class QuoteModelTest(TestCase):
    def setUp(self):
        self.base_coverage = Base_Coverage.objects.create(
            base_coverage_type="Basic", price=20.0
        )
        self.state = State.objects.create(
            state="California", tax_multiplier=1.01, flood_multiplier=1.02
        )
        self.additional_cost1 = Additional_Costs.objects.create(
            description="Pet Fee", price=20.0
        )
        self.additional_cost2 = Additional_Costs.objects.create(
            description="Additional Fee", price=10.0
        )

        self.quote = Quote.objects.create(
            name="Test User",
            has_pet=True,
            has_flood_coverage=False,
            coverage=self.base_coverage,
            coverage_state=self.state,
            subtotal=50.0,
            taxes=5.0,
            total_price=55.0,
        )
        self.quote.additional_costs.set([self.additional_cost1])

    def test_creation(self):
        self.assertEqual(Quote.objects.count(), 1)
        self.assertEqual(self.quote.name, "Test User")

    def test_default_values(self):
        self.assertFalse(Quote().has_pet)
        self.assertFalse(Quote().has_flood_coverage)

    def test_relationships(self):
        self.assertEqual(self.quote.coverage.base_coverage_type, "Basic")
        self.assertEqual(self.quote.coverage_state.state, "California")
        self.assertEqual(
            list(self.quote.additional_costs.all()), [self.additional_cost1]
        )

    def test_add_additional_costs(self):
        self.quote.additional_costs.add(self.additional_cost2)
        self.assertIn(self.additional_cost2, self.quote.additional_costs.all())

    def test_remove_additional_costs(self):
        self.quote.additional_costs.remove(self.additional_cost1)
        self.assertNotIn(self.additional_cost1, self.quote.additional_costs.all())

    def tearDown(self):
        self.base_coverage.delete()
        self.state.delete()
        self.additional_cost1.delete()
        self.additional_cost2.delete()
        self.quote.delete()
