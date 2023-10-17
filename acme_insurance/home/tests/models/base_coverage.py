from django.test import TestCase
from home.models.base_coverage import Base_Coverage
import uuid


class BaseCoverageModelTest(TestCase):
    def setUp(self):
        self.coverage1 = Base_Coverage.objects.create(
            base_coverage_type="Basic", price=20.0
        )
        self.coverage2 = Base_Coverage.objects.create(
            base_coverage_type="Premium", price=40.0
        )

    def test_creation(self):
        self.assertEqual(Base_Coverage.objects.count(), 2)

    def test_eq_method(self):
        # Test using ID
        same_coverage = Base_Coverage(
            id=self.coverage1.id, base_coverage_type="Another Type", price=50.0
        )
        self.assertEqual(self.coverage1, same_coverage)

        # Test using base_coverage_type and price
        same_coverage_different_id = Base_Coverage(
            base_coverage_type="Basic", price=20.0
        )
        self.assertEqual(self.coverage1, same_coverage_different_id)

        # Test not equal
        self.assertNotEqual(self.coverage1, self.coverage2)

    def test_hash_method(self):
        self.assertEqual(hash(self.coverage1), hash(uuid.UUID(str(self.coverage1.id))))

    def tearDown(self):
        self.coverage1.delete()
        self.coverage2.delete()
