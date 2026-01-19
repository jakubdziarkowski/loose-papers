import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.accounts.models import User
from apps.files.models import UserFile


@pytest.mark.django_db
def test_upload_file(auth_client: APIClient, uploaded_file: SimpleUploadedFile) -> None:
    url = reverse("files:user_files-list")
    response = auth_client.post(url, {"name": "My File", "file": uploaded_file}, format="multipart")

    assert response.status_code == status.HTTP_201_CREATED
    assert UserFile.objects.count() == 1


@pytest.mark.django_db
def test_list_only_own_files(
    auth_client: APIClient, user: User, other_user: User, uploaded_file: SimpleUploadedFile
) -> None:
    UserFile.objects.create(owner=user, name="Mine", file=uploaded_file)
    UserFile.objects.create(owner=other_user, name="Not mine", file=uploaded_file)

    url = reverse("files:user_files-list")
    response = auth_client.get(url)

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == "Mine"


@pytest.mark.django_db
def test_download_file(auth_client: APIClient, user: User, uploaded_file: SimpleUploadedFile) -> None:
    expected_content = uploaded_file.read()

    uf = UserFile.objects.create(owner=user, name="File1", file=uploaded_file)

    url = reverse("files:user_files-download", args=[uf.id])
    response = auth_client.get(url)

    assert response.status_code == 200
    assert response.getvalue() == expected_content


@pytest.mark.django_db
def test_cannot_access_foreign_file(
    auth_client: APIClient, other_user: User, uploaded_file: SimpleUploadedFile
) -> None:
    uf = UserFile.objects.create(owner=other_user, name="Secret", file=uploaded_file)

    url = reverse("files:user_files-detail", args=[uf.id])
    response = auth_client.get(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND
