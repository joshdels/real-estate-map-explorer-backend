import tempfile

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from django.urls import reverse
from PIL import Image
from rest_framework.test import APITestCase


def image_file(name="lot.png", size=(2, 2)):
    handle = tempfile.SpooledTemporaryFile()
    Image.new("RGB", size, "blue").save(handle, format="PNG")
    handle.seek(0)
    return SimpleUploadedFile(name, handle.read(), content_type="image/png")


class PropertyImageUploadTests(APITestCase):
    def setUp(self):
        self.url = reverse("media_uploads:property-image")
        self.user = get_user_model().objects.create_user(
            "admin@example.test", "password", role="administrator"
        )

    def test_requires_authentication(self):
        response = self.client.post(self.url, {"image": image_file()}, format="multipart")
        self.assertEqual(response.status_code, 401)

    def test_saves_valid_image_to_configured_storage(self):
        with tempfile.TemporaryDirectory() as media_root, override_settings(MEDIA_ROOT=media_root):
            self.client.force_authenticate(self.user)
            response = self.client.post(self.url, {"image": image_file()}, format="multipart")
        self.assertEqual(response.status_code, 201)
        self.assertIn("/media/property-media/", response.json()["url"])

    def test_rejects_non_image(self):
        self.client.force_authenticate(self.user)
        file = SimpleUploadedFile("notes.txt", b"not an image", content_type="text/plain")
        response = self.client.post(self.url, {"image": file}, format="multipart")
        self.assertEqual(response.status_code, 400)
