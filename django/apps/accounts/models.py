from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.core.models import TimeStampedModel


class AccessPermission(TimeStampedModel):
    code = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class Role(TimeStampedModel):
    name = models.CharField(max_length=100, unique=True)
    permissions = models.ManyToManyField(
        AccessPermission,
        blank=True,
        related_name="roles",
    )

    def __str__(self):
        return self.name


class User(AbstractUser):
    email = models.EmailField(unique=True)
    roles = models.ManyToManyField(
        Role,
        blank=True,
        related_name="users",
    )
