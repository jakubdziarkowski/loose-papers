from typing import Any

from rest_framework import serializers

from apps.accounts.models import User
from apps.files.serializers import UserFileSerializer


class UserSerializer(serializers.ModelSerializer[User]):
    files = UserFileSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ["id", "email", "files"]

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        if "request" in self.context and self.context["request"].query_params.get("with_files") != "true":
            self.fields.pop("files")
