from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.files.models import UserFile

User = get_user_model()


class AccountsAPITestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(email="test@example.com", password="securepassword")
        self.login_url = reverse("accounts:login")
        self.refresh_url = reverse("accounts:token_refresh")
        self.logout_url = reverse("accounts:logout")
        self.me_url = reverse("accounts:me")

    def test_login_with_valid_credentials(self) -> None:
        response = self.client.post(self.login_url, {"email": self.user.email, "password": "securepassword"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_login_with_invalid_credentials(self) -> None:
        response = self.client.post(self.login_url, {"email": self.user.email, "password": "wrongpassword"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_me_requires_authentication(self) -> None:
        response = self.client.get(self.me_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_me_returns_user_data(self) -> None:
        login_response = self.client.post(self.login_url, {"email": self.user.email, "password": "securepassword"})
        access_token = login_response.data["access"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        response = self.client.get(self.me_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.user.id)
        self.assertEqual(response.data["email"], self.user.email)

    def test_me_returns_user_data_with_files(self) -> None:
        login_response = self.client.post(self.login_url, {"email": self.user.email, "password": "securepassword"})
        access_token = login_response.data["access"]

        UserFile.objects.create(owner=self.user, name="test_file.txt", file="path/to/test_file.txt")

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        response = self.client.get(f"{self.me_url}?with_files=true")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.user.id)
        self.assertEqual(response.data["email"], self.user.email)
        self.assertIn("files", response.data)
        self.assertEqual(len(response.data["files"]), 1)
        self.assertEqual(response.data["files"][0]["name"], "test_file.txt")

    def test_token_refresh(self) -> None:
        login_response = self.client.post(self.login_url, {"email": self.user.email, "password": "securepassword"})
        refresh_token = login_response.data["refresh"]

        response = self.client.post(self.refresh_url, {"refresh": refresh_token})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_logout_blacklists_token(self) -> None:
        login_response = self.client.post(self.login_url, {"email": self.user.email, "password": "securepassword"})
        refresh_token = login_response.data["refresh"]

        response = self.client.post(self.logout_url, {"refresh": refresh_token})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        refresh_response = self.client.post(self.refresh_url, {"refresh": refresh_token})
        self.assertEqual(refresh_response.status_code, status.HTTP_401_UNAUTHORIZED)
