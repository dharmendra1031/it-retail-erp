import os

from .settings import *

# SQLite is limited to isolated CI/unit and browser tests.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.getenv("SQLITE_DB_PATH", ":memory:"),
    }
}


# Isolated browser tests use HTTP localhost; production cookies are Secure.
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
