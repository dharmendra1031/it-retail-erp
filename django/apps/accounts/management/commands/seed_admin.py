import os

from django.core.management.base import BaseCommand, CommandError

from apps.accounts.models import Role, User


class Command(BaseCommand):
    help = "Create or assign the configured ERP administrator."

    def handle(self, *args, **options):
        email = os.getenv("ERP_ADMIN_EMAIL", "").strip()
        password = os.getenv("ERP_ADMIN_PASSWORD", "")

        if not email or not password:
            raise CommandError("ERP_ADMIN_EMAIL and ERP_ADMIN_PASSWORD are required.")

        user = User.objects.filter(email__iexact=email).first()
        if user is None:
            user = User.objects.create_superuser(
                username=email, email=email, password=password
            )

        role, _ = Role.objects.get_or_create(name="Admin")
        user.roles.add(role)
        self.stdout.write(self.style.SUCCESS("Administrator ready."))
