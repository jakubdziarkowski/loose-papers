from typing import Any

from django.db.models.signals import post_delete
from django.dispatch import receiver

from .models import UserFile


@receiver(post_delete, sender=UserFile)
def delete_file_on_model_delete(sender: type[UserFile], instance: UserFile, **kwargs: Any) -> None:
    if instance.file:
        instance.file.delete(save=False)
