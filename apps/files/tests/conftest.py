import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient

from apps.accounts.models import User


@pytest.fixture
def user(db) -> User:  # type: ignore[no-untyped-def]
    return User.objects.create_user(email="testuser@papers.com", password="password123")


@pytest.fixture
def other_user(db) -> User:  # type: ignore[no-untyped-def]
    return User.objects.create_user(email="other@papers.com", password="password123")


@pytest.fixture
def auth_client(user: User) -> APIClient:
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.fixture
def uploaded_file() -> SimpleUploadedFile:
    return SimpleUploadedFile("hello.txt", b"hello world", content_type="text/plain")
