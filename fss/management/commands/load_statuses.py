from django.core.management.base import BaseCommand
from django.db import transaction
from fss.models import Status

STATUSES = [
    "draft",
    "submitted",
    "approved",
    "rejected",
    "archived",
    "preparing",
    "in_progress",
    "completed",
]

class Command(BaseCommand):
    help = 'Создаёт предустановленные статусы предложений.'

    @transaction.atomic
    def handle(self, *args, **kwargs):
        for status_name in STATUSES:
            obj, created = Status.objects.get_or_create(name=status_name)
            action = "Создан" if created else "Существует"
            self.stdout.write(f"{action}: {obj.name} — {dict(obj.STATUS_CHOICES).get(obj.name)}")
        self.stdout.write(self.style.SUCCESS("✅ Все статусы успешно загружены."))
