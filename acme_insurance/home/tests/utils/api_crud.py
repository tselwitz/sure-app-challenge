from django.test import TestCase, RequestFactory
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from home.models.base_coverage import (
    Base_Coverage,
)  # Example model for testing purposes
import json
from home.utils.api_crud import API_CRUD
from uuid import uuid4


class ApiCrudTest(TestCase):
    # We'll use Base_Coverage as a representative model for the other API models

    def setUp(self):
        self.factory = RequestFactory()

        # Create a sample object
        self.sample_object = Base_Coverage.objects.create(
            id=uuid4(), base_coverage_type="Basic", price=20.0
        )

    def test_get_existing_object(self):
        request = self.factory.get(f"/home/base_coverage/?id={self.sample_object.id}")
        view = API_CRUD(Base_Coverage)
        response = view.get(request)
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.sample_object.base_coverage_type, str(response.content))

    def test_post_object(self):
        body = {"id": str(uuid4()), "base_coverage_type": "Basic", "price": 20.0}

        request = self.factory.post(
            "/home/base_coverage/", json.dumps(body), content_type="application/json"
        )
        request.body_json = body
        view = API_CRUD(Base_Coverage)
        response = view.post(request)
        self.assertEqual(response.status_code, 200)
        self.assertIn(body["base_coverage_type"], str(response.content))

        # Cleanup created object after the test
        Base_Coverage.objects.filter(id=body["id"]).delete()

    def test_delete_existing_object(self):
        obj_id = str(self.sample_object.id)
        body = {"id": obj_id}

        request = self.factory.delete(
            "/home/base_coverage/", json.dumps(body), content_type="application/json"
        )
        request.body_json = body
        view = API_CRUD(Base_Coverage)
        response = view.delete(request)
        self.assertEqual(response.status_code, 200)
        self.assertIn(obj_id, str(response.content))

        # Verify deletion
        with self.assertRaises(ObjectDoesNotExist):
            Base_Coverage.objects.get(id=obj_id)

    def test_post_invalid_input(self):
        body = {"id": "THIS WILL FAIL", "base_coverage_type": "Basic", "price": 20.0}

        request = self.factory.post(
            "/home/base_coverage", json.dumps(body), content_type="application/json"
        )
        request.body_json = body
        view = API_CRUD(Base_Coverage)
        with self.assertRaises(ValidationError):
            response = view.post(request)
            self.assertEqual(response.status_code, 400)
