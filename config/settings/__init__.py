# ruff: noqa
from dotenv import load_dotenv
import django_stubs_ext

load_dotenv()
django_stubs_ext.monkeypatch()

from .base import *
from .apps import *
from .database import *
from .security import *
