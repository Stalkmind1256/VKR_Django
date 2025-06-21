from django.core.management.base import BaseCommand
from django.db import transaction
from fss.models import Divisions

DIVISION_NAMES = [
    "Технопарк",
    "Деканат",
    "Ректорат",
    "Учебно-вычислительный центр (УВЦ)",
    "Администрация",
]

class Command(BaseCommand):
    help = 'Создаёт предустановленные подразделения.'

    @transaction.atomic
    def handle(self, *args, **kwargs):
        for name in DIVISION_NAMES:
            obj, created = Divisions.objects.get_or_create(name=name)
            action = "Создано" if created else "Уже существует"
            self.stdout.write(f"{action}: {obj.name}")
        self.stdout.write(self.style.SUCCESS("✅ Подразделения загружены."))
