from django.apps import AppConfig


class FilesConfig(AppConfig):
    name = "apps.files"

    def ready(self) -> None:
        import apps.files.signals  # noqa
