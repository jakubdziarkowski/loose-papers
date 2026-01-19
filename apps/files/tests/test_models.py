import os

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile

from apps.accounts.models import User
from apps.files.models import UserFile


@pytest.mark.django_db
def test_userfile_str(user: User, uploaded_file: SimpleUploadedFile) -> None:
    uf = UserFile.objects.create(owner=user, name="My File", file=uploaded_file)
    assert str(uf) == "My File"


@pytest.mark.django_db
def test_file_is_deleted_from_storage_on_model_delete(user: User, uploaded_file: SimpleUploadedFile) -> None:
    uf = UserFile.objects.create(owner=user, name="File to delete", file=uploaded_file)
    path = uf.file.path
    assert os.path.exists(path)

    uf.delete()

    assert not os.path.exists(path)
