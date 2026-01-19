import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIRequestFactory

from apps.accounts.models import User
from apps.files.serializers import UserFileSerializer


@pytest.mark.django_db
def test_serializer_sets_owner_from_request_context(user: User, uploaded_file: SimpleUploadedFile) -> None:
    factory = APIRequestFactory()
    request = factory.post("/files/")
    request.user = user

    serializer = UserFileSerializer(
        data={"name": "Test File", "file": uploaded_file},
        context={"request": request},
    )

    assert serializer.is_valid(), serializer.errors
    instance = serializer.save()

    assert instance.owner == user
