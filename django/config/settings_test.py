from .settings import *

# Isolated unit-test database. Production and integration tests use SQL Server.
DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}}
