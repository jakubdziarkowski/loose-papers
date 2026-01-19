from django.conf import settings
from django.db import models


def user_directory_path(instance: "UserFile", filename: str) -> str:
    return f"{instance.owner.id}/{filename}"


class UserFile(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="files")
    file = models.FileField(upload_to=user_directory_path)
    name = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name
