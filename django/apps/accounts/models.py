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
    failed_login_attempts = models.PositiveSmallIntegerField(default=0)
    locked_until = models.DateTimeField(null=True, blank=True)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=30, blank=True)
    branch = models.ForeignKey("companies.Branch", null=True, blank=True, on_delete=models.PROTECT)
    roles = models.ManyToManyField(
        Role,
        blank=True,
        related_name="users",
    )
