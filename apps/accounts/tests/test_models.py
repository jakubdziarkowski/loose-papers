import pytest

from apps.accounts.models import User


@pytest.mark.django_db
def test_create_user() -> None:
    """Dummy test: can create a user in test DB."""
    user = User.objects.create_user(username="test_user", password="pass")
    assert user.username == "test_user"
    assert user.pk is not None
