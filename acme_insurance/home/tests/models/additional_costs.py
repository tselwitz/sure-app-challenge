from django.test import TestCase
from home.models.additional_costs import Additional_Costs
import uuid


class AdditionalCostsModelTest(TestCase):
    def setUp(self):
        self.cost1 = Additional_Costs.objects.create(description="Pet Fee", price=20.0)
        self.cost2 = Additional_Costs.objects.create(
            description="Service Fee", price=30.0
        )

    def test_creation(self):
        self.assertEqual(Additional_Costs.objects.count(), 2)

    def test_default_price(self):
        cost_with_default_price = Additional_Costs.objects.create(
            description="Default Fee"
        )
        self.assertEqual(cost_with_default_price.price, 0.0)

    def test_eq_method(self):
        # Test using ID
        same_cost = Additional_Costs(
            id=self.cost1.id, description="Another Pet Fee", price=50.0
        )
        self.assertEqual(self.cost1, same_cost)

        # Test using description and price
        same_cost_different_id = Additional_Costs(description="Pet Fee", price=20.0)
        self.assertEqual(self.cost1, same_cost_different_id)

        # Test not equal
        self.assertNotEqual(self.cost1, self.cost2)

    def test_hash_method(self):
        self.assertEqual(hash(self.cost1), hash(uuid.UUID(str(self.cost1.id))))

    def tearDown(self):
        self.cost1.delete()
        self.cost2.delete()
