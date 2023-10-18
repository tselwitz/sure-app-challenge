from django.test import TestCase
from unittest.mock import Mock, patch
from decimal import Decimal
from home.utils.view_helpers import *
from home.models.additional_costs import Additional_Costs


class ViewHelpersTest(TestCase):
    def test_calculate_price(self):
        coverage, add_costs, mult_costs, tax_multiplier = 100, [10, 20], [2], 0.1
        subtotal, taxes, total = calculate_price(
            coverage, add_costs, mult_costs, tax_multiplier
        )

        self.assertEqual(subtotal, Decimal("260.00"))
        self.assertEqual(taxes, Decimal("26.00"))
        self.assertEqual(total, Decimal("286.00"))

    @patch("home.models.additional_costs.Additional_Costs.objects.filter")
    def test_has_add_cost(self, mock_filter):
        mock_cost = Mock()
        mock_cost.price = Decimal("50.00")
        mock_cost.id = 1
        mock_filter.return_value.first.return_value = mock_cost

        add_costs, add_cost_ids = [], []
        add_costs, add_cost_ids = has_add_cost(
            "pet_fee", "has_pet_fee", {"has_pet_fee": True}, add_costs, add_cost_ids
        )

        self.assertEqual(add_costs, [Decimal("50.00")])
        self.assertEqual(add_cost_ids, [1])

    def test_has_mult_cost(self):
        mult_costs = []
        mult_costs = has_mult_cost(
            "pet_fee", {"pet_fee": True}, mult_costs, Decimal("2.00")
        )

        self.assertEqual(mult_costs, [Decimal("2.00")])

    @patch("home.models.additional_costs.Additional_Costs.objects.filter")
    def test_get_required_field(self, mock_filter):
        mock_obj = Mock()
        mock_obj.some_field = "test_value"
        mock_filter.return_value.first.return_value = mock_obj

        result = get_required_field(
            {"description": "test_name"}, "description", Additional_Costs, "description"
        )

        self.assertEqual(result.some_field, "test_value")
        with self.assertRaises(AttributeError):
            get_required_field({}, "name", "someClass", "someClassField")
