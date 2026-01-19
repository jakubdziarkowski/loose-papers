from typing import Any

from rest_framework import serializers

from .models import UserFile


class UserFileSerializer(serializers.ModelSerializer[UserFile]):
    class Meta:
        model = UserFile
        fields = ["id", "name", "file", "uploaded_at"]
        read_only_fields = ["id", "uploaded_at"]

    def create(self, validated_data: dict[str, Any]) -> UserFile:
        validated_data["owner"] = self.context["request"].user
        return super().create(validated_data)
