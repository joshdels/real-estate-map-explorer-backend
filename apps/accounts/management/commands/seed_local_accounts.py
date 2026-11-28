from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

LOCAL_PASSWORD = "LocalDemo123!"
LOCAL_ACCOUNTS = (
    ("admin@example.test", "administrator", ""),
    ("staff@example.test", "employee", ""),
    ("provider@example.test", "client", "provider-coastal"),
)


class Command(BaseCommand):
    help = "Create or update the documented fictional accounts used for local integration testing."

    def handle(self, *args, **options):
        user_model = get_user_model()
        for email, role, provider_id in LOCAL_ACCOUNTS:
            user, _ = user_model.objects.update_or_create(
                email=email,
                defaults={"role": role, "provider_id": provider_id, "is_active": True},
            )
            user.set_password(LOCAL_PASSWORD)
            user.save(update_fields=["password"])
            self.stdout.write(f"Prepared {email} ({role})")
        self.stdout.write(self.style.SUCCESS("Local demo accounts are ready."))
