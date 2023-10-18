from django.test import TestCase
from home.models.state import State
from decimal import Decimal


class StateModelTest(TestCase):
    def setUp(self):
        self.state1 = State.objects.create(
            state="California",
            tax_multiplier=Decimal(0.01),
            flood_multiplier=Decimal(0.02),
        )
        self.state2 = State.objects.create(
            state="Texas", tax_multiplier=Decimal(0.005), flood_multiplier=Decimal(0.5)
        )

    def test_creation(self):
        self.assertEqual(State.objects.count(), 2)
        self.assertEqual(self.state1.state, "California")

    def test_equality(self):
        duplicate_state = State(id=self.state1.id, state="California")
        self.assertEqual(duplicate_state, self.state1)

        similar_state = State(state="California")
        self.assertEqual(similar_state, self.state1)

    def test_hash_method(self):
        self.assertEqual(hash(self.state1), hash(self.state1.id))
        self.assertNotEqual(hash(self.state1), hash(self.state2.id))

    def tearDown(self):
        self.state1.delete()
        self.state2.delete()
