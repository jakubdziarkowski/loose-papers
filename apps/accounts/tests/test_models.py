import pytest

from apps.accounts.models import User


@pytest.mark.django_db
def test_create_user() -> None:
    user = User.objects.create_user(email="test_user@papers.com", password="pass")
    assert user.email == "test_user@papers.com"
    assert user.check_password("pass")
    assert user.pk is not None
    assert not user.is_staff
    assert not user.is_superuser


@pytest.mark.django_db
def test_create_user_without_email_raises_error() -> None:
    with pytest.raises(ValueError, match="Users must have an email address"):
        User.objects.create_user(email="", password="pass")


@pytest.mark.django_db
def test_create_superuser() -> None:
    superuser = User.objects.create_superuser(email="admin@papers.com", password="adminpass")
    assert superuser.email == "admin@papers.com"
    assert superuser.check_password("adminpass")
    assert superuser.is_staff
    assert superuser.is_superuser


@pytest.mark.django_db
def test_create_superuser_with_is_staff_false_raises_error() -> None:
    with pytest.raises(ValueError, match="Superuser must have is_staff=True."):
        User.objects.create_superuser(email="admin2@papers.com", password="pass", is_staff=False)


@pytest.mark.django_db
def test_create_superuser_with_is_superuser_false_raises_error() -> None:
    with pytest.raises(ValueError, match="Superuser must have is_superuser=True."):
        User.objects.create_superuser(email="admin3@papers.com", password="pass", is_superuser=False)
