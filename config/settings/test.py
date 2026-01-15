# ruff: noqa: F403, F405
from .base import *

DATABASES["default"]["NAME"] = "loose_papers_test"
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]
