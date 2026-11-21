from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APITestCase


class UserModelTests(TestCase):
    def test_superuser_uses_email_and_administrator_role(self):
        user = get_user_model().objects.create_superuser("admin@example.test", "safe-test-password")
        self.assertEqual(user.email, "admin@example.test")
        self.assertEqual(user.role, "administrator")
        self.assertTrue(user.is_superuser)


class AuthenticationRouteTests(APITestCase):
    def test_email_password_login_is_available(self):
        response = self.client.post(
            "/api/v1/auth/login/",
            {"email": "missing@example.test", "password": "not-a-real-password"},
            format="json",
        )

        self.assertEqual(response.status_code, 400)

    def test_social_login_routes_are_parked_by_default(self):
        google_response = self.client.post("/api/v1/auth/google/", {}, format="json")
        self.assertEqual(google_response.status_code, 404)
        self.assertEqual(
            self.client.post("/api/v1/auth/facebook/", {}, format="json").status_code,
            404,
        )
