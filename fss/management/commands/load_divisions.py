from django.core.management.base import BaseCommand
from django.db import transaction
from fss.models import Divisions

DIVISIONS = [
    'technopark',
    'deanery',
    'rectorate',
    'uvc',
    'administration',
]

class Command(BaseCommand):
    help = 'Создаёт предустановленные подразделения.'

    @transaction.atomic
    def handle(self, *args, **kwargs):
        for division_name in DIVISIONS:
            obj, created = Divisions.objects.get_or_create(name=division_name)
            action = "Создано" if created else "Существует"
            verbose_name = dict(obj.DIVISIONS_CHOICES).get(obj.name, obj.name)
            self.stdout.write(f"{action}: {obj.name} — {verbose_name}")
        self.stdout.write(self.style.SUCCESS("✅ Все подразделения успешно загружены."))
