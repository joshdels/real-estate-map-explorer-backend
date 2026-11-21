from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase

from .models import AppDataset

VALID_DATASET = {"properties": [], "providers": [], "groups": [], "reviews": []}


class DatasetApiTests(APITestCase):
    def setUp(self):
        self.url = reverse("datasets:dataset")
        self.dataset = AppDataset.objects.create(payload=VALID_DATASET)

    def test_dataset_is_public(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), VALID_DATASET)

    def test_dataset_allows_the_local_frontend_origin(self):
        response = self.client.get(self.url, HTTP_ORIGIN="http://localhost:3000")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Access-Control-Allow-Origin"], "http://localhost:3000")
        self.assertEqual(response["Access-Control-Allow-Credentials"], "true")

    def test_client_cannot_replace_whole_dataset(self):
        user = get_user_model().objects.create_user("client@example.test", "password")
        self.client.force_authenticate(user)
        response = self.client.put(self.url, VALID_DATASET, format="json")
        self.assertEqual(response.status_code, 403)

    def test_employee_can_replace_valid_dataset(self):
        user = get_user_model().objects.create_user(
            "staff@example.test", "password", role="employee"
        )
        self.client.force_authenticate(user)
        replacement = {**VALID_DATASET, "metadata": {"version": 1}}
        response = self.client.put(self.url, replacement, format="json")
        self.assertEqual(response.status_code, 200)
        self.dataset.refresh_from_db()
        self.assertEqual(self.dataset.payload, replacement)

    def test_invalid_dataset_is_rejected(self):
        user = get_user_model().objects.create_user(
            "staff@example.test", "password", role="employee"
        )
        self.client.force_authenticate(user)
        response = self.client.put(self.url, {"properties": []}, format="json")
        self.assertEqual(response.status_code, 400)


class ApiDocumentationTests(APITestCase):
    def test_openapi_schema_is_public_and_describes_dataset_methods(self):
        response = self.client.get(reverse("api-schema"), HTTP_ACCEPT="application/json")

        self.assertEqual(response.status_code, 200)
        schema = response.json()
        dataset_path = schema["paths"][reverse("datasets:dataset")]
        self.assertEqual(set(dataset_path), {"get", "put"})
        self.assertEqual(dataset_path["get"].get("security", []), [])

    def test_swagger_ui_is_public(self):
        response = self.client.get(reverse("api-docs"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, reverse("api-schema"))

    def test_redoc_ui_is_public(self):
        response = self.client.get(reverse("api-redoc"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, reverse("api-schema"))
